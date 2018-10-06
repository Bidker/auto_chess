#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager


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
        if kolor_przecinikow == 'biale':
            bierka = 'bialy_' + bierka
        else:
            bierka = 'czarny_' + bierka
        obiekt = self.dajBierkePoNazwie(bierka)
        yield obiekt
