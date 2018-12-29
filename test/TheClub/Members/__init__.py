from .membersPage import MembersPage
_membersPage = MembersPage()

from .membersListPage import MembersListPage
_membersListPage = MembersListPage()

from .memberViewPage import MemberViewPage
_memberViewPage = MemberViewPage()

_membersPage.list = _membersListPage
_membersPage.view_one = _memberViewPage
