#!/usr/bin/python
# -*- encoding: utf8 -*-
##xx -*- coding: latin-1 -*-
""" very old comment, left in purely for nostalgia:
    Data structures representing companies etc. Initial stubby version
    adequate for first invoice of 2013?
"""
import types
from phileas import _html40 as h


class Entity(object):
    def __init__(self, **kw):
        self.admit_args()

    def admit_args(self, **kw):
        for _key, _val in kw.items():
            print (_key, _val)
            #_translator = self.admit_args.__annotations__.get(_key, eval)
            #print (_translator)
            self.__setattr__(_key, _val)  #  _translator(_val))

    def pformat(self):  # obsolete?
        pass


class Car(Entity):
    def admit_args(self,
        modelName:str = "<model name>",
        buildYear:int = 1066,
        originalNewPrice:int = 0,
        percentBijtelling: float = 2.7,
        dateAcquired:str = '',
        dateRelinquished:str = '',
        kenteken:str = '??-??-??'
    ):
        Entity.admit_args(self,
            modelName=modelName,
            buildYear = buildYear,
            originalNewPrice=originalNewPrice,
            percentBijtelling=percentBijtelling,
            dateAcquired=dateAcquired,
            dateRelinquished=dateRelinquished,
            kenteken=kenteken,
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
    def admit_args(self,
        number: int = 0,
        name : str = '<Default Company Name>',
        address:list = list(['<Default Address, line %u>' %(n+1) for n in range(4)]),
        btwNumber:str = '', # => don't show BTW number on factuur, do charge BTW
        reference:str = '',
        paymentTerms:list = [
                 "Betaling naar bankrekening (zie gegevens boven) binnen 30 dagen wordt op prijs gesteld.",
                 "Bij betaling svp factuurnummer vermelden.",
        ],
        companyLogo:str = '',
        cars:list = [],
    ):
        Entity.admit_args(self,
            number=number,
            name = name,
            address=address,
            btwNumber=btwNumber,
            reference=reference,
            paymentTerms=paymentTerms,
            companyLogo=companyLogo,
            cars=cars,
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


#from .page import *
#from .invoice import *
from company import *