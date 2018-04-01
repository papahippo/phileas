#!/usr/bin/python
"""
This is the one essential file of the 'phileas' package.
Phileas stands for  Python/HTML Integration - Larry's Elegant Alternative Solution.
(For 'Elegant' you may wish to substitute e.g. 'Eccentric' or 'Excruciating' -
I don't mind - just try to spell it properly!)
See http://larry.myerscough.nl (n.b. no "www." up front) for an example of a site built using this module.
Use the 'show source' button of the left-hand panel to view and/or capture the python source code.
"""
from __future__ import print_function
import sys


def unravel(seq):
    """
Unravel/flatten a sequence of HTML _HTML40.Elements. This is necessary because concatenations
of _HTML40.Elements may be coded as tuples or lists. The unravelling happens when the top level _HTML40.Element is
stringified. In other words, sequencing is a form of deferred concatenation. Earlier versons of phileas didn't
support the use of '+' to 'concatenate as you go' so many levels of unravelling could be required.
As one might guess, 'unravel' is a recursive function.
    """
    ans = []
    for it in seq:
        if not it:
            continue
        if isinstance(it, (list, tuple)):
            ans += unravel(it)
        else:
            ans.append(it)
    return ans


class HTML_Error(Exception):
    pass


CoreAttrs = {'id': 1, 'class': 1, 'style': 1, 'title': 1}
I18n = {'lang': 1, 'dir': 1}
IntrinsicEvents = {'onload': 1, 'onunload': 1, 'onclick': 1,
                   'ondblclick': 1, 'onmousedown': 1, 'onmouseup': 1,
                   'onmouseover': 1, 'onmousemove': 1, 'onmouseout': 1,
                   'onfocus': 1, 'onblur': 1, 'onkeypress': 1,
                   'onkeydown': 1, 'onkeyup': 1, 'onsubmit': 1,
                   'onreset': 1, 'onselect': 1, 'onchange': 1}

AlternateText = {'alt': 1}
ImageMaps = {'shape': 1, 'coords': 1}
AnchorReference = {'href': 1}
TargetFrameInfo = {'target': 1}
TabbingNavigation = {'tabindex': 1}
AccessKeys = {'accesskey': 1}

VisualPresentation = {'height': 1, 'width': 1, 'border': 1, 'align': 1,
                      'hspace': 1, 'vspace': 1}

CellHAlign = {'align': 1, 'char': 1, 'charoff': 1}
CellVAlign = {'valign': 1}

FontModifiers = {'size': 1, 'color': 1, 'face': 1}

LinksAndAnchors = {'href': 1, 'hreflang': 1, 'type': 1, 'rel': 1, 'rev': 1}
BordersAndRules = {'frame': 1, 'rules': 1, 'border': 1}


class _HTML40(object):
    """ This class is called _HTML40 because its members correspond to HTML 4.0 tags.
        The leading _ is appropriate because it is not intended for direct use by
        external code. A single instance of this class this created within this
        module. This is conventionally imported by other modules by the construction
        'from phileas._HTML40 import _html40 as h'. html can be generated via terms
        like 'h.h1', 'h.p' etc. See the 'main' within this module for an example of
        its use.
    """

    def __getattr__(self, attr_name):
        """
This handles the first call of the form h.tag for a particular tag where h is a (usually THE) instance of class _HTML40.
It effectively return a instance of class _HTML40._tag, supplying the actual tag value (e.g. 'br', 'p', 'h4') as
an argument to the __init__. (release 0.6 change ...) This function will only be called once per _HTML40.Element type.
This is because the instance will be remembered under the tag name and hence automatically returned by the standard
'getattribute' handler on subsequent calls.
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
            to _HTML40.Elements (see class '_HTML40.Element' definition below. E.g. 'h | ('abc', 'def')'
            creates a 'tagless' _HTML40.Element with two children, each a string.
        """
        return _HTML40.Element(tag=None, separateClose=False,
                               children=[other, ])

    def __ior__(self, other):
        """ This is a 'goalkeeper' function to prevent inadvertent corruption
            of the singleton instance of this class by constructions like
            'h |= "text"' which python might 'helpfully' convert to 'h = h | "text".
            We can't prevent explicit use of the latter form but we do our best!
        """
        raise HTML_Error("you're not allowed to modify the html generator like this.")


    class Element:
    
        """
Each possible HTML tag is defined  as a class which inherits this '_HTML40.Element' class. The name of the class
is the lower case tag string with a leading underscore added, e.g. '_h3' or '_br'.
When no attributes are associated with a tag, it can be expressed simply by e.g. 'h.br' or 'h.h4' (without
the quotes). Such references are 'corrected' (by HTML40.__getattr__ - see above) to return an instance
of the corresponding class.
When, however, attributes are required, it must be expressed as e.g. 'h.a(href='somewhere')'. Note that this
calls - not creates - an instance (see member function '__call__' below).
Differences of the 'rules of use' of various html tags are handled by the attribute 'AttrDicts'.
'AttrDicts' is a (often empty) tuple of dictionaries. keys of each dictionary represent valid attributes for
this _HTML40.Element. The corresponding values are (in the current implementation) booleans indicating whether a value
is associated with this attribute. False means that the value must not be supplied and will automatically be
derived from the attribute name. This will probably be changed in a later release, e.g. to use a function or
class as a value; this will make validation and manipulation of numeric values easier.
N.B. class Element must be declared within class _HTML40. This ensures that e.g. h._h4 where h is obtained by
e.g. 'h = _HTML40()' is a valid attribute reference (see __getattr__ above).
        """
        AttrDicts = (CoreAttrs,)
        okAttrs = None
        # 'separateClose' is True for most _HTML40.Elements but False for tags like 'br' which are
        # self-contatined and so don't require a separate closing tag.
        #
        separateClose = True
        dented = True
    
        def __init__(self, tag=None, separateClose=None, children=[], **sArgs):
            self.tag = tag
            self.sArgs = sArgs
            self.children = children[:]
            if separateClose is not None:  # use None for 'no overrule'
                self.separateClose = separateClose
    
        def __call__(self, **args):
            """
This functions makes it possible to derive tags with attributes by calling the tag with arguments,
e.g. 'h.img(src='pickie.jpg')'. Beware: this looks like a simple instance creation but isn't;
h.img already returns an instance so the bracketed construction gets routed to this function.
This construction can be used with empty brackets to force a copy operation as opposed to just
a name alias; i.e. 'mytable = h.table()' is kind of analogous to the following 'trick' for lists:
'my_list = precious_list[:]'.
            """
            if self.okAttrs is None:
                self.okAttrs = {}
                for d in self.AttrDicts:
                    self.okAttrs.update(d)
            sArgs = {}
            for key, val in args.items():
                key = key.lower().replace('_', '-')
                if not key in self.okAttrs.keys():
                    raise KeyError(key)
                if not self.okAttrs[key]:
                    sArgs[key] = key
                else:
                    # the following statement is currently essentially
                    # just a cheap and cheerful way to allow numeric
                    # values to be specified without quotes; room for improvement here!
                    sArgs[key] = str(val)
            return self.__class__(tag=self.tag, separateClose=self.separateClose,
                                  **sArgs)
    
        def _as_children(self, other):
            """
    Function '_as_children' is used internally by several public customization member function.
    Its purpose is to avoid unnecessary nesting of _HTML40.Elements when the child _HTML40.Element is tagless;
    in this case, its children can be taken on board by its parent.
            """
            return ((other is self or isinstance(other, _HTML40.Element)) and other.tag is None
                    and other.children or [other,])
    
        def __or__(self, other):
            """
    member function '__or__' ensures that code like e.g. 'h.h4 | <expression>', when converted to a string, results in
    '<h4>expression</h4>'. Similarly 'h.a(href="myLink") | "text"' becomes '<a href=myLink>text</a>'.
            """
            return self.__class__(tag=self.tag, separateClose=self.separateClose,
                                  children=self._as_children(other), **self.sArgs)
    
        __ror__ = __or__
        """ 
    The above definition ensures  that the '|' operator (see above) is symmetrical.
        """
    
        def __ior__(self, other):
            """
    Member function '__ior__' facilitates adding more child _HTML40.Elements to an already defined html _HTML40.Element, using
    the '|=' in-place operator
            """
            self.children.extend(self._as_children(self, other))
            return self
    
        def __and__(self, other):
            """
    This member function facilitates the use of & (usually a bit-wise 'and') to conditionally apply HTML operators, e.g.:
    '(this_user==selected_user)&h.em | "this text is highlighted when it relates to selected user"'.
            """
            return self if other else _html40
    
        __rand__ = __and__  # '&' operator is symmetrical
    
        def __add__(self, other):
            """
This custom function was introduced very late in the development in order to
facilitate the use of '+' instead of ',' for concatenating _HTML40.Elements. This will
drastically reduce the amount of 'unravelling' when stringifying complex nested HTML objects.
            """
            if not other:
                return self()  # just return clone of self!
    
            return _HTML40.Element(tag=None, separateClose=False,
                children=self._as_children(self)+self._as_children(other))
    
        def __radd__(self, other):
            """ note that our addition is not commutative!
            """
            return _HTML40.Element(tag=None, separateClose=False,
                children=self._as_children(other)+self._as_children(self))
    
        def __mul__(self, other):
            return sum([self for i in range(other)], None)
    
        __rmul__ = __mul__  # e.g. h.br*5 and 5*h.br are equivalent
    
        def __str__(self):
            """
__str__ is used to create a character representation of the _HTML40.Element. For example this is used by 'print'.
The character representation in our case is valid HTML.
            """
            if self.children is None:
                return ''
            if self.tag is None:  # special case for 'orphan' _HTML40.Elements
                s = ''
            else:
                s = "<%s" % self.tag
                for key, val in self.sArgs.items():
                    if val is not None:
                        s += ' %s="%s"' % (key.lower(), val)
                if not self.separateClose:
                    s += '/'
                s += '>'
            for child in unravel(self.children):
                s += str(child)
            if self.separateClose:
                s += '</%s>' % self.tag
                if self.tag not in ('span', 'a'):
                    s += '\n'
            return s
    
        def join(self, seq):
            """
Member function 'join' ensures that the construction
(e.g.) 'h.br.join(seq)' causes items of sequence to
be interspersed with blank lines when output. Items of the
sequence with the value 'None' are ignored completely
(but zero length strings are treated normally!)
            """
            return _HTML40.Element( tag=None, separateClose=False , children=(seq[:1] + [(self+term) for term in seq[1:]]))
    
# we now define all legal HTML4.0 tags, all wth a leading underscore ('_').
# Each of these represents a sub-class of _HTML40.Element, but these aren't
# intended for explicit use; constructions like e.g. 'h.h3' cause the class
# (same e.g.!) _HTML40._h3 to be initiated and given the tag value 'h3'.
#

    class _bdo(Element):
        pass

    class _cite(Element):
        pass

    class _code(Element):
        pass

    class _col(Element):
        pass

    class _colgroup(Element):
        pass

    class _dfn(Element):
        pass

    class _div(Element):
        pass

    class _fieldset(Element):
        pass

    class _i(Element):
        pass

    class _isindex(Element):
        pass

    class _kbd(Element):
        pass

    class _li(Element):
        pass

    class _map(Element):
        pass

    class _object(Element):
        pass

    class _ol(Element):
        pass

    class _optgroup(Element):
        pass

    class _option(Element):
        pass
    
    class _p(Element):
        pass
    
    class _param(Element):
        pass
    
    class _q(Element):
        pass
    
    class _s(Element):
        pass
    
    class _samp(Element):
        pass
    
    class _script(Element):
        pass
    
    class _select(Element):
        pass
    
    class _small(Element):
        pass
    
    class _span(Element):
        pass
    
    class _tbody(Element):
        pass
    
    class _tfoot(Element):
        pass
    
    class _tr(Element):
        pass
    
    class _tt(Element):
        pass
    
    class _u(Element):
        pass
    
    class _ul(Element):
        pass
    
    class _dd(Element):
        pass
    
    class _dl(Element):
        pass
    
    class _dt(Element):
        pass
    
    class _var(Element):
        pass
    
    class _b(Element):
        dented = False
    
    class _big(_b):
        pass
    
    class _center(_b):
        pass
    
    class _em(_b):
        pass
    
    class _small(_b):
        pass
    
    class _big(_b):
        pass
    
    class _center(_b):
        pass
    
    class _strike(_b):
        pass
    
    class _strong(_b):
        pass
    
    class _style(_b):
        pass
    
    class _sub(_b):
        pass
    
    class _sup(_b):
        pass
    
    class _h1(Element):
        AttrDicts = (CoreAttrs, IntrinsicEvents, {'align': 1})
    
    class _h2(_h1):
        pass
    
    class _h3(_h1):
        pass
    
    class _h4(_h1):
        pass
    
    class _h5(_h1):
        pass
    
    class _h6(_h1):
        pass
    
    class _a(Element):
        AttrDicts = (
        {'name': 1, 'charset': 1}, CoreAttrs, LinksAndAnchors, ImageMaps, TargetFrameInfo, TabbingNavigation)
    
    class _area(Element):
        AttrDicts = (
        {'name': 1, 'nohref': 0}, CoreAttrs, LinksAndAnchors, ImageMaps, TargetFrameInfo, TabbingNavigation)
    
    class _map(_h1):
        pass
    
    class _br(Element):
        separateClose = False
    
    class _base(Element):
        AttrDicts = (AnchorReference, TargetFrameInfo)
    
    class _blockquote(Element):
        AttrDicts = ({'cite': 1}, CoreAttrs)
    
    class _q(_blockquote):
        pass
    
    class _button(Element):
        AttrDicts = (CoreAttrs, {'name': 1, 'value': 1, 'type': 1, 'disabled': 0})
    
    class _caption(Element):
        AttrDicts = (CoreAttrs, {'align': 1})
    
    class _colgroup(Element):
        AttrDicts = (CoreAttrs, {'cite': 1, 'datetime': 1})
    
    class _col(_colgroup):
        separateClose = False
    
    class _Del(Element):
        AttrDicts = (CoreAttrs, CellHAlign, CellVAlign, {'span': 1, 'width': 1})
    
    class _ins(_Del):
        pass
    
    class _legend(Element):
        AttrDicts = (CoreAttrs, AccessKeys, {'align': 1})
    
    class _basefont(Element):
        AttrDicts = (FontModifiers, {'id': 1})
    
    class _font(Element):
        AttrDicts = (CoreAttrs, FontModifiers, I18n)
    
    class _form(Element):
        AttrDicts = (CoreAttrs, {'action': 1, 'method': 1, 'enctype': 1, 'accept-charset': 1, 'target': 1})
    
    class _frame(Element):
        separateClose = False
        AttrDicts = (CoreAttrs, {'longdesc': 1, 'name': 1, 'src': 1, 'frameborder': 1,
                                 'marginwidth': 1, 'marginheight': 1, 'noresize': 0, 'scrolling': 1})
    
    class _frameset(Element):
        AttrDicts = (FontModifiers, IntrinsicEvents, {'rows': 1, 'cols': 1, 'border': 1})
    
    class _head(Element):
        AttrDicts = (I18n, {'profile': 1})
    
    class _headset(Element):
        AttrDicts = (I18n, {'align': 1})
    
    class _hr(Element):
        separateClose = None
        AttrDicts = (CoreAttrs, IntrinsicEvents, {'align': 1, 'noshade': 0, 'size': 1, 'width': 1})
    
    class _html(Element):
        AttrDicts = (I18n,)
    
    class _title(_html):
        pass
    
    class _body(Element):
        AttrDicts = (CoreAttrs, {'background': 1, 'text': 1, 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1})
    
    class _iframe(Element):
        AttrDicts = (CoreAttrs, {'background': 1, 'text': 1,
                                 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1, 'src': 1,
                                 'width': 1, 'height': 1, 'allowfullscreen': 0, 'frameborder': 1})
    
    class _img(Element):
        separateClose = False
        AttrDicts = (CoreAttrs, VisualPresentation, AlternateText, {'src': 1, 'longdesc': 1, 'usemap': 1, 'ismap': 0})
    
    class _input(Element):
        separateClose = False
        AttrDicts = (CoreAttrs, TabbingNavigation, AccessKeys, AlternateText,
                     {'type': 1, 'name': 1, 'value': 1, 'checked': 0, 'disabled': 0,
                      'readonly': 0, 'size': 1, 'maxlength': 1, 'src': 1,
                      'usemap': 1, 'accept': 1, 'border': 1})
    
    class _label(Element):
        AttrDicts = (CoreAttrs, {'label-for': 1, 'for': 1})
    
    class _ul(Element):
        AttrDicts = (CoreAttrs, {'compact': 0})
    
    class _ol(Element):
        AttrDicts = (CoreAttrs, {'compact': 0, 'start': 1})
    
    class _li(Element):
        AttrDicts = (CoreAttrs, {'compact': 0, 'start': 1, 'value': 1, 'type': 1})
    
    class _link(Element):
        separateClose = False
        AttrDicts = (CoreAttrs, LinksAndAnchors, {'charset': 1, 'media': 1})
    
    class _meta(Element):
        separateClose = False
        AttrDicts = (I18n,
                     {'http-equiv': 1, 'name': 1, 'content': 1, 'scheme': 1})
    
    class _object(Element):
        AttrDicts = (TabbingNavigation, {'declare': 0, 'classid': 1, 'codebase': 1, 'data': 1, 'type': 1,
                                         'codetype': 1, 'archive': 1, 'standby': 1, 'height': 1, 'width': 1,
                                         'usemap': 1})
    
    class _select(Element):
        AttrDicts = (CoreAttrs, TabbingNavigation, {'name': 1, 'size': 1, 'multiple': 0, 'disabled': 0})
    
    class _optGroup(Element):
        AttrDicts = (CoreAttrs, {'disabled': 0, 'label': 1})
    
    class _option(Element):
        AttrDicts = (CoreAttrs, {'disabled': 0, 'label': 1, 'value': 1, 'selected': 0})
    
    class _param(Element):
        AttrDicts = ({'id': 1, 'name': 1, 'value': 1, 'valuetype': 1, 'type': 1},)
    
    class _pre(Element):
        AttrDicts = (CoreAttrs,)
    
    class _span(Element):
        AttrDicts = (CoreAttrs, {'align': 1})
    
    class _script(Element):
        AttrDicts = ({'charset': 1, 'type': 1, 'src': 1, 'defer': 0},)
    
    class _div(_script):
        pass
    
    class _style(Element):
        AttrDicts = (I18n, {'type': 1, 'media': 1, 'title': 1},)
    
    class _table(Element):
        AttrDicts = (CoreAttrs, BordersAndRules,
                     {'cellspacing': 1, 'cellpadding': 1, 'summary': 1, 'align': 1, 'bgcolor': 1, 'width': 1})
    
    class _tbody(Element):
        AttrDicts = (CoreAttrs, CellHAlign, CellVAlign)
    
    class _thead(_tbody):
        pass
    
    class _tfoot(_tbody):
        pass
    
    class _tr(_tbody):
        pass
    
    class _th(Element):
        dented = False
        AttrDicts = (CoreAttrs, CellHAlign, CellVAlign,
                     {'abbv': 1, 'axis': 1, 'headers': 1, 'scope': 1, 'rowspan': 1, 'colspan': 1,
                      'nowrap': 0, 'width': 1, 'height': 1, 'bgcolor': 1},)
    
    class _td(_th):
        pass
    
    class _textarea(Element):
        AttrDicts = (CoreAttrs, TabbingNavigation, AccessKeys,
                     {'name': 1, 'rows': 1, 'cols': 1, 'disabled': 0, 'readonly': 0},)
    

# create a singleton instance of the above-defined class. We retain the leading
# underscore in the class name even though our instance is designed for import.
# But it's not intended to be bulk imported as part of *, or to be used with
# this name, so this usage isn't wrong on ALL counts:
#
_html40 = _HTML40()


# I recommend that this is imported under a much shorter name, e.g.:
# 'from phileas import _html40 as h'. This usage will be assumed and
# 'h' referred to as 'the HTML generator' in this code.

def main():
    h = _html40  # the local equivalent of 'from phileas import _html40 as h'.
    print(
        "Content-type: text/html\n\n",
        h.html | (
            (h.p |
                """ This primitive web-page was produced using 'phileas' (and python of course!).
                """ + (h.em |'aha!')
            ) +
            (h.p |
             h.br * 2 +
             h.br + "abc " * 3 + 4 * 'xyz ' + '\n' +
             3 * h.br +
             """ If you're viewing this output in a browser, you can get to some (possibly not 100% up to date!)
             background info on 'phileas' by clicking """ +
             h.br + (h.a(href="http://larry.myerscough.nl/phileas_project/") | 'this text') +
             '.' +
             (False & h.em | 'plain ') + (True & h.em | "italic")
             ) +

            h.br.join(sys.path[:3]), h.br * 2,
            # let's check the creation of 'deliberately orphaned html _HTML40.Elements:
            h | ("\n[orphaned _HTML40.Elements' text should look just like any other text.]"
            + "... even when using the '+' operator!")

        )
    )


if __name__ == '__main__':
    main()
