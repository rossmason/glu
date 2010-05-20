/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;

public abstract class GluHttpRequest
{
    /*
     * This is the base class we use for our HttpRequest.
     * By using a Java base class, we can use the HttpRequest
     * equally easily in Java as well as Python.
     */
    public abstract void    setNativeMode();       // Subsequently returned dictionaries are in native (Java) form
    public abstract void    setNativeRequest(HttpExchange nativeRequest);
    public abstract void    setResponseCode(int code);
    public abstract void    setResponseBody(String body);
    public abstract void    setResponseHeader(String name, String value);
    public abstract void    setResponse(int code, String body);
    public abstract String  getRequestProtocol();
    public abstract String  getRequestMethod();
    public abstract String  getRequestURI();
    public abstract String  getRequest();
    public abstract Headers getRequestHeaders();   // We return a dict() for Python. Python doesn't care.
    public abstract String  getRequestQuery();
    public abstract String  getRequestBody();
    public abstract void    sendResponseHeaders();
    public abstract void    sendResponseBody();
    public abstract void    sendResponse();
    public abstract void    close();    
}


