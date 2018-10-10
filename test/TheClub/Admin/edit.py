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
        valid_ = self.validate_edit(ClubMembersPage.validate(self, **kw), **kw)
        if isinstance(valid_, str):
            self.new_instance = eval(valid_)
        return valid_

    def entry_line(self, attr_name, displayed_name, placeholder):
        colour = '#000000'  # black is default
        if self.submitting:
            value = self.form.getfirst(attr_name, '')
            if self.ee and attr_name == self.ee.key_:
                colour = '#ff0000'  # red = place of error
        else:
            value = getattr(self.new_instance, attr_name)
        return (h.label(For='%s' %attr_name)|displayed_name, '<input type = "text" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, value))

    def lowerText(self):
        return self.edit_pane()

if __name__ == "__main__":
    # print ("hello Larry")
    ClubAdminEditPage().main()
    
