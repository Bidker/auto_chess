#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from livewires import games


def koniecGry():
    from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur
    from wyswietlenie_grafik.mozliwy_ruch import PodswietlMozliwePola

    for obiekt in games.screen.get_all_objects():
        obiekt.destroy()
    games.screen.quit()
