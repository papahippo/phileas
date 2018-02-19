#!/usr/bin/python3
# -*- encoding: utf8 -*-
from phileas.admin import *

vereniging = mew = Vereniging(
    name = "Muziekvereniging Eindhoven West",
)


MailGroup(name = "Musicians")
MailGroup(name = "Percussion")
MailGroup(name = "Horn")

for tag in range (2):  # in order ot easily experiment with thousands of members: range(100000)...
    larry =    Lid(
    name="Larry Myerscough%s" % tag,
    called="Larry%s" % tag,
    instrument="Pauken",
    emailAddress="hippostech@gmail.com",
    mailGroups=["Musicians", "Percussion", ],
)

gill = Lid(
    name="Gill Myerscough",
    called="Gill",
    instrument="Eb Horn",
    emailAddress="g.m.myerscough@gmail.com",
    mailGroups=["Musicians", "Horn", ],
)


if __name__=='__main__':
    if 0:
        print ('running %s as main' % __file__)
        print(MailGroup.keyLookup['name'])
