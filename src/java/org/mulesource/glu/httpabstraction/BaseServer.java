/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.httpabstraction;


/*
 * This is an abstracted HTTP server class.
 * 
 * Why don't we just use the built-in server that comes with Java?
 * Because we want to be able to quickly exchange it for some other
 * server or environment.
 */
public abstract class BaseServer
{
    public static final String METHOD_GET     = "GET";
    public static final String METHOD_PUT     = "PUT";
    public static final String METHOD_POST    = "POST";
    public static final String METHOD_DELETE  = "DELETE";
    public static final String METHOD_HEAD    = "HEAD";
    public static final String METHOD_OPTIONS = "OPTIONS";
    
    protected int                port;
    protected BaseRequestHandler requestHandler;
    
    public BaseServer(int port, BaseRequestHandler requestHandler)
    {
        this.port           = port;
        this.requestHandler = requestHandler;
    }
}


