#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from .config import warunki_biale, warunki_czarne
from .figury_mozliwosc_ruchu import MozliwoscRuchuBierki
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

    def sprawdzKrycieBierek(self):
        from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur

        for bierka in ObiektyFigur.dajObiektyFigur():
            bierka.kryta = False
        for bierka in ObiektyFigur.dajObiektyFigur():
            nm = NarzedziaMatow(bierka)
            for kryta in ObiektyFigur.dajObiektyFigur():
                if kryta.kolor == bierka.kolor and kryta.pozycja != bierka.pozycja:
                    nm.ustawKrycieBierki(kryta)


def koniecGry():
    from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur
    from wyswietlenie_grafik.mozliwy_ruch import PodswietlMozliwePola

    for obiekt in ObiektyFigur.dajObiektyFigur():
        obiekt.zbita()
    for obiekt in PodswietlMozliwePola.lista_podswietlen:
        obiekt.destroy()
    games.screen.quit()
