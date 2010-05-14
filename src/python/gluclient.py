
Blah

import sys
import json
import types
import urllib

from glu.core.parameter import *


class GluResource(object):
    """
    Encapsulate information about a resource.

    """
    def __call_service_function(self, service_name, service_url, kwargs):
        """
        Issue the REST call to the server for this service.

        """
        # Assemble query string from the argument dictionary
        if kwargs:
            qstring = "?" + "&".join( [ "%s=%s" % (argname, urllib.quote(kwargs[argname])) for argname in kwargs ] )
        else:
            qstring = ""
        full_url = service_url + qstring

        data_str = self.__glu_server_instance.send(service_url + qstring)
        try:
            data = json.loads(data_str)
        except:
            data = data_str
        return data


    def __make_service_function(self, service_name, service_url):
        """
        Create and setup a function for the advertised service (or sub-resource).

        The function will be added to this object, so that the user of the
        object can utilize a simple function interface to interact with the
        Glu server. The RESTful interactions take place behind the scenes.

        The functions that represent the various resource services are created
        and added dynamically. Docstrings are created dynamically and the functions
        have the name of the advertised service. However, the sanity of the
        parameters is only checked at runtime.

        """
        service_def = self.__resource_def['services'][service_name]

        docstr = service_def.get('desc', "No description provided for this service resource") + "\n\n"
        params = service_def.get('params')

        # 
        # A small helper function for the assembly of per-parameter docstrings
        #
        def param_docs(pname, desc, type):
            return "    %s\n        %s\n        Type: %s\n\n" % (pname, desc, type)

        # Assemble the docstring for this function.
        # For this we only use the service definition.
        if params:
            # Get lists of required and optional parameters as per the service definition
            required_params = [ pname for pname in params if params[pname]['required'] ]
            optional_params = [ pname for pname in params if not params[pname]['required'] ]
            if required_params:
                docstr += "Required parameters:\n"
                for pname in required_params:
                    docstr += param_docs(pname, service_def['params'][pname]['desc'], service_def['params'][pname]['type'])
                docstr += "\n"
            if optional_params:
                docstr += "Optional parameters:\n"
                for pname in optional_params:
                    docstr += param_docs(pname, service_def['params'][pname]['desc'], service_def['params'][pname]['type'])
                docstr += "\n"
        else:
            required_params = optional_params = list()

        #
        # Create a generic service function placeholder.
        # Note that this is a closure, which gets a lot of its 'runtime environment' from the current context
        # of the surrounding __make_service_function() method.
        #
        def generic_service_method(self, *args, **kwargs):
            """
            Function to handle all service accesses.

            Performs basic type checking.

            """
            #
            # Check that arguments with the right names are provided and that
            # all mandatory arguments are present.
            #
            if args:
                raise TypeError("Positional arguments are not supported.")
            arg_names = kwargs.keys()
            for argname in arg_names:
                if argname not in required_params  and  argname not in optional_params:
                    raise TypeError("Unknown argument '%s'." % argname)
            for argname in required_params:
                if argname not in arg_names:
                    raise TypeError("Mandatory argument '%s' is missing." % argname)
            #
            # Check whether the provided arguments have compatible types.
            #
            param_dict = service_def.get('params', list())
            for argname in param_dict:
                # The type that we have defined in the service definition
                if argname in arg_names:
                    argtype_def      = service_def['params'][argname]['type']
                    compatible_types = TYPE_COMPATIBILITY[argtype_def][0]
                    actual_argtype   = type(kwargs[argname])
                    if actual_argtype not in compatible_types:
                        raise TypeError("Incompatible type '%s' for argument '%s'. Expected type '%s'." % (actual_argtype, argname, argtype_def))

            #print 20*"-" + service_name + "\n" + str(service_def) + "\n" + 20*"-" + "\n"
            return self.__call_service_function(service_name, service_url, kwargs)


        # Finish up the function creation by setting the docstring and name.
        generic_service_method.__doc__   = docstr
        generic_service_method.func_name = str(service_name)

        # Create the document lines that go into the docstring for the GluResource object.
        if optional_params:
            optional_arg_desc_str = ", " + ", ".join([ "%s=%s" % (pname, service_def['params'][pname].get('default')) for pname in optional_params ])
        else:
            optional_arg_desc_str = ""
        func_doc = "    %s(self, %s%s)\n        %s" % (service_name, ", ".join(required_params), optional_arg_desc_str, service_def.get('desc', ""))
        return (generic_service_method, func_doc)


    def __init__(self, url, glu_server_instance, resource_def):
        self.__glu_server_instance = glu_server_instance
        self.__url                 = url
        self.__resource_def        = resource_def

        #
        # Create the service functions.
        #
        service_names = self.__resource_def['services'].keys()
        for name in service_names:
            # Attach each service function to this GluResource object.
            new_func, func_doc = self.__make_service_function(name, url + "/" + name)
            setattr(self, name, types.MethodType(new_func, self, GluResource))
            # Update this object's docstring with the brief summary of the service method.
            self.__doc__ += func_doc

    def getServices(self):
        """
        Return list of all services published by this resource.

        """
        return self.__resource_def['services'].keys()



class GluServer(object):
    """
    Used by the client to encapsulate all communication with the server.

    """
    __ERROR_INFO = None
    server_url   = None

    class __MyOpener(urllib.URLopener):
        """
        Helper class allowing us to create our own URL opener.

        """
        def http_error_default(self, url, fp, errcode, errmsg, headers):
            global __ERROR_INFO
            __ERROR_INFO = (errcode, errmsg, fp.read())
        def add_msg(self, message):
            if message:
                self._my_msg = message
                self.addheader('Content-length', str(len(message)))
        def send(self, code_url):
            if hasattr(self, "_my_msg"):
                msg = self._my_msg
            else:
                msg = None
            return self.open(code_url, msg)


    def __init__(self, server_url):
        self.server_url = server_url

    def send(self, url, data=None):
        opener = self.__MyOpener()
        opener.addheader('Connection', 'close')
        opener.addheader('Accept', 'application/json')
        if data:
            opener.add_msg(json.dumps(data))
        stream = opener.send(self.server_url + url)
        
        if stream:
            ret_data = stream.read()
        else:
            print "ERROR: ", self.__ERROR_INFO
        return ret_data

    #
    # Public interface
    #

    def listComponents(self):
        d = self.send("/code")
        data = json.loads(d)
        return data

    def listResources(self):
        d = self.send("/resource")
        data = json.loads(d)
        return data

    def getResource(self, name):
        resource_url = "/resource/" + name
        d = self.send(resource_url)
        data = json.loads(d)
        new_resource = GluResource(resource_url, self, data)
        return new_resource

