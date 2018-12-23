#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
from phileas.page import Page, h
import cherrypy

clubName = "The Club"


class ClubPage(Page):
    _upperBanner = clubName
    upperBarColour = 'SlateBlue'  # '#6060f0'
    _lowerBanner = "(dummy 'Lower banner')"
    lowerBarColour = 'Orange'
    _synopsis = """dummy synopsis"""
    _detail = """dummy detail - this page is intended to be included, not displayed in itw own right!"""
    centreImage = None
    columns = None
    homePage = "/index.py"
    styleSheet = "/TheClub/the_club.css"

    @cherrypy.expose
    def index(self, **kw):
        cherrypy.session['index_url'] = cherrypy.url()
        kw.update(cherrypy.session.get('kw', {}))
        cherrypy.session['kw'] = {}
        self.kw = kw
        sys.stderr = self
        yield  str(h.head | self.head())
        yield  str(h.body(bgcolor='white') | self.body())
        yield  str(h.pre | '\n'.join(self.errOutput))

    @cherrypy.expose
    def set_language(self, language='??'):
        print(language)
        cherrypy.session['language'] = language
        cherrypy.session['kw'] = self.kw
        # redirect back to index tha twas on view before language select:
        raise cherrypy.HTTPRedirect(cherrypy.session['index_url'])

    def gloss(self, dikkie, sep='/'):
        if not isinstance(dikkie, dict):
            return dikkie  # just a string, I presume.
        return dikkie[cherrypy.session.setdefault('language', 'EN')]


    def main(self, config=None):
        cherrypy.quickstart(self, config=config)


    # our derived classes can esily use them.

    def synopsis(self):
        return self._synopsis

    def detail(self):
        return self._detail

    def rightPanel(self):
        return self._rightPanel

    def lowerBanner(self):
        return h.h1 | self._lowerBanner

    def upperBanner(self):
        return h.h1 | self._upperBanner

    def upperText(self):
        return (
            h.br, """
These pages represent an example of a web-site for a club or society. 
            """,
            h.br,
            h.br,
            """
Two languages are supported: English and Dutch. Only this section is shown in both together.
The language used for the rest of the pages can be chosen by the links here:
            """,h.br,h.br,
            h.center | (h.h4 | (
                [((h.a(href='/set_language?language=%s' % language_code)) | language_names, '&nbsp '*4)
                    for language_code, language_names in (
                      ('EN', "English/Engels"),
                      ('NL', "Nederlands/Dutch"),
                  )
                ]
            )),

            h.em | """
Twee talen worden ondersteund: Engels en Nederlands. Alleen deze kop is getoond in beide talen.
Welke taal wordt gebruikt voor de rest van de webpagina's mag geselelcteerd worden d.m.v. 
de links hierboven.
            """, h.br, h.br,

        )

    def colourBarBox(self, header, bgcolor, content):
        return (
            h.table(width="100%",cellpadding="0",
                            cellspacing="0")| (
                h.tr | (
                    h.th(bgcolor=bgcolor, valign="top") | (
                        h.font(color="#FFFFFF", size="2") | ( header),
                    ),
                ),
                h.tr | (
                    h.td | content,
                ),
            )
        )

    def lowerText(self):
        return (
            h | self.synopsis(),
            h | self.detail()
        )
    

    def body(self):
        return (
            self.colourBarBox(self.upperBanner(), self.upperBarColour,
                    h | self.upperText()),
            self.colourBarBox(self.lowerBanner(), self.lowerBarColour,
                    h | self.lowerText()),
    )
theClubConf = os.path.join(os.path.dirname(__file__), 'theClub.conf')

_clubPage = ClubPage()

if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    _clubPage.main()
