/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.types;

import org.mulesource.glu.exceptions.GluParameterFormatException;

/*
 * A Glu parameter definition.
 * 
 * Each parameter has at name, a description and an indicator
 * whether the parameter is required or optional.
 * 
 * Also there is a value and default value.
 * 
 */

public abstract class GluType
{
    public static final String PARAM_STRING   = "string";
    public static final String PARAM_PASSWORD = "password";
    public static final String PARAM_BOOL     = "bool";
    public static final String PARAM_DATE     = "date";
    public static final String PARAM_TIME     = "time";
    public static final String PARAM_INTEGER  = "integer";
    public static final String PARAM_NUMBER   = "number";
    public static final String PARAM_URI      = "URI";
    public static final String PARAM_UNKNOWN  = "unknown";
    
    protected String  name;
    protected String  desc;
    protected boolean required;
    protected String  typeName;
    protected Object  value;
    protected Object  defaultValue;

    protected abstract Object specializedFromString(String str);
    
    public GluType(String name, String desc, boolean required)
    {
        this(name, desc, required, PARAM_UNKNOWN, null, null);
    }
    
    public GluType(String name, String desc, boolean required, String typeName,
                   Object defaultValue, Object value)
    {
        this.name         = name;
        this.desc         = desc;
        this.required     = required;
        this.typeName     = typeName;
        this.defaultValue = defaultValue;
        this.value        = value;
    }
    
    public String getName()
    {
        return name;
    }
    
    public String getDesc()
    {
        return desc;
    }
    
    public boolean isRequired()
    {
        return required;
    }
    
    public String getTypeName()
    {
        return typeName;
    }
    
    public Object getGenericValue()
    {
        if (value == null) {
            System.out.println("Getting default");
            return defaultValue;
        }
        else {
            System.out.println("Getting actual value");
            return value;
        }
    }
    
    public void setGenericValue(Object val)
    {
        value = val;
    }

    public void setValueFromString(String str) throws GluParameterFormatException
    {
        try {
            value = specializedFromString(str);
        }
        catch (Exception e) {
            throw new GluParameterFormatException("Unable to convert '" + str + "' to type " + getTypeName());
        }

    }

    public String toString()
    {
        return getGenericValue().toString();
    }
}
