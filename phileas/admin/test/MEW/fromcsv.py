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
        '%d-%bt-%Y', # catger for Sept instead of Sep

    ):
        try:
            dt = datetime.datetime.strptime(s, fmt_str)
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
                print(len(row) , row)
                (Lidcode, Naam, Initialen, Hoofddadres, Postcode, Plaats, Telefoon, Mobiele ,
                 Begindatum, Geboortedatum, Functie, Catgorie, Email  , AltEmail,
                 ) = row
                address = [Hoofddadres, "%s  %s" % (Postcode, Plaats)]
                instrument = Functie
                instruments.add(instrument)
                beginDate = figure_out_date(Begindatum)
                birthDate  = figure_out_date(Geboortedatum)
                lid = Lid(name=Naam,
                          initials=Initialen,
                          address = address,
                          instrument=instrument,
                          emailAddress=Email)
                print(lid)
    print(instruments)
if __name__=='__main__':
    print ('running %s as main' % __file__)
    main()
