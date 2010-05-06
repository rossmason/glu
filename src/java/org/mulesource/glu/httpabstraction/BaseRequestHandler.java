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

import java.net.URI;
import java.util.HashMap;

/*
 * This is the abstract base class for all request handler objects.
 * 
 * There is a request handler that's used with the standard Java server,
 * but we want to be able to abstract out the HTTP server if necessary.
 * That is why we use this abstraction layer instead.
 */
public abstract class BaseRequestHandler
{
    protected int                     responseCode;
    protected String                  responseBody;
    protected HashMap<String, String> responseHeaders;
    
    public BaseRequestHandler()
    {
        responseHeaders    = new HashMap<String, String>();
    }
    
    public void setResponseCode(int code)
    {
        responseCode = code;
    }
    
    public void setResponseBody(String body)
    {
        responseBody = body;
    }
    
    public void setResponseHeader(String name, String value)
    {
        responseHeaders.put(name, value);
    }
    
    /*
     * If a header with the specified name exists already then
     * the new value will be 'added' to the existing value,
     * separated by a comma.
     * 
     * If the specified header does not exist already then it
     * will be created.
     * 
     */
    public void addResponseHeader(String name, String value)
    {
        String storedVal = responseHeaders.get(name);
        if (storedVal == null) {
            storedVal = value;
        }
        else {
            storedVal += ", " + value;
        }
        responseHeaders.put(name, storedVal);    
    }
    
    public void setResponse(int code, String body)
    {
        setResponseCode(code);
        setResponseBody(body);
    }
    
    public abstract String getRequestProtocol();
    
    public abstract String getRequestMethod();
    
    public abstract URI getRequestURI();
    
    public abstract String getRequestPath();
    
    public abstract HashMap<String, String> getRequestHeaders();
    
    public abstract String getRequestQuery();
    
    public abstract String getRequestBody();
    
    public abstract String sendResponseHeaders();

    public abstract String sendResponseBody();
    
    public void sendResponse()
    {
        sendResponseHeaders();
        sendResponseBody();
    }
    
    public abstract void close();

}


