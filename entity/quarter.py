#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
#from entity import *
from entity.company import *
from entity.outgoing import OutgoingItem
from entity.invoice import Invoice
from phileas.page import Page, h

class AccountingException(Exception):
    pass


class AccountingTable:
    totalBruto = 0.0
    totalBtw = 0.0
    totalNetto = 0.0
    totalExtra = 0.0
    extraTitle = None
    name = "<firma>"

    def __init__(self,  chargeBtw=None,
        heading = "<dummy accounting table heading>"):
        self.chargeBtw = chargeBtw
        self.heading = heading
        self.items = []

    def resolveData(self):
        for item in self.items:
            self.totalBruto += item.amountBruto
            self.totalBtw += item.amountBtw
            self.totalNetto += item.amountNetto
            self.totalExtra += item.paidFromPrivate or 0
            
    def accounts(self, showDetail=True):
        table = h.table(style='border: 1px solid black;') |(
            h.col(style="width:8%"),
            h.col(style="width:10%"),
            h.col(style="width:12%"),
            h.col(style="width:22%"),
            h.col(style="width:13%"),
            h.col(style="width:7%"),
            h.col(style="width:12%"),
            h.col(style="width:13%"),
            h.col(style="width:3%"),
            h.tr | (
                h.th | 'Datum',
                h.th | 'Volgnr',
                h.th | self.headerName,
                h.th | 'Beschrijving',
                h.th | 'Bruto',
                h.th | '%BTW',
                h.th | 'BTW',
                h.th | 'Netto',
                self.extraTitle and (h.th | self.extraTitle),
            )
        )
        if showDetail:
            table |= (
                [ item.h_tr() for item in self.items ]
              + [h.tr | (h.td | " ")]*2
            )
        table |= (h.tr | (
            h.th(style='text-align:left')   | "kwartaal",
            h.th(style='text-align:left')   | "totaal",
            h.th(style='text-align:centre') | " - ",
            h.th(style='text-align:left')   | "(alles hierboven)",
            h.th(style='text-align:right')  | "%s" % money(self.totalBruto),
            h.th(style='text-align:centre') | " - ",
            h.th(style='text-align:right')  | money(self.totalBtw),
            h.th(style='text-align:right')  | "%s" % money(self.totalNetto),
            self.extraTitle and h.th(style='text-align:right') | "%s" % money(self.totalExtra),
        ))
        return (
            h.h4(style='text-align:centre') | "%s %s" % (self.name,  self.heading),
            table,
        )
    
class IncomeTable(AccountingTable):
    name = 'Inkomen'
    headerName = 'Client'
     
class ExpenditureTable(AccountingTable):
    name = 'Uitgaves'
    headerName = 'Supplier'
    extraTitle = "te vergoeden"

class Quarter(Entity, Page):
    styleSheet = "/home/gill/Hippos/newsite/style.css"

    def __init__(self,
        name:str='Accounts',
        StyleSheet:str=".style/hippos.css",
        accountant=Accountant(-1), #stub for base class!
        deliveryHelp:str="",
        supplier=Supplier(-1), #stub for base class!
        year:int=1588,
        quarter:int=0,
        prevSeqNumber:int=0,
        pageNo:int=0,
        uitgoings:tuple=(),
     ):
        if not deliveryHelp:
            deliveryHelp = "(betreft kwartaalgegevens '%s')" %supplier.name
        Entity.__init__(self,
            name=name,
            StyleSheet=StyleSheet,
            accountant=accountant, #stub for base class!
            deliveryHelp=deliveryHelp,
            supplier=supplier, #stub for base class!
            year=year,
            quarter=quarter,
            prevSeqNumber=prevSeqNumber,
            pageNo=pageNo,
            uitgoings=uitgoings,
        )
        Page.__init__(self)

    def resolveData(self):
        self.incomeTables,  self.expenditureTables = [
            [
                _AccountsTable(chargeBtw=None,
                                  heading = "TOTAAL"), 
                _AccountsTable(chargeBtw=True,
                                  heading = "binnen Nederland"), 
                _AccountsTable(chargeBtw=False,
                                 heading = "buitenland, binnen EU "), 
                _AccountsTable(chargeBtw=None,
                                 heading = "buiten EU"), 
            ] for _AccountsTable in (IncomeTable,  ExpenditureTable)
        ]
        
        for (ItemClass,  tableQuartet,  text, )   in (
                (Invoice,      self.incomeTables,       'income', ),
                (OutgoingItem, self.expenditureTables,  'outgoing',  ),
            ):
            dir_of_items = ItemClass.keyLookup and ItemClass.keyLookup['sequenceNumber'] or {}
            for item in dir_of_items.values():
                # determine whether item falls under  'binnenland' or 'EU (ICL)' or 'rest-of-the-world':
                for  ix,  accountsTable in enumerate(tableQuartet):
                    if ix==0  or  item.chargeBtw is accountsTable.chargeBtw:
                        #print (ix,  accountsTable.chargeBtw,  item.sequenceNumber)
                        accountsTable.items.append(item)
                        if ix!=0:
                            break
                else:
                    print ("error: can't associate '%s' with any of our three %s/BTW categories"
                                                                                % (item.name,  text))
            for accountsTable in tableQuartet:
                accountsTable.resolveData()

    def accountantDetails(self):
         return h.br.join(
             []*6 
           + ['', self.accountant.name,  self.deliveryHelp]
           + self.accountant.address
        )

    def supplierDetails(self):
        return (
            self.supplier.companyLogo and
                h.img(src=self.supplier.companyLogo, vspace='10'),
            h.em | (
                h.p(style='font-size:12px;color:#800000') | h.br.join(
                    [self.supplier.name,] 
                  + self.supplier.address
                )
            )
        )
               
    def quartet(self,  quartet):
        return [
            quartet[i].accounts(showDetail=(i!=0))
                for i in (1, 2,  3,  0)
        ]
            
    def carBijtelling(self):
        if self.quarter !=4:
            return None
        return h | (
            h.br,
            h.em |
"laaste kwartaal => autokostenforfait('bijtelling') berekenen...",
            h.h4(style='text-align:centre') |
"Privégebruik auto berekening tbv BTW 4e kwartaal %u" % self.year,
            h.p | (
"berekening volgens regeling ",
                h.a(
href="http://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/btw_en_de_auto/privegebruik_auto_van_de_zaak/privegebruik_auto_van_de_zaak") |
"Privégebruik auto van de zaak (geen kilometeradministratie)",
            ),
            [ a_car.useInYear(self.year) for a_car in self.supplier.cars ],
        )

    def pageHeader(self, pageNo=None, pageBreak=None):
        if pageNo is None:
            self.pageNo += 1
        else:
            self.pageNo = pageNo
        if pageBreak is None:
            pageBreak = self.pageNo > 1
        if pageBreak:
           kw = dict(style="page-break-before: always")
        else:
           kw = dict()
        return h.p(**kw) |(
            h.table(id='page-header') | (
                h.col(style="width:30%"),
                h.col(style="width:50%"),
                h.col(style="width:20%"),

                h.tr | (
                    h.td(id='page-header') | self.accountantDetails(),
                    h.td(id='page-header') | '', # leave the middle ground empty.
                    h.td(id='page-header') | self.supplierDetails(),
                )
            ),
            h.h3(style=
'font-family:Arial;font-size:20px;text-align:center'
                        ) | (
                h.b | (
                    "Overzicht %u" % self.quarter,
                    h.sup | 'e',
                    " kwartaal %d" % self.year, h.br,
                    "page %d" % self.pageNo
                ),
            ),
        )

    def body(self):
        return (
            self.pageHeader(),
            self.quartet(self.incomeTables),
#            h.p(style="page-break-before: always") | (
#            ),
            self.pageHeader(),
            self.quartet(self.expenditureTables),
            self.carBijtelling()
        )

if __name__=="__main__":
    quarter = Quarter()
    quarter.present()

