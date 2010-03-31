"""
Provide an abstraction layer for a concrete HTTP server implementation.

This allows the rest of our code to be written without server specifics
being spread all over the place. That way, we can always change the
concrete HttpServer implementation later on.

"""

# Java imports
from com.sun.net.httpserver import HttpServer, HttpHandler
from java.net               import InetSocketAddress
from java.lang              import String
from java.io                import InputStreamReader;
from java.io                import BufferedReader
from java.io                import DataOutputStream

# Python imports
import sys
import traceback

# Glu imports
import glu.settings as settings

from glu.logger import *

from glu.httpabstraction.base_server import BaseHttpServer, BaseHttpRequest

class JythonJavaHttpRequest(BaseHttpRequest):
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
    __response_code   = None
    __native_req      = None
    __request_uri_str = None
    __request_headers = None
    
    def __init__(self, native_request):
        """
        Initialize request wrapper with the native request class.
        
        The BaseHttpRequest may be used anywhere, but is only created within
        the http-abstraction-API. Therefore, it is ok for it to get the
        native-request object passed into it here.
        
        @param native_request:  The request representation of the native server.
        @type native_request:   com.sun.net.httpserver.HttpExchange
        
        """
        self.__native_req      = native_request
    
    def setResponseCode(self, code):
        """
        Set the response code, such as 200, 404, etc.
        
        This is the code that is sent in the response from the server
        to the client.
                
        The method can be called multiple times with different values
        before any of the send methods are called.
        
        @param code:  HTTP response code
        @type code:   int
        
        """
        self.__response_code = code
        
    def setResponseBody(self, body):
        """
        Set the response body.
        
        This method may be called multiple times with different values.
        
        @param body:    The data that should be send in the response body.
        @type body:     string
        
        """
        self.__response_body = String(body)
        
                    
    def setResponse(self, code, body):
        """
        Set response code and body in one function.

        Same as calling setResponseCode() and setResponseBody()
        separately.
        
        @param code:    HTTP response code
        @type code:     int

        @param body:    The data that should be send in the response body.
        @type body:     string
        
        """
        self.setResponseCode(code)
        self.setResponseBody(body)
    
    def getRequestProtocol(self):
        """
        Return the protocol of the request.
        
        @return:    Protocol of the request, such as "HTTP/1.1"
        @rtype:     string
        
        """
        return self.__native_req.getProtocol()
    
    def getRequestMethod(self):
        """
        Return the method of the request.

        @return:    Method of the request, such as "GET", "POST", etc.
        @rtype:     string
        
        """
        return self.__native_req.getRequestMethod().upper()

    def getRequestURI(self):
        """
        Return the full URI of the request.
        
        @return:    URI of the request, containing server, path
                    and query portion.
        @rtype:     string
        
        """
        if not self.__request_uri_str:
            self.__request_uri_str = self.__native_req.getRequestURI().toString()
        return self.__request_uri_str
    
    def getRequestPath(self):
        """
        Return only the path component of the URI.
        
        @return:    The path component of the URI.
        @rtype:     string
        
        """
        return self.__native_req.getRequestURI().getPath()
    
    def getRequestHeaders(self):
        """
        Return a dictionary with the request headers.
        
        Each header can have multiple entries, so this is a
        dictionary of lists.
        
        @return:    Dictionary containing a list of values for each header.
        @rtype:     dict
        
        """
        if not self.__request_headers:
            self.__request_headers = dict(self.__native_req.getRequestHeaders())
        return self.__request_headers
    
    def getRequestQuery(self):
        """
        Return only the query component of the URI.
        
        @return:    Query portion of the URI (the part after the first '?').
        @rtype:     string
        
        """
        return self.__native_req.getRequestURI().getQuery()
    
    def getRequestBody(self):
        """
        Return the body of the request message.
        
        Note that this is not very suitable for streaming or large message bodies
        at this point, since the entire message is read into a single string
        before it is returned to the client.
        
        @return:    Body of the request.
        @rtype:     string
        
        """
        buffered_reader = BufferedReader(InputStreamReader(self.__native_req.getRequestBody()));
        lines = []
        while True:
            line = buffered_reader.readLine()
            if not line:
                break
            lines.append(line)
        
        return '\n'.join(lines)
    
    def sendResponseHeaders(self):
        """
        Send the previously specified response headers and code.
        
        """
        self.__native_req.sendResponseHeaders(self.__response_code, self.__response_body.length())
    
    def sendResponseBody(self):
        """
        Send the previously specified request body.
        
        """
        os = DataOutputStream(self.__native_req.getResponseBody())
        os.writeBytes(self.__response_body)
        os.flush()
        os.close()
        
    def sendResponse(self):
        """
        Send the previously specified response headers, code and body.
        
        This is the same as calling sendResponseHeaders() and sendResponseBody()
        separately.
        
        """
        self.sendResponseHeaders()
        self.sendResponseBody()
        
    def close(self):
        """
        Close this connection.
        
        """
        self.__native_req.close()  


class __HttpHandler(HttpHandler):
    """
    The native HTTP server (com.sun.net.httpserver.HttpServer) requires a handler class.
    
    Since this is something specific to the particular server,
    this class is not part of the official http-abstraction-API.
    
    """
    def __init__(self, request_handler, request_class):
        """
        Initialize the handler class for the native request.
        
        After converting the native request to a BaseHttpRequest,
        this is then passed on to a generic request handler.
        
        @param request_handler: Any class that provides a 'handle()'
                                method that can take a BaseHttpRequest.
                                Those handler classes are provided by
                                or generic code and are passed through
                                to this native handler here during server
                                creation.
        @type request_handler:  Any class that provides a 'handle()' method
                                that can take a BaseHttpRequest. Normally,
                                this is our RequestDispatcher class.
                                
        @param request_class:   The class that's used to wrap the request.
        @type request_class:    Any class derived from BaseHttpRequest.
        
        """
        self.request_handler = request_handler
        self.request_class   = request_class
        
    def handle(self, native_request):
        """
        Handle a native request.
        
        Converts the native request to a BaseHttpRequest, prepares
        logging and exception handling and calls the generic
        handler class, which was specified during server creation
        (normally our RequestDispatcher class).
        
        Any so-far unhandled exceptions are caught here and a stack
        trace is printed to stderr.
        
        @param native_request:    The native request from the native server.
        @type native_request:     com.sun.net.httpserver.HttpExchange
        
        """
        try:
            start_time = datetime.datetime.now()
            req = self.request_class(native_request)            
            msg = "%s : %s : %s" % (req.getRequestProtocol(),
                                    req.getRequestMethod(),
                                    req.getRequestURI())
            #log(msg, facility=LOGF_ACCESS_LOG)
            code, response_body = self.request_handler.handle(req)
            req.setResponse(code, response_body)
            req.sendResponse()
            native_request.close()
            end_time   = datetime.datetime.now()
            td         = end_time-start_time
            request_ms = td.seconds*1000 + td.microseconds//1000
            log("%s : %sms : %s : %s" % (msg, request_ms, code, len(response_body)),
                start_time = start_time, facility=LOGF_ACCESS_LOG)
        except Exception, e:
            print traceback.format_exc()
            sys.exit(1)


class JythonJavaHttpServer(BaseHttpServer):
    """
    Wrapper class around a concrete HTTP server implementation.
    
    """
            
    __native_server = None
    
    def __init__(self, port, request_handler, request_class):
        """
        Initialize and start an HTTP server.
        
        Uses a native HTTP server implementation, in this case
        the com.sun.net.httpserver.HttpServer.
        
        @param port:            The port on which the server should listen.
        @type port:             int
        
        @param request_handler: The request handler class from our generic code.
        @type request_handler:  Any class with a 'handle()' method that can take a
                                BaseHttpRequest. In our case, this is normally the
                                RequestDispatcher class.
        
        """
        self.request_handler = request_handler
        self.__native_server = HttpServer.create(InetSocketAddress(port), 5);
        self.__native_server.createContext(settings.DOCUMENT_ROOT,
                                           __HttpHandler(request_handler, request_class));
        self.__native_server.setExecutor(None);
        self.__native_server.start();
        log("Listening for HTTP requests on port %d..." % port)
