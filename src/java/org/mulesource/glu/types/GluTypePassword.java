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
 * A Glu parameter definition for a String type.
 * 
 */

public class GluTypePassword extends GluType
{
    public GluTypePassword(String name, String desc, boolean required)
    {
        this(name, desc, required, null, null);
    }
    
    public GluTypePassword(String name, String desc, boolean required, String defaultValue)
    {
        this(name, desc, required, defaultValue, null);
    }
    
    public GluTypePassword(String name, String desc, boolean required, String defaultValue, String value)
    {
        super(name, desc, required, GluType.PARAM_PASSWORD, defaultValue, value);
    }
    
    @Override
    public String toString()
    {
        return "******";
    }

    @Override
    protected Object specializedFromString(String str)
    {
        return str;
    }
}
