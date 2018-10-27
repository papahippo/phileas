#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os, time
from phileas import _html40 as h
import cherrypy

class Page:
    topDir = os.path.dirname(__file__)
    styleSheet = "/.style/the_club0.css"
    errOutput = []
    name = os.path.splitext(os.path.basename(__file__))[0]
    metaDict = {'http-equiv': "content-type", 'content': "text/html; charset=utf-8"}
    _title = '(untitled)' # => use basename of page as page title - unless overruled.
    EntityClass = None  # only relevant for certain kinds of pages.


    def head(self):
        return h.meta(**self.metaDict) | (
            (self.styleSheet and
             h.link(type="text/css", rel="stylesheet",
                    href=self.styleSheet)),
            h.title | (h | self._title),
        )

    def write(self, s):
        """ We provide our own 'write' function so that we can handle
        our own standard error output.
        """
        self.errOutput.append(str(s))

    def body(self):
        #return "abcdé".encode('ascii','xmlcharrefreplace').decode('ascii')
        print(
            "(gratuitous 'error' output) current directory is:",
            os.getcwd(),
            # self.href("index.py", {'line_':['48', '53']}, '#42'),
            file=sys.stderr
        )
        return ('default body of content... abcdéf',
                h.br,
                h.p | 'end of content'
                )

    @cherrypy.expose
    def validate(self, **kw):
        return self.index(**kw)  # STUB!

    def html(self):
        return h.html | (
            h.head | self.head(),
            h.body(bgcolor='white') | (self.body(), h.pre | self.errOutput)
        )

    def gloss(self, dikkie, sep='/'):
        if not isinstance(dikkie, dict):
            return dikkie  # just a string, I presume.
        return dikkie[cherrypy.session.setdefault('language', 'EN')]


    @cherrypy.expose
    def index(self, **kw):
        self.kw = kw
        sys.stderr = self
        # print("Content-type: text/html;charset=UTF-8\n\n")  # the blank line really matters!
        # print(str(self.html()).encode('ascii','xmlcharrefreplace').decode('ascii'))
        return (str(self.html()).encode('ascii','xmlcharrefreplace').decode('ascii'))

    def main(self):
        return cherrypy.quickstart(self, config=os.path.join(self.topDir, 'theClub.conf'))

class HomePage(Page):
    pass

theClubConf = os.path.join(os.path.dirname(__file__), 'theClub.conf')

if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    HomePage().main()
