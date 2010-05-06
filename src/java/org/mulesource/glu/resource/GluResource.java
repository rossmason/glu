/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.resource;

import java.io.Serializable;
import java.net.URI;
import java.util.Vector;

import org.mulesource.glu.resource.GluResourceService;

public class GluResource implements Serializable
{
    /* These are the pieces of information that will be made
     * public about the resource. */ 
    private String                     name;        // Name of the resource
    private URI                        resourceUri; // The base URI of this resource
    private String                     desc;        // Short description string
    private Vector<GluResourceService> services;    // List of the various service definitions

    private URI                        codeUri;     // URI of the code (component)

    public String getName()
    {
        return name;
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public URI getResourceUri()
    {
        return resourceUri;
    }

    public void setResourceUri(URI resourceUri)
    {
        this.resourceUri = resourceUri;
    }

    public String getDesc()
    {
        return desc;
    }

    public void setDesc(String desc)
    {
        this.desc = desc;
    }

    public Vector<GluResourceService> getServices()
    {
        return services;
    }

    public void setServices(Vector<GluResourceService> services)
    {
        this.services = services;
    }

    public URI getCodeUri()
    {
        return codeUri;
    }

    public void setCodeUri(URI codeUri)
    {
        this.codeUri = codeUri;
    }
    
    
    

}


