
import glujson as json

import glu.core.codebrowser  # Wanted to be much more selective here, but a circular
                             # import issue was most easily resolved like this.
                             # We only need getComponentInstance() from this module.

from glu.exceptions import *
from glu.resources  import paramSanityCheck, fillDefaults, convertTypes, \
                           retrieveResourceFromStorage, getResourceUri

def _accessComponentService(component, services, complete_resource_def, resource_name, service_name,
                       runtime_param_dict, input, request=None, direct_call=False):
    """
    Passes control to a service method exposed by a component.
    
    @param component:                  An instance of the component.
    @type component:                   BaseComponent (object of child class)
    
    @param services:              Dictionary of services definitions for this component. Can be had
                                  by calling _getServices() on the component. But we would need the
                                  resource's base URI to get those URIs exported properly. Since
                                  we already did this call in process() from where we called this
                                  method, we just pass the services dictionary in, rather than
                                  calling _getServices() again.
    @param services:              dict
    
    @param complete_resource_def: The entire resource definition as it was retrieved from storage.
    @type complete_resource_def:  dict
    
    @param resource_name:         Name of the resource
    @type resource_name:          string
    
    @param service_name:          The name of the requested service
    @type service_name:           string
    
    @param runtime_param_dict:    Dictionary of URL command line arguments.
    @type runtime_param_dict:     dict
    
    @param input:                 Any potential input (came in the request body)
    @type input:                  string
    
    @param direct_call:           Set this if the function is called directly from another component
                                  or piece of code that's not part of Glu. In that case, it wraps
                                  the actual exception in a 'normal' exception and passes it up.
                                  That allows the framework code to react differently to exceptions
                                  in here than direct-call code.
    @type direct_call:            boolean
    
    """
    try:
        service_def = services.get(service_name)
        if not service_def:
            raise GluException("Service '%s' is not available in this resource." % service_name)

        # Some runtime parameters may have been provided as arguments on
        # the URL command line. They need to be processed and added to
        # the parameters if necessary.
        runtime_param_def  = service_def.get('params')
        if runtime_param_def:
            # If the 'allow_params_in_body' flag is set for a service then we
            # allow runtime parameters to be passed in the request body PUT or POST.
            # So, if the URL command line parameters are not specified then we
            # should take the runtime parameters out of the body.
            # Sanity checking and filling in of defaults for the runtime parameters
            if service_def.get('allow_params_in_body')  and  input:
                # Take the base definition of the parameters from the request body
                try:
                    base_params = json.loads(input.strip())
                except ValueError, e:
                    # Probably couldn't parse JSON properly.
                    base_param = {}
                # Load the values from the body into the runtime_param_dict, but
                # only those which are not defined there yet. This allows the
                # command line args to overwrite what's specified in the body.
                for name, value in base_params.items():
                    if name not in runtime_param_dict:
                        runtime_param_dict[name] = value

            paramSanityCheck(runtime_param_dict, runtime_param_def, "runtime parameter")
            fillDefaults(runtime_param_def, runtime_param_dict)
            convertTypes(runtime_param_def, runtime_param_dict)
    
        services = complete_resource_def['public']['services']
        if service_name in services  and  hasattr(component, service_name):
            service_method    = getattr(component, service_name)
            
            params = complete_resource_def['private']['params']
            if runtime_param_dict:
                # Merge the runtime parameters with the static parameters
                # from the resource definition.
                params.update(runtime_param_dict)
            
            code, data = service_method(request     = request,
                                        input       = input,
                                        params      = params)
        else:
            raise GluException("Service '%s' is not exposed by this resource." % service_name)
    except GluException, e:
        if direct_call:
            raise Exception(str(e))
        else:
            raise e
    
    return code, data



def _getResourceDetails(resource_name):
    """
    Extract and compute a number of importants facts about a resource.
    
    The information is returned as a dictionary.
    
    @param resource_name:    The name of the resource.
    @type resource_name:     string
    
    @return:                 Dictionary with information about the resource.
    @rtype:                  dict
    
    """
    complete_resource_def  = retrieveResourceFromStorage(getResourceUri(resource_name))
    if not complete_resource_def:
        raise GluResourceNotFound("Unknown resource")
    resource_home_uri      = getResourceUri(resource_name)
    public_resource_def    = complete_resource_def['public']
    
    # Instantiate the component to get the exposed sub-services. Their info
    # is added to the public information about the resource.
    code_uri  = complete_resource_def['private']['code_uri']
    component = glu.core.codebrowser.getComponentInstance(code_uri)
    services  = component._getServices(resource_base_uri = resource_home_uri)
    public_resource_def['services'] = services
    
    return dict(complete_resource_def = complete_resource_def,
                resource_home_uri     = resource_home_uri,
                public_resource_def   = public_resource_def,
                code_uri              = code_uri,
                component             = component)

     
def runResource(resource_name, service_name, input=None, params=None):
    """
    Run a resource identified by its URI.
    
    @param resource_name:    The name of the resource.
    @type resource_name:     string
    
    @param service_name:     Name of the desired service
    @type service_name:      string
    
    @param input:            Any input information that may have been sent with the request body.
    @type input:             string
    
    @param params:           Any run-time parameters for this service as key/value pairs.
    @type params:            dict
    
    """
    # Get the public representation of the resource
    rinfo = _getResourceDetails(resource_name)
    
    code, data = _accessComponentService(rinfo['component'], rinfo['public_resource_def']['services'],
                                    rinfo['complete_resource_def'], resource_name,
                                    service_name, params, input, None, True)
    return code, data
 
 
