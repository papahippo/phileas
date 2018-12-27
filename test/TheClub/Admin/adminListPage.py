#!/usr/bin/python3
# -*- encoding: utf8 -*-
from ..Members.membersListPage import MembersListPage, clubName

class AdminListPage(MembersListPage):
    admin = True
    _upperBanner = "%s - Administation zone" % clubName


if __name__ == "__main__":
    AdminListPage().main()
    
