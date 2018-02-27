#!/usr/bin/python3
# -*- encoding: utf8 -*-
from page import *
from phileas.admin import Lid
import MEW.members


class MEW_AdminIndexPage(Page):
    def one_offs(self):
        return h.p | "placeholder for one-off fields"
    
    def rows_per_lid(self, ix, lid):
        #print (lid.name, '...', lid.__init__.__annotations__)
        #return
        return (
            (ix % 10 == 0) and (h.tr | [h.th | fieldName for fieldName in
                    ('roepnaam', 'naam', 'adres', 'telefoon', 'email', 'geboortedatum', 'lidmaatschap datum',
                     'instrument', 'mailgroepen')]),
            h.tr |(
                h.td | (h.a(href='edit.py?line_=%u&line_=%u;' %lid.lineno_range) |lid.called),
                h.td | lid.name,
                h.td | (lid.streetAddress, h.br, lid.postCode, '&nbsp;'*2, lid.cityAddress),
                h.td | (lid.phone, h.br, lid.mobile),
                h.td | (lid.emailAddress, h.br, lid.altEmailAddress),
                h.td | lid.birthDate,
                h.td | lid.memberSince,
                h.td | lid.instrument,
                h.td | (lid.mailGroups)
            )
        )
    def body(self):
        #for ix, (name, lid) in enumerate(Lid.keyLookup['name'].items()):
        #    print (name, lid.name, '...', lid.__init__.__annotations__)
        #print(Lid.keyLookup['name'].items())
        return (self.one_offs(),
                h.table(id="members") | [self.rows_per_lid(ix, lid) for ix, (name, lid) in
                enumerate (sorted(Lid.keyLookup['called'].items()))]
        )

if __name__ == "__main__":
    # print ("hello Larry")
    MEW_AdminIndexPage().main()
    
