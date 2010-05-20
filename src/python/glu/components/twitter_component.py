"""
A test component.

"""
# Python imports
import urllib
import glujson as json

# Glu imports
from glu.components.api import *

class TwitterComponent(BaseComponent):
    NAME             = "TwitterComponent"
    PARAM_DEFINITION = {
                         "account_name" :     ParameterDef(PARAM_STRING, "Twitter account name"),
                         "account_password" : ParameterDef(PARAM_PASSWORD, "Password")
                       }
    
    DESCRIPTION      = "Provides access to a Twitter account."
    DOCUMENTATION    =  """
                        The Twitter component is designed to provide access to a Twitter account.
                        It can be used to get status as well as update status.
                        """
    SERVICES         = {
                         "status" :   { "desc" : "You can GET the status or POST a new status to it." },
                         "timeline" : { "desc" : "You can GET the timeline of the user." },
                       }
    

    def __get_status(self, accountname):
        """
        Get a the latest twitter status for the specified account.
        
        @param accountname: Name of the account for which we get the status.
        @type accountname:  string
        
        @return:            The status text.
        @rtype:             string
        
        """
        # Get the status for this account from Twitter (we get it in JSON format)
        code, data = self.httpGet("http://api.twitter.com/1/users/show.json?screen_name=%s" % accountname)
        if code == 200:
            obj = json.loads(data)
        else:
            return "Problem with Twitter: " + data
        
        # Return the requested information, in this case the latest status
        return obj['status']['text']
    
    def __post_status(self, accountname, password, input):
        """
        Post a the new twitter status for the specified account.
        
        @param accountname: Name of the account for which we post the status.
        @type accountname:  string
        
        @param password:    The password for this account.
        @type password:     string
        
        @param input:       The new status update text.
        @type input:        string

        @return:            The status text.
        @rtype:             string
        
        """
        # Get the status for this account from Twitter (we get it in JSON format)
        self.httpSetCredentials(accountname, password)
        code, data = self.httpPost("http://api.twitter.com/1/statuses/update.xml",
                                   "status=%s" % input)

        # Return the requested information, in this case the latest status
        return data
            
    def status(self, request, input, params, method):
        """
        Gets or updates the twitter status for the specified account.
        
        @param request:    Information about the HTTP request.
        @type request:     GluHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # Get my parameters
        account  = params['account_name']
        password = params['account_password']
        
        if not input:
            return 200, self.__get_status(account)
        else:
            return 200, self.__post_status(account, password, input)

    def timeline(self, request, input, params, method):
        """
        Get the user's timeline.
        
        @param request:    Information about the HTTP request.
        @type request:     GluHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @return:           The output data of this service.
        @rtype:            string

        """
        # Get my parameters
        self.httpSetCredentials(params['account_name'], params['account_password'])
        code, obj_str = self.httpGet("http://api.twitter.com/1/statuses/user_timeline.json")
        if code == 200:
            obj = json.loads(obj_str)
        else:
            obj = obj_str
        return code, obj

