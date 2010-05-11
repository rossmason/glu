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

public class GluResourceNotFoundException extends GluException
{
    /*
     * The default message and code is what makes this class unique.
     */
    private final static String DEFAULT_MSG = "Resource not found";
    private final static int    CODE        = 404;
    
    /*
     * The usual set of constructors for exceptions
     */
    public GluResourceNotFoundException()
    {
        super(DEFAULT_MSG);
    }

    public GluResourceNotFoundException(String msg)
    {
        super(msg);
    }
    
    public GluResourceNotFoundException(Throwable ex)
    {
        super(DEFAULT_MSG, ex);
    }

    public GluResourceNotFoundException(String msg, Throwable ex)
    {
        super(msg, ex);
    }
    
    public int getCode()
    {
        return CODE;
    }

}


