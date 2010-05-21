/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.exception;

public class GluException extends Exception
{
    public int    code;
    public String msg;
    
    public GluException(String message)
    {
        this(500, message);
    }
    
    public GluException(int code, String message)
    {
        this.code = code;
        this.msg  = message;
    }
}


