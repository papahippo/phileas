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

from membersPage import MembersPage
from editPage import EditPage, h

class MemberViewPage(EditPage, MembersPage):
    EntityClass = Member
    _lowerBanner = "view member details"
    admin = False

    def evaluate(self, str):
        return eval(str)

    def lowerText(self):
        return self.edit_pane(EntityClass=Member)

if __name__ == "__main__":
    # print ("hello Larry")
    MemberViewPage().main()
    
