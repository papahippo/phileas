#!/usr/bin/python
# -*- encoding: utf8 -*-

class Grouping:
    def __init__(self):
        self.members= []

class Entity(object):
    grouping = None
    def __init__(self, **kw):
        for _key, _val in kw.items():
            self.__setattr__(_key, _val)
        if self.grouping:
            self.grouping.members.append(self)

Cars = Grouping()

class Car(Entity):
    grouping = Cars
    def __init__(self,
        modelName:str="<model name>",
        buildYear:int=1066,
        originalNewPrice:int=0,
        percentBijtelling:float=2.7,
        dateAcquired:str='',
        dateRelinquished:str='',
        kenteken:str='??-??-??',
    ):
        Entity.__init__(self,
            modelName=modelName,
            buildYear=buildYear,
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


Companies =  Grouping()

class Company(Entity):
    grouping = Companies
    def __init__(self,
        number:int=0,
        name:str='<Default Company Name>',
        address:list=list(['<Default Address, line %u>' %(n+1) for n in range(4)]),
        btwNumber:str='', # => don't show BTW number on factuur, do charge BTW
        reference:str='',
        paymentTerms:list=[
                 "Betaling naar bankrekening (zie gegevens boven) binnen 30 dagen wordt op prijs gesteld.",
                 "Bij betaling svp factuurnummer vermelden.",
        ],
        restitutionTerms:list=[
             "Het positieve van de hierbovengenoemde negatieve totaal wordt vandaag overgeboekt ",
             "volgens uw instructies.",
        ],
        companyLogo:str='',
        cars:list=[],
    ):
        Entity.__init__(self,
            number=number,
            name=name,
            address=address,
            btwNumber=btwNumber,
            reference=reference,
            paymentTerms=paymentTerms,
            restitutionTerms=restitutionTerms,
            companyLogo=companyLogo,
            cars=cars,
        )


Suppliers = Grouping()

class Supplier(Company):
    grouping = Suppliers


Clients = Grouping()

class Client(Company):
    grouping = Clients

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
