/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.component;

import java.util.HashMap;
import java.util.Vector;

import org.mulesource.glu.parameter.*;
import org.mulesource.glu.component.api.*;
import org.mulesource.glu.exception.GluException;
import org.mulesource.glu.GluHttpRequest;

public class TestComponent extends BaseComponent
{
    public TestComponent() throws GluException
    {
        this(null);
    }
    
    public TestComponent(String resourceName) throws GluException
    {
        super(resourceName);
        
        componentDescriptor = new ComponentDescriptor("TestComponent",
                                                      "This is a Java test component",
                                                      "Here is a doc string");
        componentDescriptor.addParameter("api_key", new ParameterDefString("This is a the API key", true, ""));
        
        ServiceDescriptor sd = new ServiceDescriptor("This is the foobar service");
        sd.addParameter("query", new ParameterDefString("The search query"));
        sd.addParameter("num",   new ParameterDefNumber("Number of results", 10));
        sd.setPositionalParameters("num");
        
        componentDescriptor.addService("foobar", sd);
    }
    
    public Result foobar(GluHttpRequest request, String input, HashMap<String, Object> params, String method)
    {
        System.out.println("### request: " + request.getClass());
        System.out.println("### input:   " + input.getClass() + " === " + input);
        System.out.println("### params:  " + params.getClass());
        System.out.println("### method:  " + method.getClass() + " === " + method);
        System.out.println("----------------------------------------------------------");
        System.out.println("Protocol:   " + request.getRequestProtocol());
        System.out.println("Method:     " + request.getRequestMethod());
        System.out.println("URI:        " + request.getRequestURI());
        System.out.println("Headers:    " + request.getRequestHeaders());
        System.out.println("Query:      " + request.getRequestQuery());
        System.out.println("Body:       " + request.getRequestBody());
        request.setResponseHeader("Location", "http://www.brendel.com");
        
        System.out.println("----------------------------------------------------------");
     
        for (Object i: params.keySet()) {
            System.out.println("Key: " + i + "  Value: " + params.get(i) + "   type of value: " + params.get(i).getClass());
        }
        System.out.println("@ 1");
        HashMap res = new HashMap();
        System.out.println("@ 2");
        res.put("foo", "This is a test");
        System.out.println("@ 3");
        HashMap sub = new HashMap();
        res.put("bar", sub);
        System.out.println("@ 4");
        sub.put("some value", 1);
        System.out.println("@ 5");
        sub.put("another value", "Some text");
        System.out.println("@ 6");
        Vector v = new Vector();
        v.add("Blah");
        v.add(12345);
        sub.put("some vector", v);
        
        v = new Vector();
        v.add("Some text");
        v.add(123);
        v.add(res);
        
        return new Result(200, v);
    }

}


