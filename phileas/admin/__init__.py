#!/usr/bin/python
# -*- encoding: utf8 -*-
from phileas import _html40 as h
import datetime
import inspect
from .awhere import Awhere


class dateOrNone:
    fmt_str = '%d-%b-%Y'

    def __init__(self, s):
        if not s:
            self.date_ = ''
        elif isinstance(s, datetime.date):
            self.date_ = s
        else:
            dt  = datetime.datetime.strptime(s, self.fmt_str)
            self.date_  = datetime.datetime.date(dt)

    def __repr__(self):
        if not self.date_:
            return "''"
        else:
            return repr(self.date_.strftime(self.fmt_str))

class Entity(object):
    keyFields = ('name',)
    keyLookup = None

    def __init__(self, **kw):
        annos = self.__init__.__annotations__
        #print(annos)
        for _key, _val in kw.items():
            self.__setattr__(_key, annos[_key](_val))
        cls = self.__class__
        if cls.keyLookup is None:
            cls.keyLookup = {}
        for k_ in self.keyFields:
            try:
                cls.keyLookup.setdefault(k_, {})[getattr(self, k_)] = self
            except AttributeError:
                pass
        pass  # for breakpoint debugging!

    def by_key(cls, key_spec):
        if not isinstance(key_spec, (list, tuple)):
            key_spec = "name", key_spec
        field_name, field_value = key_spec
        return cls.keyLookup[field_name][field_value]
    by_key = classmethod(by_key)


    def __repr__(self):
        fAS = inspect.getfullargspec(self.__init__)
        return(
            '\n' + self.__class__.__name__ + '(\n    '
          + ',\n    '.join(
                [(name_ + '=' + fAS.annotations[name_].__repr__(getattr(self, name_)))
                 for name_ in fAS.args[1:]]
            )
          + '\n)\n'
        )

class MailGroup(Entity):

    def __init__(self,
        name:str='<Default Mailgroup Name>',
    ):
        Entity.__init__(self,
            name=name,
        )
        self.members = []

    def admit(self, member):
        self.members.append(member)


class Lid(Entity, Awhere):
    keyFields = ('name', 'called')
    def __init__(self,
        name:str='',
        initials:str='',
        called:str='',
        streetAddress:str='',
        postCode:str='',
        cityAddress:str='',
        emailAddress:str='',
        altEmailAddress:str='',
        birthDate:dateOrNone='',
        memberSince:dateOrNone='',
        instrument:str='',
        mailGroups:list = [],
    ):
        Awhere.__init__(self)
        if not called:
            called = name.split(', ')[-1].split(' ')[0]
        Entity.__init__(self,
                        name=name,
                        initials=initials,
                        called=called,
                        streetAddress=streetAddress,
                        postCode=postCode,
                        cityAddress=cityAddress,
                        emailAddress=emailAddress,
                        altEmailAddress=altEmailAddress,
                        birthDate=birthDate,
                        memberSince=memberSince,
                        instrument=instrument,
                        mailGroups=mailGroups,
                        )
        self.mailGroups_ = []
        for mGName in mailGroups:
            mg = MailGroup.by_key(mGName)
            mg.admit(self)
            self.mailGroups_.append(mg)

class Vereniging(Entity):

    def __init__(self,
        name:str='<Default Vereninging Name>',
    ):
        Entity.__init__(self,
                        name=name,
                        )


class Car(Entity):

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

class Company(Awhere, Entity):
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
        Awhere.__init__(self)
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


class Supplier(Company):
    pass


class Client(Company):
    pass


class Accountant(Company):
    pass


class Business(Entity):
    Admissible = [Company]


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

from ..page import *
from .invoice import *
from .quarter import *
from .mailing import *


if __name__ == "__main__":
    lid = Lid(name='test')
    print(lid)
