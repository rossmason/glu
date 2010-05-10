
import datetime

from glu.platform_specifics import *

if PLATFORM == PLATFORM_PYTHON:
    from json import *
elif PLATFORM == PLATFORM_GAE:
    from django.utils.simplejson import *
else:
    from simplejson import *

class GluJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date):
            return str(obj)
        return JSONEncoder.default(self, obj)

def dumps(obj):
    """
    Encode an object to string, using our own JSON Encoder.

    This method hides the default 'dumps' method that comes with
    the JSON module.

    """
    return GluJsonEncoder().encode(obj)

