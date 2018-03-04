#!/usr/bin/python3
# -*- encoding: utf8 -*-
from phileas.admin import *


if __name__ == "__main__":
    mailGroup = MailGroup('Musicians')
    member1 = Member(name='test1', mailGroups='Musicians')
    member2 = Member(name='test2', mailGroups='Musicians')
    member3 = Member(name='test3', mailGroups='Musicians')
    # member = Member(name='test', mailGroups='badgroup')
    for member in (member1, member2, member3):
        print(member, member.lineno_range)

