"""
Settings for Glue.

"""


DOCUMENT_ROOT   = "/"
PREFIX_META     = "/meta"
PREFIX_CODE     = "/code"
PREFIX_RESOURCE = "/resource"
PREFIX_STATIC   = "/static"

LISTEN_PORT     = 8001
#STATIC_LOCATION = "/home/jbrendel/Programming/google_appengine/glu/static_files/"
STATIC_LOCATION = "static_files/"

NEVER_HUMAN   = False

HTML_HEADER = """
<html>
    <head>
        <title>MuleSoft Glu</title>
        <style type="text/css">
            table {
                   border-color:#aaaaaa;
                   /*border-spacing:0px;*/
            }
            td {
                padding:4px;
                /*border:1px solid #aaaaaa;*/
                
            }
            td.dict {
                padding:2px 4px;
                background-color:#dddddd;
            }
        </style>
    </head>
    <body>
        <h2>Glu <small>(by MuleSoft)</small></h2>
        <hr>
"""

HTML_FOOTER = """
<hr>
<center><small>(c) 2010 by MuleSoft</small></center>
</body>
</html>
"""
