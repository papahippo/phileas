#!/usr/bin/python3
# -*- encoding: utf8 -*-
import cgitb
cgitb.enable()
from list import ClubMembersListPage

class ClubEditableListPage(ClubMembersListPage):
    admin = 1


if __name__ == "__main__":
    ClubEditableListPage().main()
    
