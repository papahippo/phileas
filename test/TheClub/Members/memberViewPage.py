#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
#import locale
#locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from entity.club import Member, EntityError
from .mailgroups import *
from . import members

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
        cherrypy.session['chosen_instance'] = key, (key and self.EntityClass.by_key(key) or self.EntityClass())
        self.exception_ = exception_
        return MembersPage.index(self, **kw)


    @cherrypy.expose
    def validate(self, button_=None, **kw):
        """
This is where validate a members details form, or simply recognize a 'cancel' (which can also happen view mode).
        """
        self.ee = None
        if button_ not in ('Cancel',):
            key, instance = cherrypy.session['chosen_instance']
            if button_ not in ('Add'):
                instance.detach()
            if button_ in ('Add', 'Modify'):
                try:
                    # Retrieve the fields and values and use these to create a new or replacement instance.
                    self.new_instance = self.EntityClass(**kw)
                except EntityError as ee:
                    return self.index(exception_=ee)
            # incorporate the updated entry into the module:
            # rough and ready try-out!
            import_stuff = ''
            with open(members.__file__, 'r') as members_file:
                while True:
                    line_ = members_file.readline()
                    if not (len(line_)<2 or line_[0]=='#' or line_.split(' ')[0] in ['from', 'import'] ):
                        break
                    import_stuff += line_
            with open(members.__file__, 'w') as updated_module_file:
            #with open('updated_members.py', 'w') as updated_module_file:
                updated_module_file.write(import_stuff)
                Member.export(updated_module_file)

        return self.back_to_list(**kw)

    def back_to_list(self, **kw):
        return _membersListPage.index(**kw)

    def lowerText(self):
        return self.edit_pane()

    # edit_pane was previously far more generic - and may become so again soon!
    def edit_pane(self, name=None, **kw):
        key, instance = cherrypy.session['chosen_instance']
        colour = '#000000'  # black is default
        if 0:
            print(self.new_instance.__class__(), file=self)
        self.ee = None  # STUB!
        return (
            #h.form(action=self.admin and 'edit_one' or 'view_one', method='get')| (
            h.form(action='./validate', method='get')| (
            [   (h.label(For='%s' %attr_name)|self.gloss(displayed_name), '<input type = "text" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, getattr(instance, attr_name)))
             for (attr_name, displayed_name, placeholder) in self.fieldDisplay],

            [(ix_<2 or key) and (h.input(type = "submit", name="button_", STYLE="background-color:%s" % colour, value=val_) | '')
             for ix_, (val_, colour) in enumerate((
                ("Cancel", "green"),
                (key and "Modify" or "Add", "orange"),
                ("Delete", "red"),
            )[:self.admin and 3 or 1])],
            h.br*2,
            h.a(STYLE="color:#ff0000;") | self.ee,
        ))


if __name__ == "__main__":
    # print ("hello Larry")
    MemberViewPage().main()
    
