#!/usr/bin/python3
# -*- encoding: utf8 -*-
from MEW import *
import csv

def main():
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
