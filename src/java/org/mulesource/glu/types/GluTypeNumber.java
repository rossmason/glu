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

import java.math.BigDecimal;

import org.mulesource.glu.exceptions.*;


/*
 * A Glu parameter definition for a Boolean type.
 * 
 */

public class GluTypeNumber extends GluType
{
    public GluTypeNumber(String name, String desc, boolean required)
    {
        this(name, desc, required, null, null);
    }
    
    public GluTypeNumber(String name, String desc, boolean required, BigDecimal defaultValue)
    {
        this(name, desc, required, defaultValue, null);
    }
    
    public GluTypeNumber(String name, String desc, boolean required, BigDecimal defaultValue, BigDecimal value)
    {
        super(name, desc, required, GluType.PARAM_NUMBER, defaultValue, value);
    }
    
    public BigDecimal getValue()
    {
        return (BigDecimal)getGenericValue();
    }
    
    @Override
    protected BigDecimal specializedFromString(String str)
    {
        return new BigDecimal(str);
    }
}
