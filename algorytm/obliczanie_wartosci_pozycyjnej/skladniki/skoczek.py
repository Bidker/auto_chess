#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tools.narzedzia_pol import dajOdlegloscPolaDoCentrum
from .baza import BazowaKlasaWartosci
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class Skoczek(BazowaKlasaWartosci):

    def __init__(self, kolor):
        super(Skoczek, self).__init__(kolor)
        self.lista_skoczkow = self.nsb.dajBierkiPoSlowieKluczowym(kolor+'_skoczek')

    funkcje_obliczajace_wartosc = {
        debiut: [
            'obliczOdlegloscOdCentrum',
        ],
        gra_srodkowa: [
            'obliczOdlegloscOdCentrum',
        ],
        wczesna_koncowka: [
            'obliczOdlegloscOdCentrum',
        ],
        koncowka: [
            'obliczOdlegloscOdCentrum',
        ],
        matowanie: [],
    }

    def obliczOdlegloscOdCentrum(self):
        wartosc = 0
        for skoczek in self.lista_skoczkow:
            wartosc += dajOdlegloscPolaDoCentrum(skoczek.pozycja)
        return wartosc
