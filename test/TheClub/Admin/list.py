#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys
from membersPage import ClubMembersPage, h
from phileas.entity.club import Member
import members


class ClubMembersListPage(ClubMembersPage):
    admin = 0

    def validate(self, sortby=('name',), **kw):
        self.sortby = sortby
        return ClubMembersPage.validate(self, **kw)

    def lowerBanner(self):
        return h.h2 | (
            self.gloss({
                'EN': "Membership list ordered according to field '%s'"
                     % {'name': 'full name'}[self.sortby[0]],
                'NL': "Ledenlijst gesorteerd op veld '%s'"
                     % {'name': 'naam'}[self.sortby[0]],
            })
        )

    def one_offs(self):
        return h.p | u""
    
    def rows_per_member(self, ix, member):
        #print(h.th | self.gloss({'EN': 'full name', 'NL': 'naam'}), file=sys.stderr)
        #return h.br, "abc", h.br
        return (
            (ix % 10 == 0) and (h.tr | (
                h.th | self.gloss({'EN': 'full name',         'NL':'naam'}),
                h.th | self.gloss({'EN': 'known as',          'NL':'roepnaam'}),
                h.th | self.gloss({'EN': 'address',           'NL': 'addres'}),
                h.th | self.gloss({'EN': 'telephone',         'NL':'telefoon'}),
                h.th | self.gloss({'EN': 'email address(es)', 'NL':'email addres(sen)'}),
                h.th | self.gloss({'EN': 'date of birth',     'NL':'geboortedatum'}),
                h.th | self.gloss({'EN': 'membership start',  'NL':'lid vanaf'}),
                h.th | self.gloss({'EN': 'instrument',        'NL':'instrument'}),
                self.admin and (
                    h.th | self.gloss({'EN': 'mail group(s)',     'NL':'mailgroep(en)'})
                ),
            )),
            h.tr |(
                h.td | member.name,
                self.admin and
                (h.td |  (h.a(id='%s' %member.lineno_range[0],
                                 href=self.href('edit.py', {'line_': map(str, member.lineno_range)})) |member.called))
                or  h.td |  member.called,
                h.td | (member.streetAddress, h.br, member.postCode, '&nbsp;'*2, member.cityAddress),
                h.td | (member.phone, h.br, member.mobile),
                h.td | (member.emailAddress, h.br, member.altEmailAddress),
                h.td | member.birthDate,
                h.td | member.memberSince,
                h.td | member.instrument,
                self.admin and (
                        h.td | (member.mailGroups)
                )
            )
        )
    def lowerText(self):
        #for ix, (name, member) in enumerate(Member.keyLookup['name'].items()):
        #    print (name, member.name, '...', member.__init__.__annotations__)
        #print(Member.keyLookup['name'].items())
        return (self.one_offs(),
                h.table(id="members") | [self.rows_per_member(ix, member) for ix, (name, member) in
                enumerate (sorted(Member.keyLookup['called'].items())[not self.admin:])]
        )

if __name__ == "__main__":
    # print ("hello Larry")
    ClubMembersListPage().main()
    
