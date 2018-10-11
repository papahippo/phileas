#!/usr/bin/python3
# -*- encoding: utf8 -*-
from clubPage import clubName, ClubPage, h
from entity.club import Member
import members


class ClubMembersPage(ClubPage):
    _upperBanner = h.h1 | "%s - Members zone" % clubName

    fieldDisplay = [
        # python name       # heading for glossing                 # field entry tip for glossing
        ('called',          {'EN':'known as', 'NL':'roepnaam'},    {'EN': 'known within MEW as...', 'NL': 'bekend binnen MEW als...'}),
        ('name',            {'EN':'full name', 'NL':'naam'},       {'EN': 'surname, initials', 'NL': 'achternaam, initielen'}),
        ('streetAddress',   {'EN':'street address', 'NL':'adres'}, {'EN': 'e.g. Rechtstraat 42', 'NL': 'b.v. Rechtstraat 42'}),
        ('postCode', 'postcode', 'e.g. 1234 XY'),
        ('cityAddress', 'Town/City', 'e.g. Eindhoven'),
        ('phone', 'telephome', 'e.g. 040-2468135'),
        ('mobile', 'mobile', 'e.g. 06-24681357'),
        ('emailAddress', '1st email address', 'e.g. fred@backofthe.net'),
        ('altEmailAddress', 'opt. 2nd email address', 'optional'),
        ('birthDate', 'date of birth', 'e.g. 15-mrt-1963'),
        ('memberSince', 'date of joining', 'e.g. 15-okt-2003'),
        ('instrument', 'instrument', 'e.g. Klarinet'),
        ('mailGroups', 'mail groups', 'e.g. Musicians, Hoorns'),
    ]
if __name__ == "__main__":
    # print ("hello Larry")
    ClubMembersPage().main()
    
