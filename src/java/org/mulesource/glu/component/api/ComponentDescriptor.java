/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.component.api;

import java.util.HashMap;

import org.mulesource.glu.exception.GluException;
import org.mulesource.glu.exception.GluDuplicateKeyException;
import org.mulesource.glu.parameter.ParameterDef;

public class ComponentDescriptor
{
    /*
     * This descriptor is assembled by the component to provide the
     * meta data description about itself to the Glu framework.
     */
    private String name;
    private String descriptionText;
    private String docText;
    
    private HashMap<String, ParameterDef>      params;
    private HashMap<String, ServiceDescriptor> services;
    
    public ComponentDescriptor(String name, String descriptionText, String docText)
    {
        this.name            = name;
        this.descriptionText = descriptionText;
        this.docText         = docText;
        this.params          = new HashMap<String, ParameterDef>();
        this.services        = new HashMap<String, ServiceDescriptor>();
    }
    
    /*
     * Add a new parameter to the list of params. If one with that
     * name exists already then it is just overwritten.
     */
    public void addParameter(String name, ParameterDef pdef) throws GluDuplicateKeyException
    {
        if (params.containsKey(name)) {
            throw new GluDuplicateKeyException("Parameter '" + name + "' already exists.");
        }
        
        params.put(name, pdef);
    }
    
    public void addService(String name, ServiceDescriptor service) throws GluDuplicateKeyException
    {
        if (services.containsKey(name)) {
            throw new GluDuplicateKeyException("Service '" + name + "' already exists.");
        }
        
        services.put(name, service);
    }
    
    public HashMap<String, ParameterDef> getParamMap()
    {
        return params;
    }
    
    public HashMap<String, ServiceDescriptor> getServicMap()
    {
        return services;
    }
    
    public String getName()
    {
        return name;
    }
    
    public String getDesc()
    {
        return descriptionText;
    }
    
    public String getDocs()
    {
        return docText;
    }
    
    /*
     * Internally, services are stored as a plain dictionary (because that's how
     * it was done in Python). Therefore, we provide this method here to return
     * a plain-dict representation of the assembled service description.
     */
    public HashMap<String, Object> getServicesAsPlainDict()
    {
        HashMap<String, Object> servicesDict = new HashMap<String, Object>();
        
        for (String name: services.keySet()) {
            ServiceDescriptor service = services.get(name);
            HashMap<String, Object> serviceDef = new HashMap<String, Object>();
            servicesDict.put(name, serviceDef);
            serviceDef.put("desc", service.getDesc());
            serviceDef.put("params", service.getParamMap());
            if (service.getPositionalParams().length > 0) {
                serviceDef.put("positional_params", service.getPositionalParams());
            }
        }
        
        return servicesDict;
    }
}


