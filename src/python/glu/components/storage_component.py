"""
A storage component.

"""
# Python imports
import urllib
import glujson as json

# Glu imports
from glu.components.api import *

class StorageComponent(BaseComponent):
    NAME             = "StorageComponent"
    
    DESCRIPTION      = "Allows the storage of arbitrary data in independent name spaces / buckets"
    DOCUMENTATION    =  """
                        This component is used to store information in arbitrary name spaces (or buckets).
                        
                        When a new storage resource is created, the resource name defines the new
                        storage bucket.

                        Subsequently, the .../resourcename/files?name=<name> sub-resource is used to PUT or GET data
                        into the storage bucket.

                        'name' is also allowed as a positional parameter. This means you can access the same
                        file like this: .../resourcename/files/<name>

                        """
    SERVICES         = {
                           "files" :   {
                               "desc"   : "Provide the name of the storaged item as parameter and use 'PUT' or 'GET'.",
                               "params" : {
                                    "name" : ParameterDef(PARAM_STRING, "Name of the stored data item", required=False),
                               },
                               "positional_params" : [ "name" ]
                           }
                       }
    
            
    def files(self, request, input, params):
        """
        Stored or retrieves data from the storage bucket.
        
        @param request:    Information about the HTTP request.
        @type request:     BaseHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # Access to our storage bucket
        storage   = self.getFileStorage()

        # Get my parameters
        data_name = params.get('name')
        if not data_name:
            # User didn't specify a specific file, which means we should generate
            # a list of all the files in that namespace.
            data = storage.listFiles()

            # We want to prepend the resource name and service name, so that the user
            # gets complete URIs for each file
            my_resource_uri = self.getMyResourceUri()
            new_data = [ "%s/%s/%s" % (my_resource_uri, "files", name) for name in data ]
            data = new_data
        else:
            if request.getRequestMethod() == "DELETE":
                storage.deleteFile(data_name)
                data = "File deleted"
            else:
                if input:
                    storage.storeFile(data_name, input)
                    data = "Successfully stored"
                else:
                    data = storage.loadFile(data_name)

        return 200, data

