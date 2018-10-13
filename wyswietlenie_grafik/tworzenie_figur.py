#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from obsluga_gry.config import figury_pola_startowe
from .figury import Figury


def pokazFigury():
    obiekty_figur = ObiektyFigur.dajObiektyFigur()
    wyswietlObiektyNaEkranie(obiekty_figur)
    return obiekty_figur


def stworzListeFigur():
    lista_bierek = []
    lista_bierek.append(figury_pola_startowe['biale'])
    lista_bierek.append(figury_pola_startowe['czarne'])

    return lista_bierek


def wyswietlObiektyNaEkranie(obiekty_do_wyswietlenia):
    for obiekt in obiekty_do_wyswietlenia:
        games.screen.add(obiekt)


class ObiektyFigur(object):
    '''Zastosowanie wzorca projektowego Singleton'''
    stworzone_bierki = []

    def __init__(self):
        pass

    @classmethod
    def dajObiektyFigur(cls):
        if not cls.stworzone_bierki:
            figury = stworzListeFigur()
            for kolory in figury:
                for bierka, pozycje_bierek in kolory.items():
                    for pozycja in pozycje_bierek:
                        bierka_stworzona = Figury(bierka, pozycja)
                        cls.stworzone_bierki.append(bierka_stworzona)

        return [bierka for bierka in cls.stworzone_bierki if not bierka.czy_zbita]
