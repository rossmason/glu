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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Vector;

import org.mulesource.glu.exception.GluException;
import org.mulesource.glu.exception.GluDuplicateKeyException;
import org.mulesource.glu.exception.GluMalformedServiceDescriptorException;
import org.mulesource.glu.parameter.ParameterDef;

public class ServiceDescriptor
{
    /*
     * Defines a single service for a resource.
     */
    private String desc;
    
    private HashMap<String, ParameterDef> params;
    private Vector<String>                positionalParams;

    public ServiceDescriptor(String desc)
    {
        this.desc             = desc;
        this.params           = new HashMap<String, ParameterDef>();
        this.positionalParams = new Vector<String>();
    }
    
    public String getDesc()
    {
        return desc;
    }
    
    public void addParameter(String name, ParameterDef param) throws GluDuplicateKeyException
    {
        if (params.containsKey(name)) {
            throw new GluDuplicateKeyException("Parameter '" + name + "' already exists.");
        }
        
        params.put(name, param);
    }
    
    public HashMap<String, ParameterDef> getParamMap()
    {
        return params;
    }
    
    public void setPositionalParameters(ArrayList<String> positionals) throws GluMalformedServiceDescriptorException
    {
        for (String name : positionals) {
            if (!params.containsKey(name)) {
                throw new GluMalformedServiceDescriptorException("Parameter '" + name + "' from positionals does not exist");
            }
        }
        
        for (String elem: positionals) {
            positionalParams.add(elem);
        }
    }
    
    public Vector<String> getPositionalParams()
    {
        return positionalParams;
    }
}

