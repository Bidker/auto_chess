#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.config import slownik_bierek

from contextlib import contextmanager
from copy import deepcopy


class NarzedziaSzukaniaBierek(object):

    def __init__(self):
        from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur
        of = ObiektyFigur()
        self.lista_obiektow = of.dajObiektyFigur()

    def dajBierkePoNazwie(self, nazwa_bierki):
        for bierka in self.lista_obiektow:
            if bierka.nazwa == nazwa_bierki:
                return bierka

    @contextmanager
    def szukanieBierki(self, bierka, kolor_przecinikow):
        if kolor_przecinikow in ('biale'):  # w razie potrzeby można dodać inne odmiany
            bierka = 'bialy_' + bierka
        else:
            bierka = 'czarny_' + bierka
        obiekt = self.dajBierkePoNazwie(bierka)
        yield obiekt

    def dajSlownikZajetychPol(self):
        slownik = {
            'czarne': self.dajSlownikCzarnych(),
            'biale': self.dajSlownikBialych(),
        }
        return slownik

    def dajSlownikBialych(self):
        return self._dajSlownikPozycji('bialy')

    def dajSlownikCzarnych(self):
        return self._dajSlownikPozycji('czarny')

    def _dajSlownikPozycji(self, kolor):
        slownik = deepcopy(slownik_bierek)
        index = len(kolor) + 1

        for bierka in self.lista_obiektow:
            if kolor in bierka.nazwa:
                slownik[bierka.nazwa[index:]].append(bierka.pozycja)
        return slownik
