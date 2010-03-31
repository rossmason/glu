"""
Simple starter for stand-alone Glu server.

"""
import time

# Glu imports
import glu.settings as settings
from glu.core               import RequestDispatcher
from glu.platform_specifics import *


if __name__ == '__main__':
    my_server = HttpServer(settings.LISTEN_PORT, RequestDispatcher(), HttpRequest)

    # For the Java server: Need to wait forever, since otherwise
    # the server disappears right after it was started.
    if PLATFORM == PLATFORM_JYTHON:
        while True: time.sleep(1000)

"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import time


def application(environ, start_response):
    writer = start_response('200 OK', [('Content-Type', 'text/html')])
    writer("This is a test: %d" % foo.FOOBAR)
    return ""

if __name__ == "__main__":
    run_wsgi_app(application)
"""

