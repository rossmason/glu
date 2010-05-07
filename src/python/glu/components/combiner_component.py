"""
A test component.

"""
# Python imports
import urllib

# Glu imports
from glu.components.api                 import *
#from glu.components                     import GsearchComponent

class CombinerComponent(BaseComponent):
    NAME             = "CombinerComponent"
    PARAM_DEFINITION = {
                       }
    
    DESCRIPTION      = "Calls another component."
    DOCUMENTATION    =  """
                        This is just a test to see how we can call another component.
                        
                        """
    SERVICES         = {
                           "combine" :   {
                               "desc"   : "Combines stuff"
                           }
                       }
    
            
    def combine(self, request, input, params):
        """
        Calls another component.
        
        @param request:    Information about the HTTP request.
        @type request:     BaseHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # If you want to use another resource from within your component
        # code you can do this in three different ways:
        #
        #   1. Issue an HTTP request to the resource's URI. Works
        #      but is not as efficient as it could be if you are
        #      already running in the same process as that other resource.
        #
        #   2. Instantiate the component and provide all the necessary
        #      arguments yourself.
        #
        #   3. Use the runResource() method to utilizse an already
        #      existing resource definition. This is nice, because
        #      you only need to provide the run-time parameters, if any.
        #
        
        #
        # Example of (2): Instantiating the component directly.
        #
        #gsearch_component = GsearchComponent()
        #code, data = gsearch_component.search(None, None, { 'query'   : 'mule+esb',
        #                                               'api_key' : "ABQIAAAApvtgUnVbhZ4o1RA5ncDnZhT2yXp_ZAY8_ufC3CFXhHIE1NvwkxS5mUUQ41lAGdMeNzzWizhSGRxfiA" })
        #
        # Example of (3): Using an already existing resource definition.
        #
        code, data = runResource("MyGoogleSearch/search", params = { "query" : "mule+esb" })
        if code == 200:
            data = "Received the following data: " + str(data)
        else:
            data = "Looks like there was a problem: " + str(data)
        return code, data

