from livewires import games

from obsluga_gry.figury_ruchy import RuchFigur
from .figury import Figury


def pokazFigury():
    obiekty_figur = ObiektyFigur.dajObiektyFigur()
    wyswietlFiguryNaEkranie(obiekty_figur)
    return obiekty_figur


def stworzListeFigur():
    ruch_figur = RuchFigur()
    lista_bierek = []
    lista_bierek.append(ruch_figur.figury_pola_startowe['biale'])
    lista_bierek.append(ruch_figur.figury_pola_startowe['czarne'])

    return lista_bierek


class ObiektyFigur(object):
    '''Zastosowanie wzorca projektowego Singleton'''
    stworzone_bierki = []

    def __init__(self):
        pass

    @classmethod
    def dajObiektyFigur(cls):
        if not cls.stworzone_bierki:
            figury = stworzListeFigur()
            for kolory in figury:
                for bierka, pozycje_bierek in kolory.items():
                    for pozycja in pozycje_bierek:
                        bierka_stworzona = Figury(bierka, pozycja)
                        cls.stworzone_bierki.append(bierka_stworzona)

        return cls.stworzone_bierki


def wyswietlFiguryNaEkranie(obiekty_figur):
    for bierka in obiekty_figur:
        games.screen.add(bierka)
