#!/usr/bin/python3
# -*- encoding: utf8 -*-
from entity.club import Member
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

import mailgroups

Member.begin()

Member(
    name='(new member)',
    initials='',
    called='(new member)',
    streetAddress='',
    postCode='',
    cityAddress='',
    phone='',
    mobile='',
    emailAddress='',
    altEmailAddress='',
    birthDate='',
    memberSince='',
    instrument='',
    mailGroups=["Musicians", "Percussion"]
)

Member(
    name='X, Frederik',
    initials='',
    called='fred x',
    streetAddress='',
    postCode='',
    cityAddress='',
    phone='',
    mobile='',
    emailAddress='',
    altEmailAddress='',
    birthDate='',
    memberSince='',
    instrument='',
    mailGroups=["Musicians", "Percussion"]
)

Member(
    name='Duck, Dafne',
    initials='',
    called='Daffie',
    streetAddress='De Vijfer 30',
    postCode='1234 AB',
    cityAddress='Eendhoven',
    phone='099-1234567',
    mobile='06-9876543',
    emailAddress='dafne.duck2@wetmail.com',
    altEmailAddress='',
    birthDate='12-aug-1953',
    memberSince='03-jul-2017',
    instrument='Clarinet',
    mailGroups=["Musicians"]
)

Member(
    name='Duck, Donaldus',
    initials='',
    called='Donald',
    streetAddress='De Vijfer 30b',
    postCode='1234 AB',
    cityAddress='Eendhoven',
    phone='099-1234567',
    mobile='06-9876543',
    emailAddress='donald.duck42@wetmail.com',
    altEmailAddress='',
    birthDate='12-aug-1951',
    memberSince='03-okt-2017',
    instrument='Flute',
    mailGroups=["Musicians"]
)

if __name__ == "__main__":
    print(Member.keyLookup['called'])
