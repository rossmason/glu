"""
A test bean.

"""
# Python imports
import urllib

# Glu imports
from glu.beans.api                 import *
#from glu.beans                     import GsearchBean

class CombinerBean(BaseBean):
    NAME             = "CombinerBean"
    PARAM_DEFINITION = {
                       }
    
    DESCRIPTION      = "Calls another bean."
    DOCUMENTATION    =  """
                        This is just a test to see how we can call another bean.
                        
                        """
    SERVICES         = {
                           "combine" :   {
                               "desc"   : "Combines stuff"
                           }
                       }
    
            
    def combine(self, request, input, params):
        """
        Calls another bean.
        
        @param request:    Information about the HTTP request.
        @type request:     BaseHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # If you want to use another resource from within your bean
        # code you can do this in three different ways:
        #
        #   1. Issue an HTTP request to the resource's URI. Works
        #      but is not as efficient as it could be if you are
        #      already running in the same process as that other resource.
        #
        #   2. Instantiate the bean and provide all the necessary
        #      arguments yourself.
        #
        #   3. Use the runResource() method to utilizse an already
        #      existing resource definition. This is nice, because
        #      you only need to provide the run-time parameters, if any.
        #
        
        #
        # Example of (2): Instantiating the bean directly.
        #
        #gsearch_bean = GsearchBean()
        #code, data = gsearch_bean.search(None, None, { 'query'   : 'mule+esb',
        #                                               'api_key' : "ABQIAAAApvtgUnVbhZ4o1RA5ncDnZhT2yXp_ZAY8_ufC3CFXhHIE1NvwkxS5mUUQ41lAGdMeNzzWizhSGRxfiA" })
        #
        # Example of (3): Using an already existing resource definition.
        #
        code, data = runResource("MyGoogleSearch", "search", params = { "query" : "mule+esb" })
        if code == 200:
            data = "Received the following data: " + data
        else:
            data = "Looks like there was a problem: " + data
        return code, data

