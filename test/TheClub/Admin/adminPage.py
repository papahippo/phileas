#!/usr/bin/python3
# -*- encoding: utf8 -*-
from membersPage import clubName, ClubMembersPage, h


class ClubAdminPage(ClubMembersPage):
    _upperBanner = "%s - Administation zone" % clubName

if __name__ == "__main__":
    # print ("hello Larry")
    ClubAdminPage().main()
    
