#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci
from obsluga_gry.config import warunki_biale, warunki_czarne
from tools.narzedzia_pol import dajOdlegloscPolaDoCentrum, dajOdlegloscMiedzyPolami
from algorytm.faza_gry import FazaGry
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class Hetman(BazowaKlasaWartosci):
    funkcje_obliczajace_wartosc = {
        debiut: [
            'odlegloscHetmanaOdCentrum',
        ],
        gra_srodkowa: [
            'odlegloscOdWrogiegoKrola',
        ],
        wczesna_koncowka: [
            'odlegloscHetmanaOdCentrum',
            'odlegloscOdWrogiegoKrola',
        ],
        koncowka: [
            'odlegloscHetmanaOdCentrum',
            'odlegloscOdWrogiegoKrola',
        ],
        matowanie: [],
    }

    def __init__(self, kolor):
        super(Hetman, self).__init__(kolor)
        self.lista_hetmanow = self.nsb.dajBierkiPoSlowieKluczowym(kolor+'_hetman')

    def odlegloscHetmanaOdCentrum(self):
        wspolczynnik = {
            debiut: -2,
            wczesna_koncowka: 2,
            koncowka: 4,
        }
        wartosc = 0

        for hetman in self.lista_hetmanow:
            wartosc += wspolczynnik[FazaGry.obecny_etap] * dajOdlegloscPolaDoCentrum(hetman.pozycja)

        return wartosc

    def odlegloscOdWrogiegoKrola(self):
        wartosc = 0
        kolor_wroga = warunki_biale if self.kolor == warunki_czarne else warunki_czarne
        wrogi_krol = self.nsb.dajBierkiPoSlowieKluczowym(kolor_wroga+'_krol')[0]

        for hetman in self.lista_hetmanow:
            wartosc += 3*dajOdlegloscMiedzyPolami(hetman.pozycja, wrogi_krol.pozycja)

        return wartosc
