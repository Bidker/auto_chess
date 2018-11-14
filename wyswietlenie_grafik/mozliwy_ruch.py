#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games

from tools.narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji, zmienWspolrzedneNaPole
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from obsluga_gry.warunki_wygranej import WarunkiWygranej


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

    def wykonajStandardowyUpdate(self):
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
        return {'bierka': bierka, 'wspolrzedne': wspolrzedne}

    def update(self):
        if games.mouse.is_pressed(0) and myszNadObiektem(self):
            slownik = self.wykonajStandardowyUpdate()
            bierka = slownik['bierka']
            wspolrzedne = slownik['wspolrzedne']
            bierka.zmienUstawienieBierki(wspolrzedne, self.pozycja)
            ww = WarunkiWygranej(bierka)
            ww.sprawdzWarunkiWygranej()


class PodswietlMozliwyRuch(PodswietlMozliwePola):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliwyRuch, self).__init__(PodswietlMozliwyRuch, wspolrzedne)


class PodswietlMozliweBicie(PodswietlMozliwePola):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie_bicia.jpg'

    def __init__(self, wspolrzedne):
        super(PodswietlMozliweBicie, self).__init__(PodswietlMozliweBicie, wspolrzedne)


class PodswietlMozliweRoszady(PodswietlMozliwyRuch):

    def __init__(self, wspolrzedne):
        super(PodswietlMozliweRoszady, self).__init__(wspolrzedne)

    def update(self):
        if games.mouse.is_pressed(0) and myszNadObiektem(self):
            slownik = self.wykonajStandardowyUpdate()
            bierka = slownik['bierka']
            wspolrzedne = slownik['wspolrzedne']
            bierka.wykonajRoszade(wspolrzedne, self.pozycja)
            ww = WarunkiWygranej(bierka)
            ww.sprawdzWarunkiWygranej()
