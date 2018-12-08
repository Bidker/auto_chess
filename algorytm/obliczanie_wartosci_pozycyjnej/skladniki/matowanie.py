#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci
from obsluga_gry.config import warunki_biale, warunki_czarne
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from algorytm.faza_gry import FazaGry
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import (
    dajOdlegloscPolaDoCentrum,
    dajOdlegloscMiedzyPolami,
    zmienWspolrzedneNaPole,
)
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
)


class Matowanie(BazowaKlasaWartosci):
    funkcje_obliczajace_wartosc = {
        debiut: [],
        gra_srodkowa: [],
        wczesna_koncowka: [],
        koncowka: [],
        matowanie: [
            'odlegloscMatowanegoKrolaDoCentrum',
            'odlegloscMatujacychOdMatowanegoKrola',
            'szachowanieSkoczkiem',
        ],
    }

    def __init__(self):
        from algorytm.kontroler_obliczania_wartosci import WartoscPlanszy

        self.nsb = NarzedziaSzukaniaBierek()

        self.kolor_matowanych = warunki_biale if WartoscPlanszy.wartosc_materialna > 0 else warunki_czarne
        self.kolor_matujacych = warunki_biale if WartoscPlanszy.wartosc_materialna < 0 else warunki_czarne
        self.wsp_matowanych = -1 if WartoscPlanszy.wartosc_materialna > 0 else 1
        self.matowany_krol = self.nsb.dajBierkiPoSlowieKluczowym(self.kolor_matowanych+'_krol')[0]

    def odlegloscMatowanegoKrolaDoCentrum(self):
        return self.wsp_matowanych*9*dajOdlegloscPolaDoCentrum(self.matowany_krol.pozycja)

    def odlegloscMatujacychOdMatowanegoKrola(self):
        lst_nazw = [self.kolor_matujacych+'_krol', self.kolor_matujacych+'_skoczek']
        matujace = self.nsb.dajBierkiZListyNazw(lst_nazw)
        wartosc = 0

        for matujaca in matujace:
            wartosc += 2*dajOdlegloscMiedzyPolami(self.matowany_krol.pozycja, matujaca.pozycja)
        return -self.wsp_matowanych*wartosc

    def szachowanieSkoczkiem(self):
        lst_skoczkow = self.nsb.dajBierkiPoSlowieKluczowym(self.kolor_matujacych+'_skoczek')
        wartosc = 0

        for skoczek in lst_skoczkow:
            ruch = MozliwoscRuchuBierki(skoczek).sprawdzMozliweRuchy()
            if self.matowany_krol.pozycja in ruch['bicie']:
                wartosc += 15

        return wartosc
