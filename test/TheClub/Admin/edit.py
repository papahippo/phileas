#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
import cgi, cgitb
cgitb.enable()
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from entity.club import Member, EntityError
import mailgroups
import members

from membersPage import ClubMembersPage, h

class ClubAdminEditPage(ClubMembersPage):
    EntityClass = Member
    _lowerBanner = "edit member details"

    def validate(self, **kw):
        return self.validate_edit(ClubMembersPage.validate(self, **kw), **kw)

    def validate_edit(self, valid_, **kw):
        self.ee = None
        self.filename, = kw.get('filename', ('?fn',))
        self.calling_script, = kw.get('calling_script', ('?cs',))
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
            if requested_action in ('Add', 'Modify'):
                answers = [(mfs.name, mfs.value) for mfs in self.form.list if not mfs.name.endswith('_')]
                #print('ff', file=sys.stderr)
                try:
                    self.new_member = self.EntityClass(**dict(answers))
                except EntityError as ee:
                    print(ee, file=sys.stderr)
                    self.ee = ee
            if self.ee is None:
                # incorporate the updated entry into the module:
                if requested_action != 'Cancel':
                    with open(self.filename, 'w') as module_src:
                        module_src.writelines(self.all_lines[:self.line_[requested_action=='Add']])
                        if requested_action != 'Delete':
                            module_src.write(str(self.new_member))
                        module_src.writelines(self.all_lines[self.line_[1]:])
                #ClubMembersPage.validate(self, **kw)
                print("Location: " + self.href(self.calling_script, {}, "#%s" % self.line_[0]) + "\n\n")
                #print("Location: editable_list.py#%s\n\n" % self.line_[0])
                return None
        else:
            #self.EntityClass.by_range(self.line_).detach()
            item_string = ''.join(self.all_lines[slice(*self.line_)])
            #print(item_string, file=sys.stderr)
            self.new_member = eval(item_string)
        return valid_


    def entry_line(self, attr_name, displayed_name, placeholder):
        colour = '#000000'  # black is default
        if self.submitting:
            value = self.form.getfirst(attr_name, '')
            if self.ee and attr_name == self.ee.key_:
                colour = '#ff0000'  # red = place of error
        else:
            value = getattr(self.new_member, attr_name)
        return (h.label(For='%s' %attr_name)|displayed_name, '<input type = "text" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, value))

    def lowerText(self):
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
if __name__ == "__main__":
    # print ("hello Larry")
    ClubAdminEditPage().main()
    
