import cherrypy
from cherrypy.lib import auth_basic
from ..page import Page, h
import sys, os


def gloss0(dikkie, sep='/'):
    if not isinstance(dikkie, dict):
        return dikkie  # just a string, I presume.
    return dikkie[cherrypy.session.setdefault('language', 'EN')]

def gloss(s="(can't translate!)", **kw):
    return kw.get(cherrypy.session.setdefault('language', 'EN'), s)


def validator(dick):
    def validate_password(realm, username, password):
        if username in dick and dick[username] == password:
            return True
        return False
    return validate_password


class CherryPage(Page):
    _title = "philes/cherrypy example page"
    _upperBanner = _title
    upperBarColour = 'SlateBlue'  # '#6060f0'
    _lowerBanner = "club details"
    lowerBarColour = 'Orange'
    _synopsis = """dummy synopsis"""
    _detail = """dummy detail - this page is intended to be included, not displayed in its own right!"""
    centreImage = None
    columns = None
    homePage = "/index.py"
    localRoot = '/'
    styleSheet = '/cherryPage.css'

    def upperBanner(self, *paths, **kw):
        yield from (h.h1(id='upperbanner') |self._upperBanner)

    def lowerBanner(self, *paths, **kw):
        yield from (h.h1(id='lowerbanner') |self._lowerBanner)

    @cherrypy.expose
    def set_language(self, language='??'):
        print(language)
        cherrypy.session['language'] = language
        # cherrypy.session['kw'] = self.kw
        # redirect back to index tha twas on view before language select:
        raise cherrypy.HTTPRedirect(cherrypy.session['index_url'])

    @cherrypy.expose
    def index(self, *paths, **kw):
        yield from self.present(self.lowerBanner, self.lowerText, *paths, **kw)

    def present(self, bannerFunc, textFunc, *paths, **kw):
        url = cherrypy.session.get('current_url')
        print('present: session[current_ur]=', url, 'kw=', kw)
        if url is True:
            # special case, coming from e.g.(?) language change.
            kw = cherrypy.session.get('current_kw', {})
        else:
            # normal case, coming from url which generated content.
            cherrypy.session['current_kw'] = kw
        cherrypy.session['current_url'] = cherrypy.url()
        sys.stderr = self
        yield from (h.head | self.head())
        yield from (h.body | self.body(bannerFunc, textFunc, *paths, **kw))
        yield from (h.pre | '\n'.join(self.errOutput))

    @cherrypy.expose
    def set_session(self, key_, value_, **kw):
        print('key_', key_, 'value+', value_)
        cherrypy.session[key_] = value_
        url = cherrypy.session['current_url']
        cherrypy.session['current_url'] = True
        raise cherrypy.HTTPRedirect(url)

    def body(self, bannerFunc, textFunc, *p, **kw):
        yield from (self.colourBarBox(self.upperBanner(), self.upperBarColour,
                    h | self.upperText()))
        yield from (self.colourBarBox(bannerFunc(*p,  **kw), self.lowerBarColour,
                    h | textFunc(*p, **kw)))

    def languageLink(self, language_code, language_text):
        return h.a(href=self.localRoot + 'set_session/language/' + language_code) | language_text

    def upperText(self):
        return (
            h.br, gloss(
                EN=(

                    "This content is determined by the 'upperText' member function of the page class.",
                    h.br,
                    h.br,
                ),
                NL=(

                    "Deze inhouod wordt bepaald door de 'upperText' member function van de page class.",
                    h.br,
                    h.br,
                ),
            ),
            h.br,
        )
    def lowerText(self):
        return (
            h.br, gloss(
                EN=(

                    "This content is determined by the 'lowerText' member function of the page class.",
                    h.br,
                    h.br,
                ),
                NL=(

                    "Deze inhouod wordt bepaald door de 'lowerText' member function van de page class.",
                    h.br,
                    h.br,
                ),
            ),
            h.br,
        )

    def colourBarBox(self, header, bgcolor, content):
        yield from h | (
            h.table | (
                h.tr | (
                    h.th | (
                       ( header),
                    ),
                ),
                h.tr | (
                    h.td | content,
                ),
            )
        )

    def lowerText(self, *p,  **kw):
        # print('lowerText', file=self)
        yield from h | (
             h.p | ( gloss(EN=
"""
Body of web-page goes here!
""",
                            NL=
"""
Echte webinoud komt hier terecht!
""",
                            )
                     ),
        )

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    # _switch.main(config=phileasConfig)
    #testConfig = os.path.join(os.path.dirname(__file__), 'test.conf')

    from .TheClub import _indexPage
    _cherryPage = CherryPage()
    _cherryPage.TheClub = _indexPage
    print(_cherryPage.TheClub)
    SESSION_PATH = '/home/gill//tmp/sessions'
    os.makedirs(SESSION_PATH, exist_ok=True)
    config = {
    'global':
    {
    'server.socket_host': "127.0.0.1",
    'server.socket_port': 8080,
    'server.thread_pool': 10,
    },
    '/':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "/home/gill/PycharmProjects/phileas/phileas/cherrypy/static",
            'tools.sessions.on': True,
            'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            'tools.sessions.storage_path': SESSION_PATH,
            'tools.sessions.timeout': 10,
        },
    '/TheClub/members_zone': {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': validator({'club': 'biscuit'}),
            'tools.auth_basic.accept_charset': 'UTF-8',
        },
    '/TheClub/admin_zone': {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': validator({'Admin': 'istrator'}),
            'tools.auth_basic.accept_charset': 'UTF-8',
        },
    }

    cherrypy.quickstart(_cherryPage, config=config)
