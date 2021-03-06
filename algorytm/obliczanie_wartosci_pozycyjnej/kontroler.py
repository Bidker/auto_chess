#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .skladniki.pion import Pion
from .skladniki.skoczek import Skoczek
from .skladniki.goniec import Goniec
from .skladniki.wieza import Wieza
from .skladniki.hetman import Hetman
from .skladniki.krol import Krol
from .skladniki.inne_aspekty import InneAspekty
from .skladniki.matowanie import Matowanie
from algorytm.faza_gry import FazaGry
from algorytm.stale_wartosci import matowanie
from obsluga_gry.config import warunki_biale, warunki_czarne


def dajWartoscPozycyjna():
    kwp = KontrolerWartosciPozycyjnych()
    return kwp.dajCalkowitaWartoscPozycyjna()


class KontrolerWartosciPozycyjnych(object):
    roszada_wykonana = {
        warunki_biale: False,
        warunki_czarne: False,
    }

    lista_klas = [
        InneAspekty,
        Pion,
        Skoczek,
        Goniec,
        Wieza,
        Hetman,
        Krol,
    ]

    def dajCalkowitaWartoscPozycyjna(self):
        wartosc = self.dajWartosciPozycyjnePoKolorze(warunki_czarne) - self.dajWartosciPozycyjnePoKolorze(warunki_biale)
        if FazaGry.obecny_etap == matowanie:
            wartosc += Matowanie().dajWartoscPozycyjna()
        return wartosc

    def dajWartosciPozycyjnePoKolorze(self, kolor):
        wartosci = 0
        for klasa in self.lista_klas:
            if len(klasa.funkcje_obliczajace_wartosc[FazaGry.obecny_etap]):
                obiekt = klasa(kolor)
                wartosci += obiekt.dajWartoscPozycyjna()
        return wartosci
