"""
Serves static files.

"""
from org.mulesource.glu   import Settings

from glu.core.basebrowser import BaseBrowser

        
class StaticBrowser(BaseBrowser):
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
        super(StaticBrowser, self).__init__(request,
                                            renderer_args = dict(raw=True))

    def process(self):
        """
        Process the request.
        
        Produce the data that needs to be displayed for any request
        handled by this browser. Currently, there is only one request
        handled by the meta browser.
        
        @return:  Http return code and data as a tuple.
        @rtype:   tuple
        
        """
        settings = Settings.getSettingsObject()
        path = self.request.getRequestPath()[len(settings.PREFIX_STATIC)+1:]
        if ".." in path:
            # Won't allow that
            return 400, "Invalid path specifier"
        if path.endswith("/"):
            path = path[:-1]
            
        try:
            f = open(settings.STATIC_LOCATION + path, "r")
            data = f.read()
            f.close()
            return 200, data
        except Exception, e:
            return 404, "Not found"
            
