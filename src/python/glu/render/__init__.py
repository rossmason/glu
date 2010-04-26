"""
This module provides renderers for data into
different output formats.

You can import these classes straight from module level:

    * BaseRenderer

"""
# Export classes on module level, so that users don't need
# to specify the individual file names in their imports.
from glu.render.htmlrenderer import HtmlRenderer
from glu.render.jsonrenderer import JsonRenderer
