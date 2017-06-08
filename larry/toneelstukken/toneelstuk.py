#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
#import cgi, cgitb
#cgitb.enable()

from orderedPage import OrderedPage, main, h
import random

class Moment:
    Id = 2
    def __init__(self):
        Moment.Id += 1
        self.Id = Moment.Id

class Scene(Moment):

    def __init__(self, num, name):
        Moment.__init__(self)
        self._num = num
        self._name = name

    def html(self, page):
      return h.h4 | 'Scene %u: %s' %(self._num, self._name)


class Speech(Moment):
    per_role = {}
    def __init__(self, *p):
        Moment.__init__(self)
        self._roles = p[:-1]
        self._text = p[-1]
        for role in self._roles:
           Speech.per_role.setdefault(role, []).append(self.Id)

    def html(self, page):
        if self.Id == page.hideId:
            text = (h.a(href=page.uri+"&reveal=%u#%u" % (self.Id, self.Id-2))
                        | "?? say the text then click here! ???")
        elif self.Id==page.revealId:
            text = (h.b |"should say:", h.br, self._text, h.br,
                    h.a(href=page.uri.split('&reveal')[0]) | "ask me another", h.br,)
        else:
            text = self._text
        return ([(h.b(Id=self.Id)| role, h.em|'(%s)' % '/'.join(page._cast_dict[role]))
               for role in self._roles], ':', h.br,
               text, h.br*2,)

class Song(Moment):

    def __init__(self, title, text):
        Moment.__init__(self)
        self._title = title
        self._text = text

    def html(self, page):
      return (h.b | self._title, h.br,  h.em | (h.pre | self._text))
    
class Toneelstuk(OrderedPage):
    _lowerBanner = "[naam van toneelstuk verschijnt hier]"
    _title = "toneelstukken"

    def __init__(self, **kw):
        OrderedPage.__init__(self, **kw)
        self._cast_dict = dict(self.cast)
        self.revealId = int(self.kw.get("reveal", (-1,))[0])
        quizzers = self.kw.get("quiz", ())
        if self.revealId>=0 or not quizzers:
            self.hideId = None
        else:
            rnd =random.Random()
            scope = Speech.per_role[quizzers[rnd.randrange(len(quizzers))]]
            self.hideId = scope[1]  # STUB for.. rnd.randrange(len(scope))]

    def upperText(self):
        return (self.uri, h.p | """
    This section of the website represents a learning aid for the text of plays (drama). 
          """)

    def lowerText(self):
        return (
            h.h3 | "Cast",
            h.table | [h.tr | (h.td | role, h.td | ' / '.join(actors)) for role, actors in self.cast],
            [moment.html(self) for moment in self.moments]
        )

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


if __name__=="__main__":
    main(Toneelstuk)
