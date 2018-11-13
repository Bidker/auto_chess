#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.config import warunki_biale, warunki_czarne
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola


def czyKrolWSzachu(krol):
    from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki

    nsb = NarzedziaSzukaniaBierek()
    kolor_wrogow = warunki_biale if warunki_czarne in krol.nazwa else warunki_czarne
    bierki_wrogow = nsb.dajBierkiPoSlowieKluczowym(kolor_wrogow)

    for bierka in bierki_wrogow:
        mrb = MozliwoscRuchuBierki(bierka)
        pola = mrb.sprawdzMozliweRuchy(False)
        ilosc_bierek_na_polu = len(nsb.dajBierkePoPolu(bierka.pozycja, True))
        pola_atakowane = zmienListeWspolrzednychNaPola(pola['bicie'])
        if krol.pozycja in pola_atakowane and ilosc_bierek_na_polu == 1:
            return True
    return False
