#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from livewires import games

from .mozliwy_ruch import PodswietlMozliwyRuch, PodswietlMozliweBicie
from tools.narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.kolejnosc_ruchu import KolejnoscRuchu
from obsluga_gry.config import warunki_biale, warunki_czarne


class Figury(games.Sprite):
    zagrozony_krol = None

    def __init__(self, figura, pozycja):
        wspolrzedne = wyznaczWspolrzednePoPozycji(pozycja)
        self.pozycja = pozycja
        self.pozycja_x = wspolrzedne['x']
        self.pozycja_y = wspolrzedne['y']
        self.kolor = warunki_biale if self.pozycja_y > 400 else warunki_czarne
        self.nazwa = self.kolor + '_' + figura
        self.ikona = self.nadajIkone()
        self.mozliwe_ruchy = {'ruch': [], 'bicie': []}
        self.czy_poruszona = False
        self.czy_zbita = False
        self.zaznaczony = False
        self.zagrozony = False
        self.kryta = False
        self.stworzDuszka()

    def zmienUstawienieBierki(self, wspolrzedne, pozycja):
        self.pozycja = pozycja
        self.czy_poruszona = True
        self.zaznaczony = False
        self.poruszBierka(wspolrzedne)
        self.usunPodswietloneRuchy()
        KolejnoscRuchu.zmien_ture()

    def poruszBierka(self, wspolrzedne):
        self.pozycja_x = wspolrzedne['x']
        self.pozycja_y = wspolrzedne['y']
        self.set_position((self.pozycja_x, self.pozycja_y))

    def nadajIkone(self):
        nazwa_ikony = 'wyswietlenie_grafik/Grafiki/'
        nazwa_ikony += self.nazwa + '.jpg'
        return nazwa_ikony

    def stworzDuszka(self):
        obraz = games.load_image(self.ikona)
        super(Figury, self).__init__(
            image=obraz,
            x=self.pozycja_x,
            y=self.pozycja_y
        )

    def poruszona(self):
        self.czy_poruszona = True

    def zbita(self):
        self.czy_zbita = True
        self.destroy()

    def update(self):
        if games.mouse.is_pressed(0) and myszNadObiektem(self) and not self.zaznaczony:
            if KolejnoscRuchu.kolej_na in self.nazwa:
                self.usunPodswietloneRuchy()
                self.podswietlMozliweRuchy()
                self.zmienZaznaczenia()

    def usunPodswietloneRuchy(self):
        from .mozliwy_ruch import PodswietlMozliwePola

        ilosc_obiektow = len(PodswietlMozliwePola.lista_podswietlen)
        for _ in range(ilosc_obiektow):
            pole = PodswietlMozliwePola.lista_podswietlen.pop()
            pole.destroy()

    def podswietlMozliweRuchy(self):
        from .tworzenie_figur import wyswietlObiektyNaEkranie

        mozliwoscRuchu = MozliwoscRuchuBierki(self)
        ruchy_do_podswietlenia = mozliwoscRuchu.sprawdzMozliweRuchy()
        podswietlony_ruch = []
        for wspolrzedne in ruchy_do_podswietlenia['ruch']:
            podswietlony_ruch.append(PodswietlMozliwyRuch(wspolrzedne))
        for wspolrzedne in ruchy_do_podswietlenia['bicie']:
            podswietlony_ruch.append(PodswietlMozliweBicie(wspolrzedne))
        wyswietlObiektyNaEkranie(podswietlony_ruch)

    def zmienZaznaczenia(self):
        from tools.narzedzia_figur import NarzedziaSzukaniaBierek
        narz_szukania_bierki = NarzedziaSzukaniaBierek()

        bierka = narz_szukania_bierki.dajZaznaczonaBierke()
        self.zaznaczony = True
        if bierka:
            bierka.zaznaczony = False
