#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from obsluga_gry.config import warunki_biale, warunki_czarne
from .stale_wartosci import wartosci_materialne_bierek
from tools.narzedzia_figur import NarzedziaSzukaniaBierek

from math import fabs


def dajWartoscMaterialna():
    wm = WartoscMaterialna()
    return wm.dajOstatecznaWartoscMaterialna()


class WartoscMaterialna(object):
    def __init__(self):
        self.nsb = NarzedziaSzukaniaBierek()
        self.lista_bialych = self.nsb.dajBierkiPoSlowieKluczowym(warunki_biale)
        self.lista_czarnych = self.nsb.dajBierkiPoSlowieKluczowym(warunki_czarne)

    def dajOstatecznaWartoscMaterialna(self):
        bialy_material = self.dajWartoscMaterialnaBialych()
        czarny_material = self.dajWartoscMaterialnaCzarnych()

        wartosciowanie_pionow = self.dajMaterialneWartosciowaniePionow(bialy_material, czarny_material)
        wartosciowanie_przewagi = self.dajMaterialneWartosciowaniePrzewagi(bialy_material, czarny_material)

        return czarny_material - bialy_material + wartosciowanie_pionow + wartosciowanie_przewagi

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

    def dajMaterialneWartosciowaniePionow(self, bialy_material, czarny_material):
        if bialy_material == czarny_material:
            return 0

        if bialy_material > czarny_material:
            kolor_z_przewaga = warunki_biale
            wspolczynnik = -1
        else:
            kolor_z_przewaga = warunki_czarne
            wspolczynnik = 1

        LP = len(self.nsb.dajBierkiPoSlowieKluczowym(kolor_z_przewaga+'_pion'))
        M = bialy_material + czarny_material

        return wspolczynnik * (LP*30000)/((LP+1) * M)

    def dajMaterialneWartosciowaniePrzewagi(self, bialy_material, czarny_material):
        if bialy_material == czarny_material:
            return 0

        wspolczynnik = -1 if bialy_material > czarny_material else 1
        PM = czarny_material - bialy_material
        M = czarny_material + bialy_material

        return wspolczynnik * (fabs(PM) * 590) / M
