#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci


class Krol(BazowaKlasaWartosci):
    funkcje_obliczajace_wartosc = {
        debiut: [],
        gra_srodkowa: [],
        wczesna_koncowka: [],
        koncowka: [],
        matowanie: [],
    }
