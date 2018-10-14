#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .config import warunki_biale, warunki_czarne


class KolejnoscRuchu(object):
    kolej_na = warunki_biale
    licznik_polruchow = 0
    licznik_ruchow = 0

    @classmethod
    def zmien_ture(cls):
        cls.kolej_na = warunki_czarne if cls.kolej_na == warunki_biale else warunki_biale
        cls.licznik_polruchow += 1
        if cls.licznik_polruchow % 2 != 0:
            cls.licznik_ruchow += 1
