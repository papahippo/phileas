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

LinksAndAnchorAttrs = {'href': 1, 'hreflang': 1, 'type': 1, 'rel': 1, 'rev': 1}

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

class Element50(Element):
    attr_dict = (GlobalAttrs,)


class HTML50(HTML):
    """
This class is called _HTML40 because its members correspond to HTML 4.0 tags.
    """
    # we now define all legal HTML4.0 tags, all wth a leading underscore ('_').
    # Each of these represents a sub-class of Element40, but these aren't
    # intended for explicit use; constructions like e.g. 'h.h3' cause the class
    # (same e.g.!) _HTML40._h3 to be initiated and given the tag value 'h3'.
    #

    class _a(Element50):
        attr_dict = {**GlobalAttrs, **EventAttrs, **LinksAndAnchorAttrs, }

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
        AttrDicts = (GlobalAttrs, IntrinsicEvents, {'align': 1})

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

    class _area(Element40):
        AttrDicts = (
            {'name': 1, 'nohref': 0}, GlobalAttrs, LinksAndAnchors, ImageMaps, TargetFrameInfo, TabbingNavigation)

    class _map(_h1):
        pass

    class _br(Element40):
        separate_close = False

    class _base(Element40):
        AttrDicts = (AnchorReference, TargetFrameInfo)

    class _blockquote(Element40):
        AttrDicts = ({'cite': 1}, GlobalAttrs)

    class _q(_blockquote):
        pass

    class _button(Element40):
        AttrDicts = (GlobalAttrs, {'name': 1, 'value': 1, 'type': 1, 'disabled': 0})

    class _caption(Element40):
        AttrDicts = (GlobalAttrs, {'align': 1})

    class _colgroup(Element40):
        AttrDicts = (GlobalAttrs, {'cite': 1, 'datetime': 1})

    class _col(_colgroup):
        separate_close = False

    class _Del(Element40):
        AttrDicts = (GlobalAttrs, CellHAlign, CellVAlign, {'span': 1, 'width': 1})

    class _ins(_Del):
        pass

    class _legend(Element40):
        AttrDicts = (GlobalAttrs, AccessKeys, {'align': 1})

    class _basefont(Element40):
        AttrDicts = (FontModifiers, {'id': 1})

    class _font(Element40):
        AttrDicts = (GlobalAttrs, FontModifiers, I18n)

    class _form(Element40):
        AttrDicts = (GlobalAttrs, {'action': 1, 'method': 1, 'enctype': 1, 'accept-charset': 1, 'target': 1})

    class _frame(Element40):
        separate_close = False
        AttrDicts = (GlobalAttrs, {'longdesc': 1, 'name': 1, 'src': 1, 'frameborder': 1,
                                 'marginwidth': 1, 'marginheight': 1, 'noresize': 0, 'scrolling': 1})

    class _frameset(Element40):
        AttrDicts = (FontModifiers, IntrinsicEvents, {'rows': 1, 'cols': 1, 'border': 1})

    class _head(Element40):
        AttrDicts = (I18n, {'profile': 1})

    class _headset(Element40):
        AttrDicts = (I18n, {'align': 1})

    class _hr(Element40):
        separate_close = None
        AttrDicts = (GlobalAttrs, IntrinsicEvents, {'align': 1, 'noshade': 0, 'size': 1, 'width': 1})

    class _html(Element40):
        AttrDicts = (I18n,)

    class _title(_html):
        pass

    class _body(Element40):
        AttrDicts = (GlobalAttrs, {'background': 1, 'text': 1, 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1})

    class _iframe(Element40):
        AttrDicts = (GlobalAttrs, {'background': 1, 'text': 1,
                                 'link': 1, 'vlink': 1, 'alink': 1, 'bgcolor': 1, 'src': 1,
                                 'width': 1, 'height': 1, 'allowfullscreen': 0, 'frameborder': 1})

    class _img(Element40):
        separate_close = False
        AttrDicts = (GlobalAttrs, VisualPresentation, AlternateText, {'src': 1, 'longdesc': 1, 'usemap': 1, 'ismap': 0})

    class _input(Element40):
        separate_close = False
        AttrDicts = (GlobalAttrs, TabbingNavigation, AccessKeys, AlternateText,
                     {'type': 1, 'name': 1, 'value': 1, 'checked': 0, 'disabled': 0,
                      'readonly': 0, 'size': 1, 'maxlength': 1, 'src': 1,
                      'usemap': 1, 'accept': 1, 'border': 1})

    class _label(Element40):
        AttrDicts = (GlobalAttrs, {'label-for': 1, 'for': 1})

    class _ul(Element40):
        AttrDicts = (GlobalAttrs, {'compact': 0})

    class _ol(Element40):
        AttrDicts = (GlobalAttrs, {'compact': 0, 'start': 1})

    class _li(Element40):
        AttrDicts = (GlobalAttrs, {'compact': 0, 'start': 1, 'value': 1, 'type': 1})

    class _link(Element40):
        separate_close = False
        AttrDicts = (GlobalAttrs, LinksAndAnchors, {'charset': 1, 'media': 1})

    class _meta(Element40):
        separate_close = False
        AttrDicts = (I18n,
                     {'http-equiv': 1, 'name': 1, 'content': 1, 'scheme': 1})

    class _object(Element40):
        AttrDicts = (TabbingNavigation, {'declare': 0, 'classid': 1, 'codebase': 1, 'data': 1, 'type': 1,
                                         'codetype': 1, 'archive': 1, 'standby': 1, 'height': 1, 'width': 1,
                                         'usemap': 1})

    class _select(Element40):
        AttrDicts = (GlobalAttrs, TabbingNavigation, {'name': 1, 'size': 1, 'multiple': 0, 'disabled': 0})

    class _optGroup(Element40):
        AttrDicts = (GlobalAttrs, {'disabled': 0, 'label': 1})

    class _option(Element40):
        AttrDicts = (GlobalAttrs, {'disabled': 0, 'label': 1, 'value': 1, 'selected': 0})

    class _param(Element40):
        AttrDicts = ({'id': 1, 'name': 1, 'value': 1, 'valuetype': 1, 'type': 1},)

    class _pre(Element40):
        AttrDicts = (GlobalAttrs,)

    class _span(Element40):
        AttrDicts = (GlobalAttrs, {'align': 1})

    class _script(Element40):
        AttrDicts = ({'charset': 1, 'type': 1, 'src': 1, 'defer': 0},)

    class _div(_script):
        pass

    class _style(Element40):
        AttrDicts = (I18n, {'type': 1, 'media': 1, 'title': 1},)

    class _table(Element40):
        AttrDicts = (GlobalAttrs, BordersAndRules,
                     {'cellspacing': 1, 'cellpadding': 1, 'summary': 1, 'align': 1, 'bgcolor': 1, 'width': 1})

    class _tbody(Element40):
        AttrDicts = (GlobalAttrs, CellHAlign, CellVAlign)

    class _thead(_tbody):
        pass

    class _tfoot(_tbody):
        pass

    class _tr(_tbody):
        pass

    class _th(Element40):
        dented = False
        AttrDicts = (GlobalAttrs, CellHAlign, CellVAlign,
                     {'abbv': 1, 'axis': 1, 'headers': 1, 'scope': 1, 'rowspan': 1, 'colspan': 1,
                      'nowrap': 0, 'width': 1, 'height': 1, 'bgcolor': 1},)

    class _td(_th):
        pass

    class _textarea(Element40):
        AttrDicts = (GlobalAttrs, TabbingNavigation, AccessKeys,
                     {'name': 1, 'rows': 1, 'cols': 1, 'disabled': 0, 'readonly': 0},)



