#!/usr/bin/python3
# -*- encoding: utf8 -*-
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from entity.club import Member
#import mailgroups
#import members

from ..Members.memberViewPage import MemberViewPage
from . import _adminListPage

class MemberEditPage(MemberViewPage):
    _lowerBanner = "edit member details STUB"
    admin = True

    def back_to_list(self, **kw):
        return _adminListPage.index(**kw)
