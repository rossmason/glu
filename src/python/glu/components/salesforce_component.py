"""
A salesforce component.

"""
# Python imports
import urllib
import glujson as json
import beatbox

# Glu imports
from glu.components.api import *
from glu.exceptions import *

class SalesforceComponent(BaseComponent):
    NAME             = "SalesforceComponent"
    PARAM_DEFINITION = {
                           "username" :       ParameterDef(PARAM_STRING,   "Salesforce Username", required=True),
                           "password" :       ParameterDef(PARAM_PASSWORD, "Salesforce Password", required=True),
                           "security_token" : ParameterDef(PARAM_PASSWORD, "Salesforce Security Token", required=True),
                           "API_URI" :        ParameterDef(PARAM_STRING,   "Salesforce API URI", required=False,
                                                           default="https://test.salesforce.com/services/Soap/u/16.0")
                       }
    
    DESCRIPTION      = "Provides an interface to Salesforce."
    DOCUMENTATION    =  """
                        This component implements a number of sub-resources,
                        which can be used to access information about the specified
                        Salesforce account.
                        """
    SERVICES         = {
                           "fields" : {
                               "desc"   : "Return a list of field names for the specified object type (table)",
                               "params" : {
                                    "type" : ParameterDef(PARAM_STRING, "The object type (table name)", required=True),
                               },
                               "positional_params" : [ "type" ]
                           },
                           "query" : {
                               "desc"   : "POST a query string to the specified name and later GET the results",
                               "params" : {
                                    "name"             : ParameterDef(PARAM_STRING, "Name for the query", required=True),
                                    "filter_fieldname" : ParameterDef(PARAM_STRING, "Field name for filtering", required=False, default=""),
                                    "filter_value"     : ParameterDef(PARAM_STRING, "Field value for filtering", required=False, default=""),

                               },
                               "positional_params" : [ "name", "filter_fieldname", "filter_value" ]
                           }
                        }
    
    def __connect(self, params):
        """
        Connect to Salesforce, returning a Python client object.

        """
        username    = params['username']
        password    = params['password']
        token       = params['security_token']
        api_uri     = params['API_URI']

        svc = beatbox.PythonClient(api_uri)
        svc.login(username, password + token)

        return svc

    def __convert_salesforce_results_to_dict(self, res):
        """
        The salesforce query results are dictionary/list like,
        but use their own type. Their string representation looks
        like those of basic types, so a quick and dirty way to
        convert to basic types is to let JSON do the job.

        I probably should upgrade the representation layer, so that
        it can deal with dictionary/list 'like' objects, but this
        works for now.

        """
        return json.loads(json.dumps(res))

    def __return_where_clause(self, field, value):
        """
        Return the where clause that should be added to 'WHERE'.

        We allow special notation for 'like', 'gt', 'gte', 'lt' and 'lte'.
        If the field name contains that at the end (after __) then we
        return the proper clause. For example:

            field = "year__lte"
            value = 1969

        In that case, we return "year < 1969"

        For 'like', we use the usual notation "field like 'foo%'

        """
        # Sanitize the value (if surrounded by '"' then we need to replace
        # those with "'".
        if value.startswith('"') and value.endswith('"'):
            value = "'" + value[1:-1] + "'"

        i = field.find("__")
        if i == -1:
            # Nothing special
            op = "="
        else:
            op_str = field[i+2:]
            field  = field[:i]
            op_translate = {
                "like" : "like",
                "eq"   : "=",
                "gt"   : ">",
                "gte"  : ">=",
                "lt"   : "<",
                "lte"  : "<="
            }
            op = op_translate.get(op_str)
            if not op:
                raise GluBadRequest("Unknown operand '%s' for field '%s'" % (op_str, field))
        return "%s %s %s" % (field, op, value)


    def query(self, request, input, params):
        """
        Return query results for a query.
        
        @param request:    Information about the HTTP request.
        @type request:     BaseHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # Access to our storage bucket
        storage = self.getFileStorage()

        query_name = params['name']

        if request.getRequestMethod() == "DELETE":
            storage.deleteFile(query_name)
            data = "Query '%s' deleted" % query_name
        else:
            if input:
                storage.storeFile(query_name, input)
                data = "Query '%s' successfully stored" % query_name
            else:
                try:
                    query_string = storage.loadFile(query_name).strip()
                    # If this was stored as JSON then there might be quotes around the query string
                    if query_string.startswith('"')  and  query_string.endswith('"'):
                        query_string = query_string[1:-1]

                    # See if there are filter parameters. If so, we add those to the query
                    # string, but only if the query string does not hold a WHERE clause already.
                    filter_field = params['filter_fieldname']
                    filter_value = params['filter_value']
                    if filter_field  and  filter_value  and 'where' not in query_string.lower():
                        query_string += " WHERE %s" % self.__return_where_clause(filter_field, filter_value)
                    svc  = self.__connect(params)
                    data = self.__convert_salesforce_results_to_dict(svc.query(query_string))
                except GluFileNotFound, e:
                    raise GluResourceNotFound("Query '%s' could not be found" % query_name)

        return 200, data


    def fields(self, request, input, params):
        """
        Return the field names for a given object type.
        
        @param request:    Information about the HTTP request.
        @type request:     BaseHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        type_name = params['type']

        svc   = self.__connect(params)
        dlist = svc.describeSObjects([type_name])

        return 200, dlist[0].fields.keys()

