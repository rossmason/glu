"""
The request dispatcher class, which directs requests
to the appropriate browsers.

"""
# Glu imports
import glu.settings as settings

from glu.exceptions             import *
from glu.core.basebrowser       import BaseBrowser
from glu.core.staticbrowser     import StaticBrowser
from glu.core.metabrowser       import MetaBrowser
from glu.core.codebrowser       import CodeBrowser 
from glu.core.resourcebrowser   import ResourceBrowser 

BROWSER_MAP   = {
                    settings.PREFIX_META     : MetaBrowser,
                    settings.PREFIX_RESOURCE : ResourceBrowser,
                    settings.PREFIX_CODE     : CodeBrowser,
                    settings.PREFIX_STATIC   : StaticBrowser,
                }
            
class RequestDispatcher(object):
    """
    Takes incoming HTTP requests and sends them off to the
    appropriate modules.
    
    """
    def handle(self, request):
        """
        Handle a request by dispatching it off to the correct handler.
        
        The handler is a 'browser' class, which can be looked up via the
        BROWSER_MAP that is defined in the settings file.
        
        This also catches any GluExceptions thrown by lower level code and
        translates them into log messages.
        
        @param request:   A properly wrapped request.
        @type request:    BaseHttpRequest
        
        @return:          Response code, body and headers
        @rtype:           Tuple of (int, string, dict)
        
        """
        #print "---- ", request.getRequestHeaders()
        content_type = None
        try:
            if request.getRequestPath() == "/":
                browser_class = BROWSER_MAP['/meta']
            else:
                method        = request.getRequestMethod().upper()
                prefix        = "/"+request.getRequestPath().split("/")[1]
                browser_class = BROWSER_MAP.get(prefix)
            
            if browser_class:
                browser_instance = browser_class(request)
                ( code, data )   = browser_instance.process()
                if code >= 200  and  code < 300:
                    # If all was OK with the request then we will
                    # render the output in the format that was
                    # requested by the client.
                    content_type, data = browser_instance.renderOutput(data)
            else:
                (code, data) = ( 404, "404 Not found" )
        except GluMethodNotAllowed, e:
            (code, data) = e.code, e.msg
        except GluMandatoryParameterMissing, e:
            (code, data) = e.code, e.msg
        except GluResourceNotFound, e:
            (code, data) = e.code, e.msg
        except GluException, e:
            (code, data) = ( 400, "Bad request: " + e.msg)

        headers = dict()
        if content_type:
            headers["Content-type"] = content_type
        
        return (code, data, headers)

