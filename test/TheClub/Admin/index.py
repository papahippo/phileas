#!/usr/bin/python3
# -*- encoding: utf8 -*-
from page import Page, h
from entity import Member


class MEW_MembersIndexPage(Page):
    admin = 0

    def one_offs(self):
        return h.p | u"placeholder for one-off é fields"
    
    def rows_per_lid(self, ix, lid):
        return (
            (ix % 10 == 0) and h.tr | (
                    h.th | 'roepnaam',
                    h.th | 'naam',
                    h.th | 'adres',
                    h.th | 'telefoon',
                    h.th | 'email',
                    h.th | 'geboortedatum',
                    self.admin and h.th | 'lidmaatschap datum',
                    h.th | 'instrument',
                    self.admin and h.th | 'mailgroepen',
               ),
            h.tr |(
                self.admin and
                    h.td |  (h.a(id='%s' %lid.lineno_range[0], href='edit.py?line_=%u&line_=%u;' %lid.lineno_range) |lid.called)
                or  h.td |  lid.called,
                h.td | lid.name,
                h.td | (lid.streetAddress, h.br, lid.postCode, '&nbsp;'*2, lid.cityAddress),
                h.td | (lid.phone, h.br, lid.mobile),
                h.td | (lid.emailAddress, h.br, lid.altEmailAddress),
                h.td | lid.birthDate,
                self.admin and h.td | lid.memberSince,
                h.td | lid.instrument,
                self.admin and h.td | (lid.mailGroups)
            )
        )
    def body(self):
        #for ix, (name, lid) in enumerate(Lid.keyLookup['name'].items()):
        #    print (name, lid.name, '...', lid.__init__.__annotations__)
        #print(Lid.keyLookup['name'].items())
        return (self.one_offs(),
                h.table(id="members") | [self.rows_per_lid(ix, lid) for ix, (name, lid) in
                                         enumerate (sorted(Member.keyLookup['called'].items())[not self.admin:])]
        )

if __name__ == "__main__":
    # print ("hello Larry")
    MEW_MembersIndexPage().main()
    
