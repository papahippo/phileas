#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
import cherrypy
from ...cherrypy import CherryPage, h, gloss, validator


clubName = "The Club"


class ClubPage(CherryPage):
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
    styleSheet = "/theClub.css"

    def upperBanner(self, *paths, **kw):
        return h.h1(id='upperbanner') | ('%s  - %s' %(clubName, gloss(EN="Public zone",
                                                                      NL="Openbare zone")))
    def lowerBanner(self, *paths, **kw):
        return h.h1(id='lowerbanner') | gloss(EN="Public Homepage",
                                              NL="Homepagina (openbaar)")

    def upperText(self):
        return (
            h.br, gloss(
EN=(
    "These web pages here contain information about 'The (fictitious) Club', divided into three zones:",
    h.ul |(
        h.li | ("The ", h.a(href=self.localRoot) | "public zone", " contains some general information. ",
             "This is avaliable ", self.languageLink('EN', 'in English (in het Engels)'),
             " and ", self.languageLink('NL', 'in Dutch(Nederlands)'), " - as is all this site "
             "- via these links. "
        ),
        h.li | ("The information in the ", h.a(href=self.localRoot+'members_zone') | "members zone",
            " and ", h.a(href=self.localRoot+'admin_zone') | "adminstration zone", " is only intended for authorized"
            " members. Hence these zones are protected by passwords."
            " Since this is a fictitious club, there's no harm in telling you that the relevant"
            " user names and passwords are visible in the source file of this page!"
                )
    ),
    "You are welcome to send feedback and enquiries regarding this supplemental site to ",
    h.a(href="mailto:hippostech@gmail.com?Subject=(sent%20via%20phileas/cherrypy%20sample%20page)") | "Larry Myerscough", h.br,
),
NL=(
    "Deze webpagina's bevatten aanvullende informatie, verdeeld over drie zones:",
    h.ul | (
        h.li | ("De ", h.a(href=self.localRoot) | "openbare zone", " bevat wat algemene informatie. ",
                "Dit is te bekijken ", self.languageLink('EN', 'in het Engels (in English)'),
                " and ", self.languageLink('NL', 'in het Nederlands (in Dutch)'),
                " door middel van deze links. "
                ),
        h.li | ("De inhoud van de ", h.a(href=self.localRoot + 'members_zone') | "leden zone",
                " en de ", h.a(href=self.localRoot + 'admin_zone') | "adminstratie zone", " is echter alleen bedoeld voor"
                " geauthoriseerde leden. Daarom zijn deze zones beveiligd met wachtwoorden."
                )
    ),
    "Met feedback en inlichtingen betreffend deze website kunt u terecht bij ",
    h.a(href="mailto:hippostech@gmail.com?Subject=(sent%20via%20phileas/cherrypy%20sample%20page)") | "Larry Myerscough",
    h.br,
),
                              ),
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
        return h.p | ( gloss(
EN=(
    """
    There is not much to see in this 'public zone. Actually, it's not much of a club.
    """
),
NL=(
    """
    Er is helaas weinig te zien in deze 'openbare zone'. Eigenlijk stelt de hele club weinig voor!
    """
)
                     ),
        )

clubPage = ClubPage()
