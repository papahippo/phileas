#!/usr/bin/python3
# -*- encoding: utf8 -*-
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from entity.club import Member
import mailgroups
import members

from memberViewPage import MemberViewPage

class MemberEditPage(MemberViewPage):
    _lowerBanner = "edit member details"

    def evaluate(self, str):
        return eval(str)

    def lowerText(self):
        return self.edit_pane()

if __name__ == "__main__":
    MemberEditPage().main()
    
