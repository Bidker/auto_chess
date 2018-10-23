#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games, color

from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola, czyPoleNaBiciu
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.kolejnosc_ruchu import koniecGry


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
            mozliwa_ucieczka = self.sprawdzMozliwoscUcieczki()
            mozliwa_ucieczka = mozliwa_ucieczka['bicie'] + mozliwa_ucieczka['ruch']
            mozliwosc_zbicia_bijacego = czyPoleNaBiciu(WarunkiWygranej.bierka_bijaca)
            print('ucieczka i bicie: ', mozliwa_ucieczka, mozliwosc_zbicia_bijacego)
            if mozliwa_ucieczka or mozliwosc_zbicia_bijacego:  # mozliwe zasłoniecie
                print('warn: %r', bool(mozliwa_ucieczka or mozliwosc_zbicia_bijacego))
                msg = games.Message('Szach!', 70, color.red, x=games.screen.width/2, y=games.screen.height/2,
                                    lifetime=(7*games.screen.fps))
            else:
                msg = games.Message('Szach Mat!', 70, color.red, x=games.screen.width/2, y=games.screen.height/2,
                                    lifetime=(7*games.screen.fps))
            games.screen.add(msg)
        else:
            WarunkiWygranej.pola_bierki = []

    def dajZagrozonegoKrola(self):
        pola_bite = WarunkiWygranej.pola_bierki['bicie']
        for pole in zmienListeWspolrzednychNaPola(pola_bite):
            zagrozona_bierka = self.szukanie_bierek.dajBierkePoPolu(pole)
            if 'krol' in zagrozona_bierka.nazwa:
                WarunkiWygranej.zagrozony_krol = zagrozona_bierka
                return zagrozona_bierka

    def sprawdzMozliwoscUcieczki(self):
        mrb = MozliwoscRuchuBierki(WarunkiWygranej.zagrozony_krol)
        return mrb.sprawdzMozliweRuchy(False)
