"""
Here we have all the defintions and implementations
for resource storage and access.

Storage is VERY simple at this point: We take the
unique name of the resource (also the last path element
of the resource's URI) as the filename under which we
store a JSON representation of the resource.

The stored representation of a resource looks like this:

    {
        "public": {
                    .... what a client can see, usually
                    the name, uri, description, sub_resources
                    and any available runtime-parameters.
                    This dictionary is returned when a
                    client requests information about a resource.
                  },
        "private": {
                    ... what was provided when the resource was
                    defined.
                   }
    }

"""

# Python imports
import os

# Glu imports
import glu.settings as settings
from glu.platform_specifics import STORAGE_OBJECT

from glu.exceptions       import GluException
from glu.logger           import *
from glu.core.parameter   import TYPE_COMPATIBILITY
from glu.core.util        import Url


def getResourceUri(resource_name):
    """
    Construct a resource's URI based on its name.
    
    @return:  URI of the named resource.
    @rtype:   string
    
    """
    return settings.PREFIX_RESOURCE + "/" + resource_name


def retrieveResourceFromStorage(uri, only_public=False):
    """
    Return the details about a stored resource.
    
    The resource is identified via its URI.
    
    @param uri:         Identifies a resource via its URI.
    @type  uri:         string
    
    @param only_public: Flag indicating whether we only want to see the
                        public information about this resource.
    @type only_public:  boolean
    
    @return:            Dictionary or None if not found.
    @rtype:             dict
    
    """
    # Need to take the resource URI prefix off to get the resource_name.
    resource_name = uri[len(settings.PREFIX_RESOURCE)+1:]
    obj = None
    try:
        obj = STORAGE_OBJECT.loadResourceFromStorage(resource_name)
        if type(obj) is not dict  or  'public' not in obj:
            obj = None
            raise Exception("Missing top-level element 'public'.")
        public_obj = obj['public']
        # Do some sanity checking on the resource. Needs to contain
        # a few key elements at least.
        for mandatory_key in [ 'uri', 'desc', 'name' ]:
            if mandatory_key not in public_obj:
                public_obj = None
                raise Exception("Mandatory key '%s' missing in stored resource '%s'" % \
                                (mandatory_key, resource_name))
        if only_public:
            obj = public_obj
            
    except Exception, e:
        log("Malformed storage for resource '%s': %s" % (resource_name, str(e)), facility=LOGF_RESOURCES)
    return obj


def listResources():
    """
    Return list of all stored resources.
    
    Data is returned as dictionary keyed by resource name.
    For each resource the complete URI, the name and the description
    are returned.
    
    @return: Dictionary of available resources.
    @rtype:  dict
    
    """
    dir_list = STORAGE_OBJECT.listResourcesInStorage()
    out = {}
    for resource_name in dir_list:
        resource_dict = retrieveResourceFromStorage(getResourceUri(resource_name), only_public=True)
        if resource_dict:
            out[resource_name] = dict(uri=Url(resource_dict['uri']), desc=resource_dict['desc'])
        else:
            out[resource_name] = "Not found"
    return out


def paramSanityCheck(param_dict, param_def_dict, name_for_errors):
    """
    Check whether a provided parameter-dict is compatible
    with a parameter-definition-dict.
    
    The following checks are performed:
    
     * Are there any keys in the params that are not in the definition?
     * Are all required parameters present?
     * Are the types are compatible?
    
    Does not return anything but raises GlueException with
    meaningful error message in case of problem.
    
    The 'name_for_errors' is used in the error message and provides
    some context to make the error message more useful.
    
    @param param_dict:      The parameter dictionary provided (for example by the client).
    @type  param_dict:      dict
    
    @param param_def_dict:  The parameter definition as provided by the bean (the code).
                            The provided parameters are checked against this definition.
    @type  param_def_dict:  dict
    
    @param name_for_errors: A section name, which helps to provide meaningful error messages.
    @type  name_for_errors: string
    
    @raise GluException:    If the sanity check fails.
    
    """
    #
    # Check whether there are unknown parameters in the 'param' section
    # and also whether the type is compatible.
    #
    if param_dict  and  type(param_dict) is not dict:
        raise GluException("The '%s' section has to be a dictionary" % name_for_errors)
    if param_def_dict  and  param_dict:
        for pname in param_dict:
            # Any unknown parameters
            if pname not in param_def_dict:
                raise GluException("Unknown parameter in '%s' section: %s" % (name_for_errors, pname))
            # Sanity check the types
            type_str   = param_def_dict[pname]['type']
            param_type = type(param_dict[pname])
            storage_types, runtime_types, conversion_func = TYPE_COMPATIBILITY[type_str]
            if param_type in runtime_types:
                pass
            elif param_type not in storage_types:
                try:
                    if conversion_func:
                        conversion_func(param_type)
                    else:
                        raise Exception("Cannot convert provided parameter type (%s) to necessary type(s) '%s'" % \
                                        (param_type, runtime_types))
                except Exception, e:
                    raise GluException("Incompatible type for parameter '%s' in section '%s': %s" % \
                                       (pname, name_for_errors, str(e)))
                    
    #
    # Check whether all required parameters are present
    #
    for pname, pdict in param_def_dict.items():
        if pdict['required']  and  (not param_dict  or  pname not in param_dict):
            raise GluException("Missing mandatory parameter '%s' in section '%s'" % (pname, name_for_errors))

def fillDefaults(param_def_dict, param_dict):
    """
    Copy defaults values into parameter dictionary if not present.
    
    The parameter dictionaries may be defined with defaults.
    So, if the param_dict does not contain anything for those
    parameters then we will create them in there with the
    default value that were specified in the parameter definition.
    
    @param param_def_dict:  The parameter definition- including default values -
                            provided by the bean code.
    @type  param_def_dict:  dict
    
    @param param_dict:      The parameter definition provided by the client.
    @type  param_dict:      dict
    
    """
    for pname, pdict in param_def_dict.items():
        if not pdict['required']  and  pname not in param_dict:
            param_dict[pname] = pdict['default']

def makeResource(bean_class, params):
    """
    Create a new resource representation from the
    specified bean class and parameter dictionary
    and store it on disk.
        
    The parameters need to look something like this:
    
            {
                "reource creation_params" : {
                        "suggested_name" : "my_twitter",
                        "public"         : "yes",
                        "desc"           : "Juergen's Twitter stream"
                },
                "params" : {
                        "user"     : "BrendelConsult",
                        "password" : "some password"
                }
            }

    The method performs sanity checking on the supplied
    parameters and also fills in default values where
    available.
    
    @param bean_class:    A class (not instance) derived from BaseBean.
    @type  bean_class:    BaseBean or derived.
    
    @param params:        The resource parameters provided by the client.
                          Needs to contain at least a 'params' dictionary
                          or a 'resource_creation_dictionary'. Can contain
                          both.
    @type  params:        dict
    
    @return:              Success message in form of dictionary that contains
                          "status", "name" and "uri" fields.
    @rtype:               dict
    
    @raise GluException:  If the resource creation failed or there was a
                          problem with the provided parameters.

    """    
    # We get the meta data (parameter definition) from the bean
    bean            = bean_class()
    bean_params_def = bean.getMetaData()

    #
    # First we check whether there are any unknown parameters specified
    # on the top level.
    #
    if type(params) is not dict:
        raise GluException("Malformed resource parameter definition. Has to be JSON dictionary.")
        
    for k in params.keys():
        if k not in [ 'params', 'resource_creation_params' ]:
            raise GluException("Malformed resource parameter definition. Unknown key: %s" % k)
    #
    # Check whether there are unknown parameters in the 'param' or 'resource_creation_params' section.
    #
    provided_params                   = params.get('params')
    if not provided_params:
        # If no parameters were provided at all, we create them as
        # an empty dictionary. We need something here to be able
        # to merge some defaults into it later on.
        provided_params = dict()
        params['params'] = provided_params
    provided_resource_creation_params = params.get('resource_creation_params')
    paramSanityCheck(provided_params, bean_params_def['params'], 'params')
    paramSanityCheck(provided_resource_creation_params,
                     bean_params_def['resource_creation_params'],
                     'resource_creation_params')

    # The parameters passed the sanity checks. We can now create the resource definition.
    suggested_name = provided_resource_creation_params['suggested_name']
    resource_uri   = settings.PREFIX_RESOURCE + "/" + suggested_name
    resource_name  = suggested_name # TODO: Should check if the resource exists already...
    params['code_uri'] = bean.getUri()  # Need a reference to the code that this applies to
    
    # Some parameters are optional. If they were not supplied,
    # we need to add their default values.
    fillDefaults(bean_params_def['params'], provided_params)
    fillDefaults(bean_params_def['resource_creation_params'], provided_resource_creation_params)
    
    # Storage for a resource contains a private and public part. The public part is what
    # any user of the resource can see: URI, name and description. In the private part we
    # store whatever was provided here during resource creation. It contains the information
    # we need to instantiate a running resource.
    resource_def = {
        "private" : params,
        "public"  : {
                        "uri"  : resource_uri,
                        "name" : resource_name,
                        "desc" : provided_resource_creation_params['desc']
                    }
    }
    
    # Storage to our 'database'.
    STORAGE_OBJECT.writeResourceToStorage(resource_name, resource_def)

    # Send a useful message back to the client.
    success_body = {
        "status" : "created",
        "name"   : resource_name,   # Is returned, because server could have chosen different name
        "uri"    : resource_uri
    }

    return success_body

