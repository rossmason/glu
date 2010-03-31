"""
Platform specific settings for Glu.

By modifying these, we can switch to a different Http server abstraction
or a different storage abstraction.

"""

PLATFORM_PYTHON = "Python"
PLATFORM_JYTHON = "Jython"
PLATFORM_GAE    = "GAE"


PLATFORM = PLATFORM_PYTHON


if PLATFORM == PLATFORM_GAE:
    from glu.storageabstraction.gae_storage import GaeStorage as Storage
    storage_args = []
else:
    from glu.storageabstraction.file_storage import FileStorage as Storage
    storage_args = [ "/tmp/rdb" ]

STORAGE_OBJECT = Storage(*storage_args)


if PLATFORM == PLATFORM_JYTHON:
    from glu.httpabstraction.jython_java_server import JythonJavaHttpServer as HttpServer
    from glu.httpabstraction.jython_java_server import JythonJavaHttpRequest as HttpRequest
elif PLATFORM == PLATFORM_PYTHON:
    from glu.httpabstraction.python_http_server import PythonHttpServer as HttpServer
    from glu.httpabstraction.python_http_server import PythonHttpRequest as HttpRequest
else:
    from glu.httpabstraction.gae_http_server import GaeHttpServer as HttpServer
    # Yes, we can use the Python http request handler
    from glu.httpabstraction.python_http_server import PythonHttpRequest as HttpRequest


