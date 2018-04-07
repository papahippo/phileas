#!/usr/bin/python3
# -*- encoding: utf8 -*-
from clubPage import clubName, ClubPage, h
from entity.club import Member
import members


class ClubMembersPage(ClubPage):
    _upperBanner = h.h1 | "%s - Members zone" % clubName

if __name__ == "__main__":
    # print ("hello Larry")
    ClubMembersPage().main()
    
