#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
from membersPage import MembersPage, h
from entity.club import Member
import members


class MembersListPage(MembersPage):
    admin = False

    def validate(self, **kw):
        self.sortby = kw.get('sortby', ('name',))
        return MembersPage.validate(self, **kw)

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
        if 0:
            print(self.fieldDisplay, file=sys.stderr)  #diagnostics
        return h.p | u""
    
    def rows_per_member(self, ix, member):
        #print(h.th | self.gloss({'EN': 'full name', 'NL': 'naam'}), file=sys.stderr)
        #return h.br, "abc", h.br
        return (
            (ix % 10 == 0) and (h.tr | (
            h.th | (h.em | ('single', h.br, 'item')),
            [h.th | self.gloss(heading)
                for attr_name, heading, tip_text in self.fieldDisplay
            ])),
            h.tr |(
                (h.td |  (h.a(id='%s' %member.lineno_range[0],
                                 href=self.href(self.admin and 'memberEditPage.py' or 'memberViewPage.py',
                                                {'calling_script_': (self.script_name,),
                                                            'line_': map(str, member.lineno_range),
                                                            'filename_': (member.filename,),
                                                 'language': self.language}))
                          | (self.admin and 'edit' or 'view'))),
                [(h.td | getattr(member, attr_name)) for attr_name, heading, tip_text in self.fieldDisplay],
            )
        )
    def lowerText(self):
        #for ix, (name, member) in enumerate(Member.keyLookup['name'].items()):
        #    print (name, member.name, '...', member.__init__.__annotations__)
        #print(self.language, file=sys.stderr)
        #print(Member.keyLookup['name'].items())
        return (self.one_offs(),
                h.table(id="members") | [self.rows_per_member(ix, member) for ix, (name, member) in
                enumerate (sorted(Member.keyLookup['called'].items())[not self.admin:]) if member]
        )

if __name__ == "__main__":
    # print ("hello Larry")
    MembersListPage().main()
    
