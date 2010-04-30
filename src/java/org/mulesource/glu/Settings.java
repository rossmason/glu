/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */


/*
 * A singleton for all of our settings.
 */

package org.mulesource.glu;

public class Settings
{
    /* ------------------- 
     * The public settings
     * ------------------- */

    public String  DOCUMENT_ROOT   = "/";
    public String  PREFIX_META     = "/meta";
    public String  PREFIX_CODE     = "/code";
    public String  PREFIX_RESOURCE = "/resource";
    public String  PREFIX_STATIC   = "/static";
    public String  STATIC_LOCATION = "static_files/";
    public int     LISTEN_PORT     = 8001;
    public boolean NEVER_HUMAN     = false;
    
    public String  HTML_HEADER     = "<html>" +
                                     "<head>" +
                                     "    <title>MuleSoft Glu</title>" +
                                     "    <style type=text/css>" +
                                     "       table {" +
                                     "               border-color:#aaaaaa;" +
                                     "               /*border-spacing:0px;*/" +
                                     "        }" +
                                     "        td {" +
                                     "            padding:4px;" +
                                     "            /*border:1px solid #aaaaaa;*/" +
                                     "        }" +
                                     "        td.dict {" +
                                     "            padding:2px 4px;" +
                                     "            background-color:#dddddd;" +
                                     "        }" +
                                     "    </style>" +
                                     "</head>" +
                                     "<body>" +
                                     "    <h2>Glu <small>(by MuleSoft)</small></h2>" +
                                     "    <hr>";

    public String  HTML_FOOTER    = "<hr>" +
                                    "<center><small>(c) 2010 by MuleSoft</small></center>" +
                                    "</body>" +
                                    "</html>";
    
    /* ----------------------------------------------------------
     * The stuff below is only here to ensure this is a singleton
     * ---------------------------------------------------------- */
    
    private static Settings ref = null;
    
    private Settings()
    {
        // No direct construction allowed (singleton)
    }

    public static synchronized Settings getSettingsObject()
    {
        // Get or return the already existing instance (singleton)
        if (ref == null) {
            ref = new Settings();
        }
        return ref;
    }

    public Object clone() throws CloneNotSupportedException
    {
        // No cloning allowed (singleton)
        throw new CloneNotSupportedException();
    }
}

