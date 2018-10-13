#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.config import slownik_bierek, warunki_biale
from .narzedzia_pol import naprawPole

from contextlib import contextmanager
from copy import deepcopy


class NarzedziaSzukaniaBierek(object):

    def __init__(self):
        from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur
        of = ObiektyFigur()
        self.lista_obiektow = of.dajObiektyFigur()

    def dajBierkePoNazwie(self, nazwa_bierki):
        for bierka in self.lista_obiektow:
            if bierka.nazwa == nazwa_bierki and not bierka.czy_zbita:
                return bierka

    def dajZaznaczonaBierke(self):
        for bierka in self.lista_obiektow:
            if bierka.zaznaczony and not bierka.czy_zbita:
                return bierka

    def dajBierkePoPolu(self, pole):
        for bierka in self.lista_obiektow:
            if naprawPole(bierka.pozycja) == naprawPole(pole) and not bierka.czy_zbita:
                return bierka

    @contextmanager
    def szukanieBierki(self, bierka, kolor_przecinikow):
        if kolor_przecinikow == warunki_biale:
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
