
"""
We isolate JSON capabilities in a single class, so that it
is easy for us to write a wrapper class in Java for this
class.

This allows us to use Python's convenient JSON capabilities
in Java.

"""

import glujson as json

from org.mulesource.glu.json import GluJson

class JsonImpl(GluJson):

    def encode(self, obj):
        return json.dumps(obj, indent=4)

    def decode(self, str):
        return json.loads(str)

