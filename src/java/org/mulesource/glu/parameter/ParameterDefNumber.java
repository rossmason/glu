/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.parameter;

import java.math.BigDecimal;

public class ParameterDefNumber extends ParameterDef
{
    private BigDecimal defaultVal;
    
    public ParameterDefNumber(String desc, boolean required, int defaultVal)
    {
        this(desc, required, new BigDecimal(defaultVal));
    }
    
    public ParameterDefNumber(String desc, boolean required, float defaultVal)
    {
        this(desc, required, new BigDecimal(defaultVal));
    }
    
    public ParameterDefNumber(String desc, boolean required, BigDecimal defaultVal)
    {
        super("number", desc, required);
        this.defaultVal = defaultVal;
    }

    @Override
    protected Object getDefaultVal()
    {
        return defaultVal;
    }
}


