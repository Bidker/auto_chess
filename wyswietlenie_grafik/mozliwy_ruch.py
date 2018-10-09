#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from util.narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji


class PodswietlMozliwePola(games.Sprite):

    def __init__(self, cls, wspolrzedne):
        self.ustaw_x(wspolrzedne['x'])
        self.ustaw_y(wspolrzedne['y'])
        self.wybrane = False
        cls.podswietlPole(self)

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
        super(PodswietlMozliwePola, self).__init__(
            image=obraz,
            x=self.pozycja_x,
            y=self.pozycja_y
        )


class PodswietlMozliwyRuch(PodswietlMozliwePola):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliwyRuch, self).__init__(PodswietlMozliwyRuch, wspolrzedne)


class PodswietlMozliweBicie(PodswietlMozliwePola):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie_bicia.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliweBicie, self).__init__(PodswietlMozliweBicie, wspolrzedne)
