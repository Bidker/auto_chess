#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta

from algorytm.faza_gry import FazaGry
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
)


class NarzedziaStatystyk(object):
    czasy_wykonan = {
        debiut: [],
        gra_srodkowa: [],
        wczesna_koncowka: [],
        koncowka: [],
        matowanie: [],
    }

    @classmethod
    def zapiszCzasWykonania(cls, czas):
        cls.czasy_wykonan[FazaGry.obecny_etap].append(czas)

    @classmethod
    def dajCzasyWykonan(cls):
        sl = {}
        for faza, lst_czas in cls.czasy_wykonan.items():
            if len(lst_czas):
                sl[faza] = sum(lst_czas, timedelta(0))/len(lst_czas)
        return sl

    @classmethod
    def wyswietlCzasy(cls):
        for faza, czas in cls.dajCzasyWykonan().items():
            print('Średni czas wykonania algorytmu w fazie ' + faza + ': ' + str(czas))
