
import sys
import json
import time
import types
import string
import urllib
import datetime

from glu.core.parameter import *

import snap_http_lib as http   # A decent URL library

SERVER_URL = "http://localhost:8001"

def _get_data(relative_url):
    """
    Helper method accesses a URL on the server and returns the data (interprets the JSON).

    @param relative_url: The relative URL on the server. A starting slash may be
                         specified, but either way, it's always interpreted to be
                         relative to "/".
    @type  relative_url: string

    @return:             The JSON interpreted data and the response object as a tuple.
    @rtype               tuple

    """
    if relative_url.startswith("/"):
        relative_url = relative_url[1:]
    resp = http.urlopen("GET", SERVER_URL + "/" + relative_url, headers={"Accept" : "application/json"})
    buf = resp.read()
    if resp.getStatus() == 200:
        data = json.loads(buf)
    else:
        data = buf
    return (data, resp)

def _delete(relative_url):
    """
    Helper method that sends a DELETE message to the server.

    @param relative_url: The relative URL on the server. A starting slash may be
                         specified, but either way, it's always interpreted to be
                         relative to "/".
    @type  relative_url: string

    @return:             The JSON interpreted data and the response object as a tuple.
    @rtype               tuple

    """
    if relative_url.startswith("/"):
        relative_url = relative_url[1:]
    resp = http.urlopen("DELETE", SERVER_URL + "/" + relative_url)
    buf = resp.read()
    return buf, resp


def _dict_compare(should_pdef, is_pdef):
    """
    Compare two parameter definition dictionaries.

    """
    assert(type(should_pdef) is dict)
    assert(type(is_pdef) is dict)
    assert(len(should_pdef) == len(is_pdef))

    for name in should_pdef:
        assert(name in is_pdef)
        if type(should_pdef[name]) is dict:
            _dict_compare(should_pdef[name], is_pdef[name])
        else:
            assert(should_pdef[name] == is_pdef[name])


# -------------------------------------------------------------------------------------------------------------------------
# Test methods
# -------------------------------------------------------------------------------------------------------------------------
def test_10_home():
    """
    Test that the home URL returns the expected data.

    """
    actual, resp = _get_data("/")
    assert(resp.getStatus() == 200)

    should = {
                    "code"     : "/code",
                    "resource" : "/resource",
                    "doc"      : "/meta/doc",
                    "static"   : "/static",
                    "name"     : "MuleSoft Glu server prototype",
                    "version"  : "(prototype)"
             }
    allkeys = [ 'code', 'resource', 'doc', 'static', 'name', 'version' ]

    for name in should:
        assert(name in actual)
        assert(actual[name] == should[name])

    for name in actual:
        assert(name in allkeys)


def test_14_not_found():
    """
    Test that the documentation can be received.

    """
    wrong_urls = [ "/sldkfjhadlskjhsdal", "/resource/alkdsjfhaljkdha", "/meta/asdkslakdhlhksa", "/code/aljkdhaljkdhfadlkf", "/static" ]
    for url in wrong_urls:
        data, resp = _get_data(url)
        assert(resp.getStatus() == 404)


def test_18_meta_doc():
    """
    Test that the documentation can be received.

    """
    data, resp = _get_data("/meta/doc")
    assert(resp.getStatus() == 200)
    assert("documentation for the server" in data)


def test_30_code():
    """
    Test that information about the installed components is returned correctly.

    """
    data, resp = _get_data("/code")
    assert(resp.getStatus() == 200)

    # We expect to see at least the TwitterComponent
    assert("TwitterComponent" in data)

    # Each entry here should have a 'desc' and 'uri' field.
    for name, cdef in data.items():
        # Make sure they contain all the mandatory fields...
        assert("desc" in cdef)
        assert("uri" in cdef)
        # ... and nothing more than that
        for k in cdef:
            assert(k in [ 'desc', 'uri' ])


def test_40_twitter_code():
    """
    Test that information returned about the Twitter component is correct.

    """
    cdef, resp = _get_data("/code/TwitterComponent")
    assert(resp.getStatus() == 200)

    expected_keys = [ "desc", "doc", "name", "params", "resource_creation_params", "services", "uri" ]
    for name in expected_keys:
        assert(name in cdef)
    assert(len(expected_keys) == len(cdef))
    assert(cdef['name'] == "TwitterComponent")
    assert(cdef['uri']  == "/code/TwitterComponent")
    assert(cdef['desc'] == "Provides access to a Twitter account.")
    assert(cdef['doc']  == "/code/TwitterComponent/doc")

    params_def = {
        "account_name": {
            "default": None, 
            "desc": "Twitter account name", 
            "required": True, 
            "type": "string"
        }, 
        "account_password": {
            "default": None, 
            "desc": "Password", 
            "required": True, 
            "type": "password"
        }
    } 

    _dict_compare(cdef['params'], params_def)

    resource_creation_params_def = {
        "desc": {
            "default": "A 'TwitterComponent' resource", 
            "desc": "Specifies a description for this new resource", 
            "required": False, 
            "type": "string"
        }, 
        "public": {
            "default": False, 
            "desc": "Indicates whether the resource should be public", 
            "required": False, 
            "type": "boolean"
        }, 
        "suggested_name": {
            "default": None, 
            "desc": "Can be used to suggest the resource name to the server", 
            "required": True, 
            "type": "string"
        }
    } 

    _dict_compare(cdef['resource_creation_params'], resource_creation_params_def)

    services_def = {
        "status": {
            "desc": "You can GET the status or POST a new status to it.", 
            "uri": "/code/TwitterComponent/status"
        }, 
        "timeline": {
            "desc": "You can GET the timeline of the user.", 
            "uri": "/code/TwitterComponent/timeline"
        }
    } 

    _dict_compare(cdef['services'], services_def)


def test_999_cleanup():
    """
    Find all resources starting with "_test_" and delete them.

    This is actually more of a cleanup function.

    """
    rlist, resp = _get_data('/resource')
    assert(resp.getStatus() == 200)
    # Find any old test resources and delete them.
    for name in rlist:
        if name.startswith("_test_"):
            uri = rlist[name]
            buf, resp = _delete(uri)
            assert(resp.getStatus() == 200)




#
# Some utility methods
#
def _log(msg, eol=True, cur_time=None, continuation=False):
    """
    Log a message.

    @param msg:          The message to be logged.
    @type  msg:          string

    @param eol:          Flag indicating whether we put an '\n' at the end.
    @type  eol:          boolean

    @param continuation: Flag indicating whether this continues a previous line (don't print time stamp).
    @type  continuation: boolean

    """
    buf = ""
    if not continuation:
        if not cur_time:
            start_time = datetime.datetime.now()
        else:
            start_time = cur_time
        buf = "### %s - " % start_time.isoformat()
    buf += msg
    if eol:
        buf += "\n"
    print buf,


def _make_timediff_str(start_time, end_time):
    """
    Return properly formatted string with difference in start and end time (datetime.datetime object).

    """
    td = end_time - start_time
    return "%d.%06d" % (td.seconds, (td.microseconds * 1000000) / 1000000)


if __name__ == '__main__':
    #
    # Collect the names of all test methods
    #
    test_methods = [ name for name in dir() if name.startswith("test_") ]
    test_methods.sort()
    for method_name in test_methods:
        start_time = datetime.datetime.now()
        _log("Executing: %s" % string.ljust(method_name, 30), cur_time=start_time, eol=False)
        method = globals()[method_name]
        method()
        msg = "Ok"
        end_time = datetime.datetime.now()
        _log(" - Duration: %ss - %s" % (_make_timediff_str(start_time, end_time), msg), continuation=True)

