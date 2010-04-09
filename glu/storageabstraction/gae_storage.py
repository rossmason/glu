"""
Base class from which all storage abstractions derive.

"""

import glujson as json

# GAE imports
from google.appengine.ext import db

# Glu imports
from glu.exceptions import *

class ResourceStorage(db.Model):
    name = db.StringProperty(multiline=False)
    data = db.StringProperty(multiline=True)

class GaeStorage(object):
    """
    Abstract implementation of the base storage methods.

    """
    def __init__(self, *args, **kwargs):
        pass

    def loadResourceFromStorage(self, resource_name):
        """
        Load the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        @return                  A Python dictionary representation or None
                                 if not found.
        @rtype                   dict

        """
        resources = ResourceStorage.gql("WHERE name = :1", resource_name)
        resource = resources[0]
        return json.loads(resource.data)

    def listResourcesInStorage(self):
        """
        Return list of resources which we currently have in storage.

        @return:                 List of resource names.
        @rtype:                  list

        """
        try:
            resources = db.GqlQuery("SELECT * FROM ResourceStorage ORDER BY name")
            dir_list = [ r.name for r in resources ]
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
            existing_resources = ResourceStorage.gql("WHERE name = :1", resource_name)
            try:
                # Make sure we update old ones
                resource = existing_resources[0]
            except Exception, e:
                # No old ones? Make a new one.
                resource = ResourceStorage()
            resource.name = resource_name
            resource.data = json.dumps(resource_def)
            resource.put()
            return "No error"
        except Exception, e:
            return str(e)

