#!/usr/bin/python
# -*- encoding: utf8 -*-
import datetime

class Entity(object):
    grouping = None
    def __init__(self, **kw):
        self.members = []
        for _key, _val in kw.items():
            self.__setattr__(_key, _val)
        if self.grouping:
            self.grouping.members.append(self)

    def add_member(self, newbie):
        self.members.append(newbie)

class Grouping(Entity):
    pass

empty_grouping_ = Grouping(name="[Emppty grouping]")

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
        start_of_year = datetime.date(year, 1, 1)
        end_of_year = datetime.date(year, 12, 31)
        start_date = self.dateAcquired and datetime.date(*self.dateAcquired) or start_of_year
        end_date = self.dateRelinquished and datetime.date(*self.dateRelinquished) or end_of_year
        if end_date < start_of_year or start_date>end_of_year:
            return None
        if start_date < start_of_year:
            start_date = start_of_year
        daysInYear = (end_of_year-start_of_year).days + 1
        daysInUse = (end_date-start_date).days + 1
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
            h.br, "in use %s t/m %s" %(start_date, end_date),
            h.br,

"€%s x %s%% = €%s"    %(self.originalNewPrice,  money(self.percentBijtelling),
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


Verenigingen = Grouping()


class Vereniging(Grouping):
    grouping = Verenigingen
    def __init__(self,
        name:str='<Default Vereninging Name>',
    ):
        Grouping.__init__(self,
            name=name,
        )


class MailGroups(Grouping):
    pass

no_mail_groups_ = MailGroups()  # for use in stubs only!


class MailGroup_(Entity):
    grouping = MailGroups()

    def __init__(self,
        name:str='<Default Mailgroup Name>',
    ):
        Entity.__init__(self,
            name=name,
        )


class Lid_(Entity):
    grouping = Vereniging

    def __init__(self,
        name:str='<Default Member Name>',
        roepnaam:str='<Default roepnaam>',
        instrument:str='<Default instrument name>',
        emailAddress:str='<Default email address>',
        mailGroups:list = [],
    ):
        Entity.__init__(self,
            name=name,
            roepnaam=roepnaam,
            instrument=instrument,
            emailAddress=emailAddress,
            mailGroups=mailGroups,
                        )
        for mailGroup in self.mailGroups:
            mailGroup.add_member(self)


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
from .mailing import *
