from .indexPage import IndexPage
from .Members import _membersPage
from .Admin import _adminPage
_indexPage = IndexPage()
_indexPage.Members = _membersPage
_indexPage.Admin = _adminPage
