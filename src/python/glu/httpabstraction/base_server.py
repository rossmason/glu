"""
Provide an abstraction layer for a concrete HTTP server implementation.

This allows the rest of our code to be written without server specifics
being spread all over the place. That way, we can always change the
concrete HttpServer implementation later on.

"""

#
# By importing GluHttpRequest, we are exporting this symbol from
# within this module. Gives the users of the abstraction a single
# place from which they get what they need.
#
# The GluHttpRequest class is an abstract Java class, thus giving us
# a convenient Java and Python interface to the same Python object.
#
from org.mulesource.glu import GluHttpRequest


class BaseHttpServer(object):
    """
    Wrapper class around a concrete HTTP server implementation.
    
    """    
    def __init__(self, port, request_handler): pass
