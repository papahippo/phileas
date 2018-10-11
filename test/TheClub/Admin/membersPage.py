#!/usr/bin/python3
# -*- encoding: utf8 -*-
from clubPage import clubName, ClubPage, h
from entity.club import Member
import members


class MembersPage(ClubPage):
    _upperBanner = h.h1 | "%s - Members zone" % clubName

    fieldDisplay = [
# python name       # heading for glossing                              # field entry tip for glossing
('called',          {'EN':'known as',         'NL':'roepnaam'},         {'EN': 'known within MEW as...', 'NL': 'bekend binnen MEW als...'}),
('name',            {'EN':'full name',        'NL':'naam'},             {'EN': 'surname, initials',      'NL': 'achternaam, initielen'}),
('streetAddress',   {'EN':'street address',   'NL':'adres'},            {'EN': 'e.g. Rechtstraat 42',    'NL': 'b.v. Rechtstraat 42'}),
('postCode',        {'EN':'post code',        'NL':'postcode'},         {'EN': 'e.g. 1234 XY',           'NL': 'b.v. 1234 XY'}),
('cityAddress',     {'EN':'Town/City',        'NL':'gemeente'},         {'EN': 'e.g. Eindhoven',         'NL': 'b.v. Eindhoven'}),
('phone',           {'EN':'telephone',        'NL':'telefoon'},         {'EN': 'e.g. 040-2468135',       'NL': 'b.v. 040-2468135'}),
('mobile',          {'EN':'mobile',           'NL':'mobiel'},           {'EN': 'e.g. 06-24681357',       'NL': 'b.v. 06-24681357'}),
('emailAddress',    {'EN':'email address(es)','NL':'email addres(sen)'},{'EN': 'e.g. 06-24681357',       'NL': 'b.v. 06-24681357'}),
('birthDate',       {'EN':'date of birth',    'NL':'geboortedtatum'},   {'EN': 'e.g. 15-mrt-1963',       'NL': 'b.v. 15-mrt-1963'}),
('memberSince',     {'EN':'date of joining',  'NL':'lid sinds'},        {'EN': 'e.g. 15-okt-2003',       'NL': 'b.v. 15-okt-2003'}),
('instrument',      {'EN':'instrument',       'NL':'instrument'},       {'EN': 'e.g. Clarinet',          'NL': 'b.v. Klarinet'}),
#('altEmailAddress', 'opt. 2nd email address', 'optional'),
#('mailGroups', 'mail groups', 'e.g. Musicians, Hoorns'),
    ]
if __name__ == "__main__":
    # print ("hello Larry")
    MembersPage().main()
    
