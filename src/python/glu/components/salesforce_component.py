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

#
# All the services have the same parameters. We only need to define them once.
#
_all_tables_params =  {
                            "spec"                : ParameterDef(PARAM_STRING,
                                                                 "Spec for query. Specify 'fields' to see all available fields and 'data' to see contents.",
                                                                 required=True),

                            "filter_fieldname_1"  : ParameterDef(PARAM_STRING,
                                                                 "Field name for filtering. Append __lt, __lte, __gt, __gte, __ne or __like to further " \
                                                                 "specify the filtering in an SQL like manner.",
                                                                 required=False, default=""),
                            "filter_value_1"      : ParameterDef(PARAM_STRING, "Field value for filtering", required=False, default=""),

                            "filter_fieldname_2"  : ParameterDef(PARAM_STRING,
                                                                 "Field name for filtering. Append __lt, __lte, __gt, __gte, __ne or __like to further " \
                                                                 "specify the filtering in an SQL like manner.",
                                                                 required=False, default=""),
                            "filter_value_2"      : ParameterDef(PARAM_STRING, "Field value for filtering", required=False, default=""),

                             "filter_fieldname_3" : ParameterDef(PARAM_STRING,
                                                                 "Field name for filtering. Append __lt, __lte, __gt, __gte, __ne or __like to further " \
                                                                 "specify the filtering in an SQL like manner.",
                                                                 required=False, default=""),
                            "filter_value_3"      : ParameterDef(PARAM_STRING, "Field value for filtering", required=False, default=""),

                             "view"               : ParameterDef(PARAM_STRING,
                                                                 "If 'data' was requested, this determines how much data is returned: 'compact' for only " \
                                                                 "the most essential fields, 'normal' for the default contact fields, 'all' for all fields, " \
                                                                 "including custom fields.",
                                                                 required=False, default="compact"),
                      }

_all_positional_params =  [ "spec",
                            "filter_fieldname_1", "filter_value_1",
                            "filter_fieldname_2", "filter_value_2",
                            "filter_fieldname_3", "filter_value_3",
                          ]


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
    DOCUMENTATION    = """
                       This component implements a number of sub-resources,
                       which can be used to access information about the specified
                       Salesforce account.

                       To filter your results, you can specify up to 3 pairs of field/value
                       on the URL command line when you access data.
                       """

    SERVICES         = {
                            "contact" : {
                                "desc"              : "Return or update information about contacts",
                                "params"            : _all_tables_params,
                                "positional_params" : _all_positional_params
                            },
                            "lead" : {
                                "desc"              : "Return or update information about leads",
                                "params"            : _all_tables_params,
                                "positional_params" : _all_positional_params
                            },
                            "opportunity" : {
                                "desc"              : "Return or update information about opportunities",
                                "params"            : _all_tables_params,
                                "positional_params" : _all_positional_params
                            },
                        }

    #
    # Fields for the contact table
    #
    __contact_fields_compact = [
        "Id", 
        "CreatedDate", 
        "Name", 
        "FirstName", 
        "LastName", 
        "Email", 
        "Phone", 
        "MailingStreet", 
        "MailingCity", 
        "MailingState", 
        "MailingPostalCode", 
        "MailingCountry" 
    ]

    __contact_fields_normal = [
        "AccountId", 
        "Title", 
        "Salutation", 
        "Department", 
        "Fax", 
        "IsDeleted", 
        "OtherPhone", 
        "OtherStreet", 
        "OtherCity", 
        "OtherState", 
        "OtherPostalCode", 
        "OtherCountry", 
        "MobilePhone", 
        "LastCUUpdateDate", 
        "LastModifiedById", 
        "EmailBouncedReason", 
        "OwnerId", 
        "SystemModstamp", 
        "MasterRecordId", 
        "AssistantPhone", 
        "LastModifiedDate", 
        "AssistantName", 
        "HasOptedOutOfEmail", 
        "LastCURequestDate", 
        "EmailBouncedDate", 
        "Birthdate", 
        "DoNotCall", 
        "ReportsToId", 
        "Description", 
        "CreatedById", 
        "LeadSource", 
        "LastActivityDate", 
        "HomePhone", 
    ]

    #
    # Fields for the lead table
    #
    __lead_fields_compact = [
        "Id",
        "CreatedDate",
        "Name",
        "FirstName",
        "LastName",
        "Email",
        "Phone",
        "Street",
        "City",
        "State",
        "PostalCode",
        "Country",
        "Company",
        "Description",
        "Status"
    ]
    __lead_fields_normal  = [
        "AnnualRevenue",
        "Title",
        "Fax",
        "IsDeleted",
        "Industry",
        "ConvertedContactId",
        "Rating",
        "MobilePhone",
        "ConvertedOpportunityId",
        "LastModifiedById",
        "IsUnreadByOwner",
        "OwnerId",
        "ConvertedDate",
        "SystemModstamp",
        "MasterRecordId",
        "ConvertedAccountId",
        "LastModifiedDate",
        "HasOptedOutOfEmail",
        "IsConverted",
        "EmailBouncedDate",
        "EmailBouncedReason",
        "NumberOfEmployees",
        "CreatedById",
        "LeadSource",
        "LastActivityDate",
        "Salutation",
        "Website"
    ]

    #
    # Fields for the opportunity table
    #
    __opportunity_fields_compact = [
        "Id",
        "CreatedDate",
        "Name",
        "IsWon",
        "IsClosed",
        "Amount",
        "Probability",
        "ExpectedRevenue",
    ]

    __opportunity_fields_normal = [
        "FiscalQuarter",
        "LastModifiedById",
        "CloseDate",
        "OwnerId",
        "Type",
        "Description",
        "StageName",
        "LastModifiedDate",
        "ForecastCategoryName",
        "CreatedById",
        "IsDeleted",
        "AccountId",
        "FiscalYear",
        "Fiscal",
        "LeadSource",
        "Pricebook2Id",
        "LastActivityDate",
        "HasOpportunityLineItem",
        "NextStep",
        "SystemModstamp",
        "ForecastCategory",
    ]

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
        encoded = json.gludumps(res)
        return json.loads(encoded)

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
                "lte"  : "<=",
                "ne"   : "<>"
            }
            op = op_translate.get(op_str)
            if not op:
                raise GluBadRequest("Unknown operand '%s' for field '%s'" % (op_str, field))
        return "%s %s %s" % (field, op, value)


    def __adding_where_clause(self, params):
        """
        Check for any filter parameters on the URL command line and
        create a WHERE clause if appropriate, which is returned as
        a string.

        """
        #
        # Any filtering on particular fields specified?
        # If so, we add this to a 'WHERE' clause in the query.
        #
        filters = [ ( params['filter_fieldname_%d' % id], params['filter_value_%d' % id] ) for id in [ 1, 2, 3 ] ]

        filter_expressions = list()
        for fieldname, value in filters:
            if fieldname  and  value:
                if type(value) is str:
                    value = "'%s'" % value
                filter_expressions.append(self.__return_where_clause(fieldname, value))

        if filter_expressions:
            where_clause = " WHERE %s" % " and ".join(filter_expressions)
        else:
            where_clause = ""

        return where_clause
        
    def __get_all_field_names(self, svc, table_name):
        """
        Return list of all field names for the given table.

        """
        dlist = svc.describeSObjects([ table_name ])
        all_fields = dlist[0].fields.keys()
        return all_fields

    def __make_select_statement_for_view(self, view, table_name, compact_fields, normal_fields, svc):
        """
        Return the select statement string for the givenview and table.

        """
        if view == "compact":
            # Run normal query, only returning a compact view
            query_string = "select %s from %s" % (", ".join(compact_fields), table_name)
        elif view == "normal":
            # Run normal query, returning all the default fields
            query_string = "select %s from %s" % (", ".join(compact_fields + normal_fields), table_name)
        elif view == "all":
            # Run a query, which returns data for all fields, even custom ones.
            # Therefore, we start by querying which fields are defined for contact
            # and then subsequently we issue the query for all those fields.
            all_fields   = self.__get_all_field_names(svc, table_name)
            query_string = "select %s from %s" % (", ".join(all_fields), table_name)
        else:
            raise GluBadRequest("Unknown view: " + view)

        return query_string


    def __salesforce_table(self, request, input, params, table_name, compact_fields, normal_fields):
        """
        A generic helper method for access to salesforce tables.

        This method implements a number of facilities that are common to all
        the various tables we want to expose through this resource. Therefore,
        after prepping the 'compact_fields' and 'other_fields' table, the actual
        service methods can just call this helper method here.

        Implements the 'fields' and 'data' specs, handles filter
        parameters and views for data.

        Besides the usual parameters that are passed to service methods, this
        one also takes 'compact_fields' and 'other_fields' to specify, which
        fields are to be shown depending on the selected view.

        The 'table_name' specifies the table on which we operate.

        """
        svc  = self.__connect(params)

        # The spec determines what we are doing with this table.
        # Either we just want to see the field names or the actual
        # data behind it.
        spec = params['spec']
        if spec == 'fields':
            #
            # Just need to return the list of fields that are defined in contact
            #
            data = self.__get_all_field_names(svc, table_name)

        elif spec == "data":
            #
            # Want to see some actual data
            #
            # An optional 'view' parameter may have been specified, which tells us
            # what fields to request in our queries.
            #
            view         = params['view'].lower()
            query_string = self.__make_select_statement_for_view(view, table_name, compact_fields, normal_fields, svc)
                
            #
            # Any filtering on particular fields specified?
            # If so, we add this to a 'WHERE' clause in the query.
            #
            query_string += self.__adding_where_clause(params)

            #
            # Finally we can run the actual query
            #
            data = self.__convert_salesforce_results_to_dict(svc.query(query_string))

        else:
            raise GluBadRequest("Unknown query spec: " + spec)

        return 200, data
 

    def contact(self, request, input, params, method):
        """
        Handle information about our contacts.
        
        @param request:    Information about the HTTP request.
        @type request:     GluHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        code, data = self.__salesforce_table(request, input, params, "contact",
                                             self.__contact_fields_compact, self.__contact_fields_normal) 
        return code, data

    def lead(self, request, input, params, method):
        """
        Handle information about our leads.
        
        @param request:    Information about the HTTP request.
        @type request:     GluHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        code, data = self.__salesforce_table(request, input, params, "lead",
                                             self.__lead_fields_compact, self.__lead_fields_normal) 
        return code, data

    def opportunity(self, request, input, params, method):
        """
        Handle information about our opportunities.
        
        @param request:    Information about the HTTP request.
        @type request:     GluHttpRequest
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @param params:     Dictionary of parameter values.
        @type params:      dict
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        code, data = self.__salesforce_table(request, input, params, "opportunity",
                                             self.__opportunity_fields_compact, self.__opportunity_fields_normal) 
        return code, data


