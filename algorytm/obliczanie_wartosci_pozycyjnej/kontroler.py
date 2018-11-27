#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''from .skladniki.pion import Pion
from .skladniki.skoczek import Skoczek
from .skladniki.goniec import Goniec
from .skladniki.wieza import Wieza
from .skladniki.hetman import Hetman
from .skladniki.krol import Krol
from .skladniki.matowanie import Matowanie
from .skladniki.inne_aspekty import InneAspekty'''
from algorytm.faza_gry import FazaGry


def dajWartoscPozycyjna():
    kwp = KontrolerWartosciPozycyjnych()
    return kwp.dajWartoscPozycyjnaCzarnych() - kwp.dajWartoscPozycyjnaBialych()


class KontrolerWartosciPozycyjnych(object):

    def dajWartoscPozycyjnaCzarnych(self):
        return 0

    def dajWartoscPozycyjnaBialych(self):
        return 0
