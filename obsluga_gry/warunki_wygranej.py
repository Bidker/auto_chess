#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games, color

from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola, czyPoleNaBiciu
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.config import warunki_biale, warunki_czarne
from obsluga_gry.etapy_gry import koniecGry


class WarunkiWygranej(object):
    zagrozony_krol = None
    bierka_bijaca = None
    pola_bierki = []

    def __init__(self, bierka):
        from wyswietlenie_grafik.figury import Figury
        ruch_bierek = MozliwoscRuchuBierki(bierka)

        WarunkiWygranej.zagrozony_krol = None
        WarunkiWygranej.bierka_bijaca = bierka
        WarunkiWygranej.pola_bierki = ruch_bierek.sprawdzMozliweRuchy()
        self.szukanie_bierek = NarzedziaSzukaniaBierek()

    def sprawdzWarunkiWygranej(self):
        self.dajZagrozonegoKrola()
        if WarunkiWygranej.zagrozony_krol:
            if self.sprawdzCzyMat():
                self.wyswietlKomunikat('Szach mat!', koniecGry)
            else:
                self.wyswietlKomunikat('Szach!')
        else:
            WarunkiWygranej.pola_bierki = []

    def sprawdzCzyMat(self):
        kolor = warunki_biale if warunki_biale in WarunkiWygranej.zagrozony_krol.nazwa else warunki_czarne
        bierki_ruszajace = self.szukanie_bierek.dajBierkiPoSlowieKluczowym(kolor)
        mozliwe_pola = {'ruch': [], 'bicie': []}
        for bierka in bierki_ruszajace:
            mrb = MozliwoscRuchuBierki(bierka)
            pola = mrb.sprawdzMozliweRuchy()
            mozliwe_pola['ruch'].extend(pola['ruch'])
            mozliwe_pola['bicie'].extend(pola['bicie'])
        if mozliwe_pola['ruch'] or mozliwe_pola['bicie']:
            return False
        return True

    def dajZagrozonegoKrola(self):
        pola_bite = WarunkiWygranej.pola_bierki['bicie']
        for pole in zmienListeWspolrzednychNaPola(pola_bite):
            zagrozona_bierka = self.szukanie_bierek.dajBierkePoPolu(pole)
            if 'krol' in zagrozona_bierka.nazwa:
                WarunkiWygranej.zagrozony_krol = zagrozona_bierka
                return zagrozona_bierka

    def wyswietlKomunikat(self, tresc, func=None):
        msg = games.Message(tresc, 70, color.red, x=games.screen.width/2, y=games.screen.height/2,
                            lifetime=(7*games.screen.fps), after_death=func)

        games.screen.add(msg)
