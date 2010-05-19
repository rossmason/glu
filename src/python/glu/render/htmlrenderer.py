"""
Contains the HTML-renderer class.

"""
# Python imports
from copy   import copy
import string

# Glu imports
import glu.settings as settings

from glu.render.baserenderer import BaseRenderer
from glu.core.util           import bool_view

from org.mulesource.glu.util import Url

class HtmlRenderer(BaseRenderer):
    """
    Outputs Python objects into HTML.
    
    Understands the renderer_args:
    
        * no_annotations (no writing of 'List' or 'Object' before lists or dicts)
        * no_table_headers (no writing of 'Key' and 'Value' above dictionaries)
        * no_list_indices (no writing of array indices)
        * no_border (no table and cell borders)
    
    """
    CONTENT_TYPE = "text/html"

    def __init__(self, renderer_args, breadcrums):
        """
        Initialize the renderer.
        
        @param renderer_args: A dictionary of flags, which can influence the
                              output. The flags are explained in the class docstring.
        @type renderer_args:  dict
        
        @param breadcrums:    The breadcrums for this request. Defined as a list
                              of (name,uri) tuples, for navigation. Breadcrums are
                              maintained by the browser class for this request.
        @type breadcrums:     list
        
        """
        super(HtmlRenderer, self).__init__(renderer_args)
        self.draw_annotations = False if self.renderer_args.get('no_annotations') else True
        self.table_headers    = False if self.renderer_args.get('no_table_headers') else True
        self.draw_indices     = False if self.renderer_args.get('no_list_indices') else True
        self.draw_borders, self.border_width = (False,0) if self.renderer_args.get('no_borders') else (True,1)
        self.breadcrums       = breadcrums
        
        self.header = settings.HTML_HEADER + \
                      '%s<br><hr>' % (self.__render_breadcrums(self.breadcrums))
                      
                      
    def __render_breadcrums(self, breadcrums):
        """
        Output HTML for breadcrums.
        
        Breadcrums are given as a list of tuples, with each tuple containing
        a (name,URI). The last breadcrum should not be rendered as a clickable
        link.
        
        @param breadcrums:    List of breadcrums.
        @type breadcrums:     list
        
        @return:              HTML for breadcrums.
        @rtype:               string
        
        """
        segments = []
        for i, elem in enumerate(breadcrums):
            name, uri = elem
            if i < len(breadcrums)-1:
                # All but the last element are rendered as clickable links
                segments.append('<a href="%s">%s</a>' % (uri, name))
            else:
                segments.append(name)
        return " > ".join(segments)            
            
    def __dict_render(self, data):
        """
        Take Python dictionary and produce HTML output.
        
        The output of a dictionary is modified by some of the renderer arguments.
        
        @param data:    A dictionary that needs to be rendered in HTML.
        @type  data:    dict
        
        @return:        HTML representation of the dictionary.
        @rtype:         string        
        """
        annotation   = "<i>Object</i><br/>\n" if self.draw_annotations else ""

        keys = copy(data.keys())
        # In the future we might want to display particular items
        # in specific positions, but for now, we just sort the
        # items alphabetically.
        keys.sort()
        out = "%s<table border=%d cellspacing=0>\n" % (annotation, self.border_width)
        if self.table_headers:
            out += '<tr><td class="dict"><i>Key</i></td><td class="dict"><i>Value</i></td></tr>\n'
        for key in keys:
            out += "<tr>\n<td valign=top>%s</td>\n<td valign=top>" % \
                                            (key.as_html() if type(key) is Url else key)
            out += self.render(data[key])
            out += "\n</td>\n</tr>"
        out += "</table>"
        return out
    
    def __list_render(self, data):
        """
        Take Python list and produce HTML output.
        
        The output of a list is modified by some of the renderer arguments.
        
        @param data:    A list that needs to be rendered in HTML.
        @type  data:    list
        
        @return:        HTML representation of the list.
        @rtype:         string
        
        """
        annotation   = "<i>List</i><br/>\n" if self.draw_annotations else ""
        out = "%s<table border=%d cellspacing=0>" % (annotation, self.border_width)
        for i, elem in enumerate(data):
            if self.draw_indices:
                index_column = "<td valign=top>%d</td>" % i
            else:
                index_column = ""
            out += "<tr>%s<td valign=top>%s</td></tr>" % (index_column, self.render(elem))
        out += "</table>"
        return out
    
    def __plain_render(self, data):
        """
        Take a non-list, non-dict Python object and produce HTML.
        
        A simple conversion to string is performed.
        
        @param data:    A Python object
        @type  data:    object
        
        @return:        HTML representation of the object.
        @rtype:         string

        """
        if type(data) is unicode  or  type(data) is str:
            # WSGI wants str(), but some unicode characters can cause exceptions.
            # I'm sure there are better ways to do this, but that works for now.
            # When we use Jython then we can get unprintable characters even
            # in str (while later string operations may fail, which is totally
            # odd...)
            data = ''.join([ (str(x) if x in string.printable else "") for x in data ])
        # Note that when we use Jython we still have unicode (the conversion to str
        # doesn't seeem to work). That's why in the following line we have to test
        # for str() as well as unicode(). The return in unicode is not a problem
        # for the Java server.
        if type(data) is str  or  type(data) is unicode:
            if data.startswith("http://") or data.startswith("https://")  or data.startswith("/"):
                data = Url(data)
        if data is None:
            out = "---"
        elif type(data) is Url:
            out = data.as_html()
        elif type(data) is bool:
            out = bool_view(data)
        else:
            if type(data) is not unicode:
                data_str = str(data)
            else:
                data_str = data
            if type(data) is not str  and  type(data) is not unicode  and  type(data) in [ int, float ]:
                # Output as number
                out = data_str
            else:
                out = '"%s"' % data_str.replace("\n", "<br/>")
        return out

    def render(self, data, top_level=False):
        """
        Take Python object and produce HTML output.
        
        @param data:        An object containing the data to be rendered.
        @param data:        object
        
        @param top_level:   Flag indicating whether this we are at the
                            top level for output (this function is called
                            recursively and therefore may not always find
                            itself at the top level). This is important for
                            some renderers, since they can insert any framing
                            elements that might be required at the top level.
                            In the case of this HTML renderer, we can add
                            some nice headers and footers.
        @param top_level:   boolean
        
        @return:            Output buffer with completed representation.
        @rtype:             string
            
        """
        out = ""
        if type(data) is dict:
            out += self.__dict_render(data)
        elif type(data) is list:
            out += self.__list_render(data)
        else:
            out += self.__plain_render(data)
        if top_level:
            out = "%s%s%s" % (self.header, out, settings.HTML_FOOTER)
        return out
