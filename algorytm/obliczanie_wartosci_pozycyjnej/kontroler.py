#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''from .skladniki.pion import Pion
from .skladniki.skoczek import Skoczek
from .skladniki.goniec import Goniec
from .skladniki.wieza import Wieza
from .skladniki.hetman import Hetman
from .skladniki.krol import Krol
from .skladniki.matowanie import Matowanie'''
from .skladniki.inne_aspekty import InneAspekty
from algorytm.faza_gry import FazaGry
from obsluga_gry.config import warunki_biale, warunki_czarne


def dajWartoscPozycyjna():
    kwp = KontrolerWartosciPozycyjnych()
    return kwp.dajCalkowitaWartoscPozycyjna()


class KontrolerWartosciPozycyjnych(object):
    roszada_wykonana = {
        warunki_biale: False,
        warunki_czarne: False,
    }

    def dajCalkowitaWartoscPozycyjna(self):
        return self.dajWartoscPozycyjnaCzarnych() - self.dajWartoscPozycyjnaBialych()

    def dajWartoscPozycyjnaCzarnych(self):
        ia = InneAspekty(warunki_czarne)
        inne_aspekty_pozycji = ia.dajWartoscPozycyjna()
        return inne_aspekty_pozycji

    def dajWartoscPozycyjnaBialych(self):
        ia = InneAspekty(warunki_biale)
        inne_aspekty_pozycji = ia.dajWartoscPozycyjna()
        return inne_aspekty_pozycji
