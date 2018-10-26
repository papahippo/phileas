from .adminPage import AdminPage
from .adminListPage import AdminListPage
from .memberEditPage import MemberEditPage

_adminPage = AdminPage()

_adminListPage = AdminListPage()
_adminPage.list = _adminListPage

_memberEditPage = MemberEditPage()
_adminPage.edit_one = _memberEditPage
