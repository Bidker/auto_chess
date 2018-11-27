#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tools.narzedzia_pol import zmienWspolrzedneNaPole, wyznaczWspolrzednePoPozycji
from tools.narzedzia_figur import NarzedziaSzukaniaBierek

from contextlib import contextmanager


@contextmanager
def wykonajPseudobicie(bierka, ruch):
    nsb = NarzedziaSzukaniaBierek()
    pole = zmienWspolrzedneNaPole(x=ruch['x'], y=ruch['y'])
    bierka_bita = nsb.dajBierkePoPolu(pole)
    with wykonajPseudoruch(bierka, ruch):
        bierka_bita.czy_zbita = True
        yield
        bierka_bita.czy_zbita = False


@contextmanager
def wykonajPseudoroszade(bierka, ruch):
    pozycja = zmienWspolrzedneNaPole(x=ruch['x'], y=ruch['y'])
    nsb = NarzedziaSzukaniaBierek()
    szerokosc = 'a' if pozycja[0] == 'c' else 'h'
    nowe_pole = 'd'+pozycja[1] if szerokosc == 'a' else 'f'+pozycja[1]
    nowe_wspolrzedne = wyznaczWspolrzednePoPozycji(nowe_pole)

    wieza = nsb.dajBierkePoPolu(szerokosc+pozycja[1])
    with wykonajPseudoruch(wieza, nowe_wspolrzedne):
        with wykonajPseudoruch(bierka, ruch):
            yield


@contextmanager
def wykonajPseudoruch(bierka, ruch):
    pozycje_wyjsciowe = {
        'x': bierka.pozycja_x,
        'y': bierka.pozycja_y,
        'pozycja': bierka.pozycja,
    }

    bierka.pozycja = zmienWspolrzedneNaPole(x=ruch['x'], y=ruch['y'])
    bierka.pozycja_x = ruch['x']
    bierka.pozycja_y = ruch['y']

    yield

    bierka.pozycja = pozycje_wyjsciowe['pozycja']
    bierka.pozycja_x = pozycje_wyjsciowe['x']
    bierka.pozycja_y = pozycje_wyjsciowe['y']
