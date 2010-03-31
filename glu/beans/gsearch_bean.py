"""
A test bean.

"""
# Python imports
import urllib
import glujson as json

# Glu imports
from glu.beans.api import *

class GsearchBean(BaseBean):
    NAME             = "GoogleSearchBean"
    PARAM_DEFINITION = {
                           "api_key" : ParameterDef(PARAM_STRING, "Google API key", required=True)
                       }
    
    DESCRIPTION      = "Provides an interface to Google Search."
    DOCUMENTATION    =  """
                        This bean is used to perform Google searches.
                        
                        Provide a search term as the 'query' attribute.
                        """
    SERVICES         = {
                           "search" :   {
                               "desc"   : "Provide 'query' as attribute to GET a search result.",
                               "params" : {
                                    "query" : ParameterDef(PARAM_STRING, "The search query",
                                                           required=True,
                                                           default="computer"),
                               }
                           }
                       }
    
            
    def search(self, request, input, params):
        """
        Perform a Google search.
        
        @param request:    Information about the HTTP request.
        @type request:     BaseHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # Get my parameters
        query      = params['query']
        key        = params['api_key']
        code, data = self.httpGet("http://base.google.com/base/feeds/snippets?q=%s&key=%s" % (query, key))
        return code, data

