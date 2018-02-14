#!/usr/bin/python
# -*- encoding: utf8 -*-
# temporary incubation area for simplification of classes relating to societies.
from phileas import _html40 as h
import datetime

class Entity(object):
    keyFields = ('name',)
    grouping = None
    keyLookup = {}

    def __init__(self, **kw):
        for _key, _val in kw.items():
            self.__setattr__(_key, _val)
        cls = self.__class__
        for k_ in self.keyFields:
            cls.keyLookup.setdefault(k_, {})[getattr(self, k_)] = self
        pass  # for breakpoint debugging!

    def __getitem__(cls, key_spec):
        if not isinstance(key_spec, (list, tuple)):
            key_spec = "name", key_spec
        field_name, field_value = key_spec
        return cls.keyLookup[field_name][field_value]
    __getitem__ = classmethod(__getitem__())



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


class Lid(Entity):
    def __init__(self,
        name:str='<Default Member Name>',
        called:str='<Default roepnaam>',
        instrument:str='<Default instrument name>',
        emailAddress:str='<Default email address>',
        mailGroups:list = [],
    ):
        Entity.__init__(self,
                        name=name,
                        called=called,
                        instrument=instrument,
                        emailAddress=emailAddress,
                        )
        self.mailGroups = []
        for mg in mailGroups:
            mg.admit(self)
            self.mailgroups.append(mg)

class Vereniging(Entity):

    def __init__(self,
        name:str='<Default Vereninging Name>',
    ):
        Entity.__init__(self,
                        name=name,
                        )

