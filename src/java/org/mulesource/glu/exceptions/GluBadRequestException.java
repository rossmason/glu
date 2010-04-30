/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.exceptions;

import org.mulesource.glu.exceptions.GluException;

public class GluBadRequestException extends GluException
{
    /*
     * The default message and code is what makes this class unique.
     */
    private final static String DEFAULT_MSG = "Bad request";
    private final static int    CODE        = 400;
    
    /*
     * The usual set of constructors for exceptions
     */
    public GluBadRequestException()
    {
        super(DEFAULT_MSG);
    }

    public GluBadRequestException(String msg)
    {
        super(msg);
        // TODO Auto-generated constructor stub
    }
    
    public GluBadRequestException(Throwable ex)
    {
        super(DEFAULT_MSG, ex);
    }

    public GluBadRequestException(String msg, Throwable ex)
    {
        super(msg, ex);
        // TODO Auto-generated constructor stub
    }
    
    public int getCode()
    {
        return CODE;
    }

}


