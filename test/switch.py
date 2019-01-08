import cherrypy
from cherrypy.lib import auth_basic
from phileas.page import Page, h
import TheClub
import sys, os

class Switch(Page):
    styleSheet = 'test.css'

    @cherrypy.expose
    def index(self, **kw):
        cherrypy.session['index_url'] = cherrypy.url()
        kw.update(cherrypy.session.get('kw', {}))
        cherrypy.session['kw'] = {}
        self.kw = kw
        sys.stderr = self
        yield  str(h.head | self.head())
        yield  str(h.body | self.body())
        yield  str(h.pre | '\n'.join(self.errOutput))

    @cherrypy.expose
    def set_language(self, language='??'):
        print(language)
        cherrypy.session['language'] = language
        # cherrypy.session['kw'] = self.kw
        # redirect back to index tha twas on view before language select:
        raise cherrypy.HTTPRedirect(cherrypy.session['index_url'])

    def gloss(self, dikkie, sep='/'):
        if not isinstance(dikkie, dict):
            return dikkie  # just a string, I presume.
        return dikkie[cherrypy.session.setdefault('language', 'EN')]


    def main(self, config=None):
        cherrypy.quickstart(self, config=config)

    def body(self):
        return h.p | ("hurrah for Cherrypy!", h.br,
                      "This top-level page is (so far!) simply a place holder for other pages to sit under.",
                      )

_switch = Switch()
_switch.TheClub = TheClub._indexPage
print(_switch.TheClub)
_switch.me = _switch


def validator(dick):
    def validate_password(realm, username, password):
        if username in dick and dick[username] == password:
            return True
        return False
    return validate_password

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    # _switch.main(config=phileasConfig)
    #testConfig = os.path.join(os.path.dirname(__file__), 'test.conf')


    config = {
    'global':
    {
    'server.socket_host': "192.168.2.6",
    'server.socket_host': "127.0.0.1",
    'server.socket_port': 8080,
    'server.thread_pool': 10,
    },
    '/':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "/home/gill/PycharmProjects/phileas/test",
            'tools.sessions.on': True,
            'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            'tools.sessions.storage_path': 'sessions',
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

    cherrypy.quickstart(_switch, config=config)
