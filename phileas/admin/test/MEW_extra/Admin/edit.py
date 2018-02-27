#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
import cgi, cgitb
cgitb.enable()
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from phileas.admin import Lid, EntityError
import MEW.mailgroups

from page import *
MEW_members_file = './MEW/members.py'
import subprocess

class MEW_AdminEditPage(Page):

    def validate(self, line_=(-1, -1), **kw):
        self.ee = None
        self.line_= list(map(int, line_))

        # we usually need the following so let's get it done now.
        with open(MEW_members_file, 'r') as module_src:
            self.all_lines = module_src.readlines()
        #print(self.all_lines, file=sys.stderr)
        # the following method of dermining whether we're here as a from validator
        # is a bit stange but works.
        self.submitting = os.environ.get("REQUEST_METHOD") == "POST"
        if self.submitting:
            self.form = cgi.FieldStorage()
            requested_action = self.form.getfirst('button_')
            if requested_action == 'Submit':
                answers = [(mfs.name, mfs.value) for mfs in self.form.list if not mfs.name.endswith('_')]
                #print(answers, file=sys.stderr)
                try:
                    self.lid_ = Lid(**dict(answers))
                except EntityError as ee:
                    print(ee, file=sys.stderr)
                    self.ee = ee
            if self.ee is None:
                # incorporate the updated entry into the module:
                if requested_action != 'Cancel':
                    with open(MEW_members_file, 'w') as module_src:
                        module_src.writelines(self.all_lines[:self.line_[0]])
                        if requested_action != 'Delete':
                            module_src.write(str(self.lid_))
                        module_src.writelines(self.all_lines[self.line_[1]:])
                # from index import MEW_AdminIndexPage
                # pg = MEW_AdminIndexPage()
                # pg.main()
                # sys.exit(0)
                subprocess.run('./index.py')
                return None
        else:
            item_string = ''.join(self.all_lines[slice(*self.line_)])
            #print(item_string, file=sys.stderr)
            self.lid_ = eval(item_string)

        return Page.validate(self, **kw)


    def entry_line(self, displayed_name, attr_name, placeholder):
        colour = '#000000'  # black is default
        if self.submitting:
            value = self.form.getfirst(attr_name, '')
            if self.ee and attr_name == self.ee.key_:
                colour = '#ff0000'  # red = place of error
        else:
            value = getattr(self.lid_, attr_name)
        return (h.label(For='%s' %attr_name)|displayed_name, '<input type = "text" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, value))
    def body(self):
        #print(lid_, file=sys.stderr)
        return (
            h.form(action='edit.py?'+os.environ.get("QUERY_STRING"), method='post')| (
            [self.entry_line(displayed_name, attr_name, placeholder)
             for (displayed_name, attr_name, placeholder) in (
                 ('roepnaam', 'called', 'bekend binnen MEW als...'),
                 ('naam', 'name', 'surname, initials'),
                 ('huisadres', 'streetAddress', 'e.g. Rechtstraat 42'),
                 ('postcode', 'postCode', 'e.g. 1234 XY'),
                 ('gemeente', 'cityAddress', 'e.g. Eindhoven'),
                 ('telefoon', 'phone', 'e.g. 040-2468135'),
                 ('mobiel', 'mobile', 'e.g. 06-24681357'),
                 ('1e emailadres', 'emailAddress', 'e.g. fred@backofthe.net'),
                 ('evt. 2e emailadress', 'altEmailAddress', 'optional'),
                 ('geboortedatum', 'birthDate', 'e.g. 15-mrt-1963'),
                 ('lidmaatschap datum', 'memberSince', 'e.g. 15-okt-2003'),
            )],
            [(h.input(type = "submit", name="button_", STYLE="background-color:%s" % colour, value=val_) | '')
             for val_, colour in (
                ("Cancel", "green"),
                ("Submit", "orange"),
                ("Delete", "red"),
            )],

            h.a(STYLE="color:#ff0000;") | self.ee
        ))
        # return (h | 'stub for body of MEW_AdminEditPage')
if __name__ == "__main__":
    # print ("hello Larry")
    MEW_AdminEditPage().main()
    
