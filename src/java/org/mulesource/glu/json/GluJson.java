/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.json;

import org.python.util.PythonInterpreter;
import org.python.core.PyObject;
import org.python.core.PyString;

public abstract class GluJson
{
    public static GluJson make()
    {
        PythonInterpreter interp   = new PythonInterpreter();
        interp.exec("from glu.json import JsonImpl");
        PyObject pyObjectClass     = interp.get("JsonImpl");
        PyObject pyObject          = pyObjectClass.__call__();
        return (GluJson)pyObject.__tojava__(GluJson.class);
    }
    
    public abstract String encode(Object obj);
    
}


