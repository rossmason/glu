"""
Defines a base class for all beans.

"""
# Python imports
import urllib, urllib2
from copy import deepcopy

#Glu imports
import glu.settings as settings

from glu.core.util       import Url 
from glu.core.parameter  import *

#
# Utility method.
#
def _change_params_to_plain_dict(param_dict):
    """
    Unwraps all the parameter definitions into a plain dictionary.
    
    Needed for browsing or accessing the meta info.
    
    @param param_dict: Dictionary of parameter definitions, with each
                       individual parameter represented by a ParameterDef object.
    @type param_dict:  dict or ParameterDef objects
    
    @return:           Plain dictionary.
    @rtype:            dict
    
    """
    d = dict()
    for name in param_dict.keys():
        d[name] = param_dict[name].as_dict()
    return d


class BaseBean(object):
    """
    The base class for all code beans.
    
    A bean author only needs to override a few methods or data values
    to get started.
    
    Specifically:
    
        NAME
        PARAM_DEFINITION
        DESCRIPTION
        DOCUMENTATION
        SERVICES
        baseService()
        
    SERVICES and baseService() need to be explained.
    
    baseServices() is the normal method that is called to processes a request.
    However, a bean may also specify 'sub-SERVICES'. To do so, implement any
    number of additional services methods (with the same interface as baseService()).
    Then list those methods in the 'SERVICES' dictionary (use any name as key to
    a tuple containing the method itself as well as a doc string). Then your
    additional methods will be exposed as sub-services, which can be accessed
        like this: <resource_uri>/<sub_service_method>/....
    The name of the sub-service method is directly specified in the URI.
    
    If you don't want your bean to provide a base service (a fall back that catches
    all request that are not handled by a sub-service method) then specify the
    BASE_SERVICE flag in the class a false.
    
    """
    NAME             = ""
    """The name used to refer to this bean. Also used to construct its URL. No spaces allowed."""
    PARAM_DEFINITION = dict()
    """The parameter definition in the form of a dictionary."""
    DESCRIPTION      = ""
    """A short, one line description."""
    DOCUMENTATION    = ""
    """Longer, man-page style documentation."""
    BASE_SERVICE     = True
    """Indicates that the bean provides a base service on the resource's base URI."""
    SERVICES         = None
    """A dictionary keying method name to docstring for exposed sub-service methods. May be left empty."""
    
    def __init__(self):
        self.__accountname = None
        self.__password    = None
    
    def __get_http_opener(self, url):
        """
        Return an HTTP handler class, with credentials enabled if specified.
        
        @param url:    URL that needs to be fetched.
        @type url:     string
        
        @return:       HTTP opener (from urllib2)
        
        """
        if self.__accountname  and  self.__password:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, self.__accountname, self.__password)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
        else:
            opener = urllib2.build_opener()
        return opener
        
    def httpSetCredentials(self, accountname, password):
        """
        The bean author can set credentials for sites that require authentication.
        
        @param accountname:    Name of account
        @type accountname:     string
        
        @param password:       Password for account.
        @type password:        string
        
        """
        self.__accountname = accountname
        self.__password    = password
    
    def __http_access(self, url, data=None):
        """
        Access an HTTP resource with GET or POST.
        
        @param url:    The URL to access.
        @type url:     string
        
        @param data:   If present specifies the data for a POST request.
        @type data:    Data to be sent or None.
        
        @return:       Code and response data tuple.
        @rtype:        tuple
        
        """
        opener = self.__get_http_opener(url)
        resp = opener.open(url, data)
        code = 200
        data = resp.read()
        return code, data
        
    def httpGet(self, url):
        """
        Accesses the specified URL.
        
        If credentials have been specified, they will be used in case
        of HTTP basic authentication.
        
        @param url:        The URL to be accessed.
        @type url:         string
        
        @return:           Status and data as tuple.
        @rtype:            tuple
        
        """
        return self.__http_access(url)


    def httpPost(self, url, data):
        """
        Send the specified data to the specified URL.
        
        If credentials have been specified, they will be used in case
        of HTTP basic authentication.
        
        @param url:        The URL to be accessed.
        @type url:         string
        
        @param data:       The data to be sent to the URL.
        @type data:        string
        
        @return:           Status and data as tuple.
        @rtype:            tuple
        
        """
        return self.__http_access(url, data)


    def getMetaData(self):
        """
        Return meta data about this code.
        
        Contains name, description, documentation URI and parameter
        definitions as dictionary.
        
        @return: Meta info about the bean.
        @rtype:  dict
        
        """
        d = dict(uri    = Url(self.getUri()),
                 name   = self.getName(),
                 desc   = self.getDesc(),
                 doc    = Url(self.getUri() + "/doc"),
                 params = _change_params_to_plain_dict(self.getParams()),
                 services = self._getServices()
                )
        #
        # There is also a set of resource meta parameters that always remain
        # the same. Just some of the defaults and descriptions may change
        # from bean to bean.
        rp = dict(suggested_name = ParameterDef(PARAM_STRING,
                                                "Can be used to suggest the resource name to the server",
                                                required=True),
                  public         = ParameterDef(PARAM_BOOL,
                                                "Indicates whether the resource should be public",
                                                required=False, default=False),
                  desc           = ParameterDef(PARAM_STRING,
                                                "Specifies a description for this new resource",
                                                required=False, default="A '%s' resource" % self.getName())
                 )
        d['resource_creation_params'] = _change_params_to_plain_dict(rp)
        return d
    
    def getName(self):
        """
        Return the name of the bean.
        
        @return:  Name
        @rtype:   string
        
        """
        return self.NAME

    def getDesc(self):
        """
        Return the brief description string of the bean.
        
        @return:  Description.
        @rtype:   string
        
        """
        return self.DESCRIPTION
    
    def getDocs(self):
        """
        Return the documentation text for this bean.
        
        @return:  Documentation.
        @rtype:   string
        
        """
        return self.DOCUMENTATION

    def getUri(self):
        """
        Return the URI for this bean.
        
        @return: URI for the bean.
        @rtype:  string
        
        """
        return settings.PREFIX_CODE + "/" + self.getName()
    
    def getParams(self):
        """
        Return the parameter definition for this bean.
        
        @return: Parameter definition.
        @rtype:  dict (of ParameterDef objects)
        
        """
        return self.PARAM_DEFINITION

    
    #
    # -------------------------------------------------------------------------------------
    # Following are some methods that are used by the framework and that are not part
    # of the official bean-API.
    # -------------------------------------------------------------------------------------
    #
    def _getServices(self, resource_base_uri=None):
        """
        Return a dictionary with the exposed services.
        
        Keyed by name, for each service we return the uri and short description
        and service-specific parameter definition.
        
        @param resource_base_uri:  The base URI for the resource in which the services are
                                   exposed. The base URI through which services are accessed
                                   is the one of the resource (not of this code). Therefore,
                                   if we want the URI of the services in the context of the
                                   resource then we can call this method here with the base
                                   URI of the resource passed in.
        @type resource_base_uri:   string
        
        @return:                   Dictionary with sub-service info.
        @rtype:                    dict
        
        """
        if resource_base_uri:
            base_uri = resource_base_uri
        else:
            # No base URI specified? Then we can get the service URIs relative to
            # the code's URI.
            base_uri = self.getUri()
        if self.SERVICES:
            ret = dict()
            for name in self.SERVICES.keys():
                ret[name]  = deepcopy(self.SERVICES[name])  # That's a dictionary with params definitions and descs
                # Create proper dict representations of each parameter definition
                if 'params' in ret[name]:
                    for pname in ret[name]['params'].keys():
                        if type(ret[name]['params'][pname]) is ParameterDef:
                            # Need the type check since we may have constructed the
                            # representation from storage, rather than in memory.
                            # If it's from storage then we don't have ParameterDefs
                            # in this dictionary here, so we don't need to convert
                            # anything.
                            ret[name]['params'][pname] = ret[name]['params'][pname].as_dict()
                ret[name]['uri'] = base_uri + "/" + name
            return ret
            #return dict([(name, dict(uri=base_uri + "/" + name, desc=self.SERVICES[name])) for name in self.SERVICES.keys() ])
        else:
            return None
        
    def _requestProcessor(self, request, uri_suffix, params):
        """
        Initial processing of a request.
        
        Inspect the URI and determine if the request is for a known
        sub-resource of this resource. If not then pass the request
        on to the baseService() method.
        
        Does any pre-processing of the request, such as extracting
        parameters from the URI.
        
        This method is called by the framework in response to a
        request to a resource (not the code). Therefore, the path
        in the request indicates the stored resource. This code here
        does not know anything about the stored resource. Therefore,
        the components AFTER the resource URI have been provided to
        us by the framework as well in the path_suffix parameter.
        
        This method is called by the framework and is not part of
        the official bean-API.
        
        @param request:    The HTTP request.
        @type request:     BaseHttpRequest
        
        @param uri_suffix: The URI suffix AFTER the part that identifies
                           the resource. So, if /foo/bar identifies the
                           resource and the request was /foo/bar/blah?a=123
                           then uri_suffix contains "/blah?a=123".
        @type uri_suffix:  string
        
        @param params:     The parameters specified for this resource. Those
                           are the parameters that have been stored as part
                           of the resource definition, possibly with some of
                           them overwritten by run-time parameters.
        @type params:      dict
        
        @return:           Output to be returned to client as (code, data) tuple.
        @rtype:            tuple.
        
        """
        path, query = urllib.splitquery(uri_suffix)
        method = None
        if self.SERVICES:
            if path:
                sub_resource_path = path.split[1:]("/")  # Skip leading '/'
                sub_resource_name = sub_resource_path[0] # There could be multiple path elements
                if sub_resource_name in self.SERVICES:
                    # See if we can find the specified sub-service method.
                    try:
                        docs   = self.SERVICES[sub_resource_name]
                        # Get handle on the method with the same name as the service
                        method = getattr(self, sub_resource_name)
                    except AttributeError, e:
                        method = None
                    return (404, "sub-resource '%s' not found in implementation" % sub_resource_name)
        
        if self.BASE_SERVICE:
            method = self.baseService
        else:
            return (404, "no matching sub-service found for '%s'" % sub_resource_name)
        
        # Finally call the service method
        return method(request, params)

        

