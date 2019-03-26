#!/usr/bin/python
# -*- encoding: utf8 -*-
from __future__ import print_function
from entity import *
from entity.company import *
from phileas.page import Page, h

class AccountingException(Exception):
    pass


class Common:
    prevOutgoingitem = None


class OutgoingItem(Entity):
# currently in transition to new Entity class , hence strange mix of arguments
    expressExtra = {None: 'n.v.t', False: 'al gedaan'}
    keyFields = ('sequenceNumber',)

    def __init__(self,
        date:str='',
        sequenceNumber:str=None,
        supplierName:str="(unknown supplier)",
        description:str="(no description)",
        amountBruto:FloatOrNone=None,
        percentBtw:FloatOrNone=0.0,
        amountBtw:FloatOrNone=None,
        amountNetto:FloatOrNone=None,
        paidFromPrivate:BoolOrNone=None,
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
            h.td(style='border:1px solid black;text-align:left') | self.date[:6],
            h.td(style='text-align:left')  | "%s" % self.sequenceNumber,
            h.td(style='text-align:left')  | self.composeName(),
            h.td(style='text-align:left')  | self.composeDescription(),
            h.td(style='text-align:right') | "%s" % money(self.amountBruto),
        )
        if self.chargeBtw is None:
            tr |= (
                h.td(style='text-align:centre') | "n.v.t.",
                h.td(style='text-align:right')  | " ",
            )
        else:
            tr |= (
                h.td(style='text-align:right') | "%s%%" % (self.percentBtw or 0),
                h.td(style='text-align:right') | money(self.amountBtw),
            )
        tr |= (
            h.td(style='text-align:right') | "%s" % money(self.amountNetto),
        )
        if self.paidFromPrivate is not None:
            tr |= (h.td(style='text-align:right') |
                   ((self.paidFromPrivate and money(self.paidFromPrivate)) or ''),
            )
        return tr
