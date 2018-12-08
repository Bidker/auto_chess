#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci
from tools.narzedzia_pol import dajOdlegloscPolaDoCentrum
from algorytm.faza_gry import FazaGry
from obsluga_gry.config import (
    warunki_biale,
    warunki_czarne,
    lista_szerokosci,
    lista_wysokosci,
)
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class Krol(BazowaKlasaWartosci):
    funkcje_obliczajace_wartosc = {
        debiut: [
            'wartosciZaPolozenieKrola',
            'sprawdzPolaPrzedKrolem',
        ],
        gra_srodkowa: [
            'wartosciZaPolozenieKrola',
            'sprawdzPolaPrzedKrolem',
        ],
        wczesna_koncowka: [
            'dajOdlegloscKrolaOdCentrum',
        ],
        koncowka: [
            'dajOdlegloscKrolaOdCentrum',
        ],
        matowanie: [],
    }

    def __init__(self, kolor):
        super(Krol, self).__init__(kolor)
        self.krol = self.nsb.dajBierkiPoSlowieKluczowym(kolor+'_krol')[0]

    def wartosciZaPolozenieKrola(self):
        wartosci_pol = {
            warunki_biale: {
                'b1': 25, 'g1': 25, 'b2': 15, 'a1': 15, 'g2': 15, 'h1': 15, 'c1': 10, 'a2': 10, 'h2': 10,
                'f1': 5, 'e1': 0, 'e2': 0, 'd1': -5, 'c2': -40, 'd2': -40, 'f2': -40, 'a3': -100, 'b3': -100,
                'c3': -100, 'd3': -100, 'e3': -100, 'f3': -100, 'g3': -100, 'h3': -100, 'a4': -200, 'b4': -200,
                'c4': -200, 'd4': -200, 'e4': -200, 'f4': -200, 'g4': -200, 'h4': -200,
            },
            warunki_czarne: {
                'b8': 25, 'g8': 25, 'b7': 15, 'a8': 15, 'g7': 15, 'h8': 15, 'c8': 10, 'a7': 10, 'h7': 10,
                'f8': 5, 'e8': 0, 'e7': 0, 'd8': -5, 'c7': -40, 'd7': -40, 'f7': -40, 'a6': -100, 'b6': -100,
                'c6': -100, 'd6': -100, 'e6': -100, 'f6': -100, 'g6': -100, 'h6': -100, 'a5': -200, 'b5': -200,
                'c5': -200, 'd5': -200, 'e5': -200, 'f5': -200, 'g5': -200, 'h5': -200,
            },
        }

        return wartosci_pol[self.kolor].get(self.krol.pozycja, -400)

    def sprawdzPolaPrzedKrolem(self):
        roznica_wysokosci = 1 if self.kolor == warunki_czarne else -1
        koniec_planszy = 0 if self.kolor == warunki_czarne else 7
        idx_wysokosci_krola = lista_wysokosci.index(self.krol.pozycja[1])

        if idx_wysokosci_krola != koniec_planszy:
            wysokosc = lista_wysokosci[idx_wysokosci_krola + roznica_wysokosci]
            idx_szerokosci = lista_szerokosci.index(self.krol.pozycja[0])
            lst_pol = [self.krol.pozycja[0]+wysokosc]
            if idx_szerokosci != 0:
                lst_pol.append(wysokosc+lista_szerokosci[idx_szerokosci-1])
            if idx_szerokosci != 7:
                lst_pol.append(wysokosc+lista_szerokosci[idx_szerokosci+1])

            piony_z_pol = self.nsb.dajBierkiZPolPoSlowie(self.kolor+'_pion', lst_pol)
            if len(piony_z_pol) != 3:
                return len(piony_z_pol)*15
        return 0

    def dajOdlegloscKrolaOdCentrum(self):
        wspolczynnik = {
            wczesna_koncowka: 3,
            koncowka: 8,
        }

        return wspolczynnik[FazaGry.obecny_etap] * dajOdlegloscPolaDoCentrum(self.krol.pozycja)
