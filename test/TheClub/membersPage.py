#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
from collections import OrderedDict
from .clubPage import clubName, ClubPage, h
from entity.club import Member, EntityError
from .mailgroups import *
from . import members
import cherrypy

def strRef(text):
    def fn(stringList):
        return  h.br.join([h.a(href=text + string) | string for string in stringList])
    return fn


#def mailStr(mailAddressList):
#    return h.br.join([h.a(href='mailto:'+mailAddress) | mailAddress for mailAddress in mailAddressList])


class MembersPage(ClubPage):
    EntityClass = Member
    admin = False
    fieldDisplay = OrderedDict([
# python name       # heading for glossing                              # field entry tip for glossing
('called',          ({'EN':'known as',         'NL':'roepnaam'},         {'EN': 'known within MEW as...', 'NL': 'bekend binnen MEW als...'})),
('name',            ({'EN':'full name',        'NL':'naam'},             {'EN': 'surname, initials',      'NL': 'achternaam, initielen'})),
('streetAddress',   ({'EN':'street address',   'NL':'adres'},            {'EN': 'e.g. Rechtstraat 42',    'NL': 'b.v. Rechtstraat 42'})),
('postCode',        ({'EN':'post code',        'NL':'postcode'},         {'EN': 'e.g. 1234 XY',           'NL': 'b.v. 1234 XY'})),
('cityAddress',     ({'EN':'Town/City',        'NL':'gemeente'},         {'EN': 'e.g. Eindhoven',         'NL': 'b.v. Eindhoven'})),
('phone',           ({'EN':'telephone',        'NL':'telefoon'},         {'EN': 'e.g. 040-2468135',       'NL': 'b.v. 040-2468135'})),
('mobile',          ({'EN':'mobile',           'NL':'mobiel'},           {'EN': 'e.g. 06-24681357',       'NL': 'b.v. 06-24681357'})),
('emailAddress',    ({'EN':'email address(es)','NL':'email addres(sen)'},{'EN': 'e.g. 06-24681357',       'NL': 'b.v. 06-24681357'})),
('birthDate',       ({'EN':'date of birth',    'NL':'geboortedtatum'},   {'EN': 'e.g. 15-mrt-1963',       'NL': 'b.v. 15-mrt-1963'})),
('memberSince',     ({'EN':'date of joining',  'NL':'lid sinds'},        {'EN': 'e.g. 15-okt-2003',       'NL': 'b.v. 15-okt-2003'})),
('instrument',      ({'EN':'instrument',       'NL':'instrument'},       {'EN': 'e.g. Clarinet',          'NL': 'b.v. Klarinet'})),
#('altEmailAddress', 'opt. 2nd email address', 'optional'),
#('mailGroups', 'mail groups', 'e.g. Musicians, Hoorns'),
    ])
    formatDict = {'emailAddress': strRef('mailto:'),'phone': strRef('tel:'), 'mobile': strRef('tel:'),}

    @cherrypy.expose
    def list(self, *paths, **kw):
        yield from self.present(self.lowerBanner, self.list_, *paths, **kw)

    @cherrypy.expose
    def view_one(self, *paths, **kw):
        return self.edit_one(*paths, **kw)

    @cherrypy.expose
    def edit_one(self, *paths, **kw):
        yield from self.present(self.lowerBanner, self.edit_one_, *paths, **kw)

    @cherrypy.expose
    def validate(self, key, *paths, button_=None, **kw):
        """
This is where validate a members details form, or simply recognize a 'cancel' (which can also happen view mode).
        """
        if button_ not in ('Cancel',):
            inst = (key != '__new__') and self.EntityClass.by_key(key)
            if inst and button_ not in ('Add'):
                try:
                    inst.detach()
                except KeyError:
                    print("failed to detach key member", key)
                    pass
            if button_ in ('Add', 'Modify'):
                try:
                    # Retrieve the fields and values and use these to create a new or replacement instance.
                    self.new_instance = self.EntityClass(**kw)
                except EntityError as ee:
                    print("Exception while validating!", ee)
                    if button_ in ('Modify'):
                        inst.attach()
                    return self.edit_one_(*paths, exception_=ee, **kw)
            print("exporting updated members file")
            self.EntityClass.export((members.__file__))
        print("successful change (or just cancel): redirecting from %s ..." %cherrypy.url())
        raise cherrypy.HTTPRedirect('../list')

    def upperBanner(self, *paths, **kw):
        print("paths", paths,
              "kw", kw,
              "url", cherrypy.url(),
              'base', cherrypy.request.base,
              'script_name', cherrypy.request.script_name,
              'params', cherrypy.request.params, file=self)
        return h.h1(id='upperbanner')| ('%s - %s' %(clubName,
                                   self.gloss({'EN': "Members zone",
                                               'NL': "Ledenzone"})))
    def lowerBanner(self, *paths, **kw):
        bannerStart =  self.gloss({
                'EN': "Membership list ordered according to field",
                'NL': "Ledenlijst gesorteerd op veld",
        })
        sortKey = cherrypy.session.get('sortby', 'name')
        sortName = self.gloss(self.fieldDisplay[sortKey][0])
        return h.h2(id="lowerbanner") | ("%s '%s'"       %(bannerStart, sortName))

    def list_(self, *paths, **kw):
        sortKey = cherrypy.session.get('sortby', 'name')
        return (h.table(id="members") | [(self.rows_per_member(ix, member)) for ix, (name, member) in
                                         enumerate(sorted(self.EntityClass.keyLookup[sortKey].items()))]
                )

    def rows_per_member(self, ix, member):
        # print(h.th | self.gloss({'EN': 'full name', 'NL': 'naam'}), file=sys.stderr)
        # return h.br, "abc", h.br
        return (
            (ix % 10 == 0) and (h.tr | (
                h.th | (self.admin and (h.a(href='./edit_one/__new__') | self.gloss({'EN':'new', 'NL':'nieuw',}))
                        or '...'),
                [h.th | ((attr_name in self.EntityClass.keyFields and h.a(href=self.localRoot+'set_session/sortby/'+attr_name) or h) | self.gloss(heading))
                 for attr_name, (heading, tip_text) in self.fieldDisplay.items()
                 ])),
            h.tr | (
                (h.td | (h.a(id='%s' % getattr(member, member.keyFields[0]),
                             href=(self.admin and './edit_one/' or './view_one/') +
                                  getattr(member, member.keyFields[0]))
                         | (self.admin and (self.gloss({'EN': 'edit', 'NL': 'wijzig'}))
                            or (self.gloss({'EN': 'view', 'NL': 'toon'}))))),
                [(h.td | self.formatDict.get(attr_name, str)(getattr(member, attr_name)))
                 for attr_name, (heading, tip_text) in self.fieldDisplay.items()],
            )
        )

    def edit_one_(self, key, *paths, exception_=None, **kw):
        print('key', key )
        inst = (key != '__new__')  and not exception_ and self.EntityClass.by_key(key)
        colour = '#000000'  # black is default
        return (
            h.form(action=os.path.join('../validate/'+key, *paths), method='get')| (
            [   (h.label(For='%s' %attr_name)|self.gloss(displayed_name),
                         '<input type = "text" title="testing!" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, inst and getattr(inst, attr_name) or kw.get(attr_name, '')))
             for (attr_name, (displayed_name, placeholder)) in self.fieldDisplay.items()],

            [(ix_<2 or (key != '__new__')) and (h.input(type = "submit", name="button_", STYLE="background-color:%s" % colour, value=val_) | '')
             for ix_, (val_, colour) in enumerate((
                (self.gloss({'EN': "Cancel",
                             'NL': "Terug"}), "green"),
                ((key != '__new__') and self.gloss({'EN': "Modify",
                                     'NL': "Accepteer"})
                    or self.gloss({'EN': "Add",
                                   'NL': "Voeg toe"}), "orange"),
                (self.gloss({'EN': "Delete",
                                   'NL': "Verwijder"}), "red"),
            )[:self.admin and 3 or 1])],
            h.br*2,
            h.a(STYLE="color:#ff0000;") | (exception_ or ''),
        ))


_membersPage = MembersPage()
