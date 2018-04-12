from .html40 import HTML40
from .__main__ import main


# create a singleton instance of this class. The approved method to use phileas is to include this
# by  "from phileas import html40 as h" (The alias with leading '_' is deprecated but retained to avoid
# having to refactor lots of stuff!). Then html element creation can use the compact form
# (e.g.) "h.h4 ..." etc. (html40.h4 ... would soon get cumbersome!)

_html40 = html40_ = HTML40()
# I recommend that this is imported under a much shorter name, e.g.:
# 'from phileas import html40 as h'. This usage will be assumed and
# 'h' referred to as 'the HTML generator' in this code.
