#!/usr/bin/python
# -*- encoding: utf8 -*-
##xx -*- coding: latin-1 -*-
""" very old comment, left in purely for nostalgia:
    Data structures representing companies etc. Initial stubby version
    adequate for first invoice of 2013?
"""
from phileas.admin import *

AlteaXL = Car(
    modelName = "Altea XL 1.6",
    buildYear = 2007,
    originalNewPrice = 27077,
    percentBijtelling = 2.7,
    kenteken = '95-XX-SP'
)
    
Hippos = Supplier(
    name = "Hippos Technical Systems BV",
    address = [
        "Normandiëlaan 107",
         "5627HR Eindhoven", 
# treat rest of info as extension of address 'for now':
        'telephone: (31)(40)2926707',
        'fax: by appointment only', 
         'email: hippos@chello.nl',
        'regd. KvK Eindhoven 17074196', 
        'VAT/BTW  NL-802629507.B.01', 
        'Bank: ABN/Amro 0527077879', 
        '- BIC: ABNANL2A',
        '- IBAN: NL55ABNA0527077879',
    ],
    btwNumber = 'NL-802629507.B.01',
    companyLogo = "file:///home/larry/Hippos/logo/hipposLogo.png",
    #companyLogo = "/Hippos/logo/hipposLogo.png",
    cars = [AlteaXL,]
)
    
AdHoeks = Accountant(
    name = 'A.G.M. Hoeks B.V.',
    address = [
        "Kuiper 1"
        "5521 DG Eersel"
    ]
)
    
LearnIt = Client(
    number = 31,
    reference = "Python training",
    name = 'Learnit Training B.V.',
    address = ['Antonio Vivaldistraat 52a', 
        '1083 HP Amsterdam', 
    ]
)

Geckotech = Client(    
    number = 34,
    reference = """"(conform freelanceovereenkomst dd 11 Juli 2012)""",
    name = 'Geckotech B.V.',
    address = [
        'Ruthardlaan 19', 
        '1406RR Bussum', 
    ]
)

Oreda = Client(    
    number = 35,
    reference = """"(conform “Aannemings contract 201208”)""",
    name = 'Oreda Consulting B.V.',
    address = [
        'Fellenoord 130', 
        '5611 ZB Eindhoven', 
    ],
    paymentTerms = [
             "Betaling naar bankrekening (zie gegevens boven) binnen 14 dagen wordt op prijs gesteld.", 
             "Bij betaling svp factuurnummer vermelden.", 
    ]
)

OneAudio = Client(
    number = 36,
    reference = "project 'OneAudio'",
    name = 'R&S Projects',
    address = [
        'Emiel Becquaertlaan 2', 
        '2400 Mol', 
        'België', 
    ],
    btwNumber = "BE 0889 137 038"
)

ComputerFuturesBelgium = Client(    
    number = 37,
    reference = "Antwerp Space",
    name = 'Computer Futures',
    address = [
        '11 Rond-point Schuman', 
        '1040 Brussels', 
        'België', 
    ],
    btwNumber = "BE 0892 363 574"
)

YrzEindhoven = Client(    
    number = 38,
    reference = "NXP-03",
    name = 'Yrz',
    address = [
        'Turijnstraat 6', 
        '5237 ER ‘s-Hertogenbosch', 
        'Nederland', 
    ],
    btwNumber = "NL1765.37.673.B01",
    paymentTerms = [
             "Betaling naar bankrekening (zie gegevens boven) binnen 60 dagen wordt op prijs gesteld.", 
             "Bij betaling svp factuurnummer vermelden.", 
    ]
)

AmoriaBond = Client(    
    number = 39,
    reference = "J35734",
    name = 'Amoria Bond B.V.',
    address = [
        'Keizersgracht 270', 
        '1016 EV Amsterdam', 
        'Nederland', 
    ],
    btwNumber = "NL8198.86907.B01",
    paymentTerms = [
             "Betaling naar bankrekening (zie gegevens boven) binnen 30 dagen",
             " wordt verwacht i.v.m. verleende korting.", 
    ],
)
Acknowledge = Client(    
    number = 40,
    reference = "Deelovereenkomst 20160301",
    name = 'Acknowledge Benelux B.V.',
    address = [
        'Postbus 2282', 
        '5500BG Veldhoven', 
        'Nederland', 
    ],
    btwNumber = "NL8094.84.596B03",
    paymentTerms = [
             "Betaling naar bankrekening (zie gegevens boven) binnen 45 dagen",
             " wordt of prijs gesteld.", 
    ],
)
Huxley = Client(    
    number = 41,
    reference = "Deelovereenkomst 20160301",
    name = 'Huxley IT.',
    address = [
        'De Geelvinck',
        'Singel 540',
        '5500BG Amsterdam', 
        'Nederland', 
    ],
    btwNumber = "NL8094.84.596B03",
    paymentTerms = [
             "Betaling naar bankrekening (zie gegevens boven) binnen 30 dagen",
             " wordt of prijs gesteld.", 
    ],
)
if __name__=='__main__':
    print ()
