#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from obsluga_gry.config import warunki_biale, warunki_czarne
from .stale_wartosci import wartosci_materialne_bierek
from tools.narzedzia_figur import NarzedziaSzukaniaBierek


def dajWartoscMaterialna():
    wm = WartoscMaterialna()
    return wm.dajWartoscMaterialnaCzarnych() - wm.dajWartoscMaterialnaCzarnych()


class WartoscMaterialna(object):
    def __init__(self):
        nsb = NarzedziaSzukaniaBierek()
        self.lista_bialych = nsb.dajBierkiPoSlowieKluczowym(warunki_biale)
        self.lista_czarnych = nsb.dajBierkiPoSlowieKluczowym(warunki_czarne)

    def dajWartoscMaterialnaBialych(self):
        return self._dajSumePoLiscieISlowie(self.lista_bialych, warunki_biale)

    def dajWartoscMaterialnaCzarnych(self):
        return self._dajSumePoLiscieISlowie(self.lista_czarnych, warunki_czarne)

    def _dajSumePoLiscieISlowie(self, lista, warunki):
        suma = 0
        len_war = len(warunki)
        for bierka in lista:
            suma += wartosci_materialne_bierek[bierka.nazwa[len_war+1:]]
        return suma
