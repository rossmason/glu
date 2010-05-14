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
     * In addition to a message, a Glu Exception also carries a code,
     * which is equivalent to an HTTP status code.
     */
    private final static String DEFAULT_MSG  = "Internal server error";  
    private final static int    DEFAULT_CODE = 500;
    
    protected String msg;
    protected int    code;
    
    /*
     * The usual set of constructors for exceptions
     */
    public GluException()
    {
        this(DEFAULT_MSG, DEFAULT_CODE);
    }

    public GluException(String msg)
    {
        this(msg, DEFAULT_CODE);
    }
    
    public GluException(Throwable ex)
    {
        this(DEFAULT_MSG, DEFAULT_CODE, ex);
    }

    public GluException(String msg, Throwable ex)
    {
        this(msg, DEFAULT_CODE, ex);
    }
    
    public GluException(String msg, int code)
    {
        super(msg);
        this.msg  = msg;
        this.code = code;
    }
    
    public GluException(String msg, int code, Throwable ex)
    {
        super(msg, ex);
        this.msg  = msg;
        this.code = code;
    }
    
    public int getCode()
    {
        return code;
    }
}


