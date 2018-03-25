from obsluga_gry.figury_ruchy import RuchFigur
from .figury import Figury

def pokaz_figury(games):
    obiekty_figur = []
    figury = stworz_liste_figur()
    for kolory in figury:
        obiekty_figur.extend(stworz_obiekty_figur(kolory))
    wyswietl_figury_na_ekranie(obiekty_figur, games)

def stworz_liste_figur():
    ruch_figur = RuchFigur()
    lista_bierek = []
    lista_bierek.append(ruch_figur.figury_pola_startowe.get('biale'))
    lista_bierek.append(ruch_figur.figury_pola_startowe.get('czarne'))

    return lista_bierek

def stworz_obiekty_figur(kolor):
    stworzone_bierki = []
    for bierka in kolor.keys():
        for pozycja in kolor[bierka]:
            bierka_stworzona = Figury(bierka, pozycja)
            stworzone_bierki.append(bierka_stworzona)

    return stworzone_bierki

def wyswietl_figury_na_ekranie(obiekty_figur, games):
    obrazy = []
    wspolrzedne = []
    for figura in obiekty_figur:
        obrazy.append(figura.ikona)
        wspolrzedne.append(figura.wspolrzedne)
    pokaz_obrazy(obrazy, wspolrzedne, games)

def pokaz_obrazy(obrazy, wspolrzedne, games):
    for i in range(len(obrazy)):
        w = wspolrzedne[i]
        obraz = games.load_image(obrazy[i])
        wyswietlony = games.Sprite(
                image = obraz,
                x = int(w['szerokosc']),
                y = int(w['wysokosc']))
        games.screen.add(wyswietlony)
