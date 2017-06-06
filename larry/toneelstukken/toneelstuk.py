#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
import cgi, cgitb, urlparse
cgitb.enable()

from orderedPage import OrderedPage, main, h

class Moment:
    pass

class Scene(Moment):
    def __init__(self, num, name):
      self._num = num
      self._name = name

    def html(self, page):
      return h.h4 | 'Scene %u: %s' %(self._num, self._name)
    
class Speech(Moment):
    def __init__(self, *p):
      self._roles = p[:-1]
      self._text = p[-1]

    def html(self, page):
      return ([(h.b| role, h.em|'(%s)' % '/'.join(page._cast_dict[role]))
               for role in self._roles], ':', h.br,
               self._text, h.br*2,)

class Song(Moment):
    def __init__(self, title, text):
        self._title = title
        self._text = text

    def html(self, page):
      return (h.b | self._title, h.br,  h.em | (h.pre | self._text))
    
class Toneelstuk(OrderedPage):
    _lowerBanner = "[naam van toneelstuk verschijnt hier]"
    _title = "toneelstukken"

    cast = (
      ('role 1', ('always Matthew',)),
      ('role 2', ('always Mark',)),
      ('role 3', ('sometimes Luke', 'sometimes John',)),
    )
    moments = (
      
Scene(1, "what happened first"),
    
Speech("role 1","""
Well I never!
    """),

Scene(2, "what happened next"),
    )

    def __init__(self):
      OrderedPage.__init__(self)
      self._cast_dict = dict(self.cast)

    def upperText(self):
	return( h.p |"""
This section of the website represents a learning aid for the text of plays (drama). 
      """)
    
    def lowerText(self):
        return (
            h.h3 | "Cast",
            h.table | [h.tr | (h.td | role, h.td | ' / '.join(actors)) for role, actors in self.cast],
            [moment.html(self) for moment in self.moments]
	      )


if __name__=="__main__":
    main(Toneelstuk)
