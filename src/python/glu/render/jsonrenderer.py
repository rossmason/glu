"""
Outputs JSON representation of data.
 
"""

# Python imports
import glujson as json

# Glu imports
from glu.render.baserenderer import BaseRenderer

from glu.platform_specifics  import *

from org.mulesource.glu.util import Url


def _default(obj):
    """
    Take a non-standard data type and return its string representation.
    
    This function is given to simplejson as a fall back for any types
    that it doesn't know how to render.
    
    @param obj:    A non-standard object to be rendered for JSON.
    @type  obj:    object
    
    @return:       String representation suitable for JSON.
    
    """
    return str(obj)

def _recursive_type_fixer(obj):
    """
    Convert unusual types to strings in recursive structures.

    Under GAE we cannot specify a default for the JSON encoder,
    which is very annoying. So this method is only called when
    we are running under GAE. It traverses the entire data structure
    and converts the types specified in FIX_TYPES to strings.

    """
    FIX_TYPES = [ Url ]
    if type(obj) in FIX_TYPES:
        return str(obj)
    if type(obj) is list:
        new_list = []
        for e in obj:
            new_list.append(_recursive_type_fixer(e))
        return new_list
    if type(obj) is dict:
        new_dict = {}
        for k, v in obj.items():
            if type(k) in FIX_TYPES:
                k = str(k)
            if type(v) in FIX_TYPES:
                v = str(v)
            else:
                v = _recursive_type_fixer(v)
            new_dict[k] = v
        return new_dict
    return obj
        

class JsonRenderer(BaseRenderer):
    """
    Class to render data as JSON.
        
    """
    CONTENT_TYPE = "application/json"

    def render(self, data, top_level=False):
        """
        Render the provided data for output.
        
        @param data:        An object containing the data to be rendered.
        @param data:        object
        
        @param top_level:   Flag indicating whether this we are at the
                            top level for output (this function is called
                            recursively and therefore may not always find
                            itself at the top level). This is important for
                            some renderers, since they can insert any framing
                            elements that might be required at the top level.
                            However, for the JSON renderer this is just
                            ignored.
        @param top_level:   boolean
        
        @return:            Output buffer with completed representation.
        @rtype:             string
        
        """
        # simplejson can only handle some of the base Python datatypes.
        # Since we also have other types in the output dictionaries (URIs
        # for example), we need to provide a 'default' method, which
        # simplejson calls in case it doesn't know what to do.

        # Need to use our newly defined Url encoder, since otherwise
        # json wouldn't know how to encode a URL
        if PLATFORM == PLATFORM_GAE:
            # That doesn't seem to be supported when running in
            # GAE, though. So, in that case we first perform a very
            # manual fixup of the object, replacing all occurrances
            # of unusual types with their string representations.
            data = _recursive_type_fixer(data)
            out = json.dumps(data, sort_keys=True, indent=4)
        else:
            out = json.dumps(data, default=_default, sort_keys=True, indent=4)

        return out

