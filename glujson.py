
from glu.platform_specifics import *

if PLATFORM == PLATFORM_PYTHON:
    from json import *
elif PLATFORM == PLATFORM_GAE:
    from django.utils.simplejson import *
else:
    from simplejson import *
