#!/usr/bin/python
# -*- encoding: utf8 -*-
from entity import *


class Club(Entity):

    def __init__(self,
        name:str='<Default club Name>',
    ):
        Entity.__init__(self,
                        name=name,
                        )

class MailGroup(Entity):
    keyFields = ('name',)
    def __init__(self,
        name:str='<Default Mailgroup Name>',
    ):
        Entity.__init__(self,
            name=name,
        )
        self.members = []

    def admit(self, member):
        self.members.append(member)


class Member(Entity):
    keyFields = ('called', 'name')

    fieldDisplay = [
        ('called', {'EN':'known as', 'NL': 'roepnaam'},
                        {'EN': 'known within MEW as...', 'NL': 'bekend binnen MEW als...'}),
        ('name', 'full name', 'surname, initials'),
        ('streetAddress', 'street address', 'e.g. Rechtstraat 42'),
        ('postCode', 'postcode', 'e.g. 1234 XY'),
        ('cityAddress', 'Town/City', 'e.g. Eindhoven'),
        ('phone', 'telephome', 'e.g. 040-2468135'),
        ('mobile', 'mobile', 'e.g. 06-24681357'),
        ('emailAddress', '1st email address', 'e.g. fred@backofthe.net'),
        ('altEmailAddress', 'opt. 2nd email address', 'optional'),
        ('birthDate', 'date of birth', 'e.g. 15-mrt-1963'),
        ('memberSince', 'date of joining', 'e.g. 15-okt-2003'),
        ('instrument', 'instrument', 'e.g. Klarinet'),
        ('mailGroups', 'mail groups', 'e.g. Musicians, Hoorns'),
    ]
    def __init__(self,
                 name:str='',
                 initials:str='',
                 called:str='',
                 streetAddress:str='',
                 postCode:str='',
                 cityAddress:str='',
                 phone:StringList=[],
                 mobile:StringList=[],
                 emailAddress:StringList=[],
                 altEmailAddress:StringList=[],
                 birthDate:DateOrNone= '',
                 memberSince:DateOrNone= '',
                 instrument='',
                 mailGroups:StringList = [],
                 ):
        if (not called) and (not name.startswith('(')):
            called = name.split(', ')[-1].split(' ')[0]
        Entity.__init__(self,
                        name=name,
                        initials=initials,
                        called=called,
                        streetAddress=streetAddress,
                        postCode=postCode,
                        cityAddress=cityAddress,
                        phone=phone,
                        mobile=mobile,
                        emailAddress=emailAddress,
                        altEmailAddress=altEmailAddress,
                        birthDate=birthDate,
                        memberSince=memberSince,
                        instrument=instrument,
                        mailGroups=mailGroups,
                        )
        self.mailGroups_ = [] # note the _!
        for mGName in self.mailGroups.list_:  # note no _!
            try:
                mg = MailGroup.by_key(mGName)
            except KeyError as _exc:
                raise EntityError('mailgroup', mGName, _exc)
            mg.admit(self)
            self.mailGroups_.append(mg)


if __name__ == "__main__":
    # This is of (very?) limited value owing to use of relative includes; see .../admin/test/veri.py.
    #mailGroup = MailGroup('tryers')
    #member = Member(name='test', memberSince='bad date')
    #member = Member(name='test', mailGroups='asdf')
    print(Member)
