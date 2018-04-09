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

from html import HTML
from element import Element


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

class Element40(Element):
    AttrDicts = (CoreAttrs,)


class HTML40(HTML):
    """
This class is called _HTML40 because its members correspond to HTML 4.0 tags.
    """
    # we now define all legal HTML4.0 tags, all wth a leading underscore ('_').
    # Each of these represents a sub-class of Element40, but these aren't
    # intended for explicit use; constructions like e.g. 'h.h3' cause the class
    # (same e.g.!) _HTML40._h3 to be initiated and given the tag value 'h3'.
    #

    class _bdo(Element40):
        pass

    class _cite(Element40):
        pass

    class _code(Element40):
        pass

    class _col(Element40):
        pass

    class _colgroup(Element40):
        pass

    class _dfn(Element40):
        pass

    class _div(Element40):
        pass

    class _fieldset(Element40):
        pass

    class _i(Element40):
        pass

    class _isindex(Element40):
        pass

    class _kbd(Element40):
        pass

    class _li(Element40):
        pass

    class _map(Element40):
        pass

    class _object(Element40):
        pass

    class _ol(Element40):
        pass

    class _optgroup(Element40):
        pass

    class _option(Element40):
        pass

    class _p(Element40):
        pass

    class _param(Element40):
        pass

    class _q(Element40):
        pass

    class _s(Element40):
        pass

    class _samp(Element40):
        pass

    class _script(Element40):
        pass

    class _select(Element40):
        pass

    class _small(Element40):
        pass

    class _span(Element40):
        pass

    class _tbody(Element40):
        pass

    class _tfoot(Element40):
        pass

    class _tr(Element40):
        pass

    class _tt(Element40):
        pass

    class _u(Element40):
        pass

    class _ul(Element40):
        pass

    class _dd(Element40):
        pass

    class _dl(Element40):
        pass

    class _dt(Element40):
        pass

    class _var(Element40):
        pass

    class _b(Element40):
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

    class _h1(Element40):
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

    class _a(Element40):
        AttrDicts = (
            {'name': 1, 'charset': 1}, CoreAttrs, LinksAndAnchors, ImageMaps, TargetFrameInfo, TabbingNavigation)

    class _area(Element40):
        AttrDicts = (
            {'name': 1, 'nohref': 0}, CoreAttrs, LinksAndAnchors, ImageMaps, TargetFrameInfo, TabbingNavigation)

    class _map(_h1):
        pass

    class _br(Element40):
        separateClose = False

    class _base(Element40):
        AttrDicts = (AnchorReference, TargetFrameInfo)

    class _blockquote(Element40):
        AttrDicts = ({'cite': 1}, CoreAttrs)

    class _q(_blockquote):
        pass

    class _button(Element40):
        AttrDicts = (CoreAttrs, {'name': 1, 'value': 1, 'type': 1, 'disabled': 0})

    class _caption(Element40):
        AttrDicts = (CoreAttrs, {'align': 1})

    class _colgroup(Element40):
        AttrDicts = (CoreAttrs, {'cite': 1, 'datetime': 1})

    class _col(_colgroup):
        separateClose = False

    class _Del(Element40):
        AttrDicts = (CoreAttrs, CellHAlign, CellVAlign, {'span': 1, 'width': 1})

    class _ins(_Del):
        pass

    class _legend(Element40):
        AttrDicts = (CoreAttrs, AccessKeys, {'align': 1})

    class _basefont(Element40):
        AttrDicts = (FontModifiers, {'id': 1})

    class _font(Element40):
        AttrDicts = (CoreAttrs, FontModifiers, I18n)

    class _form(Element40):
        AttrDicts = (CoreAttrs, {'action': 1, 'method': 1, 'enctype': 1, 'accept-charset': 1, 'target': 1})

    class _frame(Element40):
        separateClose = False
        AttrDicts = (CoreAttrs, {'longdesc': 1, 'name': 1, 'src': 1, 'frameborder': 1,
                                 'marginwidth': 1, 'marginheight': 1, 'noresize': 0, 'scrolling': 1})

    class _frameset(Element40):
        AttrDicts = (FontModifiers, IntrinsicEvents, {'rows': 1, 'cols': 1, 'border': 1})

    class _head(Element40):
        AttrDicts = (I18n, {'profile': 1})

    class _headset(Element40):
        AttrDicts = (I18n, {'align': 1})

    class _hr(Element40):
        separateClose = None
        AttrDicts = (CoreAttrs, IntrinsicEvents, {'align': 1, 'noshade': 0, 'size': 1, 'width': 1})

    class _html(Element40):
        AttrDicts = (I18n,)

    class _title(_html):
        pass

    class _body(Element40):
        AttrDicts = (CoreAttrs, {'background': 1, 'text': 1, 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1})

    class _iframe(Element40):
        AttrDicts = (CoreAttrs, {'background': 1, 'text': 1,
                                 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1, 'src': 1,
                                 'width': 1, 'height': 1, 'allowfullscreen': 0, 'frameborder': 1})

    class _img(Element40):
        separateClose = False
        AttrDicts = (CoreAttrs, VisualPresentation, AlternateText, {'src': 1, 'longdesc': 1, 'usemap': 1, 'ismap': 0})

    class _input(Element40):
        separateClose = False
        AttrDicts = (CoreAttrs, TabbingNavigation, AccessKeys, AlternateText,
                     {'type': 1, 'name': 1, 'value': 1, 'checked': 0, 'disabled': 0,
                      'readonly': 0, 'size': 1, 'maxlength': 1, 'src': 1,
                      'usemap': 1, 'accept': 1, 'border': 1})

    class _label(Element40):
        AttrDicts = (CoreAttrs, {'label-for': 1, 'for': 1})

    class _ul(Element40):
        AttrDicts = (CoreAttrs, {'compact': 0})

    class _ol(Element40):
        AttrDicts = (CoreAttrs, {'compact': 0, 'start': 1})

    class _li(Element40):
        AttrDicts = (CoreAttrs, {'compact': 0, 'start': 1, 'value': 1, 'type': 1})

    class _link(Element40):
        separateClose = False
        AttrDicts = (CoreAttrs, LinksAndAnchors, {'charset': 1, 'media': 1})

    class _meta(Element40):
        separateClose = False
        AttrDicts = (I18n,
                     {'http-equiv': 1, 'name': 1, 'content': 1, 'scheme': 1})

    class _object(Element40):
        AttrDicts = (TabbingNavigation, {'declare': 0, 'classid': 1, 'codebase': 1, 'data': 1, 'type': 1,
                                         'codetype': 1, 'archive': 1, 'standby': 1, 'height': 1, 'width': 1,
                                         'usemap': 1})

    class _select(Element40):
        AttrDicts = (CoreAttrs, TabbingNavigation, {'name': 1, 'size': 1, 'multiple': 0, 'disabled': 0})

    class _optGroup(Element40):
        AttrDicts = (CoreAttrs, {'disabled': 0, 'label': 1})

    class _option(Element40):
        AttrDicts = (CoreAttrs, {'disabled': 0, 'label': 1, 'value': 1, 'selected': 0})

    class _param(Element40):
        AttrDicts = ({'id': 1, 'name': 1, 'value': 1, 'valuetype': 1, 'type': 1},)

    class _pre(Element40):
        AttrDicts = (CoreAttrs,)

    class _span(Element40):
        AttrDicts = (CoreAttrs, {'align': 1})

    class _script(Element40):
        AttrDicts = ({'charset': 1, 'type': 1, 'src': 1, 'defer': 0},)

    class _div(_script):
        pass

    class _style(Element40):
        AttrDicts = (I18n, {'type': 1, 'media': 1, 'title': 1},)

    class _table(Element40):
        AttrDicts = (CoreAttrs, BordersAndRules,
                     {'cellspacing': 1, 'cellpadding': 1, 'summary': 1, 'align': 1, 'bgcolor': 1, 'width': 1})

    class _tbody(Element40):
        AttrDicts = (CoreAttrs, CellHAlign, CellVAlign)

    class _thead(_tbody):
        pass

    class _tfoot(_tbody):
        pass

    class _tr(_tbody):
        pass

    class _th(Element40):
        dented = False
        AttrDicts = (CoreAttrs, CellHAlign, CellVAlign,
                     {'abbv': 1, 'axis': 1, 'headers': 1, 'scope': 1, 'rowspan': 1, 'colspan': 1,
                      'nowrap': 0, 'width': 1, 'height': 1, 'bgcolor': 1},)

    class _td(_th):
        pass

    class _textarea(Element40):
        AttrDicts = (CoreAttrs, TabbingNavigation, AccessKeys,
                     {'name': 1, 'rows': 1, 'cols': 1, 'disabled': 0, 'readonly': 0},)



# I recommend that this is imported under a much shorter name, e.g.:
# 'from phileas import html40 as h'. This usage will be assumed and
# 'h' referred to as 'the HTML generator' in this code.

def main():
    h = HTML40()  # the local equivalent of 'from phileas import html40 as h'.
    print(
        "Content-type: text/html\n\n",
        h.html | (
            (h.p |
             """ This primitive web-page was produced using 'phileas' (and python of course!).
             """ + (h.em | 'aha!')
             ) +
            (h.p |
             h.br * 2 +
             h.br + "abc " * 3 + 4 * 'xyz ' + '\n' +
             3 * h.br +
             """ If you're viewing this output in a browser, you can get to some (possibly not
              100% up to date!) background info on 'phileas' by clicking """ +
             h.br + (h.a(href="http://larry.myerscough.nl/phileas_project/") | 'this text') +
             '.' +
             (False & h.em | 'plain ') + (True & h.em | "italic")
             ) +

            h.br.join(sys.path[:3]), h.br * 2,
            # let's check the creation of 'deliberately orphaned html Elements:
            h | ("\n[orphaned Elements' text should look just like any other text.]"
                 + "... even when using the '+' operator!")

        )
    )


if __name__ == '__main__':
    main()
