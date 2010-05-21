"""
A test component.

"""
# Python imports
import math
import random
import urllib
import glujson as json

# Glu imports
from glu.components.api import *

class GpsWalkerComponent(BaseComponent):
    NAME             = "GpsWalkerComponent"
    PARAM_DEFINITION = {
                       }
    
    DESCRIPTION      = "Modifies GPS coordinates in a random manner."
    DOCUMENTATION    =  """
                        Modifies GPS coordinates in a random manner.

                        Coordinates are passed to the exposed 'walk' service, which
                        returns a modified set to the caller.

                        """
    SERVICES         = {
                           "walk" :   {
                               "desc"   : "Provide 'lat' and 'long' as attribute to GET modified coordinates.",
                               "allow_params_in_body" : True,
                               "params" : {
                                    "lat"        : ParameterDef(PARAM_NUMBER, "Latitude as float number", required=True),
                                    "long"       : ParameterDef(PARAM_NUMBER, "Longitude as float number", required=True),
                               }
                           },
                           "city" : {
                                "desc"  : "Return coordinates for the specified city: 'SanFrancisco', 'London', 'Valletta', 'Auckland'",
                                "allow_params_in_body" : True,
                                "params" : {
                                    "name"       : ParameterDef(PARAM_STRING, "Name of the city", required=True)
                                }
                            }
                       }
    
            
    def walk(self, method, input, lat, long):
        """
        Performs a random modification of passed in GPS coordinates.
        
        @param method:     The HTTP request method.
        @type method:      string

        @param input:      Any data that came in the body of the request.
        @type input:       string
                
        @return:           Return dictionary with 'lat' and 'long' keys.
        @rtype:            dict
        
        """
        dist  = random.random() * 0.002
        angle = random.random() * math.pi * 2

        lat  += dist * math.sin(angle)
        long += dist * math.cos(angle)
        data = {
                    "lat"  : lat,
                    "long" : long,
               }
        code = 200
        return code, data


    CITY_COORDS = {
        "SanFrancisco" : { "lat" : 37.789167,  "long" : -122.419281 },
        "London"       : { "lat" : 51.515259,  "long" : -0.11776 },
        "Valletta"     : { "lat" : 35.897655,  "long" : 14.511631 },
        "Auckland"     : { "lat" : -36.848461, "long" : 174.762183 },
    }

    def city(self, method, input, city_name):
        """
        Return the coordinates of a specified city.

        """
        # Getting the coordinates of that city. If the city is unknown
        # then we just return the coordinates for Auckland.
        new_coords = self.CITY_COORDS.get(city_name, self.CITY_COORDS['Auckland'])
        return 200, new_coords


