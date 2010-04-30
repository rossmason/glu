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

import org.mulesource.glu.exceptions.GluException;

public class GluMandatoryParameterMissingException extends GluException
{
    /*
     * The default message and code is what makes this class unique.
     */
    private final static String DEFAULT_MSG = "Mandatory parameter missing";
    private final static int    CODE        = 400;
    
    /*
     * The usual set of constructors for exceptions
     */
    public GluMandatoryParameterMissingException()
    {
        super(DEFAULT_MSG);
    }

    public GluMandatoryParameterMissingException(String msg)
    {
        super(msg);
        // TODO Auto-generated constructor stub
    }
    
    public GluMandatoryParameterMissingException(Throwable ex)
    {
        super(DEFAULT_MSG, ex);
    }

    public GluMandatoryParameterMissingException(String msg, Throwable ex)
    {
        super(msg, ex);
        // TODO Auto-generated constructor stub
    }
    
    public int getCode()
    {
        return CODE;
    }

}


