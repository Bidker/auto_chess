from .figury import Figury

def pokaz_figury():
    figury = stworz_liste_figur()
    for figura in figury:
        obiekty_figur = stworz_obiekty_figur(figura)
    wyswietl_figury_na_ekranie(obiekty_figur)

def stworz_liste_figur():
    slowniki_figur = Figury()
    figury = []
    figury.append(slowniki_figur.poczatkowe_pozycje.get('biale'))
    figury.append(slowniki_figur.poczatkowe_pozycje.get('czarne'))
    return figury

def stworz_obiekty_figur(figura_i_pozycja):
    figura = Figury()
    lista_obiektow = []
    for figura in figura_i_pozycja.keys():
        for pozycja in figura_i_pozycja.get(figura):
            lista_obiektow.append(figura.__init__(figura, pozycja))
    return lista_obiektow

def wyswietl_figury_na_ekranie(obiekty_figur):
    obrazy = []
    wspolrzedne = []
    for figura in obiekty_figur:
        obrazy.append(figura.ikona)
        wspolrzedne.append(figura.wspolrzedne)
    pokaz_obrazy(obrazy, wspolrzedne)

def pokaz_obrazy(obrazy, wspolrzedne):
    pokazane = []
    for i in range(len(obrazy)):
        w = wspolrzedne[i]
        wyswietlony = games.Sprite(image = obrazy[i], x = w['szerokosc'], y = w['wysokosc'])
        pokazane.append(wyswietlony)
