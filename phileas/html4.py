#!/usr/bin/python

from .html_ import HTML
from .element import Element


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


class HTML4_Element(Element):
    attr_dict = (CoreAttrs,)


class HTML4(HTML):
    """
This class is called _HTML40 because its members correspond to HTML 4.0 tags.
    """
    # we now define all legal HTML4.0 tags, all with the first letter captialized.
    # Each of these represents a sub-class of Element40, but these aren't
    # intended for explicit use; constructions like e.g. 'h.h3' cause the class
    # (same e.g.) HTML40.H3 to be initiated and given the tag value 'h3'.
    #

    class Bdo(HTML4_Element):
        pass

    class Cite(HTML4_Element):
        pass

    class Code(HTML4_Element):
        pass

    class Col(HTML4_Element):
        pass

    class Colgroup(HTML4_Element):
        pass

    class Dfn(HTML4_Element):
        pass

    class Fieldset(HTML4_Element):
        pass

    class I(HTML4_Element):
        pass

    class Isindex(HTML4_Element):
        pass

    class Kbd(HTML4_Element):
        pass

    class Map(HTML4_Element):
        pass

    class Optgroup(HTML4_Element):
        pass

    class P(HTML4_Element):
        pass

    class Q(HTML4_Element):
        pass

    class S(HTML4_Element):
        pass

    class Samp(HTML4_Element):
        pass

    class Tt(HTML4_Element):
        pass

    class U(HTML4_Element):
        pass

    class Dd(HTML4_Element):
        pass

    class Dl(HTML4_Element):
        pass

    class Dt(HTML4_Element):
        pass

    class Var(HTML4_Element):
        pass

    class B(HTML4_Element):
        dented = False

    class Strike(HTML4_Element):
        dented = False

    class Big(HTML4_Element):
        dented = False

    class Center(HTML4_Element):
        dented = False

    class Em(HTML4_Element):
        dented = False

    class Small(HTML4_Element):
        dented = False

    class Strong(HTML4_Element):
        dented = False

    class Sub(HTML4_Element):
        dented = False

    class Sup(HTML4_Element):
        dented = False

    class H1(HTML4_Element):
        attr_dict = (CoreAttrs, IntrinsicEvents, {'align': 1})

    class H2(H1):
        pass

    class H3(H1):
        pass

    class H4(H1):
        pass

    class H5(H1):
        pass

    class H6(H1):
        pass

    class A(HTML4_Element):
        attr_dict = (
            {'name': 1, 'charset': 1}, CoreAttrs, LinksAndAnchors, ImageMaps,
            TargetFrameInfo, TabbingNavigation)

    class Area(HTML4_Element):
        attr_dict = (
            {'name': 1, 'nohref': 0}, CoreAttrs, LinksAndAnchors, ImageMaps,
            TargetFrameInfo, TabbingNavigation)

    class Map(H1):
        pass

    class Br(HTML4_Element):
        separate_close = False

    class Base(HTML4_Element):
        attr_dict = (AnchorReference, TargetFrameInfo)

    class Blockquote(HTML4_Element):
        attr_dict = ({'cite': 1}, CoreAttrs)

    class Q(Blockquote):
        pass

    class Button(HTML4_Element):
        attr_dict = (CoreAttrs, {'name': 1, 'value': 1, 'type': 1, 'disabled': 0})

    class Caption(HTML4_Element):
        attr_dict = (CoreAttrs, {'align': 1})

    class Colgroup(HTML4_Element):
        attr_dict = (CoreAttrs, {'cite': 1, 'datetime': 1})

    class Col(Colgroup):
        separate_close = False

    class Del(HTML4_Element):
        attr_dict = (CoreAttrs, CellHAlign, CellVAlign, {'span': 1, 'width': 1})

    class Ins(Del):
        pass

    class Legend(HTML4_Element):
        attr_dict = (CoreAttrs, AccessKeys, {'align': 1})

    class Basefont(HTML4_Element):
        attr_dict = (FontModifiers, {'id': 1})

    class Font(HTML4_Element):
        attr_dict = (CoreAttrs, FontModifiers, I18n)

    class Form(HTML4_Element):
        attr_dict = (CoreAttrs, {'action': 1, 'method': 1, 'enctype': 1, 'accept-charset': 1, 'target': 1})

    class Frame(HTML4_Element):
        separate_close = False
        attr_dict = (CoreAttrs, {'longdesc': 1, 'name': 1, 'src': 1, 'frameborder': 1,
                                 'marginwidth': 1, 'marginheight': 1, 'noresize': 0, 'scrolling': 1})

    class Frameset(HTML4_Element):
        attr_dict = (FontModifiers, IntrinsicEvents, {'rows': 1, 'cols': 1, 'border': 1})

    class Head(HTML4_Element):
        attr_dict = (I18n, {'profile': 1})

    class Headset(HTML4_Element):
        attr_dict = (I18n, {'align': 1})

    class Hr(HTML4_Element):
        separate_close = None
        attr_dict = (CoreAttrs, IntrinsicEvents, {'align': 1, 'noshade': 0, 'size': 1, 'width': 1})

    class Html(HTML4_Element):
        attr_dict = (I18n,)

    class Title(Html):
        pass

    class Body(HTML4_Element):
        attr_dict = (CoreAttrs, {'background': 1, 'text': 1, 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1})

    class Iframe(HTML4_Element):
        attr_dict = (CoreAttrs, {'background': 1, 'text': 1,
                                 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1, 'src': 1,
                                 'width': 1, 'height': 1, 'allowfullscreen': 0, 'frameborder': 1})

    class Img(HTML4_Element):
        separate_close = False
        attr_dict = (CoreAttrs, VisualPresentation, AlternateText, {'src': 1, 'longdesc': 1, 'usemap': 1, 'ismap': 0})

    class Input(HTML4_Element):
        separate_close = False
        attr_dict = (CoreAttrs, TabbingNavigation, AccessKeys, AlternateText,
                     {'type': 1, 'name': 1, 'value': 1, 'checked': 0, 'disabled': 0,
                      'readonly': 0, 'size': 1, 'maxlength': 1, 'src': 1,
                      'usemap': 1, 'accept': 1, 'border': 1})

    class Label(HTML4_Element):
        attr_dict = (CoreAttrs, {'label-for': 1, 'for': 1})

    class Ul(HTML4_Element):
        attr_dict = (CoreAttrs, {'compact': 0})

    class Ol(HTML4_Element):
        attr_dict = (CoreAttrs, {'compact': 0, 'start': 1})

    class Li(HTML4_Element):
        attr_dict = (CoreAttrs, {'compact': 0, 'start': 1, 'value': 1, 'type': 1})

    class Link(HTML4_Element):
        separate_close = False
        attr_dict = (CoreAttrs, LinksAndAnchors, {'charset': 1, 'media': 1})

    class Meta(HTML4_Element):
        separate_close = False
        attr_dict = (I18n,
                     {'http-equiv': 1, 'name': 1, 'content': 1, 'scheme': 1})

    class Object(HTML4_Element):
        attr_dict = (TabbingNavigation, {'declare': 0, 'classid': 1, 'codebase': 1, 'data': 1, 'type': 1,
                                         'codetype': 1, 'archive': 1, 'standby': 1, 'height': 1, 'width': 1,
                                         'usemap': 1})

    class Select(HTML4_Element):
        attr_dict = (CoreAttrs, TabbingNavigation, {'name': 1, 'size': 1, 'multiple': 0, 'disabled': 0})

    class OptGroup(HTML4_Element):
        attr_dict = (CoreAttrs, {'disabled': 0, 'label': 1})

    class Option(HTML4_Element):
        attr_dict = (CoreAttrs, {'disabled': 0, 'label': 1, 'value': 1, 'selected': 0})

    class Param(HTML4_Element):
        attr_dict = ({'id': 1, 'name': 1, 'value': 1, 'valuetype': 1, 'type': 1},)

    class Pre(HTML4_Element):
        attr_dict = (CoreAttrs,)

    class Span(HTML4_Element):
        attr_dict = (CoreAttrs, {'align': 1})

    class Script(HTML4_Element):
        attr_dict = ({'charset': 1, 'type': 1, 'src': 1, 'defer': 0},)

    class Div(Script):
        pass

    class Style(HTML4_Element):
        attr_dict = (I18n, {'type': 1, 'media': 1, 'title': 1},)

    class Table(HTML4_Element):
        attr_dict = (CoreAttrs, BordersAndRules,
                     {'cellspacing': 1, 'cellpadding': 1, 'summary': 1, 'align': 1, 'bgcolor': 1, 'width': 1})

    class Tbody(HTML4_Element):
        attr_dict = (CoreAttrs, CellHAlign, CellVAlign)

    class Thead(Tbody):
        pass

    class Tfoot(Tbody):
        pass

    class Tr(Tbody):
        pass

    class Th(HTML4_Element):
        dented = False
        attr_dict = (CoreAttrs, CellHAlign, CellVAlign,
                     {'abbv': 1, 'axis': 1, 'headers': 1, 'scope': 1, 'rowspan': 1, 'colspan': 1,
                      'nowrap': 0, 'width': 1, 'height': 1, 'bgcolor': 1},)

    class Td(Th):
        pass

    class Textarea(HTML4_Element):
        attr_dict = (CoreAttrs, TabbingNavigation, AccessKeys,
                     {'name': 1, 'rows': 1, 'cols': 1, 'disabled': 0, 'readonly': 0},)



