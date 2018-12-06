#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games
from math import fabs  # funkcja służąca do obliczania wartoci bezwzględnej

from obsluga_gry.config import (
    lista_szerokosci,
    lista_wysokosci,
    warunki_biale,
    warunki_czarne,
    szerokosc_pola,
    srodek_pola,
)


def dajOdlegloscPolaDoCentrum(pole):
    pole = naprawPole(pole)
    idx_szerokosci = lista_szerokosci.index(pole[0])
    idx_wysokosci = lista_wysokosci.index(pole[1])
    return fabs(3.5-idx_szerokosci) + fabs(3.5-idx_wysokosci)


def dajOdlegloscMiedzyPolami(pole_a, pole_b):
    pole_a = naprawPole(pole_a)
    pole_b = naprawPole(pole_b)

    idx_szrksc_a = lista_szerokosci.index(pole_a[0])
    idx_szrksc_b = lista_szerokosci.index(pole_b[0])
    idx_wsksc_a = lista_wysokosci.index(pole_a[1])
    idx_wsksc_b = lista_wysokosci.index(pole_b[1])

    return fabs(idx_szrksc_a-idx_szrksc_b) + fabs(idx_wsksc_a-idx_wsksc_b)


def zmienListePolNaWspolrzedneZeSprawdzeniem(lista_pol):
    for i, pole in enumerate(lista_pol):
        if not isinstance(pole, dict):
            lista_pol[i] = wyznaczWspolrzednePoPozycji(pole)
    return lista_pol


def zmienListePolNaWspolrzedne(lista_pol):
    ret = []
    for pole in lista_pol:
        ret.append(wyznaczWspolrzednePoPozycji(pole))
    return ret


def wyznaczWspolrzednePoPozycji(pole):
    pole = naprawPole(pole)
    return {
        'x': dajWspolrzedna(lista_szerokosci.index(pole[0])),
        'y': dajWspolrzedna(lista_wysokosci.index(pole[1])),
    }


def dajWspolrzedna(i):
    return (srodek_pola+(i*szerokosc_pola))


def zmienListeWspolrzednychNaPolaZeSprawdzeniem(lista_wspolrzednych):
    for i, wspolrzedna in enumerate(lista_wspolrzednych):
        if isinstance(wspolrzedna, dict):
            lista_wspolrzednych[i] = zmienWspolrzedneNaPole(wspolrzedna['x'], wspolrzedna['y'])
        else:
            lista_wspolrzednych[i] = naprawPole(wspolrzedna)
    return lista_wspolrzednych


def zmienListeWspolrzednychNaPola(lista_wspolrzednych):
    ret = []
    for wspolrzedne in lista_wspolrzednych:
        ret.append(zmienWspolrzedneNaPole(wspolrzedne['x'], wspolrzedne['y']))
    return ret


def zmienWspolrzedneNaPole(x, y):
    pole = lista_szerokosci[dajIndexPola(x)]
    pole += lista_wysokosci[dajIndexPola(y)]
    return naprawPole(pole)


def dajIndexPola(wspolrzedna):
    return int(((wspolrzedna - srodek_pola)/szerokosc_pola))


def myszNadObiektem(obiekt):
    krawedzie_pola = dajPunktyGranicznePola(obiekt)
    if (games.mouse.x >= krawedzie_pola['lewa'] and
            games.mouse.x <= krawedzie_pola['prawa'] and
            games.mouse.y <= krawedzie_pola['gorna'] and
            games.mouse.y >= krawedzie_pola['dolna']):
        return True
    else:
        return False


def dajPunktyGranicznePola(obiekt):
    return {
        'prawa': obiekt.pozycja_x + srodek_pola,
        'lewa': obiekt.pozycja_x - srodek_pola,
        'gorna': obiekt.pozycja_y + srodek_pola,
        'dolna': obiekt.pozycja_y - srodek_pola,
    }


def czyWszpolrzedneWPolu(x, y):
    if (x >= 0 and x <= games.screen.width and y >= 0 and y <= games.screen.height):
        return True
    return False


def naprawPole(pole):
    if pole[0] in lista_szerokosci:
        return pole
    return pole[1] + pole[0]


def czyPoleNaBiciu(bierka):
    from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki

    mrb = MozliwoscRuchuBierki(bierka)
    kolor = warunki_czarne if warunki_biale in bierka.nazwa else warunki_biale
    return not bool(mrb.wykreslPolaBitePrzez(kolor, [bierka.pozycja]))
