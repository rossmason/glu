"""
Simple starter for stand-alone Glu server.

"""
import time

# Glu imports
import glu.settings as settings
from glu.core               import RequestDispatcher
from glu.platform_specifics import *


if __name__ == '__main__':
    my_server = HttpServer(settings.LISTEN_PORT, RequestDispatcher())

    # For the Java server: Need to wait forever, since otherwise
    # the server disappears right after it was started.
    if PLATFORM == PLATFORM_JYTHON:
        while True: time.sleep(1000)


