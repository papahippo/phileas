from .membersPage import MembersPage
from .membersListPage import MembersListPage
from .memberViewPage import MemberViewPage

_membersPage = MembersPage()

_membersListPage = MembersListPage()
_membersPage.list = _membersListPage

_memberViewPage = MemberViewPage()
_membersPage.view_one = _memberViewPage
