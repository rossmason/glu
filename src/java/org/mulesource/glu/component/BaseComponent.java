/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.component;

import java.util.HashMap;

import javax.print.attribute.standard.Severity;
import javax.swing.text.html.HTMLDocument.HTMLReader.IsindexAction;

import org.mulesource.glu.Settings;
import org.mulesource.glu.util.Url;
import org.mulesource.glu.parameter.*;

public abstract class BaseComponent
{
    public final String LANGUAGE = "JAVA";
    /*
     * Attributes, which need to be set by the constructor.
     */
    protected String                        name;
    protected String                        desc;
    protected String                        docs;
    protected HashMap<String, ParameterDef> params;
    protected HashMap<String, Object>       services;
    
    private String resourceName;
    private String accountName;
    private String password; 
    
    public BaseComponent(String resourceName)
    {
        this.resourceName = resourceName;        
        this.accountName  = "";
        this.password     = "";       
    }
    
    public String getMyResourceName()
    {
        return resourceName;
    }
    
    public String getMyResourceUri()
    {
        return Settings.PREFIX_RESOURCE + "/" + getMyResourceName();
    }
    
    // TODO: getFileStorage()

    public void httpSetCredentials(String accountName, String password)
    {
        this.accountName = accountName;
        this.password    = password;
    }
    
    // TODO: httpGet()
    
    // TODO: httpPost()
    
    private HashMap<String, Object> changeParamsToPlainDict(HashMap<String, ParameterDef> paramDict)
    {
        HashMap<String, Object> d = new HashMap<String, Object>();
        for (String name: paramDict.keySet()) {
            d.put(name, paramDict.get(name).asDict());
        }
        return d;
    }
    
    public HashMap<String, Object> getMetaData()
    {
        HashMap<String, Object> d = new HashMap<String, Object>();
        
        d.put("uri",      getUri());
        d.put("name",     getName());
        d.put("desc",     getDesc());
        d.put("doc",      getDoc());
        d.put("params",   changeParamsToPlainDict(getParams()));
        d.put("services", _getServices(null));
        
        HashMap<String, ParameterDef> rp = new HashMap<String, ParameterDef>();
        rp.put("suggested_name", new ParameterDefString("Can be used to suggest the resource name to the server",
                                                        true, ""));
        rp.put("public",         new ParameterDefBoolean("Indicates whether the resource should be public",
                                                         false, false));
        rp.put("desc",           new ParameterDefString("Specifies a description for this new resource",
                                                        false, "A '" + getName() + "' resource")); 

        d.put("resource_creation_params", changeParamsToPlainDict(rp));
        
        return d;
    }
    
    public String getName()
    {
        return name;
    }
    
    public String getDesc()
    {
        return desc;
    }
    
    public String getDoc()
    {
        return docs;
    }
    
    public String getUri()
    {
        return Settings.PREFIX_CODE + "/" + getName();
    }
    
    public HashMap<String, ParameterDef> getParams()
    {
        return params;
    }
    
    /*
     * Following are some methods that are used by the framework and that are not part
     * of the official component-API.
     */
    
    /*
     * Return a dictionary of all defined services. resourceBaseUri may be set to null,
     * in which case all service URLs are relative to the code URL of the component.
     */
    public HashMap<String, Object> _getServices(String resourceBaseUri)
    {
        // Get the base URI for all services. If no resource base URI
        // was defined (can happen when we just look at code meta data)
        // then we use the code base URI instead.
        String baseUri;        
        if (resourceBaseUri == null) {
            baseUri = getUri();
        }
        else {
            baseUri = resourceBaseUri;
        }
        
        // Create a map of service descriptions.
        if (services != null  &&  !services.isEmpty()) {            
            HashMap<String, Object> ret = new HashMap<String, Object>();
            for (String name: services.keySet()) {
                HashMap<String, Object> thisService = (HashMap<String, Object>)services.get(name);
                thisService.put("uri", baseUri + "/" + name);
                ret.put(name, thisService);
                HashMap<String, Object> params = (HashMap<String, Object>)thisService.get("params");
                if (params != null) {
                    for (String pname: params.keySet()) {
                        Object param = params.get(pname);
                        if (param instanceof ParameterDef) {
                            // Need the type check since we may have constructed the
                            // representation from storage, rather than in memory.
                            // If it's from storage then we don't have ParameterDefs
                            // in this dictionary here, so we don't need to convert
                            // anything.
                            param = ((ParameterDef)param).asDict();
                            params.put(pname, param);
                        }
                    }
                }
            }
            
            return ret;
        }
        else {
            // No services defined? Nothing to return...
            return null;
        }
    }
 }


