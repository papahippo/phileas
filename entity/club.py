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

    def __init__(self,
                 name:str='',
                 initials:str='',
                 called:str='',
                 streetAddress:str='',
                 postCode:str='',
                 cityAddress:str='',
                 phone:List[str]=[],
                 mobile:List[str]=[],
                 emailAddress:List[str]=[],
                 altEmailAddress:List=[],
                 birthDate:List[DateOrNone]= [],
                 memberSince:List[DateOrNone]= [],
                 instrument:str='',
                 mailGroups:List[str] = [],
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
        for mGName in self.mailGroups:  # note no _!
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
    member = Member(name='test')
    print(Member)
