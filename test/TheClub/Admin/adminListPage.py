#!/usr/bin/python3
# -*- encoding: utf8 -*-
import cgitb
cgitb.enable()
from membersListPage import MembersListPage

class AdminListPage(MembersListPage):
    admin = True


if __name__ == "__main__":
    AdminListPage().main()
    
