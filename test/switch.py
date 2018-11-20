import cherrypy
from cherrypy.lib import auth_basic
from phileas.page import Page, h
import TheClub
import sys, os

class Switch(Page):
    styleSheet = 'test.css'

    def body(self):
        return h.p | ("hurrah for Cherrypy!", h.br,
                      "This top-level page is (so far!) simply a place holder for other pages to sit under.",
                      )

_switch = Switch()
_switch.TheClub = TheClub._indexPage


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
        { 'tools.staticdir.on': True,
          'tools.staticdir.dir': "/home/gill/PycharmProjects/phileas/test"
          },
    '/TheClub/Members': {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': validator({'MEW': '@1945'}),
            'tools.auth_basic.accept_charset': 'UTF-8',
        },
    '/TheClub/Admin': {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': validator({'gill': 'Cr4covia'}),
            'tools.auth_basic.accept_charset': 'UTF-8',
        },
    }

    cherrypy.quickstart(_switch, config=config)
