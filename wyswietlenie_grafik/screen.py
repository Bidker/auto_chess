import pygame
from livewires import games
from .tworzenie_figur import pokaz_figury

def rozpocznijGre():
    pygame.init()
    s = pygame.Surface((793, 798))

    pygame.image.load("Grafiki/chess.jpg")

    pokaz_figury()

    return s
