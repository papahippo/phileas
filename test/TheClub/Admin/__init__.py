from .adminPage import AdminPage
_adminPage = AdminPage()

from .adminListPage import AdminListPage
_adminListPage = AdminListPage()

from .memberEditPage import MemberEditPage
_memberEditPage = MemberEditPage()

_adminPage.list = _adminListPage
_adminPage.edit_one = _memberEditPage
