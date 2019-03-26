#!/usr/bin/python
# -*- encoding: utf8 -*-
"""
module 'entity' is housed within package 'phileas' but the connection between the two is tenuous; they were developed
roughly over the same time frame and represent rather off-beat approaches to pythn-html integration (phileas') and
minimalistic database definition (entity) respectively.
"""
import sys,os, io
import datetime
import inspect
from typing import List
from collections import OrderedDict
from phileas import html4 as h
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

# function requiring improvement!
def as_python_name(s):
    return s.replace(' ', '_').replace('-', '__')


def cast_as_nec(var, Class=None):
    if Class is None or isinstance(var, Class):
        return var
    return Class(var)

class EntityError(Exception):
    """
The purpose of EntityError is to intercept exceptions that occur while creating an Entity object and add information do
that a higher-level exception handler can pinpoint which of the arguments supplied on object creation is responsible
for the exception.
    """

    def __init__(self, key_, val_, exc_):
        self.key_ = key_
        self.val_ = val_
        self.exc_ = exc_

    def __str__(self):
        return ("%s was raised when trying to set %s=%s "
                % (self.exc_, self.key_, self.val_))

class FloatOrNone:
    """
FloatOrNone is is a quick hack because my entity stuff isn't yet compatible with python's
typing module which may ultimaetly provide a neat solution.
    """
    def __new__(cls, wild):
        """
The date may be supplied as '' (or equivalently None), as a ready-made datetime.datetime.date instance, or as a
string representing a date in the format '%d-%b-%Y'. (refer to pythn docs to see what this means!)
        """
        if wild is None:
            return None
        return float.__new__(float, wild)


class BoolOrNone:
    """
BoolOrNone is is a quick hack because my entity stuff isn't yet compatible with python's
typing module which may ultimaetly provide a neat solution.
    """
    def __new__(cls, wild):
        """
The date may be supplied as '' (or equivalently None), as a ready-made datetime.datetime.date instance, or as a
string representing a date in the format '%d-%b-%Y'. (refer to pythn docs to see what this means!)
        """
        if wild is None:
            return None
        return bool.__new__(bool, wild)


class DateOrNone(datetime.date):
    """
Objects of Class 'DateOrNone' are essentially datetime.datetime.date objects except that a value
of '' (the empty string) is allowed.
    """
    fmt_str = '%d-%b-%Y'

    def __new__(cls, wild):
        """
The date may be supplied as '' (or equivalently None), as a ready-made datetime.datetime.date instance, or as a
string representing a date in the format '%d-%b-%Y'. (refer to pythn docs to see what this means!)
        """
        if not wild:
            return ''
        elif isinstance(wild, bytes):
            wild = wild,
        elif not isinstance(wild, (tuple,)):
            dt  = datetime.datetime.strptime(wild, str(cls.fmt_str))
            wild = (dt.year, dt.month, dt.day)
        return datetime.date.__new__(cls, *wild)

    def __str__(self):
        return datetime.date.strftime(self, self.fmt_str)


    def __repr__(self):
        return "'%s'" % self.__str__()

class EntityType(type):
    """
    The sole (so far) purpose of this metaclass is to make 'len(Class)' work when 'Class' inherits from 'Entity'.
    """
    def __len__(cls):
        return cls.cls__len()

class Entity(object, metaclass=EntityType):
    """
Class 'Entity' is the start of module 'entity'. Some features of enity obects are:
    (1) initialization values are more stringently checked than is usual within python.
    (2) The statement which created an enity can be effectively recreated.
    (3) The position within a python (module) source file where the entity is created is
        remembered along with the object provided that a few constraints on
        source code layout are adhered to:
        (a) All entities of a particular must be declared consecutively.
        (b) The first such entity must be preceded by a call to [EntityName].begin().
    """
    keyFields = ()
    keyLookup = None
# following few represent quick(?) hack to get cool tale display and may disappear later!
    fieldDisplay = None
    admin = 1


    def __init__(self, **kw):
        annos = self.__init__.__annotations__
        for _key, _val in kw.items():
            try:
                reqd_class = annos.get(_key)
                try:
                    subscripted = reqd_class.__origin__
                    reqd_class = reqd_class.__args__[0]
                    if isinstance(_val, str):
                        _val = [v.strip() for v in _val.split(',')]
                    # Horrible hack to get tis towork onpython3.6!
                    # cast_val = subscripted([cast_as_nec(var, reqd_class) for var in _val])
                    cast_val = list([cast_as_nec(var, reqd_class) for var in _val])
                except AttributeError:
                    cast_val = cast_as_nec(_val, reqd_class)
                self.__setattr__(_key, cast_val)
            except (ValueError) as _exc:
                raise EntityError(_key, _val, _exc)
        self.attach()

    def attach(self):
        cls = self.__class__
        if cls.keyLookup is None:
            cls.keyLookup = {}    # don't share between inheriting classes!
        for k_ in self.keyFields:
            key_dict = cls.keyLookup.setdefault(k_, OrderedDict())
            try:
                key_ = getattr(self, k_)
            except AttributeError:
                continue
            if not key_:
                continue
            if key_ in key_dict:
                raise EntityError(k_, key_, "not unique")

            key_dict[key_] = self

    def __repr__(self):
        fAS = inspect.getfullargspec(self.__init__)
        return(
            self.__class__.__name__ + '(\n    '
          + ',\n    '.join(
                #[(name_ + '=' + fAS.annotations[name_].__repr__(getattr(self, name_)))
                 [(name_ + '=' + repr(getattr(self, name_)))
                 for name_ in fAS.args[1:]]
            )
          + '\n)\n'
        )

    def detach(self):
        cls = self.__class__
        for k_ in self.keyFields:
            key_dict = cls.keyLookup.setdefault(k_, {})
            del key_dict[getattr(self, k_)]

    @classmethod
    def cls__len(cls):
        # can't just use '__len__' for classes; see 'metaclass' stuff above.
        return cls.keyLookup and len(cls.keyLookup[cls.keyFields[0]]) or 0

    @classmethod
    def by_key(cls, key_spec):
        if not isinstance(key_spec, (list, tuple)):
            key_spec = cls.keyFields[0], key_spec
        field_name, field_value = key_spec
        return cls.keyLookup[field_name][field_value]

    @classmethod
    def export(cls, file_or_filename=sys.stdout, filter_ =lambda x:x):
        if not isinstance(file_or_filename, io.IOBase):
            file_or_filename = open(file_or_filename, 'w')

        with  file_or_filename as file_:
            print('from %s import %s' %(cls.__module__, cls.__name__), file=file_)
            print(file=file_)
            for k_, v_ in cls.keyLookup[cls.keyFields[0]].items():
                print("%s = %s" %(as_python_name(k_), filter_(v_)), file=file_)


# I don't remember how the following stuff ended up here but it surely belongs elsewhere?
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

if __name__ == "old __main__":
    # ad hoc testing stuff:
    import pickle
    d = DateOrNone('29-apr-1954')
    pickle.dump(d, open("date.p", "wb"))
    d1 = pickle.load(open("date.p", "rb"))
    print(d, d1)

    sl =List[str](['a, b'])
    print(', '.join([c+'!' for c in sl]))

if __name__ == "__main__":
    class MainEntity(Entity):
        keyFields = ('test',)
        def __init__(self,
            strScalar:str='<Default test string>',
            strList: List[str] = '<Default string list left>,<Default string list right>',
                     ):
            Entity.__init__(self,
                            strScalar=strScalar,
                            strList=strList)

    print("MainEntity empty length = ", len(MainEntity))
    firstMainEntity = MainEntity(strScalar='twine', strList='twine, rope')
    print ("After firstr instance creation, length = ", len(MainEntity))
    print(firstMainEntity.strScalar)
    print(firstMainEntity.strList)
