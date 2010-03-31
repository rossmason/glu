"""
Base class from which all storage abstractions derive.

"""

# Python imports
import os
import glujson as json

# Glu imports
from glu.exceptions import *

class FileStorage(object):
    """
    Abstract implementation of the base storage methods.

    """
    def __init__(self, storage_location):
        self.storage_location = storage_location

    def loadResourceFromStorage(self, resource_name):
        """
        Load the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        @return                  A Python dictionary representation or None
                                 if not found.
        @rtype                   dict

        """
        buf = None
        try:
            f   = open(self.storage_location + "/" + resource_name, "r")
            buf = f.read()
            f.close()
        except:
            # Looks like this object didn't exist
            return None
        obj = json.loads(buf)
        return obj

    def listResourcesInStorage(self):
        """
        Return list of resources which we currently have in storage.

        @return:                 List of resource names.
        @rtype:                  list

        """
        try:
            dir_list = os.listdir(self.storage_location)
            return dir_list
        except Exception, e:
            raise GluException("Problems getting resource list from storage: " + str(e))

    def writeResourceToStorage(self, resource_name, resource_def):
        """
        Store a resource definition.
        
        No return value, but raises GluException if there is an issue.
        
        @param resource_name: The storage name for this resource
        @type  resource_name: string
        
        @param resource_def: The dictionary containing the resource definition.
        @type  resource_def: dict
        
        @raise GluException: If the resource cannot be stored.
            
        """
        try:
            f = open(self.storage_location + "/" + resource_name, "w")
            buf = json.dumps(resource_def, indent=4)
            f.write(buf)
            f.close()
        except Exception, e:
            raise GluException("Problems storing new resource: " + str(e))

