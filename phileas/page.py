#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os, time
from phileas import _html40 as h
import cherrypy

class Page:
    topDir = os.path.split(__file__)[0]
    styleSheet = "/.style/mew.css"
    errOutput = []
    metaDict = {'http-equiv': "content-type", 'content': "text/html; charset=utf-8"}
    _title = '(untitled)'  # => use basename of page as page title - unless overruled.


    def title(self):
        return self._title

    def head(self):
        return h.meta(**self.metaDict) | (
            (self.styleSheet and
             h.link(type="text/css", rel="stylesheet",
                    href=self.styleSheet)),
            h.title | (h | self.title()),
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
            file=self
        )
        return ('default body of content... abcdéf',
                h.br,
                h.p | 'end of content'
                )

    @cherrypy.expose
    def index(self):
        yield  str(h.head | self.head())
        yield  str(h.body(bgcolor='white') | self.body())
        yield  str(h.pre | '\n'.join(self.errOutput))

    def index0(self):
        sys.stderr = self
        yield (str(self.html()))   # .encode('ascii','xmlcharrefreplace').decode('ascii'))

    def main(self, config=None):
        cherrypy.quickstart(self, config=config)


phileasConfig = os.path.join(os.path.dirname(__file__), 'phileas.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    Page().main(config=phileasConfig)
