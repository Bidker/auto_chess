#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games, color


class ObslugaAlgorytmu(object):
    czy_uruchomiony = False
    wiadomosc = None

    @classmethod
    def wyswietlKomunikat(cls):
        cls.wiadomosc = games.Message('Czarny analizuje ruch', 70, color.blue,
                                      x=games.screen.width/2, y=games.screen.height/4, lifetime=(20*games.screen.fps))
        games.screen.add(cls.wiadomosc)

    @classmethod
    def zniszczKomunikat(cls):
        cls.wiadomosc.destroy()
