#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
from phileas import _html40 as h
from admin.page import ( Page, main )
from admin.company import ( Supplier, Accountant, AdHoeks )

from admin.utils import ( money, euros, AccountsItem )

class AccountingException(Exception):
    pass

class Common:
    prevOutgoingitem = None

class OutgoingItem(AccountsItem):
    
    expressExtra = {None: 'n.v.t', False: 'al gedaan'}
    
    def __init__(self,  date=None,  sequenceNumber=None,  supplierName="(unknown supplier)",  description="(no description)", 
                 amountBruto=None, percentBtw=None,  amountBtw=None,  amountNetto=None, paidFromPrivate=False):
        if sequenceNumber is None:
            psn = Common.prevOutgoingitem.sequenceNumber
            sequenceNumber = psn[:-3]+"%03u" % (eval('1'+psn[-3:]) - 999)
        if amountBruto is None:
            if amountNetto is None:
                raise AccountingException("need so supply gross and/or net price")
            else:
                amountBruto = amountNetto * 100.0 /(100+(percentBtw or 0))
        else:
            calcNetto = amountBruto * (100+(percentBtw or 0))/100.0
            if amountNetto is None:
                amountNetto = calcNetto
            elif not (calcNetto-0.02) < amountNetto < (calcNetto+0.02):
                raise AccountingException("discrepancy between supplied (%s) and calculated net price(%s)"
                                                                                                                %(amountNetto,       calcNetto      ))
        calcBtw = amountNetto - amountBruto
        if amountBtw  is None:
             amountBtw = calcBtw
        elif not (calcBtw-0.02) < amountBtw < (calcBtw+0.02):
            raise AccountingException("discrepancy between supplied (%s) and calculated btw(%s)"
                                                                                                                   %(amountBtw,       calcBtw      ))
        if paidFromPrivate is True:
            paidFromPrivate = amountNetto
        self.setAttributes(date=date,  sequenceNumber=sequenceNumber,
                supplierName=supplierName,  description=description, amountBruto=amountBruto,
                   percentBtw=percentBtw,  amountBtw=amountBtw,  amountNetto=amountNetto,
                   paidFromPrivate=paidFromPrivate)
        Common.prevOutgoingitem = self

    def setAttributes(self,  **kw):
        for key,  val in kw.items():
            setattr(self,  key,  val)
        # loose end: following allows table output to be quite generic but doesn't cater
        # for 'rest-of-the-world' - just Ned and other EU.
        #
        #self.chargeBtw = self.percentBtw != 0
        self.chargeBtw = ((self.percentBtw is not False) and
                            (self.percentBtw is not None))

    def composeName(self):
        return self.supplierName

    def composeDescription(self):
        return self.description
        

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
        table = h.table(border="1") |(
            h.tr | (
                h.th(width="8%")  | 'Datum',
                h.th(width="10%") | 'Volgnr',
                h.th(width="12%") | self.headerName,
                h.th(width="22%") | 'Beschrijving',
                h.th(width="13%") | 'Bruto',
                h.th(width="7%")  | '%BTW',
                h.th(width="12%") | 'BTW',
                h.th(width="13%") | 'Netto',
                self.extraTitle and (h.th(width="3%")  | self.extraTitle),
            )
        )
        if showDetail:
            table |= (
                [ item.h_tr() for item in self.items ]
              + [h.tr | (h.td | " ")]*2
            )
        table |= (h.tr | (
            h.th(align='left')   | "kwartaal",  
            h.th(align='left')   | "totaal",  
            h.th(align='centre') | " - ",  
            h.th(align='left')   | "(alles hierboven)",  
            h.th(align='right')  | "%s" % money(self.totalBruto),  
            h.th(align='centre') | " - ",  
            h.th(align='right')  | money(self.totalBtw),  
            h.th(align='right')  | "%s" % money(self.totalNetto),  
            self.extraTitle and h.th(align='right')  | "%s" % money(self.totalExtra),  
        ))
        return (
            h.h4 | (h.center | "%s %s" % (self.name,  self.heading)),
            table,
        )
    
class IncomeTable(AccountingTable):
    name = 'Inkomen'
    headerName = 'Client'
     
class ExpenditureTable(AccountingTable):
    name = 'Uitgaves'
    headerName = 'Supplier'
    extraTitle = "te vergoeden"

class Quarter(Page):
    name = 'Accounts'
    StyleSheet = ".style/hippos.css"
    accountant  = AdHoeks #stub for base class!
    deliveryHelp = """(betreft kwartaalgegevens)"""
    supplier = Supplier #stub for base class!
    year = 2012
    quarter = 4
    prevSeqNumber = 0
    InvoiceModules = ()
    rawUitgoings = ()
    pageNo = 0

    uitgoings= ()

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
        
        # determine which invoices are 'binnenland' which are EU (ICL) and which are rest-of-the-world
        for (content,  tableQuartet,  text, )   in (
                ([invoiceModule.Invoice() for invoiceModule in self.InvoiceModules],
                            self.incomeTables, 'income', ), 
                ( self.uitgoings,
                            self.expenditureTables, 'outgoing',  ), 
                                         ):
            for item in content:
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
"laaste kwartaal => autokostenforfait('bijtelling') berekenen...",            h.h4 | (h.center | 
"Privégebruik auto berekening tbv BTW 4e kwartaal %u" % self.year
            ),
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
            h.table(width="100%") | (
                h.tr | (
                    h.td(width='30%') | self.accountantDetails(),
                    h.td(width='50%') | '', # leave the middle ground empty.
                    h.td(width='20%') | self.supplierDetails(),
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
    main(Quarter)

    
