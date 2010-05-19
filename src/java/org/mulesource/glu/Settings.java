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

import org.python.util.PythonInterpreter;
import org.python.core.PyObject;
import org.python.core.PyString;

public class Settings
{
    /*
     * Eventually this will provide access to all config parameters.
     * In the meantime, it uses some Jython specifics to get access to
     * the configs that are stored in settings.py
     */
    
    /*
     * Our handle on the Python interpreter. It is initialized in the static
     * initializer and then re-used in the getFromPythonSettings() method.
     */
    private static PythonInterpreter interp;

    /*
     * Used to initialize individual Java class members with values from
     * the Python settings.py module.
     */
    private static String getFromPythonSettings(String objName)
    {
        PyObject pyObject = interp.get(objName);
        return (String)pyObject.__tojava__(String.class);        
    }
    
    /*
     * Initialize and import only once.
     */
    static {
        interp = new PythonInterpreter();
        interp.exec("from glu.settings import *");
    }

    /*
     * Here finally we have the publicly exported symbols.
     */
    public static String PREFIX_CODE     = getFromPythonSettings("PREFIX_CODE");
    public static String PREFIX_RESOURCE = getFromPythonSettings("PREFIX_RESOURCE");;
}


