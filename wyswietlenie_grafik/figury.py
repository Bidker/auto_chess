#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from livewires import games

from .mozliwy_ruch import PodswietlMozliwyRuch, PodswietlMozliweBicie
from util.narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki


class Figury(games.Sprite):
    def __init__(self, figura, pozycja):
        wspolrzedne = wyznaczWspolrzednePoPozycji(pozycja)
        self.pozycja = pozycja
        self.ustaw_x(wspolrzedne.get('x'))
        self.ustaw_y(wspolrzedne.get('y'))
        self.nazwa = self.dajNazwe(figura)
        self.ikona = self.nadajIkone()
        self.czy_poruszona = False
        self.stworzDuszka()

    def zmienUstawienieBierki(self, wspolrzedne, pozycja):
        self.pozycja = pozycja
        self.ustaw_x = wspolrzedne['x']
        self.ustaw_y = wspolrzedne['y']

    def ustaw_x(self, x):
        self.pozycja_x = x

    def ustaw_y(self, y):
        self.pozycja_y = y

    def dajNazwe(self, figura):
        kolor = self.sprawdzKolorPoPozycji()
        return kolor + '_' + figura

    def sprawdzKolorPoPozycji(self):
        if self.pozycja_y > 600:
            kolor = 'bialy'
        else:
            kolor = 'czarny'
        return kolor

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
        self.destroy()

    def update(self):
        if games.mouse.is_pressed(0) == 1:
            if myszNadObiektem(self) and 'bialy' in self.nazwa:
                self.podswietlMozliweRuchy()

    def podswietlMozliweRuchy(self):
        mozliwoscRuchu = MozliwoscRuchuBierki()
        ruchy_do_podswietlenia = mozliwoscRuchu.sprawdzMozliweRuchy(self)
        podswietlony_ruch = []
        print('ruchy: %r', ruchy_do_podswietlenia)
        for i, wspolrzedne in enumerate(ruchy_do_podswietlenia['ruch']):
            podswietlony_ruch.append(PodswietlMozliwyRuch(wspolrzedne))
            games.screen.add(podswietlony_ruch[i])
        for i, wspolrzedne in enumerate(ruchy_do_podswietlenia['bicie']):
            podswietlony_ruch.append(PodswietlMozliweBicie(wspolrzedne))
            games.screen.add(podswietlony_ruch[i])
