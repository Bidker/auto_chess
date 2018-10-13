#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from util.narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji, zmienWspolrzedneNaPole
from util.narzedzia_figur import NarzedziaSzukaniaBierek


class PodswietlMozliwePola(games.Sprite):
    lista_podswietlen = []

    def __init__(self, cls, wspolrzedne):
        self.pozycja_x = wspolrzedne['x']
        self.pozycja_y = wspolrzedne['y']
        self.pozycja = zmienWspolrzedneNaPole(self.pozycja_x, self.pozycja_y)
        self.wybrane = False
        cls.podswietlPole(self)
        PodswietlMozliwePola.lista_podswietlen.append(self)

    @classmethod
    def podswietlPole(cls, self):
        obraz = games.load_image(cls.ikona, False)
        super(PodswietlMozliwePola, self).__init__(
            image=obraz,
            x=self.pozycja_x,
            y=self.pozycja_y
        )

    def update(self):
        if games.mouse.is_pressed(0) and myszNadObiektem(self):
            self.wybrane = True
            szukanie_bierek = NarzedziaSzukaniaBierek()
            wspolrzedne = {
                'x': self.pozycja_x,
                'y': self.pozycja_y,
            }

            bita_bierka = szukanie_bierek.dajBierkePoPolu(self.pozycja)
            if bita_bierka:
                bita_bierka.zbita()

            bierka = szukanie_bierek.dajZaznaczonaBierke()
            if bierka:
                bierka.zmienUstawienieBierki(wspolrzedne, self.pozycja)


class PodswietlMozliwyRuch(PodswietlMozliwePola):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliwyRuch, self).__init__(PodswietlMozliwyRuch, wspolrzedne)


class PodswietlMozliweBicie(PodswietlMozliwePola):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie_bicia.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliweBicie, self).__init__(PodswietlMozliweBicie, wspolrzedne)
