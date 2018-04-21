from obsluga_gry.figury_ruchy import RuchFigur
from .figury import Figury

def pokaz_figury(games):
    obiekty_figur = []
    figury = stworz_liste_figur()
    for kolory in figury:
        obiekty_figur.extend(stworz_obiekty_figur(kolory))
    wyswietl_figury_na_ekranie(obiekty_figur, games)
    return obiekty_figur

def stworz_liste_figur():
    ruch_figur = RuchFigur()
    lista_bierek = []
    lista_bierek.append(ruch_figur.figury_pola_startowe.get('biale'))
    lista_bierek.append(ruch_figur.figury_pola_startowe.get('czarne'))

    return lista_bierek

def stworz_obiekty_figur(kolor):
    stworzone_bierki = []
    for bierka in kolor.keys():
        for i, pozycja in enumerate(kolor[bierka]):
            bierka_stworzona = Figury(bierka, pozycja)
            stworzone_bierki.append(bierka_stworzona)

    return stworzone_bierki

def wyswietl_figury_na_ekranie(obiekty_figur, games):
    for bierka in obiekty_figur:
        games.screen.add(bierka)
