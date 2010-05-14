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

public class GluPermissionDeniedException extends GluException
{
    /*
     * The default message and code is what makes this class unique.
     */
    private final static String DEFAULT_MSG  = "Permission denied";
    private final static int    DEFAULT_CODE = 403;
    
    /*
     * The usual set of constructors for exceptions
     */
    public GluPermissionDeniedException()
    {
        super(DEFAULT_MSG, DEFAULT_CODE);
    }

    public GluPermissionDeniedException(String msg)
    {
        super(msg, DEFAULT_CODE);
    }
    
    public GluPermissionDeniedException(Throwable ex)
    {
        super(DEFAULT_MSG, DEFAULT_CODE, ex);
    }

    public GluPermissionDeniedException(String msg, Throwable ex)
    {
        super(msg, DEFAULT_CODE, ex);
    }
}


