#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki


class WarunkiWygranej(object):

    def __init__(self, bierka):
        from wyswietlenie_grafik.figury import Figury

        self.zagrozony_krol = Figury.zagrozony_krol
        self.szukanie_bierek = NarzedziaSzukaniaBierek()
        self.ruch_bierek = MozliwoscRuchuBierki(bierka)
        self.pola_bierki = ruch_bierek.sprawdzMozliweRuchy(bierka)
        self.bierka = bierka

    def sprawdz_warunki_wygranej(self):
        zagrozony_krol = self.sprawdz_czy_krol_zagrozony()
        if zagrozony_krol:
            self.sprawdz_mozliwosc_ucieczki(zagrozony_krol)

    def sprawdz_czy_krol_zagrozony(self):
        self.zagrozony_krol = None

        pola_bite = self.pola_bierki['bicie']
        for pole in zmienListeWspolrzednychNaPola(pola_bite):
            zagrozona_bierka = self.szukanie_bierek.dajBierkePoPolu(pole)
            if 'krol' in zagrozona_bierka.nazwa:
                self.zagrozony_krol = zagrozona_bierka
                return zagrozona_bierka
