"""
Exports the various components, which are available.

Also defines a base class for all components.

"""
#
# When adding a new component, all that is required is to
# add the import statement and add the component to the 'KNOWN_COMPONENTS' list.
# 

# Exporting these components
from glu.components.base_component         import BaseComponent
from glu.components.twitter_component      import TwitterComponent
from glu.components.gsearch_component      import GsearchComponent
from glu.components.combiner_component     import CombinerComponent
from glu.components.gpswalker_component    import GpsWalkerComponent
from glu.components.storage_component      import StorageComponent
#from glu.components.salesforce_component   import SalesforceComponent
#from glu.components.marakana_component     import MarakanaComponent

#
# The known components
#
_KNOWN_COMPONENTS = [ TwitterComponent, GsearchComponent, CombinerComponent, GpsWalkerComponent, StorageComponent ]
#                      SalesforceComponent, MarakanaComponent ]

# -------------------------------------------------------------------------------------
# Don't edit down here...
# -------------------------------------------------------------------------------------

_CODE_MAP = dict([ (component_class().getName(), component_class) for component_class in _KNOWN_COMPONENTS ])
