#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games
from obsluga_gry.config import lista_szerokosci, lista_wysokosci


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
    return (50+(i*100))


def zmienListeWspolrzednychNaPolaZeSprawdzeniem(lista_wspolrzednych):
    for i, wspolrzedna in enumerate(lista_wspolrzednych):
        if isinstance(wspolrzedna, dict):
            lista_wspolrzednych[i] = zmienWspolrzedneNaPole(wspolrzedna['x'], wspolrzedna['y'])
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
    return int(((wspolrzedna - 50)/100))


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
        'prawa': obiekt.pozycja_x + 49,
        'lewa': obiekt.pozycja_x - 49,
        'gorna': obiekt.pozycja_y + 49,
        'dolna': obiekt.pozycja_y - 49
    }


def czyWszpolrzedneWPolu(x, y):
    if (x >= 0 and
            x <= games.screen.width and
            y >= 0 and
            y <= games.screen.height):
        return True
    else:
        return False


def naprawPole(pole):
    if pole[0] in lista_szerokosci:
        return pole
    return pole[1] + pole[0]
