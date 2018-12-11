#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .stale_wartosci import debiut, gra_srodkowa, wczesna_koncowka, koncowka, matowanie
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_obliczania_wartosci import NarzedziaObliczaniaWartosci
from obsluga_gry.config import warunki_biale, warunki_czarne

from math import fabs


class FazaGry(object):
    obecny_etap = debiut

    def __init__(self):
        self.now = NarzedziaObliczaniaWartosci()
        self.nsb = NarzedziaSzukaniaBierek()

    def sprawdzFazeGry(self):
        lst_nieporuszonych = self.nsb.dajNieruszoneBierkiBezKroli()

        if len(lst_nieporuszonych) >= 18:
            FazaGry.obecny_etap = debiut
        else:
            now = NarzedziaObliczaniaWartosci()
            suma_materialu = now.sumaMaterialuNaPlanszyBezKroli()

            if self.sprawdzCzyMatowanie():
                FazaGry.obecny_etap = matowanie
            elif suma_materialu > 4300:
                FazaGry.obecny_etap = gra_srodkowa
            elif suma_materialu > 2800:
                FazaGry.obecny_etap = wczesna_koncowka
            elif suma_materialu < 2800:
                FazaGry.obecny_etap = koncowka

    def sprawdzCzyMatowanie(self):
        roznica_materialu = self.now.roznicaMaterialuNaPlanszy()

        if fabs(roznica_materialu) > 450:
            matujacy = warunki_biale if roznica_materialu < 0 else warunki_czarne
            lst_bierek_matujacych = self.nsb.dajBierkiPoSlowieKluczowym(matujacy)
            return len(lst_bierek_matujacych) >= 2
        return False
