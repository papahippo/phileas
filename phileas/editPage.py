#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os, time
from page import Page, h
from entity import EntityError
import cgi


class EditPage(Page):

    def validate(self, **kw):
        # validate_edit only comes into force for field-by-field-edit style page so maybe belongs in a
        # subclass
        self.filename, = kw.pop('filename_', ('?fn',))
        self.calling_script, = kw.pop('calling_script_', ('?cs',))
        self.line_ = list(map(int, kw.pop('line_', (-1, -1))))
        if not Page.validate(self, **kw):
            return False
        self.ee = None

        # we must avoid trying to create an entity which already exists according to the source file.
        self.EntityClass.by_range(self.line_).detach()
        # we usually need the following so let's get it done now.
        with open(self.filename, 'r') as module_src:
            self.all_lines = module_src.readlines()
        # the following method of dermining whether we're here as a from validator
        # is a bit stange but works.
        self.submitting = os.environ.get("REQUEST_METHOD") == "POST"
        if self.submitting and self.EntityClass:

            # So the user has finished editing an item which was taken from a page containing a list of such items.
            # If we're happy with his edit we return to that list page, otherwsie we stay on this page and helphim sort it out.
            #
            self.form = cgi.FieldStorage()
            requested_action = self.form.getfirst('button_')
            if requested_action in ('Add', 'Modify'):
                try:
                    # Retrieve the fields and values and use thses to create a new or replacement instance.
                    answers = [(mfs.name, mfs.value) for mfs in self.form.list if not mfs.name.endswith('_')]
                    self.new_instance = self.EntityClass(**dict(answers))
                except EntityError as ee:
                # except Exception as ee:
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
                            module_src.write(str(self.new_instance))
                        module_src.writelines(self.all_lines[self.line_[1]:])
                print("Location: " + self.href(self.calling_script, {}, "#%s" % self.line_[0]) + "\n\n")
                return  None
            else:
                return True
        else:
            item_string = ''.join(self.all_lines[slice(*self.line_)])
            print(item_string, file=sys.stderr)
            #print("Location: " + self.href('/testing/test3.py', {'item_string_': (str('item_string'),)}, "#%s" % self.line_[0]) + "\n\n")
            # return None
            self.new_instance = self.evaluate(item_string)
            return True

    def edit_pane(self):
        if 0:
            print(self.new_instance.__class__(), file=sys.stderr)
        existing = self.ee or self.new_instance.called != '(new member)'
        _, low_name = os.path.split(self.calling_script)
        return (
            h.form(action=low_name + '?language=%s' % self.language[0], method='post')| (
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
            value = getattr(self.new_instance, attr_name)
        return (h.label(For='%s' %attr_name)|displayed_name, '<input type = "text" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, value))

