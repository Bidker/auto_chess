#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.config import warunki_biale, warunki_czarne
from .narzedzia_pol import zmienListeWspolrzednychNaPola


class NarzedziaMatow(object):

    def __init__(self, kryjaca):
        self.mrb = MozliwoscRuchuBierki(kryjaca)
        self.kryjaca = kryjaca
        self.kolor_bierki = warunki_biale if warunki_biale in self.kryjaca.nazwa else warunki_czarne

    def ustawKrycieBierki(self, bierka_kryta):
        bierka_kryta.kryta = True if self.sprawdzKrycieBierek(bierka_kryta) else bierka_kryta.kryta

    def sprawdzKrycieBierek(self, bierka_kryta):
        if 'pion' in self.kryjaca.nazwa:
            return self._dajDlaPiona(bierka_kryta)
        elif 'skoczek' in self.kryjaca.nazwa:
            return self._dajDlaSkoczka(bierka_kryta)

        kryta = False
        if 'wieza' or 'hetman' or 'krol' in self.kryjaca.nazwa:
            kryta = self._dajKrzyzowy(bierka_kryta)
        if ('goniec' or 'hetman' or 'krol' in self.kryjaca.nazwa) and not kryta:
            kryta = self._dajIksowy(bierka_kryta)

        return kryta

    def _dajDlaPiona(self, bierka_kryta):
        pola_kryte = self.mrb.dajBiciePionow(self.kryjaca.pozycja, self.kryjaca.nazwa)
        if bierka_kryta.pozycja in pola_kryte:
            return True
        return False

    def _dajDlaSkoczka(self, bierka_kryta):
        pola_kryte = self.mrb.przygotujRuchySKoczka(self.kryjaca.pozycja)
        if bierka_kryta.pozycja in pola_kryte:
            return True
        return False

    def _dajKrzyzowy(self, bierka_kryta):
        listy_ruchow = self.mrb.dajListyRuchowKrzyzowych(self.kryjaca)
        for lista in listy_ruchow:
            if self._sprawdzDlaProstych(lista, bierka_kryta):
                return True
        return False

    def _dajIksowy(self, bierka_kryta):
        listy_ruchow = self.mrb.dajListyRuchowPoprzecznych(self.kryjaca)
        for lista in listy_ruchow:
            if self._sprawdzDlaProstych(lista, bierka_kryta):
                return True
        return False

    def _sprawdzDlaProstych(self, lista, bierka_kryta):
        mozliwe_pola = zmienListeWspolrzednychNaPola(lista)
        mozliwe_pola = self.mrb.sprawdzCzyZawadza(mozliwe_pola, 1)
        if mozliwe_pola and bierka_kryta.pozycja == mozliwe_pola[-1]:
            return True
