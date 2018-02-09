#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
import sys, os, time
from phileas import _html40 as h

#import cgitb
#cgitb.enable()

from urllib.parse import urlparse, parse_qs

def text2modulename(text):
    prefix = ('_','')[text[0].isalpha()]
    return prefix+text.replace(' ','_').replace("'","__")
    
def modulename2text(name):
    return (name.lstrip('_')).replace('__',"'").replace("_"," ")

class Page(object):
    topDir = os.path.split(__file__)[0]
    styleSheet = "/.style/papa.css"
    errOutput = []
    dateTimeFormat = "%Y %b %d %a %H:%M"
    dateTime = None
    name = os.path.splitext(os.path.basename(__file__))[0]
    metaDict = {'http-equiv':"content-type", 'content':"text/html; charset=utf-8"}
    _title = None # => use basename of page as page title - unless overruled.

    def __init__(self, localIndex=None):
        self.localIndex = localIndex
        if self.dateTime is None:
            pTime = os.stat(sys.argv[0]).st_ctime,
            self.dateTime = time.strftime('%Y %b %d %a %H:%M', time.gmtime(*pTime))
        self.nameToPrint = modulename2text(
            os.path.splitext(os.path.split(sys.argv[0])[1])[0]
        )
        self.resolveData();

    def resolveData(self): #just a 'hook' at this level
        pass

    def title(self):
        return self._title or self.nameToPrint

    def href(self, url, text=None):
        return h.a(href=url) | (text or os.path.split(url)[1])

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
        print (
"(gratuitous 'error' output) current directory is:",
            os.getcwd(),
            file=sys.stderr
        )
        return ('€ default body of content',
                h.br,
                h.p | 'end of content'
        )

    def html(self):
        return h.html | (
            h.head | self.head(),
            #h.body | ( self.body())
            h.body | ( self.body(), h.pre | self.errOutput)
        )

    def present(self):
        #sys.stderr = self
        print ("Content-type: text/html;charset=UTF-8\n\n") # the blank line really matters!
        print (self.html())

    def asFileName(self, path):
        if path[0] != '/':
            return path
        return self.topDir + path

    def asUrl(self, fileName):
        if fileName[0] != '/':
            return fileName
        return fileName[len(self.topDir):]

def main(pageClass,  localIndex=None):
    uri = os.environ.get('REQUEST_URI')
    if uri:
        o = urlparse(uri)
        path = os.environ['DOCUMENT_ROOT'] + o.path # geturl()
        #print ("path=", path)
        if not os.path.isdir(path):
            path = os.path.split(path)[0]
        os.chdir(path)
        kw = parse_qs(o.query)
    else:
        pairs = [p.split('=') for p in sys.argv[1:]]
        #print (pairs)
        kw = dict(pairs)
    page = pageClass(localIndex=localIndex, **kw)
    if 1: # uri:
        sys.stderr = page
        print ("Content-type: text/html;charset=UTF-8\n\n") # the blank line really matters!
    print (page.html())

if __name__=="__main__":
    main(Page)
