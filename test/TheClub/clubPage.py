#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
from phileas.page import Page, h
import cherrypy


clubName = "The Club"

def gloss(dikkie):
    if not isinstance(dikkie, dict):
        return dikkie  # just a string, I presume.
    return dikkie[cherrypy.session.setdefault('language', 'EN')]


class ClubPage(Page):
    _title = clubName
    _upperBanner = clubName
    upperBarColour = 'SlateBlue'  # '#6060f0'
    _lowerBanner = "club details"
    lowerBarColour = 'Orange'
    _synopsis = """dummy synopsis"""
    _detail = """dummy detail - this page is intended to be included, not displayed in its own right!"""
    centreImage = None
    columns = None
    homePage = "/index.py"
    localRoot = '/TheClub/'
    styleSheet = localRoot + "the_club.css"

    def _cp_dispatch(self, vpath):
        print ('vpath', vpath)

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
        yield str(h.head | self.head())
        yield str(h.body | self.body(bannerFunc(*paths, **kw), textFunc(*paths, **kw)))
        yield str(h.pre | '\n'.join(self.errOutput))

    @cherrypy.expose
    def set_session(self, key_, value_, **kw):
        print('key_', key_, 'value+', value_)
        cherrypy.session[key_] = value_
        url = cherrypy.session['current_url']
        cherrypy.session['current_url'] = True
        raise cherrypy.HTTPRedirect(url)

    def upperBanner(self, *paths, **kw):
        return h.h1(id='upperbanner') | ('%s - (supplemental) - %s' %(clubName,
                                   gloss({'EN': "Public zone",
                                               'NL': "Openbare zone"})))
    def lowerBanner(self, *paths, **kw):
        return h.h1(id='lowerbanner') | gloss({'EN': "Public Homepage",
                                  'NL': "Homepagina (openbaar)"})

    def languageLink(self, language_code, language_text):
        return h.a(href=self.localRoot+'set_session/language/'+language_code) | language_text

    def upperText(self):
        return (
            h.br, gloss({
'EN': (
    "You are urged to visit ",
     h.a(href="http://www.muziekverenigingeindhovenwest.nl") | "MEW's official website",
    " if you haven't done so already. There you can find a wealth of information about MEW, "
    "including our agenda for the coming months and some Youtube clips. "
    "These web pages here contain supplementary information, divided into three zones:",
    h.ul |(
        h.li | ("The ", h.a(href=self.localRoot) | "public zone", " contains some general information. ",
             "This is avaliable ", self.languageLink('EN', 'in English (in hetEngels)'),
             " and ", self.languageLink('NL', 'in Dutch(Nederlands)'), " - as is all this supplementary site "
             "- via these links. This is aimed at bringing MEW to the attention of a wider public,"
             "including Eindhoven's diverse expat community."
        ),
        h.li | ("The information in the ", h.a(href=self.localRoot+'members_zone') | "members zone",
            " and ", h.a(href=self.localRoot+'admin_zone') | "adminstration zone", " is only intended for authorized"
            " MEW members. Hence these zones are protected by passwords."
            )
    ),
    "You are welcome to send feedback and enquiries regarding this supplemental site to ",
    h.a(href="mailto:hippostech@gmail.com?Subject=(sent%20via%20MEW%20supplemental%20website)") | "Larry Myerscough", h.br,
),
'NL': (
    "Deze webpagina's bevatten aanvullende informatie, verdeeld over drie zones:",
    h.ul | (
        h.li | ("De ", h.a(href=self.localRoot) | "openbare zone", " bevat wat algemene informatie. ",
                "Dit is te bekijken ", self.languageLink('EN', 'in het Engels (in English)'),
                " and ", self.languageLink('NL', 'in het Nederlands (in Dutch)'),
                " door middel van deze links. "
                "Dit is bedoeld om aandacht voor MEW to trekken vanuit een breder publiek, inclusief "
                "de diverse expat gemeenschap van Eindhoven."
                ),
        h.li | ("De inhoud van de ", h.a(href=self.localRoot + 'members_zone') | "leden zone",
                " en de ", h.a(href=self.localRoot + 'admin_zone') | "adminstratie zone", " is echter alleen bedoeld voor"
                " geauthoriseerde MEW leden. Daarom zijn deze zones beveiligd met wachtwoorden."
                )
    ),
    "Met feedback en inlichtingen betreffend deze aanvullende website kunt u terecht bij ",
    h.a(href="mailto:hippostech@gmail.com?Subject=(sent%20via%20MEW%20supplemental%20website)") | "Larry Myerscough",
    h.br,
),
                              }),
            h.br,
        )

    def colourBarBox(self, header, bgcolor, content):
        return (
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

    def lowerText(self, **kw):
        return (
             h.p | ( gloss({'EN':
"""
There is not much to see in this 'public zone' yet! I'll be working on it in the coming weeks.
Meanwhile, Please go to the main site or, if authorized, the members' zone, via the links above.
""",
                            'NL':
"""
Er is helaas nog weinig te zien in deze 'openbare zone'! Ik ga eraan werken in de komende weken.
In de tussentijd, ga naar de hoofdsitde of, mocht u geauthoiriseerd zijn, naar de ledenzone,
d.m.v. de links hierboven. 
""",

                            })
                     ),
        )

    def body(self, banner, text):
        return (
            self.colourBarBox(self.upperBanner(), self.upperBarColour,
                    h | self.upperText()),
            self.colourBarBox(banner, self.lowerBarColour,
                    h | text),
    )

_clubPage = ClubPage()
