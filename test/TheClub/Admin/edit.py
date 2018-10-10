#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
import cgi, cgitb
cgitb.enable()
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from entity.club import Member, EntityError
import mailgroups
import members

from membersPage import ClubMembersPage, h
from editPage import EditPage

class ClubAdminEditPage(EditPage, ClubMembersPage):
    EntityClass = Member
    _lowerBanner = "edit member details"

    def validate(self, **kw):
        valid_ = self.validate_edit(ClubMembersPage.validate(self, **kw), **kw)
        return valid_

    def lowerText(self):
        self.new_instance = isinstance(self.validated, str) and eval(self.validated) or None
        return self.edit_pane()

if __name__ == "__main__":
    # print ("hello Larry")
    ClubAdminEditPage().main()
    
