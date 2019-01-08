#!/usr/bin/python3
# -*- encoding: utf8 -*-
from .membersPage import clubName, MembersPage, h


class AdminPage(MembersPage):
    admin = True

    def upperBanner(self, *paths, **kw):
        return h.h1 | ('%s  %s' %(clubName,
                                   self.gloss({'EN': "(supplemental) - Administration zone",
                                               'NL': "(aanvullend) - Administratiezone"})))
    def lowerBanner(self, *paths, **kw):
        return h.h1 | self.gloss({'EN': "Administration Homepage",
                                  'NL': "Homepagina voor Administratiezone"})

_adminPage = AdminPage()
