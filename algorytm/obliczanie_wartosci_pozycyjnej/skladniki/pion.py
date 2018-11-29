#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci
from obsluga_gry.config import warunki_biale, warunki_czarne, lista_szerokosci
from tools.narzedzia_pol import dajOdlegloscPolaDoCentrum
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
    scisle_centrum,
    okolice_centrum,
)


class Pion(BazowaKlasaWartosci):

    funkcje_obliczajace_wartosc = {
        debiut: [
            'sprawdzIzolowanePiony',
            'sprawdzZdublowanePiony',
            'doliczPktZaCentrum',
            'sprawdzOdlegloscDoCentrum',
            'ocenaDebiutowa',
        ],
        gra_srodkowa: [
            'sprawdzIzolowanePiony',
            'sprawdzZdublowanePiony',
            'doliczPktZaCentrum',
            'sprawdzOdlegloscDoCentrum',
            'wplywKoncaPlanszy',
        ],
        wczesna_koncowka: [
            'sprawdzIzolowanePiony',
            'sprawdzZdublowanePiony',
            'doliczPktZaCentrum',
            'wplywKoncaPlanszy',
        ],
        koncowka: [
            'sprawdzIzolowanePiony',
            'sprawdzZdublowanePiony',
            'doliczPktZaCentrum',
            'wplywKoncaPlanszy',
        ],
        matowanie: [],
    }

    def __init__(self, kolor):
        super(Pion, self).__init__(kolor)
        self.lista_pionow = self.nsb.dajBierkiPoSlowieKluczowym(kolor+'_pion')

    @staticmethod
    def sprawdzIzolowanePiony(**kwargs):
        self = kwargs['self']
        znak = '2' if self.kolor == warunki_biale else '7'
        wartosc = 0

        for pion in self.lista_pionow:
            if znak not in pion.pozycja:
                lst_poz = []
                idx = lista_szerokosci.index(pion.pozycja[0])
                if idx < 7:
                    pozycja = lista_szerokosci[idx+1] + pion.pozycja[1]
                    lst_poz.append(pozycja)
                if idx > 0:
                    pozycja = lista_szerokosci[idx-1] + pion.pozycja[1]
                    lst_poz.append(pozycja)
                for poz in lst_poz:
                    bierka = self.nsb.dajBierkePoPolu(poz)
                    if not bierka or 'pion' not in bierka.nazwa:
                        wartosc -= 20

        return wartosc

    @staticmethod
    def sprawdzZdublowanePiony(**kwargs):
        self = kwargs['self']
        slownik_kolumn = {}
        wartosc = 0

        for pion in self.lista_pionow:
            if pion.pozycja[0] not in slownik_kolumn.keys():
                slownik_kolumn[pion.pozycja[0]] = 0
            slownik_kolumn[pion.pozycja[0]] += 1

        for klucz, wrt in slownik_kolumn.items():
            if wrt >= 2:
                wartosc -= wrt*10

        return wartosc

    @staticmethod
    def doliczPktZaCentrum(**kwargs):
        self = kwargs['self']
        wartosc = 0

        for pion in self.lista_pionow:
            if pion.pozycja in scisle_centrum:
                wartosc += 15
            elif pion.pozycja in okolice_centrum:
                wartosc += 10

        return wartosc

    @staticmethod
    def sprawdzOdlegloscDoCentrum(**kwargs):
        self = kwargs['self']
        wartosc = 0

        for pion in self.lista_pionow:
            wartosc = dajOdlegloscPolaDoCentrum(pion.pozycja)

        return wartosc

    @staticmethod
    def ocenaDebiutowa(**kwargs):
        self = kwargs['self']
        wartosc = 0
        poz_pionow_przed_kr_i_hetm = ['d2', 'e2'] if self.kolor == warunki_biale else ['d7', 'e7']

        for pozycja in poz_pionow_przed_kr_i_hetm:
            bierka = self.nsb.dajBierkePoPolu(pozycja)
            if bierka:
                wartosc -= 10

        if wartosc == -20:
            wartosc -= 50

        return wartosc

    @staticmethod
    def wplywKoncaPlanszy(**kwargs):
        self = kwargs['self']
        ostatnia_linia = '8' if self.kolor == warunki_biale else '1'
        warunki = 0

        for pion in self.lista_pionow:
            if ostatnia_linia in pion.pozycja:
                warunki -= 100

        return warunki
