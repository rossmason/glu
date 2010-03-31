"""
Base class from which all storage abstractions derive.

"""

class BaseStorage(object):
    """
    Abstract implementation of the base storage methods.

    """
    def loadResourceFromStorage(self, resource_name):
        """
        Load the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        @return                  Buffer containing the resource definition
                                 as a JSON string or None if not found.
        @rtype                   string

        """
        pass

    def listResourcesInStorage(self):
        """
        Return list of resources which we currently have in storage.

        @return:                 List of resource names.
        @rtype:                  list

        """
        pass

    def writeResourceToStorage(resource_name, resource_def):
        """
        Store a resource definition.
        
        No return value, but raises GluException if there is an issue.
        
        @param resource_name: The storage name for this resource
        @type  resource_name: string
        
        @param resource_def: The dictionary containing the resource definition.
        @type  resource_def: string
        
        @raise GluException: If the resource cannot be stored.
            
        """
        pass

