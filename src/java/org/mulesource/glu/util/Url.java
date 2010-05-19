/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.util;

public class Url
{
    private String urlStr;
    private String displayStr;
    
    public Url(String urlStr)
    {
        this(urlStr, null);
    }
    
    public Url(String urlStr, String displayStr)
    {
        this.urlStr     = urlStr;
        if (displayStr == null) {
            this.displayStr = urlStr;
        }
        else {
            this.displayStr = displayStr;
        }
    }
    
    public String toString()
    {
        return urlStr;
    }
    
    public String as_html()
    {
        return "<a href=\"" + urlStr + "\">" + displayStr + "</a>";
    }
}


