#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .config import warunki_biale, warunki_czarne
from algorytm.kontroler_obliczania_wartosci import uruchomAlgorytm
from tools.narzedzia_matow import NarzedziaMatow


class KolejnoscRuchu(object):
    kolej_na = warunki_biale
    licznik_polruchow = 0
    licznik_ruchow = 0

    @classmethod
    def zmien_ture(cls):
        cls.kolej_na = warunki_czarne if cls.kolej_na == warunki_biale else warunki_biale
        cls.licznik_polruchow += 1
        if cls.licznik_polruchow % 2 != 0:
            cls.licznik_ruchow += 1
        kr = cls()
        kr.sprawdzKrycieBierek()

        if cls.kolej_na == warunki_czarne:
            uruchomAlgorytm()

    def sprawdzKrycieBierek(self):
        from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur

        for bierka in ObiektyFigur.dajObiektyFigur():
            bierka.kryta = False
        for bierka in ObiektyFigur.dajObiektyFigur():
            nm = NarzedziaMatow(bierka)
            for kryta in ObiektyFigur.dajObiektyFigur():
                if kryta.kolor == bierka.kolor and kryta.pozycja != bierka.pozycja:
                    nm.ustawKrycieBierki(kryta)
