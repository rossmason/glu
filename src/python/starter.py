"""
Simple starter for stand-alone Glu server.

"""
from java.lang import String

import time

# Glu imports
from org.mulesource.glu     import Settings

from glu.core               import RequestDispatcher
from glu.platform_specifics import *
#from java.lang import Exception

if __name__ == '__main__':
    
    settings  = Settings.getSettingsObject()
    my_server = HttpServer(settings.LISTEN_PORT, RequestDispatcher())

    # For the Java server: Need to wait forever, since otherwise
    # the server disappears right after it was started.
    if PLATFORM == PLATFORM_JYTHON:
        while True: time.sleep(1000)


