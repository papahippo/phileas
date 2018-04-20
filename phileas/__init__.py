from .html4 import HTML4
from .html5 import HTML5

# create a singleton instance of this class. The approved method to use phileas is to include this
# by  "from phileas import html40 as h" (The alias with leading '_' is deprecated but retained to avoid
# having to refactor lots of stuff!). Then html element creation can use the compact form
# (e.g.) "h.h4 ..." etc. (html4.h4 ... would soon get cumbersome!)

_html40 = html4 = HTML4()
html5 = HTML5()
