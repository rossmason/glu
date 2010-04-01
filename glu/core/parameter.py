"""
The parameter class.

"""
from datetime import date
from datetime import time as time_class

#
# Types for resource parameters
#
PARAM_STRING   = "string"
PARAM_PASSWORD = "password"
PARAM_BOOL     = "boolean"
PARAM_DATE     = "date"
PARAM_TIME     = "time"
PARAM_NUMBER   = "number"
PARAM_URI      = "uri"

KNOWN_BASIC_TYPES = [ PARAM_STRING, PARAM_PASSWORD, PARAM_BOOL, PARAM_DATE,
                      PARAM_TIME, PARAM_NUMBER, PARAM_URI ]


#
# Each entry in the following table has the format:
#    ( storage_types, runtime_types, conversion_func )
#
# 'storage_types' defines a list of types that this value may
# have after being read in via JSON. For example, 'date'
# will not be recognized by JSON, it is stored and loaded
# as a string. So, 'str' is one of the valid types for date
# parameters.
#
# 'runtime_types' is a list of types that are acceptable after
# proper conversion, so that we can actually work with that
# type in our programming language. For example, we really
# want dates to be of class 'date', which is why for date
# parameters we specify that type.
#
# 'conversion_func' is a function that can be used to convert
# from a storatge-type to a runtime-type. Calling this function
# also provides a proper sanity check, since those functions
# will throw errors if they fail.
#
# Note: Date is defined as YYYY-MM-DD
# Note: Time is defined as HH:MM:SS
# 
def __numstr_to_num(x):
    if type(x) in [ int, float ]:
        return x
    elif type(x) in [ str, unicode ]:
        try:
            return int(x)
        except:
            return float(x)
    # Can't convert anything else
    return None


TYPE_COMPATIBILITY = {
    PARAM_STRING   : ([ unicode, str ], [ str ], None),
    PARAM_PASSWORD : ([ unicode, str ], [ str ], None),
    PARAM_BOOL     : ([ bool ], [ bool ], None),
    PARAM_DATE     : ([ unicode, str ], [ date ], lambda x : date(*[ int(elem) for elem in x.split("-")])),
    PARAM_TIME     : ([ unicode, str ], [ time_class ], lambda x : time_class(*[ int(elem) for elem in x.split(":")])),
    PARAM_NUMBER   : ([ int, float ], [ int, float ], __numstr_to_num),
    PARAM_URI      : ([ unicode, str ], [ str ], None)
}

class ParameterDef(object):
    """
    This class encapsulates a parameter definition.
    
    Parameters are defined by each individual bean.
    Therefore, in its __init__() method each bean
    has to create its dictionary of ParameterDef classes
    and make it available via the getParams() method.
    
    By default, a parameter is 'required'. Note that
    this parameter definition does not contain the
    name of the parameter, since the name is merely
    the key in the paramater definition dictionary,
    which is maintained by each bean.
    
    """
    def __init__(self, ptype, desc="", required=True, default=None):
        """
        Define a new parameter.
        
        A parameter is defined with the following attributes:
        
        @param ptype:            A type, such as PARAM_STRING, etc.
        @type prtype:            string
                
        @param desc:             A short, one-line description in human readable form.
        @type desc:              string
        
        @param required:         A flag indicating whether this parameter needs to be
                                 set by the resource creator, or whether a default
                                 value can be used.
        @type required:          boolean
        
        @param default:          A default value for this parameter of a suitable type.
                                 Only used if 'required == False'.
        @type default:           Whatever is needed as default value
        
        """
        self.ptype            = ptype
        self.desc             = desc
        self.required         = required
        self.default          = default
        
    def as_dict(self):
        """
        Unwraps this single parameter definition into a plain dictionary.
        
        Needed for browsing or accessing the bean's meta info.
        
        @return:  Dictionary representation of the parameter.
        @rtype:   dict
        
        """
        return dict(type             = self.ptype,
                    desc             = self.desc,
                    required         = self.required,
                    default          = self.default)


