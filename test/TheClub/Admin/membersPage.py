#!/usr/bin/python3
# -*- encoding: utf8 -*-
from clubPage import clubName, ClubPage, h
from entity.club import Member
import members


class ClubMembersPage(ClubPage):
    _upperBanner = h.h1 | "%s - Members zone" % clubName

    fieldDisplay = [
        ('known as', 'called', 'bekend binnen MEW als...'),
        ('full name', 'name', 'surname, initials'),
        ('street address', 'streetAddress', 'e.g. Rechtstraat 42'),
        ('postcode', 'postCode', 'e.g. 1234 XY'),
        ('Town/City', 'cityAddress', 'e.g. Eindhoven'),
        ('telephome', 'phone', 'e.g. 040-2468135'),
        ('mobile', 'mobile', 'e.g. 06-24681357'),
        ('1st email address', 'emailAddress', 'e.g. fred@backofthe.net'),
        ('opt. 2nd email address', 'altEmailAddress', 'optional'),
        ('date of birth', 'birthDate', 'e.g. 15-mrt-1963'),
        ('date of joining', 'memberSince', 'e.g. 15-okt-2003'),
        ('instrument', 'instrument', 'e.g. Klarinet'),
        ('mail groups', 'mailGroups', 'e.g. Musicians, Hoorns'),
    ]
if __name__ == "__main__":
    # print ("hello Larry")
    ClubMembersPage().main()
    
