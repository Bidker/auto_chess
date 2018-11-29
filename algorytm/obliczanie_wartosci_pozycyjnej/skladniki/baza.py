#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from algorytm.faza_gry import FazaGry


class BazowaKlasaWartosci(object):

    def __init__(self, kolor):
        self.nsb = NarzedziaSzukaniaBierek()
        self.kolor = kolor

    def dajWartoscPozycyjna(self):
        wartosc = 0
        for nazwa_funkcji in self.funkcje_obliczajace_wartosc[FazaGry.obecny_etap]:
            funkcja = getattr(self, nazwa_funkcji)
            wartosc += funkcja.__call__(self=self)
        return wartosc
