"""
Base class for all content browser classes.

"""
# Glu imports
import glu.settings as settings

from glu.render import HtmlRenderer
from glu.render import JsonRenderer

class BaseBrowser(object):
    """
    A browser is a class that handles specific requests after they
    are assigned by the request-dispatcher.
    
    For example, there might be a specialized browser to deal with
    the installed beans/code, another browser for server meta data
    and another to deal with resources.
    
    The RequestDispatcher instantiates specific browsers based on
    the URI prefix.
    
    This base class provides methods to detect the requested content
    type and to format output according to that content type.
    
    """
    def __init__(self, request, renderer_args = None):
        """
        Initialize and perform analysis of request headers.
        
        The 'human_client' flag is set unless 'application/json'
        was requested in the accept header. This is because we
        are assuming that a non-human client wants the easily
        parsable json.
                        
        @param request:        This HTTP request.
        @type request:         BaseHttpRequest
        
        @param renderer_args:  A dictionary of arguments for the
                               chosen renderer. It's passed straight through
                               to the renderer and is not used by the browser.
        @type renderer_args:   dict (or None)
        
        """
        self.request       = request
        self.headers       = request.getRequestHeaders()
        accept_header      = self.headers.get("Accept", list())
        self.human_client  = False if "application/json" in accept_header or settings.NEVER_HUMAN else True
        self.header        = ""
        self.footer        = ""
        self.renderer_args = renderer_args
        self.breadcrums    = []
    
    def getBreadcrums(self):
        """
        Return the breadcrum definition for this request.
        
        Breadcrums are maintained by each browser according to
        a simpe definition: [ (name, uri), (name, uri), ... ]
        
        The breadcrums are passed to the renderer.
        
        @return:     List of breadcrums.
        @rtype:      list
        
        """
        return self.breadcrums
            
    def renderOutput(self, data):
        """
        Take a Python object and return it rendered.
        
        This uses a specific renderer class to convert the raw
        data (a Python object) to data that can be sent back to
        the client.
        
        @param data:  A Python object that should consist only of dictionaries
                      and lists. The output is rendered in JSON, HTML, etc.
                      based on details we have gleaned from the request. For
                      example, there is a human_client flag, which if set indicates
                      that the output should be in HTML.
        @type data:   object
        
        @return:      Rendered data, ready to be sent to the client.
        @rtype:       string

        """
        if self.human_client:
            renderer = HtmlRenderer(self.renderer_args, self.breadcrums)
        else:
            renderer = JsonRenderer(self.renderer_args)
        return renderer.base_renderer(data, top_level=True)
    
    def process(self):
        """
        Process the request.
        
        This needs to be overwritten with a specific implementation.
        
        @return:  Http return code and data as a tuple.
        @rtype:   tuple
        
        """
        return ( 200, "Base Browser" )

                
