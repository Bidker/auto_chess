#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.kolejnosc_ruchu import KolejnoscRuchu
from obsluga_gry.config import warunki_biale, warunki_czarne, lista_szerokosci
from tools.narzedzia_pol import naprawPole
from tools.narzedzia_figur import NarzedziaSzukaniaBierek


class NarzedziaWyznaczaniaRuchow(object):

    def czyMozliwaRoszadaDluga(self, obiekt_krola):
        pole = 'a1' if warunki_biale == KolejnoscRuchu.kolej_na else 'a8'
        return self.czyMozliwaRoszada(obiekt_krola, pole)

    def czyMozliwaRoszadaKrotka(self, obiekt_krola):
        pole = 'h1'if warunki_biale == KolejnoscRuchu.kolej_na else 'h8'
        return self.czyMozliwaRoszada(obiekt_krola, pole)

    def czyMozliwaRoszada(self, obiekt_krola, pole):
        from obsluga_gry.warunki_wygranej import WarunkiWygranej

        nsb = NarzedziaSzukaniaBierek()
        wieza = nsb.dajBierkePoPolu(pole)
        if wieza:
            czy_nie_poruszone = not (obiekt_krola.czy_poruszona or wieza.czy_poruszona)
            czy_krol_nie_szachowany = bool(
                not WarunkiWygranej.zagrozony_krol or
                WarunkiWygranej.zagrozony_krol.nazwa != obiekt_krola.nazwa
            )
            return (
                czy_nie_poruszone and
                czy_krol_nie_szachowany and
                self.czyNaSzerokosciMiedzyPolamiNieMaBierek(obiekt_krola.pozycja, wieza.pozycja)
            )
        return False

    def czyNaSzerokosciMiedzyPolamiNieMaBierek(self, pole_a, pole_b):
        from tools.narzedzia_figur import NarzedziaSzukaniaBierek

        pole_a = naprawPole(pole_a)
        pole_b = naprawPole(pole_b)

        if pole_a[1] != pole_b[1]:
            return False

        idx_a = lista_szerokosci.index(pole_a[0])
        idx_b = lista_szerokosci.index(pole_b[0])

        if idx_a < idx_b:
            minor_idx = idx_a + 1
            max_idx = idx_b
        else:
            minor_idx = idx_b + 1
            max_idx = idx_a

        nsb = NarzedziaSzukaniaBierek()
        for i in range(minor_idx, max_idx):
            pole = lista_szerokosci[i] + pole_a[1]
            bierka = nsb.dajBierkePoPolu(pole)
            if bierka:
                return False
        return True
