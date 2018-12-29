#!/usr/bin/python3
# -*- encoding: utf8 -*-
from ..Members.membersPage import clubName, MembersPage, h


class AdminPage(MembersPage):
    _upperBanner = "%s - Administation zone" % clubName


