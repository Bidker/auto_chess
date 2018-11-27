#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .narzedzia_figur import NarzedziaSzukaniaBierek
from algorytm.stale_wartosci import wartosci_materialne_bierek
from obsluga_gry.config import warunki_biale, warunki_czarne


class NarzedziaObliczaniaWartosci(object):
    def __init__(self):
        self.nsb = NarzedziaSzukaniaBierek()

    def sumaMaterialuNaPlanszyBezKroli(self):
        suma = 0
        for bierka in self.nsb.dajBierkiBezKroli():
            for klucz, wartosc in wartosci_materialne_bierek.items():
                if klucz in bierka.nazwa:
                    suma += wartosc
        return suma

    def roznicaMaterialuNaPlanszy(self):
        roznica = 0
        for bierka in self.nsb.lista_obiektow:
            for klucz, wartosc in wartosci_materialne_bierek.items():
                if klucz in bierka.nazwa:
                    if warunki_biale in bierka.nazwa:
                        roznica -= wartosc
                    elif warunki_czarne in bierka.nazwa:
                        roznica += wartosc

        return roznica
