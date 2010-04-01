"""
Exports the various beans, which are available.

Also defines a base class for all beans.

"""
#
# When adding a new bean, all that is required is to
# add the import statement and add the bean to the 'KNOWN_BEANS' list.
# 

# Exporting these beans
from glu.beans.base_bean      import BaseBean
from glu.beans.twitter_bean   import TwitterBean
from glu.beans.gsearch_bean   import GsearchBean
from glu.beans.combiner_bean  import CombinerBean
from glu.beans.gpswalker_bean import GpsWalkerBean

#
# The known beans
#
_KNOWN_BEANS = [ TwitterBean, GsearchBean, CombinerBean, GpsWalkerBean ]

# -------------------------------------------------------------------------------------
# Don't edit down here...
# -------------------------------------------------------------------------------------

_CODE_MAP = dict([ (bean_class().getName(), bean_class) for bean_class in _KNOWN_BEANS ])
