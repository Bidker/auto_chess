#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games, color

from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola, czyPoleNaBiciu
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.kolejnosc_ruchu import KolejnoscRuchu
from obsluga_gry.config import warunki_biale, warunki_czarne
from obsluga_gry.etapy_gry import koniecGry


class WarunkiWygranej(object):
    zagrozony_krol = None
    bierka_bijaca = None

    def __init__(self, bierka):
        self.szukanie_bierek = NarzedziaSzukaniaBierek()
        self.kolor_ruszajacych = warunki_biale if warunki_czarne == KolejnoscRuchu.kolej_na else warunki_czarne
        self.kolor_broniacych = warunki_czarne if warunki_czarne == KolejnoscRuchu.kolej_na else warunki_biale
        self.bierki_ruszajace = self.szukanie_bierek.dajBierkiPoSlowieKluczowym(self.kolor_ruszajacych)
        self.bierki_broniace = self.szukanie_bierek.dajBierkiPoSlowieKluczowym(self.kolor_broniacych)

    def sprawdzWarunkiWygranej(self):
        self.dajZagrozonegoKrola()
        if WarunkiWygranej.zagrozony_krol:
            if self.sprawdzCzyMat():
                kolor = self.kolor_ruszajacych.capitalize()
                komunikat = 'Szach mat! ' + kolor + ' wygrał!'
                self.wyswietlKomunikat(komunikat, koniecGry)
            else:
                self.wyswietlKomunikat('Szach!')
        elif self.sprawdzCzyPat():
            self.wyswietlKomunikat('Pat!', koniecGry)

    def sprawdzCzyPat(self):
        for bierka in self.bierki_broniace:
            print(bierka.nazwa)
            mrb = MozliwoscRuchuBierki(bierka)
            pola = mrb.sprawdzMozliweRuchy()
            if pola['ruch'] or pola['bicie'] or pola.get('roszada'):
                return False
        return True

    def sprawdzCzyMat(self):
        mozliwe_pola = {'ruch': [], 'bicie': []}
        for bierka in self.bierki_broniace:
            mrb = MozliwoscRuchuBierki(bierka)
            pola = mrb.sprawdzMozliweRuchy()
            mozliwe_pola['ruch'].extend(pola['ruch'])
            mozliwe_pola['bicie'].extend(pola['bicie'])
        if mozliwe_pola['ruch'] or mozliwe_pola['bicie']:
            return False
        return True

    def dajZagrozonegoKrola(self):
        for bierka in self.bierki_ruszajace:
            zagrozony_krol = self.sprawdzCzyKrolZagrozonyPrzezBierke(bierka)
            if zagrozony_krol:
                self._zmienWartosciKlasy(zagrozony_krol, bierka)
                return zagrozony_krol
        self._zmienWartosciKlasy()

    def sprawdzCzyKrolZagrozonyPrzezBierke(self, bierka):
        mrb = MozliwoscRuchuBierki(bierka)
        pola = mrb.sprawdzMozliweRuchy(False)['bicie']
        for pole in zmienListeWspolrzednychNaPola(pola):
            zagrozona_bierka = self.szukanie_bierek.dajBierkePoPolu(pole)
            if 'krol' in zagrozona_bierka.nazwa:
                return zagrozona_bierka
        return False

    def wyswietlKomunikat(self, tresc, func=None):
        msg = games.Message(tresc, 70, color.red, x=games.screen.width/2, y=games.screen.height/2,
                            lifetime=(7*games.screen.fps), after_death=func)

        games.screen.add(msg)

    def _zmienWartosciKlasy(self, zagrozona_bierka=None, bierka_bijaca=None):
        WarunkiWygranej.zagrozony_krol = zagrozona_bierka
        WarunkiWygranej.bierka_bijaca = bierka_bijaca
