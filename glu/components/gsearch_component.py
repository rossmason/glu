"""
A test component.

"""
# Python imports
import urllib
import glujson as json

# Glu imports
from glu.components.api import *

class GsearchComponent(BaseComponent):
    NAME             = "GoogleSearchComponent"
    PARAM_DEFINITION = {
                           "api_key" : ParameterDef(PARAM_STRING, "Google API key", required=True)
                       }
    
    DESCRIPTION      = "Provides an interface to Google Search."
    DOCUMENTATION    =  """
                        This component is used to perform Google searches.
                        
                        Provide a search term as the 'query' attribute.
                        """
    SERVICES         = {
                           "search" :   {
                               "desc"   : "Provide 'query' as attribute to GET a search result. A 'num'ber of results can optionally be specified as well.",
                               "params" : {
                                    "query" : ParameterDef(PARAM_STRING, "The search query",
                                                           required=True,
                                                           default="computer"),
                                    "num"   : ParameterDef(PARAM_NUMBER, "The number of results you would like to have returned",
                                                           required=False,
                                                           default=10)
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
        num        = params['num']
        key        = params['api_key']
        # This is the official API, which seems to require the API key
        #code, data = self.httpGet("http://base.google.com/base/feeds/snippets?q=%s&key=%s" % (query, key))
        #
        # But we like things in JSON. There is another Google search API, which does things in JSON,
        # and which does not require the API key. It only seems to read 10 (or so) results at any
        # time, so we put this in a loop until we have the requested number of results.
        # 
        start = 1
        results = []
        while len(results) < num:
            url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&start=%d" % (query, start)
            code, data_str = self.httpGet(url)
            if code == 200:
                try:
                    data      = json.loads(data_str)
                    new_batch = data['responseData']['results']
                    results  += new_batch
                except Exception, e:
                    return 400, "Result data was malformed: " + str(e)
        return code, results[:num]

