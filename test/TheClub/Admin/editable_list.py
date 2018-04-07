#!/usr/bin/python3
# -*- encoding: utf8 -*-
from list import ClubMembersListPage

class ClubEditableListPage(ClubMembersListPage):
    admin = 1


if __name__ == "__main__":
    ClubEditableListPage().main()
    
