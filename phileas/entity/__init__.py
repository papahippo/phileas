#!/usr/bin/python
# -*- encoding: utf8 -*-
from phileas import _html40 as h
import datetime
import inspect

class EntityError(Exception):
    def __init__(self, key_, val_, exc_):
        self.key_ = key_
        self.val_ = val_
        self.exc_ = exc_

    def __str__(self):
        return ("%s was raised when trying to set %s=%s "
            % (self.exc_, self.key_, self.val_))

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

    def __str__(self):
        if not self.date_:
            return ""
        else:
            return self.date_.strftime(self.fmt_str)


    def __repr__(self):
            return "'%s'" % self.__str__()

class StringList:
    def __init__(self, sl):
        if isinstance(sl, list):
            self.list_ = sl
        else:
            self.list_  = [s.strip() for s in sl.split(',') if s]

    def __str__(self):
        return ', '.join(self.list_)

    def __repr__(self):
        return '[%s]' % ', '.join(['"%s"' % s for s in self.list_])


class Entity(object):
    keyFields = ()
    keyLookup = None
    prev_lineno = -1

    def __init__(self, **kw):
        cls = self.__class__
        frames = inspect.getouterframes(inspect.currentframe())
        last_lineno = frames[2].lineno
        self.lineno_range = (cls.prev_lineno+1, last_lineno + 1)
        cls.prev_lineno = last_lineno
        annos = self.__init__.__annotations__
        for _key, _val in kw.items():
            try:
                self.__setattr__(_key, annos.get(_key, lambda x:x)(_val))
            except (ValueError) as _exc:
                raise EntityError(_key, _val, _exc)
        if cls.keyLookup is None:
            cls.keyLookup = {}
        for k_ in self.keyFields:
            key_dict = cls.keyLookup.setdefault(k_, {})
            try:
                key_ = getattr(self, k_)
            except AttributeError:
                continue
            #if key_ in key_dict:
            #    raise EntityError(k_, key_, "not unique")

            key_dict[key_] = self

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
                #[(name_ + '=' + fAS.annotations[name_].__repr__(getattr(self, name_)))
                 [(name_ + '=' + repr(getattr(self, name_)))
                 for name_ in fAS.args[1:]]
            )
          + '\n)\n'
        )


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
