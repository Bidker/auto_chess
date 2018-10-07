#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from util.narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji
from obsluga_gry.listy_planszy import Plansza


class PodswietlMozliwyRuch(games.Sprite):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie.jpg'

    def __init__(self, wspolrzedne):
        self.ustaw_x(wspolrzedne['x'])
        self.ustaw_y(wspolrzedne['y'])
        self.wybrane = False
        self.podswietlPole(self)

    def ustaw_x(self, x):
        self.pozycja_x = x

    def ustaw_y(self, y):
        self.pozycja_y = y

    def ustawWspolrzedne(self, wspolrzedne):
        self.pozycja_x = wspolrzedne['x']
        self.pozycja_y = wspolrzedne['y']

    @classmethod
    def podswietlPole(cls, self):
        obraz = games.load_image(cls.ikona, False)
        super(PodswietlMozliwyRuch, self).__init__(
            image=obraz,
            x=self.pozycja_x,
            y=self.pozycja_y
        )


class PodswietlMozliweBicie(PodswietlMozliwyRuch):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie_bicia.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliweBicie, self).__init__(wspolrzedne)

        '''def podswietlPole(self):
        obraz = games.load_image(PodscwietlMozliweBicie.ikona, False)
        super(PodswietlMozliweBicie, self).__init__(
            image=obraz,
            x=self.pozycja_x,
            y=self.pozycja_y
        )'''
