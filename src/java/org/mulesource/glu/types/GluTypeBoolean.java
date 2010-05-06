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
 * A Glu parameter definition for a Boolean type.
 * 
 */

public class GluTypeBoolean extends GluType
{
    public GluTypeBoolean(String name, String desc, boolean required)
    {
        this(name, desc, required, null, null);
    }
    
    public GluTypeBoolean(String name, String desc, boolean required, Boolean defaultValue)
    {
        this(name, desc, required, defaultValue, null);
    }
    
    public GluTypeBoolean(String name, String desc, boolean required, Boolean defaultValue, Boolean value)
    {
        super(name, desc, required, GluType.PARAM_BOOL, defaultValue, value);
    }
    
    public Boolean getValue()
    {
        return (Boolean)getGenericValue();
    }
    
    @Override
    protected Boolean specializedFromString(String str)
    {
        return Boolean.parseBoolean(str);
    }
}
