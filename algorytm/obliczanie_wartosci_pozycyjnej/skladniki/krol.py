#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class Krol(BazowaKlasaWartosci):
    funkcje_obliczajace_wartosc = {
        debiut: [],
        gra_srodkowa: [],
        wczesna_koncowka: [],
        koncowka: [],
        matowanie: [],
    }
