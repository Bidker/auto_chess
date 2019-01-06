#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.config import warunki_biale, warunki_czarne
from tools.narzedzia_pol import zmienWspolrzedneNaPole
from tools.narzedzia_matow import NarzedziaMatow
from .baza import BazowaKlasaWartosci
from algorytm.faza_gry import FazaGry
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class Goniec(BazowaKlasaWartosci):

    funkcje_obliczajace_wartosc = {
        debiut: [],
        gra_srodkowa: [
            'wzorHartmana',
        ],
        wczesna_koncowka: [
            'wzorHartmana',
        ],
        koncowka: [],
        matowanie: [],
    }

    def __init__(self, kolor):
        super(Goniec, self).__init__(kolor)
        self.lista_goncow = self.nsb.dajBierkiPoSlowieKluczowym(kolor+'_goniec')
        self.lista_sojusznikow = self.nsb.dajBierkiPoSlowieKluczowym(kolor)

    def wzorHartmana(self):
        wspolczynnik = {
            gra_srodkowa: 3,
            wczesna_koncowka: 1,
        }

        wartosci_bierek = {
            'bialy_pion': 0,
            'czarny_pion': 0,
            'bialy_skoczek': 3,
            'czarny_skoczek': 3,
            'bialy_goniec': 4,
            'czarny_goniec': 4,
            'bialy_wieza': 5,
            'czarny_wieza': 5,
            'bialy_hetman': 9,
            'czarny_hetman': 9,
            'bialy_krol': 10,
            'czarny_krol': 10,
        }

        wartosc = 0

        for goniec in self.lista_goncow:
            mrb = MozliwoscRuchuBierki(goniec)
            mozliwe_ruchy = mrb.sprawdzMozliweRuchy()

            # obliczanie EM
            for wspolrzedne in mozliwe_ruchy['bicie']:
                pole = zmienWspolrzedneNaPole(x=wspolrzedne['x'], y=wspolrzedne['y'])
                bierka = self.nsb.dajBierkePoPolu(pole)
                wartosc += wartosci_bierek[bierka.nazwa]

            # obliczanie OM i OW
            wartosc += self._obliczWartoscOMiOW(goniec)

            # obliczanie DL
            mrb = MozliwoscRuchuBierki(goniec)
            wartosc += len(mrb.dajListyRuchowPoprzecznych(goniec)) - 7

        return wspolczynnik[FazaGry.obecny_etap] * wartosc

    def _obliczWartoscOMiOW(self, goniec):
        wartosc = 0
        for bierka in self.lista_sojusznikow:
            if 'pion' in bierka.nazwa:
                wartosc = self._obliczDlaPionow(goniec, bierka)
            elif 'skoczek' in bierka.nazwa or 'goniec' in bierka.nazwa:
                wartosc += 1
            elif 'wieza' in bierka.nazwa:
                wartosc += 2
            elif 'hetman' in bierka.nazwa:
                wartosc += 3
        return wartosc

    def _obliczDlaPionow(self, goniec, bierka):
        wartosc = 0
        pozycja_gonca = int(goniec.pozycja[1])
        pozycja_bierki = int(bierka.pozycja[1])

        if warunki_biale == self.kolor:
            if pozycja_gonca > pozycja_bierki:
                wartosc += 1
            elif pozycja_gonca < pozycja_bierki and pozycja_bierki <= 4:
                wartosc -= 5
            elif pozycja_gonca < pozycja_bierki and pozycja_bierki > 4:
                wartosc -= 1
        if warunki_czarne == self.kolor:
            if pozycja_gonca < pozycja_bierki:
                wartosc += 1
            elif pozycja_gonca > pozycja_bierki and pozycja_bierki >= 4:
                wartosc -= 5
            elif pozycja_gonca > pozycja_bierki and pozycja_bierki < 4:
                wartosc -= 1

        return wartosc
