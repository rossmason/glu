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

public class TestComponent extends BaseComponent
{
    public TestComponent()
    {
        this(null);
    }
    
    public TestComponent(String resourceName)
    {
        super(resourceName);
        name         = "TestComponent";
        desc         = "This is a Java test component";
        docs         = "Here is a doc string";
        
        params       = new HashMap<String, ParameterDef>();
        params.put("api_key", new ParameterDefString("This is the API key", true, ""));
        
        services     = new HashMap<String, Object>();
        HashMap<String, Object> serviceDef = new HashMap<String, Object>();
        services.put("foobar", serviceDef);
        serviceDef.put("desc", "This is the foobar service");
        HashMap<String, ParameterDef> paramDef = new HashMap<String, ParameterDef>();
        serviceDef.put("params", paramDef);
        paramDef.put("query", new ParameterDefString("The search query", true, ""));
        paramDef.put("num", new ParameterDefNumber("Number of results", false, 10));
    }
    
    public Result foobar(Object request, Object input, Object params, Object method)
    {
        System.out.println("### request: " + request.getClass());
        System.out.println("### input:   " + input.getClass());
        System.out.println("### params:  " + params.getClass());
        System.out.println("### method:  " + method.getClass());
     
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


