import sys
import urllib
import simplejson as json

#
# For the TWITTER component:
#
# Specify the account name and password
#
TWITTER_ACCOUNT  = "BrendelConsult"      # Replace those two with actual account credentials
TWITTER_PASSWORD = "tw88erbahn"

#SERVER_URL = "http://mulesoft-glu.appspot.com"
#SERVER_URL = "http://localhost:8080"
SERVER_URL = "http://localhost:8001"




def json_pretty_print(json_str):
    obj = json.loads(json_str)
    print json.dumps(obj, indent=4)

#
# A URL opener and handler class
#
ERROR_INFO = None
class MyOpener(urllib.URLopener):
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        global ERROR_INFO
        ERROR_INFO = (errcode, errmsg, fp.read())
    def add_msg(self, message):
        if message:
            self._my_msg = message
            self.addheader('Content-length', str(len(message)))
    def send(self, code_url):
        if hasattr(self, "_my_msg"):
            msg = self._my_msg
            print "@@ POSTing to server: ", msg
        else:
            msg = None
        return self.open(code_url, msg)
        

#
# Post stuff to create a resource
#
def send_test(data, code_url):
    global ERROR_INFO
    print "="*80
    opener = MyOpener()
    opener.addheader('Connection', 'close')
    opener.addheader('Accept', 'application/json')
    opener.add_msg(json.dumps(data))
    stream = opener.send(code_url)
    
    if stream:
        data   = stream.read()
        print "Received data: ", data
    else:
        print "ERROR: ", ERROR_INFO


print "\nCreating a few resources on the server...\n"

# Create the Twitter component
send_test({
            'params' : {
                "account_password" : TWITTER_PASSWORD,
                "account_name" :     TWITTER_ACCOUNT
             },
             "resource_creation_params" : {
                "suggested_name" : "%sTwitter" % TWITTER_ACCOUNT
             }
          },
          code_url=SERVER_URL + "/code/TwitterComponent")


# Create the Gsearch component
send_test({
            'params' : {
                'api_key' : "ABQIAAAApvtgUnVbhZ4o1RA5ncDnZhT2yXp_ZAY8_ufC3CFXhHIE1NvwkxS5mUUQ41lAGdMeNzzWizhSGRxfiA"
            },
            'resource_creation_params' : {
                'suggested_name' : 'MyGoogleSearch'
            }
          },
          code_url=SERVER_URL + "/code/GoogleSearchComponent")

# Create the Combiner component
send_test({
            'resource_creation_params' : {
                'suggested_name' : 'Combiner',
                'desc'           : "Just a test, don't use this one..."
            }
          },
          code_url=SERVER_URL + "/code/CombinerComponent")

# Create the GpsWalker component
send_test({
            'resource_creation_params' : {
                'suggested_name' : 'MyGPSWalker'
            }
          },
          code_url=SERVER_URL + "/code/GpsWalkerComponent")

# Create the Storage component
send_test({
            'resource_creation_params' : {
                'suggested_name' : 'MyStorageResource'
            },
          },
          code_url=SERVER_URL + "/code/StorageComponent")

# Create another Storage component
send_test({
            'resource_creation_params' : {
                'suggested_name' : 'MySecondStorageResource'
            },
          },
          code_url=SERVER_URL + "/code/StorageComponent")

# Create a Salesforce component
send_test({
            'params' : {
                'username'       : 'development@mulesource.com.support',
                'password'       : 'mul3d3v201510',
                'security_token' : '9UUFx84vYkL1GcUPGOPQG0IfB',
                'API_URI'        : 'https://test.salesforce.com/services/Soap/u/16.0'
            },
            'resource_creation_params' : {
                'suggested_name' : 'MySalesforceResource'
            },
          },
          code_url=SERVER_URL + "/code/SalesforceComponent")

send_test("blah blah", "http://localhost:8001/resource/MySalesforceResource/query/contact")

print "\nDone..."