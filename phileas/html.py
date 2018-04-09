#!/usr/bin/python
"""
This is the '__init__' file of the 'phileas' package.
Phileas stands for  Python/HTML Integration - Larry's Elegant Alternative Solution.
(For 'Elegant' you may wish to substitute e.g. 'Eccentric' or 'Excruciating' -
I don't mind - just try to spell it properly!) See http://larry.myerscough.nl
(n.b. no "www." up front) for an example of a site built using this module.
Use the 'show source' button of the left-hand panel to view and/or capture the
python source code.
"""
import sys
from element import Element


class HTML_Error(Exception):
    pass


class HTML(object):
    """
This class is called _HTML40 because its members correspond to HTML 4.0 tags.
The leading _ is appropriate because it is not intended for direct use by
external code. A single instance of this class this created within this
module. This is conventionally imported by other modules by the construction
'from phileas._HTML40 import _html40 as h'. html can be generated via terms
like 'h.h1', 'h.p' etc. See the 'main' within this module for an example of
its use.
    """

    def __getattr__(self, attr_name):
        """
This handles the first call of the form h.tag for a particular tag where h is
a (usually THE) instance of class _HTML40. It effectively return a instance of
class _HTML40._tag, supplying the actual tag value (e.g. 'br', 'p', 'h4') as an argument
to the __init__. (release 0.6 change ...) This function will only be called once per
Element type. This is because the instance will be remembered under the tag name
and hence automatically returned by the standard 'getattribute' handler on subsequent calls.
        """
        if attr_name.startswith('__'):
            return object.__getattribute__(self, attr_name)
        elif attr_name.startswith('_'):
            # This seems to be the easiest way to pick up invalid
            # tags BEFORE a run-time recursion error occurs!
            # src'
            raise HTML_Error("Invalid tag '%s'" % attr_name)
        attr = getattr(self, '_' + attr_name)(tag=attr_name)

        # ensure that subsequent attribute references will work without our intervention!
        #
        object.__setattr__(self, attr_name, attr)
        return attr

    def __setattr__(self, attr_name, value):
        """ Once set, attributes may not be overwritten. This reduces the risk
            of accidental damage to the HTML tag generation mechanism. This is
            done heavy-handedly by refusing all attempts to set attributes.
            (We get round this internally by invoking 'object.__setattr__'!)
        """
        raise HTML_Error("Not allowed; would change behaviour of tag '%s'" % attr_name)

    def __or__(self, other):
        """ This is really a special case of the '__or__' operation as applied
            to Elements (see class '_Element' definition below. E.g. 'h | ('abc', 'def')'
            creates a 'tagless' Element with two children, each a string.
        """
        return Element(tag=None, separateClose=False,
                               children=[other, ])

    def __ior__(self, other):
        """ This is a 'goalkeeper' function to prevent inadvertent corruption
            of the singleton instance of this class by constructions like
            'h |= "text"' which python might 'helpfully' convert to 'h = h | "text".
            We can't prevent explicit use of the latter form but we do our best!
        """
        raise HTML_Error("you're not allowed to modify the html generator like this.")

