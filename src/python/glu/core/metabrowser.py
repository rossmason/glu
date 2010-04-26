"""
Allows users and clients to browse the server's meta information.

"""
import glu.settings as settings

from glu.core.basebrowser import BaseBrowser
from glu.core.util        import Url

        
class MetaBrowser(BaseBrowser):
    """
    Handles requests for meta data of the server.
    
    Meta data here is defined as non-code and non-resource data.
    For example, the name of the server, version number, links to
    the other, more interesting sections, etc.
    
    Just contains a bunch of static links.
    
    """
    def __init__(self, request):
        """
        Create the new meta browser for a request.
        
        @param request:  The client's HTTP request.
        @type request:   BaseHttpRequest
        
        """
        # Initialize the browser with the render-args we need for meta data browsing
        super(MetaBrowser, self).__init__(request,
                                          renderer_args = dict(no_annotations=True,
                                                               no_list_indices=True,
                                                               no_borders=False))
    def process(self):
        """
        Process the request.
        
        Produce the data that needs to be displayed for any request
        handled by this browser. Currently, there is only one request
        handled by the meta browser.
        
        @return:  Http return code and data as a tuple.
        @rtype:   tuple
        
        """
        self.breadcrums = [ ("Home","/") ]

        path = self.request.getRequestPath()
        if path in [ "/", settings.PREFIX_META ]:
            data = {
                    "code"     : Url(settings.PREFIX_CODE),
                    "resource" : Url(settings.PREFIX_RESOURCE),
                    "static"   : Url(settings.PREFIX_STATIC),
                    "name"     : "MuleSoft Glu server prototype",
                    "version"  : "(prototype)",
                    "doc"      : Url(settings.PREFIX_META + "/doc")
            }
            code = 200
            
        elif path == settings.PREFIX_META + "/doc":
            self.breadcrums.append(("Doc", settings.PREFIX_META + "/doc"))
            data = """
This is the documentation for the server.

Click around and have fun.
"""
            code = 200
        else:
            data = "Don't know this meta page"
            code = 404
        
        return ( code, data )
