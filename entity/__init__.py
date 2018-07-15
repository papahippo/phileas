#!/usr/bin/python
# -*- encoding: utf8 -*-
"""
module 'entity' is housed within package 'phileas' but the connection between the two is tenuous; they were developed
roughly over the same time frame and represent rather off-beat approaches to pythn-html integration (phileas') and
minimalistic database definition (entity) respectively.
"""
import sys,os
import datetime
import inspect
from collections import OrderedDict
from phileas import html4 as h
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')


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
        elif not isinstance(wild, tuple):
            dt  = datetime.datetime.strptime(wild, cls.fmt_str)
            wild = (dt.year, dt.month, dt.day)
        return datetime.date.__new__(cls, *wild)

    def __str__(self):
        return datetime.date.strftime(self, self.fmt_str)


    def __repr__(self):
        return "'%s'" % self.__str__()

class StringList:
    """
A 'StringList' is - as the name suggests a list of strings (hmmm... list of names might be more accurate!).
    """
    def __init__(self, sl):
        """
The initial value may be supplies a a read-made lsit of strings or as a string comma-separated list of strings(names)
        :param sl:
        """
        if isinstance(sl, list):
            self.list_ = sl
        else:
            self.list_  = [s.strip() for s in sl.split(',') if s]

    def __str__(self):
        return ', '.join(self.list_)

    def __repr__(self):
        return '[%s]' % ', '.join(['"%s"' % s for s in self.list_])


def get_frame(depth):
    """
This returns the line number following
    """
    frames = inspect.getouterframes(inspect.currentframe())
    return frames[depth]


def gloss(dikkie, language=('EN',), sep='/'):
    if not isinstance(dikkie, dict):
        return dikkie  # just a string, I presume.
    return '/'.join([dikkie[taal] for taal in language])


class Entity(object):
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
    rangeLookup = None
    next_lineno = -1
# following few represent quick(?) hack to get cool tale display and may disappear later!
    fieldDisplay = None
    admin = 1


    def __init__(self, **kw):
        cls = self.__class__
        frame = get_frame(3)
        self.filename = frame.filename
        self.lineno_range = (cls.next_lineno, 1 +frame.lineno)
        cls.next_lineno = 1 +frame.lineno
        annos = self.__init__.__annotations__
        for _key, _val in kw.items():
            try:
                reqd_class = annos.get(_key)
                if (reqd_class is not None) and not isinstance(_val, reqd_class):
                    if isinstance(reqd_class, tuple):
                        reqd_class = reqd_class[0]
                    cast_val = reqd_class(_val)
                else:
                    cast_val = _val
                # cast_val = (((reqd_class is not None) and not isinstance(_val, reqd_class)) and  ) or _val
                self.__setattr__(_key, cast_val)
            except (ValueError) as _exc:
                raise EntityError(_key, _val, _exc)

        if cls.keyLookup is None:
            cls.rangeLookup = {}  # don't share between inheriting classes!
            cls.keyLookup = {}    # don't share between inheriting classes!
        cls.rangeLookup[self.lineno_range] = self
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
            '\n' + self.__class__.__name__ + '(\n    '
          + ',\n    '.join(
                #[(name_ + '=' + fAS.annotations[name_].__repr__(getattr(self, name_)))
                 [(name_ + '=' + repr(getattr(self, name_)))
                 for name_ in fAS.args[1:]]
            )
          + '\n)\n'
        )

    def detach(self):
        cls = self.__class__
        del cls.rangeLookup[self.lineno_range]
        for k_ in self.keyFields:
            key_dict = cls.keyLookup.setdefault(k_, {})
            del key_dict[getattr(self, k_)]

    def by_key(cls, key_spec):
        if not isinstance(key_spec, (list, tuple)):
            key_spec = "name", key_spec
        field_name, field_value = key_spec
        return cls.keyLookup[field_name][field_value]
    by_key = classmethod(by_key)

    def by_range(cls, line_range):
        return cls.rangeLookup[tuple(line_range)]
    by_range = classmethod(by_range)

    def begin(cls):
        cls.next_lineno = 1 + get_frame(2).lineno
    begin = classmethod(begin)

    def display0(self, ix, name):
        # = stub!
        return (
                h.tr | (h.th | (str(ix), name, self.name))
        )

    def display(self, ix, name, page):
        #print(h.th | self.gloss({'EN': 'full name', 'NL': 'naam'}), file=sys.stderr)
        #return h.br, "abc", h.br
        if 0:
            return (
                (ix % 10 == 0) and (h.tr | (
                    [h.th | gloss(dikkie, language=language)
                        for _, dikkie, _ in self.fieldDisplay ]
                    ),
                )
        )
        else:
            return h.tr |(
                h.td | self.name,
                self.admin and
                (h.td |  (h.a(id='%s' %self.lineno_range[0],
                                 href=page.href('edit.py', {'calling_script_': (os.environ.get('SCRIPT_NAME'),),
                                                            'line_': map(str, self.lineno_range),
                                                            'filename_': (self.filename,)}))
                          |self.called))
                or  h.td |  self.called,
                h.td | (self.streetAddress, h.br, self.postCode, '&nbsp;'*2, self.cityAddress),
                h.td | (self.phone, h.br, self.mobile),
                h.td | (self.emailAddress, h.br, self.altEmailAddress),
                h.td | self.birthDate,
                h.td | self.memberSince,
                h.td | self.instrument,
                self.admin and (
                        h.td | (self.mailGroups)
                )
            )

    def Display(cls, filter_=True, sort_key_=None, page=None):
        return (
            h.table(id="members") | [member.display(ix, name, page=page) for ix, (name, member) in
                             enumerate(sorted(cls.keyLookup[sort_key_].items())[not cls.admin:])]
        )

    Display = classmethod(Display)

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

#if __name__ == "__main__":
