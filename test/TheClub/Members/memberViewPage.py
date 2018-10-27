#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
#import locale
#locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from entity.club import Member, EntityError
from .mailgroups import *
from .members import *

from .membersPage import MembersPage, h
from . import _membersListPage
import cherrypy

## class MemberViewPage(EditPage, MembersPage):
class MemberViewPage(MembersPage):

    EntityClass = Member
    _lowerBanner = "view member details (STUB!)"
    admin = False

    @cherrypy.expose
    def index(self, key=None, exception_=None, **kw):
        """
This is where we handle an 'edit' or 'new'(key=None) URL-click in a list of members.
        """
        self.chosen_instance = key and self.EntityClass.by_key(key)
        self.exception_ = exception_
        return MembersPage.index(self, **kw)


    @cherrypy.expose
    def validate(self, button_=None, **kw):
        """
This is where validate a members details form, or simply recognize a 'cancel' (which can also happen view mode).
        """
        self.ee = None
        if button_ not in ('Cancel',):
            self.chosen_instance.detach()
            if button_ in ('Add', 'Modify'):
                try:
                    # Retrieve the fields and values and use these to create a new or replacement instance.
                    self.new_instance = self.EntityClass(**kw)
                except EntityError as ee:
                    return self.index(exception_=ee)
            # incorporate the updated entry into the module:
            # rough and ready try-out!
            with open('updated_members.py', 'w') as updated_module_source:
                pass

        return self.back_to_list(**kw)

    def back_to_list(self, **kw):
        return _membersListPage.index(**kw)

    def lowerText(self):
        return self.edit_pane()

    # edit_pane was previously far more generic - and may become so again soon!
    def edit_pane(self, name=None, **kw):
        if 0:
            print(self.new_instance.__class__(), file=self)
            existing = self.ee or self.new_instance.called != '(new member)'
        self.ee = None  # STUB!
        existing = True  # STUB!
        self.submitting = False  # STUB!
        return (
            #h.form(action=self.admin and 'edit_one' or 'view_one', method='get')| (
            h.form(action='./validate', method='get')| (
            [self.entry_line(attr_name, self.gloss(displayed_name), self.gloss(placeholder))
             for (attr_name, displayed_name, placeholder) in self.fieldDisplay],

            [(ix_<2 or existing) and (h.input(type = "submit", name="button_", STYLE="background-color:%s" % colour, value=val_) | '')
             for ix_, (val_, colour) in enumerate((
                ("Cancel", "green"),
                (existing and "Modify" or "Add", "orange"),
                ("Delete", "red"),
            )[:self.admin and 3 or 1])],
            h.br*2,
            h.a(STYLE="color:#ff0000;") | self.ee,
        ))

    def entry_line(self, attr_name, displayed_name, placeholder):
        colour = '#000000'  # black is default
        if self.submitting:
            value = self.form.getfirst(attr_name, '')
            if self.ee and attr_name == self.ee.key_:
                colour = '#ff0000'  # red = place of error
        else:
            value = getattr(self.chosen_instance, attr_name)
        return (h.label(For='%s' %attr_name)|displayed_name, '<input type = "text" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, value))


if __name__ == "__main__":
    # print ("hello Larry")
    MemberViewPage().main()
    
