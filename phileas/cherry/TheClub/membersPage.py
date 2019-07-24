#!/usr/bin/python3
# -*- encoding: utf8 -*-
import sys, os
from collections import OrderedDict
from .clubPage import clubName, ClubPage, h, gloss
from entity.club import Member, EntityError, DateOrNone
from .mailgroups import *
from . import members
import cherrypy

def strRef(text):
    def fn(stringList):
        return  h.br.join([h.a(href=text + string) | string for string in stringList])
    return fn

def comma_sep(s):
    if isinstance(s, (list, tuple)):
        return ', '.join([str(s1) for s1 in s])
    return s

def as_html_text(s):
    return s.replace('_', '&nbsp;')

def map_url_str(s):
    return h.a(href='https://www.google.com/maps/place/'+s) | '?'

def one_per_row(s):
    if isinstance(s, (list, tuple)):
        return h.br.join([str(s1) for s1 in s])
    return s


class MembersPage(ClubPage):
    EntityClass = Member
    admin = False
    fieldDisplay = OrderedDict([
# python name       # heading for glossing                              # field entry tip for glossing
('called',          ({'EN':'known as',         'NL':'roepnaam'},         {'EN': 'known within MEW as...', 'NL': 'bekend binnen MEW als...'})),
('name',            ({'EN':'full name',        'NL':'naam'},             {'EN': 'surname, initials',      'NL': 'achternaam, initielen'})),
('streetAddress',   ({'EN':'street address',   'NL':'adres'},            {'EN': 'e.g. Rechtstraat 42',    'NL': 'b.v. Rechtstraat 42'})),
('postCode',        ({'EN':'post_code',        'NL':'postcode'},         {'EN': 'e.g. 1234 XY',           'NL': 'b.v. 1234 XY'})),
('cityAddress',     ({'EN':'Town/City',        'NL':'gemeente'},         {'EN': 'e.g. Eindhoven',         'NL': 'b.v. Eindhoven'})),
('_locator',         ({'EN':'show map',        'NL':'toon kaart'},      {'EN': 'show in google maps',    'NL': 'toon met googel maps'})),
('phone',           ({'EN':'telephone',        'NL':'telefoon'},         {'EN': 'e.g. 040-2468135',       'NL': 'b.v. 040-2468135'})),
('emailAddress',    ({'EN':'email address(es)','NL':'email addres(sen)'},{'EN': 'e.g. 06-24681357',       'NL': 'b.v. 06-24681357'})),
('birthDate',       ({'EN':'date__of__birth',  'NL':'geboortedtatum'},   {'EN': 'e.g. 15-mrt-1963',       'NL': 'b.v. 15-mrt-1963'})),
('memberSince',     ({'EN':'membership date(s)','NL':'lidmaatschapsdatum(s)'},        {'EN': 'e.g. 15-okt-2003',       'NL': 'b.v. 15-okt-2003'})),
('instrument',      ({'EN':'instrument',       'NL':'instrument'},       {'EN': 'e.g. Clarinet',          'NL': 'b.v. Klarinet'})),
    ])
    formatDict = {'emailAddress': strRef('mailto:'),
                  'phone': strRef('tel:'),
                  'mobile': strRef('tel:'),
                  '_locator': map_url_str,
                  }

    @cherrypy.expose
    def list(self, *paths, **kw):
        yield from self.present(self.listLowerBanner, self.list_, *paths, **kw)

    @cherrypy.expose
    def view_one(self, *paths, **kw):
        yield from self.present(self.view_oneBanner, self.edit_one_, *paths, **kw)

    @cherrypy.expose
    def edit_one(self, *paths, **kw):
        yield from self.present(self.edit_oneBanner, self.edit_one_, *paths, **kw)

    @cherrypy.expose
    def validate(self, key, *paths, button_=None, **kw):
        """
This is where validate a members details form, or simply recognize a 'cancel' (which can also happen view mode).
        """
        if button_ not in ('Cancel', 'Terug',):
            inst = (key != '__new__') and self.EntityClass.by_key(key)
            if inst and button_ not in ('Add', 'Voeg toe', ):
                try:
                    inst.detach()
                except KeyError:
                    print("failed to detach key member", key)
                    pass
            if button_ in ('Add', 'Voeg toe', 'Modify', 'Accepteer', ):
                try:
                    # Retrieve the fields and values and use these to create a new or replacement instance.
                    self.new_instance = self.EntityClass(**kw)
                except EntityError as ee:
                    print("Exception while validating!", ee)
                    if button_ in ('Modify', 'Accepteer', ):
                        inst.attach()
                    yield from self.edit_one(key, *paths, exception_=ee, **kw)
                    return
            print("exporting updated members file (python module)")
            self.EntityClass.export((members.__file__))
            print("exporting updated members file (csv for import to spreadsheet)")
            self.export_csv(self.EntityClass,os.path.splitext(members.__file__)[0]+'.csv')
        print("successful change (or just cancel): redirecting from %s ..." %cherrypy.url())
        raise cherrypy.HTTPRedirect('../list')

    def export_csv(self, cls, out_file):
        sortKey = cherrypy.session.get('sortby', 'name')
        with open(out_file, 'w') as file_:
            print(';'.join([gloss(heading) for attr_name, (heading, tip_text) in self.fieldDisplay.items()]),
                  file=file_)
            print (*[';'.join([str(getattr(member, attr_name))
                 for attr_name, (heading, tip_text) in self.fieldDisplay.items() if not attr_name.startswith('_')])
                    for name, member in sorted(self.EntityClass.keyLookup[sortKey].items())],
                   sep='\n', file=file_)


    def upperBanner(self, *paths, **kw):
        yield from h.h1(id='upperbanner')| ('%s - (supplemental) - %s' %(clubName,
                                   gloss({'EN': "Members zone",
                                               'NL': "Ledenzone"})))

    def lowerBanner(self, *paths, **kw):
        yield from h.h2(id="lowerbanner") | gloss({'EN': "Members' zone -  index page",
                                               'NL': "Ledenzone - indexpagina"})

    def lowerText(self, **kw):
        yield from h | (
                h.p | (gloss({'EN':(
"This is the index page of the members' zone. Click one of the followng links to get to the ",
h.a(href=cherrypy.url()+'list') | "membership list",
" or the ",
h.a(href=cherrypy.url() + 'music') | "music collection",
". More goodies will be added later as and when needed.",
                                    ),
                              'NL':(
"Deze indexpagina dient momenteel alleen als tussenstop richting de ",
h.a(href=cherrypy.url() + 'list') | "ledenlist",
". Meer splullen zullen t.z.t. toegevoegd worden.",
                              )})
                       ),
                #h.p | "2nd paragraph?"
            )
        # yield "more stuff just for testing!"


    def listLowerBanner(self, *paths, **kw):
        bannerStart =  gloss({
                'EN': "Membership list ordered according to field",
                'NL': "Ledenlijst gesorteerd op veld",
        })
        sortKey = cherrypy.session.get('sortby', 'name')
        sortName = gloss(self.fieldDisplay[sortKey][0])
        yield from h.h2(id="lowerbanner") | ("%s '%s'"       %(bannerStart, sortName))

    def list_(self, *paths, **kw):
        sortKey = cherrypy.session.get('sortby', 'name')
        self.row_count = -1
        self.count_line = h | "number of members = "
        #yield self.count_line
        # yield from h.br
        yield from h.table(id="members") | [(self.rows_per_member(member))
                                     for name, member in
                                         sorted(self.EntityClass.keyLookup[sortKey].items())]
        #self.count_line |= ('%d' %  self.row_count)
        #yield ''

    def rows_per_member(self, member):
        # print(h.th | gloss({'EN': 'full name', 'NL': 'naam'}), file=sys.stderr)
        # return h.br, "abc", h.br
        member._locator = (member.streetAddress + '+' + member.postCode + '+' + member.cityAddress).replace(' ', '+')
        current = len(member.memberSince) & 1  # false for departed members
        if not current and not self.admin:
            return ''  # don't show borrowed members, except in admin mode
        self.row_count += 1
        yield from h | (
            (self.row_count % 15 == 0) and (h.tr(id='tableguide') | (
                h.th | (self.admin and (h.a(href='./edit_one/__new__') | gloss({'EN':'new', 'NL':'nieuw',}))
                        or '...'),
                [h.th | ((attr_name in self.EntityClass.keyFields and
                          h.a(href=self.localRoot+'set_session/sortby/'+attr_name)
                          or h) | as_html_text(gloss(heading)))
                 for attr_name, (heading, tip_text) in self.fieldDisplay.items()
                 ])),
            h.tr | (
                (h.td | (h.a(id='%s' % getattr(member, member.keyFields[0]),
                             href=(self.admin and './edit_one/' or './view_one/') +
                                  getattr(member, member.keyFields[0]))
                         | (self.admin and (gloss({'EN': 'edit', 'NL': 'wijzig'}))
                            or (gloss({'EN': 'view', 'NL': 'toon'}))))),
                [h.td | ((current and h or h.dEL) |
                         (self.formatDict.get(attr_name, one_per_row)(getattr(member, attr_name))))
                 for attr_name, (heading, tip_text) in self.fieldDisplay.items()],
            )
        )


    def view_oneBanner(self, key, *paths, exception_=None, **kw):
        bannerFormat =  gloss({
                'EN': "Viewing details of member '%s'",
                'NL': "Gegevens van lid '%s' zijn hieronder getoond",
        })
        yield from h.h2(id="lowerbanner") | (bannerFormat % key)

    def edit_oneBanner(self, key, *paths, exception_=None, **kw):
        bannerText = gloss(
            (key == '__new__') and  {
                    'EN': ("Adding details of new member",
                           (key == '__new__') and 'new member'),
                    'NL': ("Toevoegen gegevens nieuw lid"),
            }
            or {
                'EN': "Editing details of member '%s'" % key,
                'NL': "Aanpassen gegevens van lid '%s'" %key,
            }
        )
        yield from h.h2(id="lowerbanner") | bannerText

    def edit_one_(self, key, *paths, exception_=None, **kw):
        # print('key', key )
        inst = (key != '__new__')  and not exception_ and self.EntityClass.by_key(key)
        colour = '#000000'  # black is default
        yield from h.form(action=os.path.join('../validate/'+key, *paths), method='get')| (
            [   (h.label(For='%s' %attr_name)|as_html_text(gloss(displayed_name)),
                         '<input type = "text" title="testing!" STYLE="color:%s;" name = "%s" value="%s"><br />\n'
                % (colour, attr_name, comma_sep(inst and getattr(inst, attr_name) or kw.get(attr_name, ''))))
             for (attr_name, (displayed_name, placeholder)) in self.fieldDisplay.items() if not attr_name.startswith('_')],

            [(ix_<2 or (key != '__new__')) and (h.input(type = "submit", name="button_", STYLE="background-color:%s" % colour, value=val_) | '')
             for ix_, (val_, colour) in enumerate((
                (gloss({'EN': "Cancel",
                             'NL': "Terug"}), "green"),
                ((key != '__new__') and gloss({'EN': "Modify",
                                     'NL': "Accepteer"})
                    or gloss({'EN': "Add",
                                   'NL': "Voeg toe"}), "orange"),
                (gloss({'EN': "Delete",
                                   'NL': "Verwijder"}), "red"),
            )[:self.admin and 3 or 1])],
            h.br*2,
            h.a(STYLE="color:#ff0000;") | (exception_ and str(exception_) or ''),
        )


_membersPage = MembersPage()
