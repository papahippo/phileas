#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
from .membersPage import MembersPage, h, clubName
from entity.club import Member
from .members import *
import cherrypy

class MembersListPage(MembersPage):
    admin = False

    def validate(self, **kw):
        self.sortby = kw.get('sortby', ('name',))
        return MembersPage.validate(self, **kw)

    def lowerBanner(self):
        sortKey = cherrypy.session.setdefault('sortby', 'name')
        return h.h2 | (
            self.gloss({
                'EN': "Membership list ordered according to field '%s'"
                     % {'name': 'full name'}[sortKey],
                'NL': "Ledenlijst gesorteerd op veld '%s'"
                     % {'name': 'naam'}[sortKey],
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
            h.th | (self.admin and (h.a(href='../edit_one') | ('new')) or '...'),
            [h.th | self.gloss(heading)
                for attr_name, heading, tip_text in self.fieldDisplay
            ])),
            h.tr |(
                (h.td |  (h.a(id='%s' % getattr(member, member.keyFields[0] ),
                                 href=(self.admin and '../edit_one' or '../view_one') +
                                      '?key=%s' % getattr(member, member.keyFields[0] ))
                          | (self.admin and (self.gloss({'EN': 'edit', 'NL': 'wijzig'}))
                                         or (self.gloss({'EN': 'view', 'NL': 'toon'}))))),
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
                enumerate (sorted(Member.keyLookup['called'].items())) if member]
        )

if __name__ == "__main__":
    # print ("hello Larry")
    MembersListPage().main()
