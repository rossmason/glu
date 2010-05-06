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

import org.mulesource.glu.exceptions.*;

/*
 * A Glu parameter definition for an Integer type.
 * 
 */

public class GluTypeInteger extends GluType
{
    public GluTypeInteger(String name, String desc, boolean required)
    {
        this(name, desc, required, null, null);
    }
    
    public GluTypeInteger(String name, String desc, boolean required, Integer defaultValue)
    {
        this(name, desc, required, defaultValue, null);
    }
    
    public GluTypeInteger(String name, String desc, boolean required, Integer defaultValue, Integer value)
    {
        super(name, desc, required, GluType.PARAM_INTEGER, defaultValue, value);
    }
    
    public Integer getValue()
    {
        return (Integer)getGenericValue();
    }
    
    @Override
    protected Integer specializedFromString(String str)
    {
        return Integer.parseInt(str);
    }
}
