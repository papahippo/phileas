from phileas.page import Page, h
from TheClub.clubPage import ClubPage
import sys, os

class Switch(Page):
    styleSheet = 'test.css'

    def body(self):
        return h.p | ("hurrah for Cherrypy!", h.br,
                      "This top-level page is (so far!) simply a place holder for other pages to sit under.",
                      )

phileasConfig = os.path.join(os.path.dirname(__file__), 'test.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    switch = Switch()
    switch.TheClub = ClubPage()
    switch.main(config=phileasConfig)
