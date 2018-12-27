#!/usr/bin/python3
# -*- encoding: utf8 -*-
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from ..Members.memberViewPage import MemberViewPage
from . import _adminListPage

class MemberEditPage(MemberViewPage):
    _lowerBanner = "edit member details"
    admin = True
