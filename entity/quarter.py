#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
from entity import *
from entity.company import *
from phileas.page import Page, h

class AccountingException(Exception):
    pass


class AccountsItem:
    pass


class Common:
    prevOutgoingitem = None


class OutgoingItem(Entity):
# currently in transition to new Entity class , hence strange mix of arguments
    expressExtra = {None: 'n.v.t', False: 'al gedaan'}
    keyFields = ('sequenceNumber',)

    def __init__(self,
        date:str='',
        sequenceNumber:(str, type(None))=None,
        supplierName:str="(unknown supplier)",
        description:str="(no description)",
        amountBruto:(float, type(None))=None,
        percentBtw:(float, type(None))=0.0,
        amountBtw:(float, type(None))=None,
        amountNetto:(float, type(None))=None,
        paidFromPrivate:(bool, type(None))=None,
    ):
        Entity.__init__(self,
            date=date,
            sequenceNumber=sequenceNumber,
            supplierName=supplierName,
            description=description,
            amountBruto=amountBruto,
            percentBtw=percentBtw,
            amountBtw=amountBtw,
            amountNetto=amountNetto,
            paidFromPrivate=paidFromPrivate
        )

        if not self.sequenceNumber:
            psn = Common.prevOutgoingitem.sequenceNumber
            self.sequenceNumber = psn[:-3]+"%03u" % (eval('1'+psn[-3:]) - 999)
        if not self.amountBruto:
            if not self.amountNetto:
                raise AccountingException("need to supply gross and/or net price")
            self.amountBruto = self.amountNetto * 100.0 /(100 + self.percentBtw)
        else:
            calcNetto = self.amountBruto * (100+self.percentBtw)/100.0
            if not self.amountNetto:
                self.amountNetto = calcNetto
            elif not (calcNetto-0.02) < self.amountNetto < (calcNetto+0.02):
                raise AccountingException("discrepancy between supplied (%s) and calculated net price(%s)"
                                                                                                                %(amountNetto,       calcNetto      ))
        calcBtw = self.amountNetto - self.amountBruto
        if not self.amountBtw:
             self.amountBtw = calcBtw
        elif not (calcBtw-0.02) < self.amountBtw < (calcBtw+0.02):
            raise AccountingException("discrepancy between supplied (%s) and calculated btw(%s)"
                                                                                                                   %(amountBtw,       calcBtw      ))
        if self.paidFromPrivate is True:
            self.paidFromPrivate = self.amountNetto
        Common.prevOutgoingitem = self

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
        
    def h_tr(self):
        tr= h.tr | (
            h.td(align='left')  | self.date[:6],
            h.td(align='left')  | "%s" % self.sequenceNumber,
            h.td(align='left')  | self.composeName(),
            h.td(align='left')  | self.composeDescription(),
            h.td(align='right') | "%s" % money(self.amountBruto),
        )
        if self.chargeBtw is None:
            tr |= (
                h.td(align='centre') | "n.v.t.",
                h.td(align='right')  | " ",
            )
        else:
            tr |= (
                h.td(align='right') | "%s%%" % (self.percentBtw or 0),
                h.td(align='right') | money(self.amountBtw),
            )
        tr |= (
            h.td(align='right') | "%s" % money(self.amountNetto),
        )
        if self.paidFromPrivate is not None:
            tr |= (h.td(align='right') |
                   ((self.paidFromPrivate and money(self.paidFromPrivate)) or ''),
            )
        return tr

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

class Quarter(Entity, Page):

    def __init__(self,
        name:str='Accounts',
        StyleSheet:str=".style/hippos.css",
        accountant=Accountant(-1), #stub for base class!
        deliveryHelp:str="",
        supplier=Supplier(-1), #stub for base class!
        year:int=1588,
        quarter:int=0,
        prevSeqNumber:int=0,
        invoiceModules:tuple=(),
        rawUitgoings:tuple=(),
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
            invoiceModules=invoiceModules,
            rawUitgoings=rawUitgoings,
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
        
        # determine which invoices are 'binnenland' which are EU (ICL) and which are rest-of-the-world
        for (content,  tableQuartet,  text, )   in (
                ([invoiceModule.invoice for invoiceModule in self.invoiceModules],
                            self.incomeTables, 'income', ),
                ( (OutgoingItem.keyLookup['sequenceNumber']).values(),  # self.uitgoings,
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
    quarter = Quarter()
    quarter.present()

