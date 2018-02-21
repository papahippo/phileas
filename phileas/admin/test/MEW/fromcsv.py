#!/usr/bin/python3
# -*- encoding: utf8 -*-
from MEW import *
import csv
import locale

def figure_out_date(s):
    for fmt_str in  (
        '%m-%d-%Y',
        '%d/%B/%Y',
        '%d/%b/%Y',
        '%d-%b-%Y',
        '%d-%bt-%Y', # cater for Sept instead of Sep
        '%d-%m-%y',  # only use if mm-dd gives impossible result!

    ):
        try:
            dt = datetime.datetime.strptime(s, fmt_str)
            if '%Y' not in fmt_str and dt.year > (1 + datetime.datetime.now().year):
                dt.replace(year=dt.year-100)
            return datetime.datetime.date(dt)

        except ValueError:
            continue
    if s:
        print("can't crack date %s" %s)
    return None

def main():
    locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
    instruments = set()
    with open("members.py", 'w') as output:
        with open("members.csv", 'r') as csvfile:
            header_line = csvfile.readline()
            reader = csv.reader(csvfile, delimiter=',', dialect=csv.excel)
            for row in reader:
                # print(len(row) , row)
                (Lidcode, Naam, Initialen, Hoofddadres, Postcode, Plaats, Telefoon, Mobiele ,
                 Begindatum, Geboortedatum, Functie, Catgorie, Email  , AltEmail,
                 ) = row
                instrument = Functie
                instruments.add(instrument)
                memberSince = figure_out_date(Begindatum)
                birthDate  = figure_out_date(Geboortedatum)
                lid = Lid(name=Naam,
                          initials=Initialen,
                          streetAddress = Hoofddadres,
                          postCode=Postcode,
                          cityAddress=Plaats,
                          emailAddress=Email,
                          altEmailAddress=AltEmail,
                          birthDate=birthDate,
                          memberSince=memberSince,
                          instrument=instrument,
                          mailGroups= ['Musicians',]
                          )
                print(lid)
    print(instruments)
if __name__=='__main__':
    print ('running %s as main' % __file__)
    main()
