#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from livewires import games

from .tworzenie_figur import pokazFigury
from obsluga_gry.config import wysokosc_ekranu, szerokosc_ekranu


def rozpocznijGre():
    games.init(screen_width=szerokosc_ekranu, screen_height=wysokosc_ekranu, fps=50)
    wall_image = games.load_image("wyswietlenie_grafik/Grafiki/chess.jpg", False)

    games.screen.background = wall_image
    obiekty_bierek = pokazFigury()

    games.screen.mainloop()
