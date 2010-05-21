
"""
This module takes care of the translation of language
specific data structures and types into the types that
are used in the Python core.

You may wonder why this functionality is not simply integrated
in the base component class for each language. Turns out that
such conversion is much simpler in Python than in (for example)
Java. Therefore, we put this conversion outside of the base
component.

The tradeof is that we need to make sure to call the proper
conversion function whenever we use the components.

"""

from glu.platform_specifics import PLATFORM, PLATFORM_JYTHON

from org.mulesource.glu.exception import *

if PLATFORM == PLATFORM_JYTHON:
    import java.lang.Exception
    from java.lang import String
    from java.util import HashMap, Vector


def __javaStructToPython(hm):
    """
    Convert a Java HashMap and Vector based structure to a Python dictionary or list.
    
    Sadly, this is not done automatically. So, we recursively
    iterate over the hash map and convert using the 'update' method
    of dictionaries. Unfortunately, 'update' only works on the same
    level and doesn't do the conversion recursively.
    
    """
    if type(hm) is HashMap:
        d2 = dict()
        d2.update(hm)
        for key, val in d2.items():
            if type(val) in [ HashMap, Vector ]:
                d2[key] = __javaStructToPython(val)

    elif type(hm) is Vector:
        d2 = list()
        for val in hm:
            if type(val) in [ HashMap, Vector ]:
                d2.append(__javaStructToPython(val))
            else:
                d2.append(val)
    else:
        return hm
            
    return d2


def __pythonStructToPython(obj):
    """
    Nothing needs to be done for Python.
    
    """
    return obj


#
# Translation table, which finds the correct conversion function
# based on the language ID of the component.
#
__LANG_STRUCT_TO_PYTHON = {
   "JAVA"   : __javaStructToPython,
   "PYTHON" : __pythonStructToPython
}


def languageStructToPython(component, obj):
    """
    Convert a struct of the component's language to a Python equivalent.
    
    Chooses the correct conversion function for this component, based
    on the language ID that's returned by the component.
    
    """
    func = __LANG_STRUCT_TO_PYTHON[component.LANGUAGE]
    return func(obj)


#
# Proxies for calling language specific component service methods
#
def __javaServiceMethodProxy(method, request, input, params, http_method):
    """
    Calls service methods in Java components.
    
    Prepares parameters, converts exceptions and results.
    
    """
    request.setNativeMode()
    try:
        # The parameter dictionary needs to be transcribed into a HashMap
        hm = HashMap()
        for key, val in params.items():
            hm[key] = val        
        res = method(request, String(input), hm, String(http_method))
    except java.lang.Exception, e:        
        raise GluException(str(e))   # Re-raises a native exception as GluException, leading to 500 message
    code = res.getCode()
    data = res.getObject()
    if type(data) in [ HashMap, Vector ]:
        data = __javaStructToPython(data)
    return code, data

def __pythonServiceMethodProxy(method, request, input, params, http_method):
    """
    Calls service methods in Python components.
    
    """
    return method(request, input, params, http_method)

#
# Translation table, which finds the correct conversion function
# based on the language ID of the component.
#
__LANG_METHOD_PROXIES = {
   "JAVA"   : __javaServiceMethodProxy,
   "PYTHON" : __pythonServiceMethodProxy,
}


def serviceMethodProxy(component, method, *args):
    """
    Call the service method of a component.
    
    'method' is not the name of the method, but a handle to
    the actual method itself already.
    
    'component' is passed in only so that we can decide
    here, which proxy to use.
    
    """
    func = __LANG_METHOD_PROXIES[component.LANGUAGE]
    return func(method, *args)
