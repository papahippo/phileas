#!/usr/bin/python

from .html import HTML
from .element import Element


GlobalAttrs = {  # allowd on any HTML5 element
    'accesskey': 1,    'class': 1,    'contenteditable': 1,    'contextmenu': 1,
# data-* .. how to handel this?
    'dir': 1,    'draggable': 1,    'dropzone': 1,   'hidden': 1,    'id': 1,    'lang': 1,
    'spellcheck': 1,    'style': 1,    'tabindex': 1,    'title': 1,    'translate': 1,}

WindowEventAttrs = {    'onafterprint': 1,    'onbeforeprint': 1,    'onbeforeunload': 1,
    'onerror': 1,    'onhashchange': 1,    'onload': 1,    'onmessage': 1,    'onoffline': 1,
    'ononline': 1,    'onpagehide': 1,    'onpageshow': 1,    'onpopstate': 1,    'onresize': 1,
    'onstorage': 1,    'onunload': 1,}
# ?? I18n = {'lang': 1, 'dir': 1}

FormEventAttrs = {'onblur': 1,    'onchange': 1,    'oncontextmenu': 1,    'onfocus': 1,    'oninput': 1,
                  'oninvalid': 1, 'onreset': 1,    'onsearch': 1,    'onselect': 1,    'onsubmit': 1,}
KeyboardEventAttrs = { 'onkeydown': 1,    'onkeypress': 1,    'onkeyup': 1, }

MouseEventAttrs = {'onclick': 1,    'ondblclick': 1,    'onmousedown': 1,    'onmousemove': 1,
                    'onmouseout': 1,    'onmouseover': 1,    'onmouseup 	': 1,    'onwheel': 1,}

DragEventAttrs = {    'ondrag': 1,    'ondragend': 1,    'ondragenter': 1,    'ondragleave': 1,
                        'ondragover': 1,    'ondragstart': 1,    'ondrop 	': 1,    'onscroll': 1,}

ClipboardEventAttrs = {    'oncopy': 1,    'oncut': 1,    'onpaste': 1,}

MediaEventAttrs = { 'onabort': 1,    'oncanplay': 1,    'oncanplaythrough': 1,    'oncuechange': 1,
                    'ondurationchange': 1,    'onemptied': 1,    'onended 	': 1,    'onerror': 1,
                    'onloadeddata': 1,    'onloadedmetadata': 1,    'onloadstart': 1,    'onpause': 1,
                    'onplay': 1,   'onplaying': 1,    'onprogress 	': 1,    'onratechange': 1,
                    'onseeked': 1,    'onseeking': 1,    'onstalled': 1,    'onsuspend': 1,
                    'ontimeupdate': 1,    'onvolumechange': 1,    'onwaiting': 1,}

MiscEventAttrs = {    'onshow': 1,    'ontoggle': 1,}

EventAttrs = {**WindowEventAttrs, **FormEventAttrs, **KeyboardEventAttrs, **MouseEventAttrs,
              **DragEventAttrs, **ClipboardEventAttrs, **MediaEventAttrs, **MiscEventAttrs}

GlobalAndEventAttrs  = {**GlobalAttrs, **EventAttrs}

LinksAndAnchorAttrs = {'href': 1, 'hreflang': 1, 'type': 1, 'rel': 1, 'download': 1}

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

BordersAndRules = {'frame': 1, 'rules': 1, 'border': 1}

class HTML5_Element(Element):
    attr_dict = GlobalAndEventAttrs


class HTML5(HTML):
    """
This class is called HTML5 because its members correspond to HTML5 tags.
    """
    # we now define all legal HTML5 tags, all with the first letter capitalized.
    # Each of these represents a sub-class of HTML5_Element, but these aren't
    # intended for explicit use; constructions like e.g. 'h.h3' cause the class
    # (same e.g.) HTML40.H3 to be initiated and given the tag value 'h3'.


    class A(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs, LinksAndAnchorAttrs)

    class Abbr(HTML5_Element):
        pass

    class Area(HTML5_Element):
# {'name': 1, 'nohref': 0}, GlobalAttrs, LinksAndAnchors, ImageMaps, TargetFrameInfo, TabbingNavigation)
        attr_dict = (GlobalAndEventAttrs, LinksAndAnchorAttrs, ImageMaps, AlternateText,
                    {'coords': 1, 'type': 1, })

    class Article(HTML5_Element):
        pass

    class Aside(HTML5_Element):
        pass

    class Audio(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'autoplay': 1, 'controls':1, 'loop':1, 'muted':1,  'preload':1, 'src':1, })

    class B(HTML5_Element):
        dented = False

    class Base(HTML5_Element):
        attr_dict = (GlobalAttrs,
                     {'href': 1, 'target':1, })

    class Bdi(HTML5_Element):
        pass

    class Blockquote(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
        {'cite': 1})

    class Body(HTML5_Element):
        pass

    class Br(HTML5_Element):
        separate_close = False

    class Button(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'autotfocus': 1, 'disabled':1, 'form':1, 'formaction':1, 'formenctype':1, 'formmethod': 1,
                     'formnovalidate': 1, 'formtarget': 1, 'name': 1, 'type': 1, 'value': 1, })

    class Canvas(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'height': 1, 'width': 1, })

    class Caption(HTML5_Element):
        pass


    class Cite(HTML5_Element):
        pass

    class Code(HTML5_Element):
        attr_dict = {}

    class Col(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'span': 1, })

    class Colgroup(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'span': 1, })

    class Data(HTML5_Element):  # N.B. limited browser suupport!
        attr_dict = (GlobalAttrs,
                     {'value':1, })

    class Datalist(HTML5_Element):  # N.B. perhaps needs devloper attention!?
        pass

    class Dd(HTML5_Element):
        pass

    class Del(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'cite':1, 'datetime':1, })

    class Details(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'open':1, })

    class Dfn(HTML5_Element):
        pass

    class Dialog(HTML5_Element): # N>B> not supported on IE
        attr_dict = (GlobalAndEventAttrs,
                     {'open':1, })

    class Div(HTML5_Element):
        pass

    class Dl(HTML5_Element):
        pass

    class Dt(HTML5_Element):
        pass

    class Em(HTML5_Element):
        dented = False

    class Embed(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'height': 1, 'src': 1, 'type': 1, 'width': 1, })

    class Fieldset(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'disabled': 1, 'form': 1, 'name': 1, })

    class Figcaption(HTML5_Element):
        dented = False

    class Figure(HTML5_Element):
        dented = False

    class Font(HTML5_Element):
        pass

    class Footer(HTML5_Element):
        pass

    class Form(HTML5_Element):
        attr_dict = (GlobalAttrs,
                    {'accept-charset': 1, 'action': 1, 'autocomplete': 1, 'enctype': 1,
                     'method': 1, 'name':1, 'novalidate':1, 'target': 1,})

    class H1(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'align': 1})

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

    class Head(HTML5_Element):
        pass

    class Header(HTML5_Element):
        pass

    class Hr(HTML5_Element):
        separate_close = False

    class Html(HTML5_Element):
        attr_dict = (GlobalAttrs,
                     {'xmlns': 1,})

    class I(HTML5_Element):
        pass

    class Iframe(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'height':1, 'name':1, 'src':1, 'width': 1,})

    class Img(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'alt':1, 'crossorigin':1, 'height':1, 'ismap':1, 'longdesc':1, 'sizes': 1,
                     'src': 1, 'srcset':1, 'src':1, 'usemap': 1,'vspace': 1,'width': 1,})

    class Input(HTML5_Element):
        separate_close = False
        attr_dict = (GlobalAndEventAttrs,
                     {'accept':1, 'alt':1, 'autocomplete':1, 'autofocus':1,
                     'checked':1, 'dirname': 1, 'disabled': 1, 'form':1,
                     'formaction':1, 'formenctype': 1,'formmethod': 1,'formnovalidate': 1, 'formtarget': 1,
                     'height': 1, 'list': 1, 'max': 1, 'maxlength': 1, 'min': 1, 'multiple': 1, 'name': 1,
                     'pattern': 1, 'placeholder': 1, 'readonly': 1, 'required': 1, 'size': 1,  'src': 1,
                     'step': 1, 'type': 1, 'value': 1, 'width': 1, })

    class Ins(Del):
        pass

    class Kbd(HTML5_Element):
        pass

    class Label(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'for': 1, 'form': 1})

    class Legend(HTML5_Element):
        pass

    class Li(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'value': 1,})

    class Link(HTML5_Element):
        separate_close = False
        AttrDicts = (GlobalAndEventAttrs,
                     {'corssorigin':1, 'href':1, 'hreflang':1, 'media':1,
                     'rel':1, 'sizes': 1,  'target': 1, 'type': 1, })

    class Main(HTML5_Element):
        pass

    class Map(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'data': 1, 'form': 1, 'height': 1, 'name': 1,
                      'type': 1, 'width': 1, })

    class Mark(HTML5_Element):
        pass

    class Menu(HTML5_Element):
        pass

    class Menuitem(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'checked': 1, 'command': 1, 'default': 1, 'disabled': 1,
                      'icon': 1, 'label': 1, 'radiogroup': 1, 'type': 1, })

    class Meta(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'charset': 1, 'content': 1, 'http-equiv': 1, 'name': 1,
                      'scheme': 1, })

    class Menuitem(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'form': 1, 'high': 1, 'low': 1, 'max': 1, 'min': 1,
                      'optimum': 1, 'value': 1, })

    class Nav(HTML5_Element):
        pass

    class Noscript(HTML5_Element):
        AttrDicts = (GlobalAttrs,)

    class Object(HTML5_Element):
         AttrDicts = (GlobalAndEventAttrs,
                     {'data': 1, 'form': 1, 'height': 1, 'name': 1,
                      'type': 1, 'usemap': 1, 'width': 1, })

    class Ol(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'reversed': 1, 'start': 1, 'type': 1, })

    class Optgroup(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'disabled': 1, 'name': 1, })

    class Option(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'disabled': 1, 'label': 1, 'selected': 1, 'value': 1, })


    class P(HTML5_Element):
        pass

    class Param(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'name': 1, 'value': 1, })

    class Picture(HTML5_Element):
        pass

    class Pre(HTML5_Element):
        pass

    class Progress(HTML5_Element):
        attr_dict = (GlobalAndEventAttrs,
                     {'max': 1, 'value': 1, })

    class Q(HTML5_Element):
        pass

    class Rp(HTML5_Element):
        pass

    class Rt(HTML5_Element):
        pass

    class Ruby(HTML5_Element):
        pass

    class S(HTML5_Element):
        pass

    class Samp(HTML5_Element):
        pass

    class Script(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'async': 1, 'charset': 1, 'defer': 1, 'src': 1, 'type': 1, })

    class Section(HTML5_Element):
        pass

    class Select(HTML5_Element):
        AttrDicts = (GlobalAndEventAttrs,
                     {'autofocus': 1, 'disabled': 1, 'form': 1, 'multiple': 1,
                      'name': 1, 'required': 1, 'size': 1, })

    class Small(HTML5_Element):
        pass

# from here on, not yet fully filled in!

    class Source(HTML5_Element):
        pass

    class Span(HTML5_Element):
        pass

    class Strike(HTML5_Element):
        pass

    class Strong(HTML5_Element):
        pass

    class Style(HTML5_Element):
        pass

    class Sub(HTML5_Element):
        pass

    class Summary(HTML5_Element):
        pass

    class Sup(HTML5_Element):
        pass

    class Strong(HTML5_Element):
        pass

    class Svg(HTML5_Element):
        pass

    class Table(HTML5_Element):
        pass

    class Tbody(HTML5_Element):
        pass

    class Td(HTML5_Element):
        pass

    class Template(HTML5_Element):
        pass

    class Textarea(HTML5_Element):
        pass

    class Tfoot(HTML5_Element):
        pass

    class Th(HTML5_Element):
        pass

    class Thead(HTML5_Element):
        pass

    class Time(HTML5_Element):
        pass

    class Title(HTML5_Element):
        pass

    class Tr(HTML5_Element):
        pass

    class Track(HTML5_Element):
        pass

    class Tt(HTML5_Element):
        pass

    class U(HTML5_Element):
        pass

    class Ul(HTML5_Element):
        pass

    class Var(HTML5_Element):
        pass

    class Video(HTML5_Element):
        pass

    class Wbr(HTML5_Element):
        pass

