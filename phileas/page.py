#!/usr/bin/python3
# -*- encoding: utf8 -*-
from __future__ import print_function
import sys, os, time
from phileas import _html40 as h
from entity import EntityError
from entity.club import Member
import cgi
import cgitb
#cgitb.enable()

from urllib.parse import urlparse, parse_qs


def text2modulename(text):
    prefix = ('_', '')[text[0].isalpha()]
    return prefix + text.replace(' ', '_').replace("'", "__")


def modulename2text(name):
    return (name.lstrip('_')).replace('__', "'").replace("_", " ")


class Page(object):
    topDir = os.path.split(__file__)[0]
    styleSheet = "/.style/mew.css"
    errOutput = []
    dateTimeFormat = "%Y %b %d %a %H:%M"
    dateTime = None
    name = os.path.splitext(os.path.basename(__file__))[0]
    metaDict = {'http-equiv': "content-type", 'content': "text/html; charset=utf-8"}
    _title = None  # => use basename of page as page title - unless overruled.

    def __init__(self, localIndex=None):
        self.localIndex = localIndex
        try:
            if self.dateTime is None:
                pTime = os.stat(sys.argv[0]).st_ctime,
                self.dateTime = time.strftime('%Y %b %d %a %H:%M', time.gmtime(*pTime))
            self.nameToPrint = modulename2text(
                os.path.splitext(os.path.split(sys.argv[0])[1])[0])
        except FileNotFoundError:
            self.dateTime = self.nameToPrint = ''

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

        if self.validate(**kw):
            self.present()

    def validate_edit(self, valid_, **kw):
        self.ee = None
        self.filename, = kw.get('filename_', ('?fn',))
        self.calling_script, = kw.get('calling_script_', ('?cs',))
        self.line_ = list(map(int, kw.get('line_', (-1, -1))))
        self.EntityClass.by_range(self.line_).detach()
        # we usually need the following so let's get it done now.
        with open(self.filename, 'r') as module_src:
            self.all_lines = module_src.readlines()
        # the following method of dermining whether we're here as a from validator
        # is a bit stange but works.
        self.submitting = os.environ.get("REQUEST_METHOD") == "POST"
        if self.submitting:
            self.form = cgi.FieldStorage()
            requested_action = self.form.getfirst('button_')
            answers = [(mfs.name, mfs.value) for mfs in self.form.list if not mfs.name.endswith('_')]
            print(answers, file=sys.stderr)
            if requested_action in ('Add', 'Modify'):
                answers = [(mfs.name, mfs.value) for mfs in self.form.list if not mfs.name.endswith('_')]
                try:
                    self.new_member = Member(**dict(answers))
                    #self.new_member = self.EntityClass(**dict(answers))
                    # print("Location: " + self.href('/testing/test3.py', {'exc': ('None!',)}, "#%s" % self.line_[0]) + "\n\n")
                    # return  None
                #except EntityError as ee:
                except Exception as ee:
                    # except KeyError as ee:
                    print(ee, file=sys.stderr)
                    self.ee = ee
                    #print("Location: " + self.href('/testing/test3.py', {'exc': (str(ee),)}, "#%s" % self.line_[0]) + "\n\n")
                    #return None
            if self.ee is None:
                # incorporate the updated entry into the module:
                if requested_action != 'Cancel':
                    with open(self.filename, 'w') as module_src:
                        module_src.writelines(self.all_lines[:self.line_[requested_action=='Add']])
                        if requested_action != 'Delete':
                            module_src.write(str(self.new_member))
                        module_src.writelines(self.all_lines[self.line_[1]:])
                print("Location: " + self.href(self.calling_script, {}, "#%s" % self.line_[0]) + "\n\n")
                #print("Location: " + self.href('/testing/test3.py', {}, "#%s" % self.line_[0]) + "\n\n")
                return  None
            else:
                return valid_
        else:
            item_string = ''.join(self.all_lines[slice(*self.line_)])
            print(item_string, file=sys.stderr)
            #print("Location: " + self.href('/testing/test3.py', {'item_string_': (str('item_string'),)}, "#%s" % self.line_[0]) + "\n\n")
            # return None
            return item_string



    def edit_pane(self):
        existing = self.ee or self.new_member.called!='(new member)'
        print('edit.py?'+os.environ.get("QUERY_STRING"), file=sys.stderr)
        print(self.href('edit.py', {'line_': map(str, self.line_)}), file=sys.stderr)
        return (
            h.form(action='edit.py?' + os.environ.get("QUERY_STRING"), method='post')| (
            #h.form(action=self.href('edit.py', {'line_': map(str, self.line_)}), method='post')| (
            [self.entry_line(attr_name, self.gloss(displayed_name), self.gloss(placeholder))
             for (attr_name, displayed_name, placeholder) in self.fieldDisplay],
            [(ix_<2 or existing) and (h.input(type = "submit", name="button_", STYLE="background-color:%s" % colour, value=val_) | '')
             for ix_, (val_, colour) in enumerate((
                ("Cancel", "green"),
                (existing and "Modify" or "Add", "orange"),
                ("Delete", "red"),
            ))],
            h.br*2,
            h.a(STYLE="color:#ff0000;") | self.ee,
        ))


def main(pageClass, localIndex=None):
    # the use of this outer level main function is deprecated... but some pages (including my
    # entire business administration!) currently depend on it.
    pageClass(localIndex=localIndex).main()


if __name__ == "__main__":
    # old style...    main(Page)
    Page().main()
