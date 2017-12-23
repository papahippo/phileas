#!/usr/bin/python3
from phileas.page import Page, h, main

Players=[]

def where():
    return("source location ...?")

class Player:
    def __init__(self, name, desc=None):
        self._name = name
        self._desc = desc or "who is {0}?".format(name)
        Players.append(self)

    def says(self, text):
        print(where())
        return h.u | (self._name + ': '), text, h.br*2
    s = says

ks = Player("Kees")
pt = Player("Piet")

class PlayPage(Page):
    def body(self):
        # print(ks.says("some other text"))
        return (
ks.s("some text"),
pt.s("different text"),
        )

if 1: #  __name__ == "__main__":
    main(PlayPage)
