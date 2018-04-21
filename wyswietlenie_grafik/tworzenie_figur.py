from livewires import games

from obsluga_gry.figury_ruchy import RuchFigur
from .figury import Figury

def pokazFigury():
    obiekty_figur = []
    figury = stworzListeFigur()
    for kolory in figury:
        obiekty_figur.extend(stworzObiektyFigur(kolory))
    wyswietlFiguryNaEkranie(obiekty_figur)
    return obiekty_figur

def stworzListeFigur():
    ruch_figur = RuchFigur()
    lista_bierek = []
    lista_bierek.append(ruch_figur.figury_pola_startowe.get('biale'))
    lista_bierek.append(ruch_figur.figury_pola_startowe.get('czarne'))

    return lista_bierek

def stworzObiektyFigur(kolor):
    stworzone_bierki = []
    for bierka in kolor.keys():
        for i, pozycja in enumerate(kolor[bierka]):
            bierka_stworzona = Figury(bierka, pozycja)
            stworzone_bierki.append(bierka_stworzona)

    return stworzone_bierki

def wyswietlFiguryNaEkranie(obiekty_figur):
    for bierka in obiekty_figur:
        games.screen.add(bierka)
