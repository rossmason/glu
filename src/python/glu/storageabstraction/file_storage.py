"""
Base class from which all storage abstractions derive.

"""

# Python imports
import os
import glujson as json

# Glu imports
from org.mulesource.glu.exceptions import *

class FileStorage(object):
    """
    Abstract implementation of the base storage methods.

    """
    def __init__(self, storage_location, unique_prefix=""):
        """
        The unique prefix is used to create a namespace in a flat bucket.

        """
        self.storage_location = storage_location
        self.unique_prefix    = unique_prefix

    def __make_filename(self, file_name):
        if self.unique_prefix:
            name = "%s/%s__%s" % (self.storage_location, self.unique_prefix, file_name)
        else:
            name = "%s/%s" % (self.storage_location, file_name)
        return name

    def __remove_filename_prefix(self, file_name):
        if self.unique_prefix:
            if file_name.startswith(self.unique_prefix):
                file_name = file_name[len(self.unique_prefix) + 2:]
        return file_name

    def loadFile(self, file_name):
        """
        Load the specified file from storage.

        @param file_name:    Name of the selected file.
        @type file_name:     string

        @return              Buffer containing the file contents.
        @rtype               string

        """
        try:
            f   = open(self.__make_filename(file_name), "r")
            buf = f.read()
            f.close()
        except Exception, e:
            raise GluFileNotFound("File '%s' could not be found'" % (file_name))
        return buf

    def storeFile(self, file_name, data):
        """
        Store the specified file in storage.

        @param file_name:    Name of the file.
        @type file_name:     string

        @param data:         Buffer containing the file contents.
        @type data:          string

        """
        f = open(self.__make_filename(file_name), "w")
        f.write(data)
        f.close()

    def deleteFile(self, file_name):
        """
        Delete the specified file from storage.

        @param file_name:    Name of the selected file.
        @type file_name:     string

        """
        try:
            os.remove(self.__make_filename(file_name))
        except OSError, e:
            if e.errno == 2:
                raise GluFileNotFound(file_name)
            elif e.errno == 13:
                raise GluPermissionDenied(file_name)
            else:
                raise GlException("Cannot delete file '%s (%s)'" % (resource_name, str(e)))
        except Exception, e:
            raise GluException("Cannot delete file '%s' (%s)" % (resource_name, str(e)))

    def listFiles(self):
        """
        Return list of all files in the storage.

        @return:                 List of file names.
        @rtype:                  list

        """
        try:
            dir_list = os.listdir(self.storage_location)
            # Need to filter all those out, which are not part of our storage space
            if self.unique_prefix:
                our_files = [ name for name in dir_list if name.startswith(self.unique_prefix) ]
            else:
                our_files = dir_list
            no_prefix_dir_list = [ self.__remove_filename_prefix(name) for name in our_files ]
            return no_prefix_dir_list
        except Exception, e:
            raise GluException("Problems getting file list from storage: " + str(e))

    def loadResourceFromStorage(self, resource_name):
        """
        Load the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        @return                  A Python dictionary representation or None
                                 if not found.
        @rtype                   dict

        """
        try:
            buf = self.loadFile(resource_name)
        except GluFileNotFound, e:
            return None
        obj = json.loads(buf)
        return obj

    def deleteResourceFromStorage(self, resource_name):
        """
        Delete the specified resource from storage.

        @param resource_name:    Name of the selected resource.
        @type resource_name:     string

        """
        self.deleteFile(resource_name)

    def listResourcesInStorage(self):
        """
        Return list of resources which we currently have in storage.

        @return:                 List of resource names.
        @rtype:                  list

        """
        try:
            dir_list = self.listFiles()
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
            buf = json.dumps(resource_def, indent=4)
            self.storeFile(resource_name, buf)
        except Exception, e:
            raise GluException("Problems storing new resource: " + str(e))

