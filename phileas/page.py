#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os, time
from phileas import _html40 as h
from entity import EntityError
import cgi
import cgitb
#cgitb.enable()

from urllib.parse import urlparse, parse_qs


class Page:
    topDir = os.path.split(__file__)[0]
    styleSheet = "/.style/mew.css"
    errOutput = []
    name = os.path.splitext(os.path.basename(__file__))[0]
    metaDict = {'http-equiv': "content-type", 'content': "text/html; charset=utf-8"}
    _title = None  # => use basename of page as page title - unless overruled.
    EntityClass = None  # only relevant for certain kinds of pages.

    def __init__(self, localIndex=None):
        self.localIndex = localIndex
        try:
            self.nameToPrint = modulename2text(
                os.path.splitext(os.path.split(sys.argv[0])[1])[0])
        except FileNotFoundError:
            self.nameToPrint = ''

        self.resolveData()

    def resolveData(self):
        """
'resolveData'is just a 'hook' at this level. Furthermore, its role has been largely taken over
by 'validate'.
"""
        pass

    def title(self):
        return self._title or self.nameToPrint

    def href(self, url=None, new_kw={}, hashtag=''):
        total_dict = {}
        total_dict.update(self.kw)
        total_dict.update(new_kw)
        if not url:
            url = self.script_name
        return (url + '?' +
                '&'.join(sum([([(key_+'='+val_) for val_ in val_list])
                         for key_, val_list in total_dict.items()], []))
                + hashtag
                )

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
            self.href("index.py", {'line_':['48', '53']}, '#42'),
            file=sys.stderr
        )
        return ('default body of content... abcdéf',
                h.br,
                h.p | 'end of content'
                )

    def html(self):
        return h.html | (
            h.head | self.head(),
            h.body(bgcolor='white') | (self.body(), h.pre | self.errOutput)
        )

    def validate(self, **kw):
        """
'validate' interprets the 'keywords' (actually cgi-parameters) passed to the page. It returns
True if this page is be presented. Alternatively it may cause some other page to be presented
and return False.
        """
        print('validate!', file=sys.stderr)
        self.language = kw.pop('language', ('EN',))
        self.kw = kw  # stub / base class version
        return True  # =>  # go ahead an prsent this page.

    def gloss(self, dikkie, sep='/'):
        if not isinstance(dikkie, dict):
            return dikkie  # just a string, I presume.
        return '/'.join([dikkie[taal] for taal in self.language])

    def present(self):
        sys.stderr = self
        print("Content-type: text/html;charset=UTF-8\n\n")  # the blank line really matters!
        print(str(self.html()).encode('ascii','xmlcharrefreplace').decode('ascii'))

    def asFileName(self, path):
        if path[0] != '/':
            return path
        return self.topDir + path

    def asUrl(self, fileName):
        if fileName[0] != '/':
            return fileName
        return fileName[len(self.topDir):]

    def main(self):
        self.uri = os.environ.get('REQUEST_URI')
        if self.uri:
            self.script_name = os.environ['SCRIPT_NAME']
            o = urlparse(self.uri)
            path = os.environ['DOCUMENT_ROOT'] + o.path  # geturl()
            if not os.path.isdir(path):
                path = os.path.split(path)[0]
            os.chdir(path)
            kw = parse_qs(o.query)
        else:
            self.script_name = sys.argv[0]
            kw = {}
            for p in sys.argv[1:]:
                key_, vals_ = p.split('=')
                kw[key_] = vals_.split(',')

        self.validated = self.validate(**kw)
        if self.validated:
            self.present()


if __name__ == "__main__":
    Page().main()
