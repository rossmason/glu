"""
Provide an abstraction layer for a concrete HTTP server implementation.

This allows the rest of our code to be written without server specifics
being spread all over the place. That way, we can always change the
concrete HttpServer implementation later on.

"""

class BaseHttpRequest(object):
    """
    Wrapper class around a concrete HTTP request representation.
    
    The class contains information about the received request and
    also provided the means to send a response. Therefore, this
    class encapsulates and controls the entire HTTP exchange between
    client and server.
    
    This class is part of the official http-abstraction-API. It is
    intended to be used by the rest of the code, shielding it from
    the specific server implementation.
    
    """
    def __init__(self, native_request): pass
    
    def setResponseCode(self, code): pass
        
    def setResponseBody(self, body): pass
                    
    def setResponse(self, code, body): pass
    
    def getRequestProtocol(self): pass
    
    def getRequestMethod(self): pass

    def getRequestURI(self): pass
    
    def getRequestPath(self): pass
    
    def getRequestHeaders(self): pass
    
    def getRequestQuery(self): pass
    
    def getRequestQueryDict(self):
        """
        Return a dictionary of the parsed query arguments.
        
        @return:  Dictionary with query arguments.
        @rtype:   dict
        
        """
        query_string = self.getRequestQuery()
        if query_string:
            # Parse the query string apart and put values into a dictionary
            runtime_param_dict = dict([elem.split("=") if "=" in elem else (elem, None) \
                                                       for elem in query_string.split("&")])
        else:
            runtime_param_dict = dict()
        return runtime_param_dict
    
    def getRequestBody(self): pass
    
    def sendResponseHeaders(self): pass
    
    def sendResponseBody(self): pass
        
    def sendResponse(self): pass
        
    def close(self): pass


class BaseHttpServer(object):
    """
    Wrapper class around a concrete HTTP server implementation.
    
    """    
    def __init__(self, port, request_handler, request_class): pass
