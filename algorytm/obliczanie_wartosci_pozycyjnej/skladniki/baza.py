#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from algorytm.faza_gry import FazaGry
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class BazowaKlasaWartosci(object):

    funkcje_obliczajace_wartosc = {
        debiut: [],
        gra_srodkowa: [],
        wczesna_koncowka: [],
        koncowka: [],
        matowanie: [],
    }

    def __init__(self, kolor):
        self.nsb = NarzedziaSzukaniaBierek()
        self.lista_bierek = self.nsb.dajBierkiPoSlowieKluczowym(kolor)
        self.kolor = kolor

    def dajWartoscPozycyjna(self):
        wartosc = 0
        for nazwa_funkcji in self.funkcje_obliczajace_wartosc[FazaGry.obecny_etap]:
            funkcja = getattr(self, nazwa_funkcji)
            wartosc += funkcja.__call__(self=self)
        return wartosc
