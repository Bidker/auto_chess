#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji
from obsluga_gry.listy_planszy import Plansza


class PodswietlMozliwyRuch(games.Sprite):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie.jpg'

    def __init__(self, wspolrzedne):
        self.ustaw_x(wspolrzedne.get('x'))
        self.ustaw_y(wspolrzedne.get('y'))
        self.wybrane = False
        self.podswietlPole()

    def ustaw_x(self, x):
        self.pozycja_x = x

    def ustaw_y(self, y):
        self.pozycja_y = y

    def ustawWspolrzedne(self, wspolrzedne):
        self.pozycja_x = wspolrzedne.get('x')
        self.pozycja_y = wspolrzedne.get('y')

    def podswietlPole(self):
        obraz = games.load_image(PodswietlMozliwyRuch.ikona, False)
        super(PodswietlMozliwyRuch, self).__init__(
            image=obraz,
            x=self.pozycja_x,
            y=self.pozycja_y
        )
