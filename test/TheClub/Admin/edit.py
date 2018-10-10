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

from membersPage import ClubMembersPage
from editPage import EditPage, h

class ClubAdminEditPage(EditPage, ClubMembersPage):
    EntityClass = Member
    _lowerBanner = "edit member details"

    def evaluate(self, str):
        return eval(str)

    def lowerText(self):
        return self.edit_pane()

if __name__ == "__main__":
    # print ("hello Larry")
    ClubAdminEditPage().main()
    
