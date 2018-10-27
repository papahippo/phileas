import cherrypy
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

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    # _switch.main(config=phileasConfig)
    testConfig = os.path.join(os.path.dirname(__file__), 'test.conf')
    cherrypy.quickstart(_switch, config=testConfig)