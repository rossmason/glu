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

public class GluException extends Exception
{
    /*
     * The default message and code is what makes this class unique.
     */
    private final static String DEFAULT_MSG  = "Internal server error";  
    private final static int    CODE         = 500;
    
    /*
     * The usual set of constructors for exceptions
     */
    public GluException()
    {
        super(DEFAULT_MSG);
    }

    public GluException(String msg)
    {
        super(msg);
    }
    
    public GluException(Throwable ex)
    {
        super(DEFAULT_MSG, ex);
    }

    public GluException(String msg, Throwable ex)
    {
        super(msg, ex);
    }
    
    public int getCode()
    {
        return CODE;
    }
}


