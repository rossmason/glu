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

public class GluResourceNotFoundException extends GluFileNotFoundException
{
    public GluResourceNotFoundException()
    {
        this("Resource not found");
    }
    
    public GluResourceNotFoundException(String message)
    {
        super(message);
    }
}


