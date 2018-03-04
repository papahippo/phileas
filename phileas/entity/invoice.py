#!/usr/bin/python
# -*- encoding: utf8 -*-
from phileas.entity import *
from phileas.entity.page import Page

class InvoiceItem(Entity):

    def __init__(self,
        project:str="<fictitious project>: ",
        whatDone:str='werk uitgevoerd door ',
        whoBy:str='Larry Myerscough',
        howMany:float=42, # stub!
        timesWhat:list=['uur',  'uren'],
        whenDone:str="St. Juttemas 2099",
        rate=0,
        percentDiscount:float=0,
        cost:float=0,
        costBtw:float=0,
        description:str='',
        chargeBtw:float=21.,
                 ):
        Entity.__init__(self,
            project=project,
            whatDone=whatDone,
            whoBy=whoBy,
            howMany=howMany,
            timesWhat=timesWhat,
            whenDone=whenDone,
            rate=rate,
            percentDiscount=percentDiscount,
            cost=cost,
            costBtw=costBtw,
            description=description,
            chargeBtw=chargeBtw,
                        )

    def resolveData(self):
        if self.rate is not None:
            self.cost = self.howMany*self.rate
        self.appliedCost = self.cost
        self.costBtw = (self.appliedCost * int(self.chargeBtw)) / 100.0
        if self.percentDiscount:
            self.amountDiscount = (self.cost * self.percentDiscount) / 100.0
            self.appliedCost -= self.amountDiscount
        if not self.description:
            self.description = ("%s %s %s, %s"
                            %(self.project,  self.whatDone,  self.whoBy,  self.whenDone))

    def details(self):
        answer = h.tr | (    h.td(width='40%', align='left') | self.description,
            h.td(width='30%', align='center') | (
                                 (self.rate is None) and 'n.v.t.' or ("%s %s x %s"
                %(self.howMany,  self.timesWhat[self.howMany!=1],  money(self.rate)))
            ),
            h.td(width='30%', align='right',  valign='top') | (
                "%s" %(money(self.cost)), h.br,
            ),
        ),
        if self.percentDiscount:
            answer += h.tr | (    h.td(width='40%', align='left') | self.reasonDiscount,
                h.td(width='30%', align='center') | (
                    "%s%% x %s"
                    %(self.percentDiscount,   money(self.cost))
                ),
                h.td(width='30%', align='right',  valign='top') | (
                    "%s" %(money(self.amountDiscount)),
                ),
            ),
        return answer


class Invoice(Page, Entity):
    def __init__(self,
        date:str="42 Januari, 2099",
        styleSheet:str="file:///home/gill/hippos.css",
        sequenceNumber:str='N2099/042', #stub
        items:list=[InvoiceItem(cost=54.),],
        description:str='',
        client=Client(-1), #stub for base class!
        deliveryHelp:str='',
        supplier=Supplier(-1), #stub for base class!
        textSundries:str='',
        costSundries:float=0.0,
        percentBtw:float=21,
        chargeBtw=None, # only applies for "rest of world"; currently always overruled!
        paidFromPrivate=None,
    ):
        Entity.__init__(self,
            date=date,
            styleSheet=styleSheet,
            sequenceNumber=sequenceNumber,
            items=items,
            description=description,
            client=client,
            deliveryHelp=deliveryHelp,
            supplier=supplier,
            textSundries=textSundries,
            costSundries=costSundries,
            percentBtw=percentBtw,
            chargeBtw=chargeBtw,
            paidFromPrivate=paidFromPrivate,
        )
        Page.__init__(self)


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

    def resolveData(self):
        self.amountBruto = 0.0
        self.amountTaxable = 0.0
        self.amountBtw = 0.0
        self.amountTeVergoeden = 0.0
        self.chargeBtw =  (self.client.btwNumber is None) or (self.client.btwNumber[0:2]==self.supplier.btwNumber[0:2])
        for item in self.items:
            item.resolveData()
            if not self.description:
                self.description = item.description
                if len(self.description) > 40:
                    self.description = self.description[:38]+'...'
            self.amountBruto += item.appliedCost
            self.amountBtw += item.costBtw
            if item.chargeBtw is not False:
                self.amountTaxable += item.appliedCost
        self.amountNetto = self.amountBruto + self.amountBtw

    def clientDetails(self):
        return h.br.join(
             []*6
           + ['', self.client.name,  self.deliveryHelp]
           + self.client.address
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

    def headerBlock(self):
        return (h.hr,
            h.table(width="50%",  style='font-size:12px;') |
                h.tr | (
                    h.td(width='50%',align='left') | h.br.join([
                          "Datum:",
                          "Notanummer:",
                          "Cliëntnummer:",
                          self.client.btwNumber and "Cliënt BTW nummer:",
                          "Cliënt Referentie:",
                    ]),
                    h.td(width='50%',align='left') |  h.br.join([
                            self.date,
                            self.sequenceNumber,
                            "%03u" %(self.client.number),
                            self.client.btwNumber,
                            self.client.reference,
                    ]),
                ),
            h.hr,
        )

    def btw(self):
        return h.tr | (
            self.chargeBtw and (
                h.td(width='30%', align='center') | h.br,
                h.td(width='50%', align='right',  valign='top') | (
                        "BTW: %s%% x %s ="
                        %(self.percentBtw,  money(self.amountTaxable)),
                ),
                h.td(width='20%', align='right',  valign='top') | (
                    "%s" %(money(self.amountBtw)),
                    h.br,
                ),
            ) or (
                h.td(width='30%', align='left',  valign='top') | (
                    "BTW wordt niet toegepast (ICL regeling)"
                )
            ),
        )

    def detailBlock(self):
        return (
            h.br,
            h.table(width="100%",  frame='none',  rules='none',
                        style='font-size:12px;') | (

                h.tr(style='text-decoration:underline;') | (
                    h.th(valign='top',  width='30%') | 'Beschrijving',
                    h.th(valign='top',  width='30%') | 'Aantal   x  Prijs',
                    h.th(width='40%', align='right') | 'Bedrag (Euros)',
                    h.br,
                    h.br,
                ),
                [item.details() for item in self.items],
                h.tr | (
                    h.td(width='50%', align='left') | h.br,
                    h.td(width='30%', align='right', valign='top') | (
                            "Subtotaal = "),
                    h.td(width='20%', align='right', valign='top') | (
                            "%s" % money(self.amountBruto), h.br),
                ),
                self.btw(),
                h.tr | (
                    h.th( width='50%', align='left') | h.br,
                    h.th( width='30%', align='right') | (
                            h.br*2,"TOTAAL = €"),
                    h.th(width='20%', align='right',  valign='bottom',
                                style='text-decoration:underline;') |
                                ("%s" %money(self.amountNetto), h.br),
                ),
            ),
            h.br,
            h.hr,
            h.br,
            h.p(style='font-size:12px;') |  h.br.join((self.amountNetto<0 and self.client.restitutionTerms) or self.client.paymentTerms),
        )

    def body(self):
        return (
            h.table(width="100%") | (
                h.tr | (
                    h.td(width='30%') | self.clientDetails(),
                    h.td(width='50%') | '',
                    h.td(width='20%') | self.supplierDetails(),
                ),
            ),
            h.p(style='font-family:Arial;font-size:20px;text-align:center') |
                    (h.b  | ((self.amountNetto<0 and "CREDIT NOTA") or "FACTUUR")),
            self.headerBlock(),
            self.detailBlock(), 
        )

    def composeName(self):
        return self.client.name

    def composeDescription(self):
        return self.items and self.items[0].description
 
if __name__=="__main__":
    invoice = Invoice()
    invoice.present()

    
