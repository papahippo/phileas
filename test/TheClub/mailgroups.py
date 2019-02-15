#!/usr/bin/python3
# -*- encoding: utf8 -*-
from entity.club import MailGroup
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')


MailGroup(name = "Musicians")
MailGroup(name = "Percussion")
MailGroup(name = "Horn")


if __name__=='__main__':
    print ('running %s as main' % __file__)
    print(MailGroup.keyLookup['name'])

