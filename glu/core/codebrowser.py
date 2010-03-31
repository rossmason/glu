"""
Allows users and clients to browse the server's installed code.

"""
# Java imports
import glujson as json

# Glu imports
import glu.settings as settings

from glu.exceptions       import GluException
from glu.beans            import _CODE_MAP
from glu.resources        import makeResource 
from glu.core.basebrowser import BaseBrowser
from glu.core.util        import Url


def getBeanClass(uri):
    """
    Return the specified bean class, based on a given URI.
    
    @param uri:     The official URI for this code.
    @type uri:      string
    
    @return         Class of the specified bean
                    or None if no matching bean class was found.
    @rtype          A class derived from BaseBean
    
    """
    path_elems = uri[len(settings.PREFIX_CODE):].split("/")[1:]
    bean_name  = path_elems[0]   # This should be the name of the code element
    
    # Instantiate the bean
    return _CODE_MAP.get(bean_name)

def getBeanInstance(uri):
    """
    Return an instantiated bean, the class of which was identified by a URI.

    @param uri:     The official URI for this code.
    @type uri:      string
    
    @return         Instance of the specified bean
                    or None if no matching bean class was found.
    @rtype          Instance of a class derived from BaseBean
    
    """
    bean_class = getBeanClass(uri)
    if bean_class:
        return bean_class()
    else:
        return None
        
class CodeBrowser(BaseBrowser):
    """
    Handles requests for code info.
    
    """
    def __init__(self, request):
        """
        Initialize the browser with the render-args we need for meta data browsing.
        
        @param request: Handle to the HTTP request that needs to be processed.
        @type request:  BaseHttpRequest
        
        """
        super(CodeBrowser, self).__init__(request,
                                          renderer_args = dict(no_annotations=True,
                                                               no_table_headers=False,
                                                               no_list_indices=False,
                                                               no_borders=False))
    
    def __process_get(self):
        """
        Respond to GET requests.
        
        When someone sends GET requests to the code then
        they want to browse the available code options.
        
        @return:  HTTP return code and data as a tuple.
        @rtype:   tuple

        """
        # It's the responsibility of the browser class to provide breadcrums
        self.breadcrums = [ ("Home", settings.DOCUMENT_ROOT), ("Code", settings.PREFIX_CODE) ]

        if self.request.getRequestPath() == settings.PREFIX_CODE:
            #
            # Just show the home page of the code browser (list of all installed code)
            #
            data = dict([ (name, { "uri" : Url(class_name().getUri()), "desc" : class_name().getDesc() } ) \
                                for (name, class_name) in _CODE_MAP.items() ])
        else:
            # Path elements (the known code prefix is stripped off)
            path_elems = self.request.getRequestPath()[len(settings.PREFIX_CODE):].split("/")[1:]
            bean_name  = path_elems[0]   # This should be the name of the code element
            
            # Instantiate the bean
            bean_class = getBeanClass(self.request.getRequestPath())
            if not bean_class:
                return (404, "Unknown bean")
            bean          = bean_class()
            bean_home_uri = bean.getUri()
            self.breadcrums.append((bean_name, bean_home_uri))

            if len(path_elems) == 1:
                #
                # No sub-detail specified: We want meta info about a code segment (bean)
                #
                data = bean.getMetaData()
            else:
                #
                # Some sub-detail of the requested bean was requested
                #
                sub_name = path_elems[1]
                if sub_name == "doc":
                    data       = bean.getDocs()
                    self.breadcrums.append(("Doc", bean_home_uri + "/doc"))
                else:
                    return (404, "Unknown code detail")
                
        return ( 200, data )
    
    
    def __process_post(self):
        """
        Process a POST request.
        
        The only allowed POST requests to code are requests
        to the base URI of a bean. This creates a new resource.
        
        @return:  HTTP return code and data as a tuple.
        @rtype:   tuple

        """
        #
        # Start by processing and sanity-checking the request.
        #
        bean_class = getBeanClass(self.request.getRequestPath())
        if not bean_class:
            return (404, "Unknown bean")
        #bean = bean_class()
        body = self.request.getRequestBody()
        try:
            param_dict = json.loads(body)
        except Exception, e:
            raise GluException("Malformed request body: " + str(e))
        ret_msg = makeResource(bean_class, param_dict)
        return ( 200, ret_msg )
    
    def process(self):
        """
        Process the request.
        
        @return:  HTTP return code and data as a tuple.
        @rtype:   tuple
        
        """
        method = self.request.getRequestMethod()
        if method == "GET":
            (code, data) = self.__process_get()
        elif method == "POST":
            (code, data) = self.__process_post()
        return (code, data)
