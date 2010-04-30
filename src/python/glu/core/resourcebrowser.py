"""
Allows users and clients to browse the defined resources.
      
"""
# Python imports
import os
import traceback

# Glu imports
from org.mulesource.glu            import Settings
from org.mulesource.glu.exceptions import *

from glu.logger                    import *
from glu.core.basebrowser          import BaseBrowser
from glu.core.util                 import Url
from glu.core.codebrowser          import getComponentInstance
from glu.resources                 import paramSanityCheck, fillDefaults, makeResource, listResources, \
                                          retrieveResourceFromStorage, getResourceUri, deleteResourceFromStorage
from glu.resources.resource_runner import _accessComponentService, _getResourceDetails

class ResourceBrowser(BaseBrowser):
    """
    Handles requests for resource info.
    
    """
    def __init__(self, request):
        """
        Initialize the browser with the render-args we need for meta data browsing.
        
        @param request: Handle to the HTTP request that needs to be processed.
        @type request:  BaseHttpRequest
        
        """
        super(ResourceBrowser, self).__init__(request,
                                              renderer_args = dict(no_annotations=True,
                                                                   no_table_headers=False,
                                                                   no_list_indices=False,
                                                                   no_borders=False))
 

    def process(self):
        """
        Process the request.
     
        @return:  HTTP return code and data as a tuple.
        @rtype:   tuple
        
        """
        method = self.request.getRequestMethod()

        if method == "DELETE":
            try:
                deleteResourceFromStorage(self.request.getRequestPath())
                return (200, "Resource deleted")
            except GluException, e:
                return (e.code, str(e))

        settings = Settings.getSettingsObject()
        if method == "GET":
            # It's the responsibility of the browser class to provide breadcrums
            self.breadcrums = [ ("Home", settings.DOCUMENT_ROOT), ("Resource", settings.PREFIX_RESOURCE) ]

        code = 200
        if self.request.getRequestPath() == settings.PREFIX_RESOURCE:
            #
            # Request to the base URL of all resources (listing resources)
            #
            if method == "GET":
                #
                # List all the resources
                #
                data = listResources()
            else:
                raise GluMethodNotAllowedException()
            
        else:
            # Path elements (the known resource prefix is stripped off)
            path          = self.request.getRequestPath()[len(settings.PREFIX_RESOURCE):]
            path_elems    = path.split("/")[1:]
            resource_name = path_elems[0]   # This should be the name of the resource base
            
            # Get the public representation of the resource
            rinfo = _getResourceDetails(resource_name)
            complete_resource_def = rinfo['complete_resource_def']
            resource_home_uri     = rinfo['resource_home_uri']
            public_resource_def   = rinfo['public_resource_def']
            code_uri              = rinfo['code_uri']
            component             = rinfo['component']
            services              = public_resource_def['services']

            if method == "GET":
                self.breadcrums.append((resource_name, resource_home_uri))

            # Was there more to access?
            if len(path_elems) > 1:
                #
                # Some sub-service of the component was requested. This means
                # we actually need to pass the parameters to the component
                # and call this service function.
                #
                
                # This service has some possible runtime parameters defined.
                runtime_param_dict = self.request.getRequestQueryDict()

                service_name = path_elems[1]
                input        = self.request.getRequestBody()
                try:
                    code, data = _accessComponentService(component, services, complete_resource_def,
                                                    resource_name, service_name, runtime_param_dict,
                                                    input, self.request)
                except GluException, e:
                    code = e.getCode()
                    data = e.getMessage()
                except Exception, e:
                    # The service code threw an exception. We need to log that and return a
                    # normal error back to the user.
                    print traceback.format_exc()
                    log("Exception in component for service '%s': %s" % (service_name, str(e)), facility=LOGF_COMPONENTS)
                    code, data = (500, "Internal server error. Details have been logged...")
                if code != 404  and  method == "GET"  and  service_name in services:
                    self.breadcrums.append((service_name, services[service_name]['uri']))

            else:
                # No, nothing else. Someone just wanted to know more about the resource.
                if method == "POST":
                    raise GluMethodNotAllowedException()
                data = public_resource_def

        return (code, data)

