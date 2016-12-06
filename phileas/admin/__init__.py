#!/usr/bin/python
# -*- encoding: utf8 -*-

class Entity(object):
    argd = {}  # superclass accepts no args!

    def __init__(self, **kw):
        self.kw = kw  # copy before pruning; dubious merit
        for _key, (_type, _default) in self.argd.items():
            _val = kw.pop(_key, _default)
            if (not isinstance(_type, tuple)
                and not isinstance(_val, _type)):
                _val = _type(_val)
            self.__setattr__(_key, _val)
        if kw:
            raise KeyError("arguments not allowed: %s" % kw)
    def pformat(self):  # obsolete?
        pass


class Car(Entity):
    argd = dict(
        modelName=(str, "<model name>"),
        buildYear=(int, 1066),
        originalNewPrice=(int, 0),
        percentBijtelling=(float, 2.7),
        dateAcquired=(str, ''),
        dateRelinquished=(str, ''),
        kenteken=(str, '??-??-??'),
    )

    def useInYear(self, year):
        daysInYear = 365 + ((year%4)==0)
        daysInUse = daysInYear #fudged!
        yearBijTelling = self.originalNewPrice * self.percentBijtelling /100
        actualBijTelling = (yearBijTelling * daysInUse) / daysInYear

        return h.p | (
"type auto:  %s"  % self.modelName,
            h.br,
"bouwjaar:  %04u" % self.buildYear,
            h.br,
"nieuwprijs in bouwjaar %s" %   euros(self.originalNewPrice),
            h.br,
"kenteken: %s"  % self.kenteken,
            h.br,
            h.br,

"€%s x %s = €%s"    %(self.originalNewPrice,  money(self.percentBijtelling),
                        money(yearBijTelling)),
            h.br,
            h.br,
"%d/%d x €%s = €%s => invullen '%s' op aangifte"  % (daysInUse, daysInYear,
money(yearBijTelling),  money(actualBijTelling), euros(actualBijTelling)),
            h.br,
        )

class Company(Entity):
    argd = dict(
        number=(int, 0),
        name= (str, '<Default Company Name>'),
        address=(list, ['<Default Address, line %u>' %(n+1) for n in range(4)]),
        btwNumber=(str, ''), # => don't show BTW number on factuur, do charge BTW
        reference=(str, ''),
        paymentTerms=(list, [
                 "Betaling naar bankrekening (zie gegevens boven) binnen 30 dagen wordt op prijs gesteld.",
                 "Bij betaling svp factuurnummer vermelden.",
        ]),
        restitutionTerms=(list, [
             "Het positieve van de hierbovengenoemde negatieve totaal wordt vandaag overgeboekt ",
             "volgens uw instructies.", 
        ]),
        companyLogo=(str, ''),
        cars=(list, []),
    )


class Supplier(Company):
    pass

class Client(Company):
    pass # for now!

class Accountant(Company):
    pass # for now!

def money(amount):
    l = list(("%.2f" % amount ).replace('.',  ','))
    i=len(l)-6
    while i>0:
        l.insert(i, '.')
        i -=3
    return ''.join(l)

def euros(amount):
    return money(amount)[:-3]

def putLines(el,  *lines):
    for line in lines:
        if line is None:
            continue
        el.text(line)
        el.br

from .page import *
from .invoice import *
from .quarter import *
