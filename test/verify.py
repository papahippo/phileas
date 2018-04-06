#!/usr/bin/python3
# -*- encoding: utf8 -*-


if __name__ == "__main__":
    mailGroup = MailGroup('Musicians')
    Member.begin()
    member1 = Member(name='test1', mailGroups='Musicians')
    member2 = Member(name='test2', mailGroups='Musicians')
    member3 = Member(name='test3', mailGroups='Musicians')
    # member = Member(name='test', mailGroups='badgroup')
    for member in (member1, member2, member3):
        print(member, member.lineno_range)
    print (sorted(Member.keyLookup['called'].keys()))
    Member.by_range(member2.lineno_range).detach()
    print (sorted(Member.keyLookup['called'].keys()))
