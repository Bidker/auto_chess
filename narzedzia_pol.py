from livewires import games

from obsluga_gry.listy_planszy import Plansza


def zmienListePolNaWspolrzedne(lista_pol):
    ret = []
    for pole in lista_pol:
        ret.append(wyznaczWspolrzednePoPozycji(pole))
    return ret


def wyznaczWspolrzednePoPozycji(pole):
    plansza = Plansza()
    szerokosc = plansza.lista_szerokosci
    wysokosc = plansza.lista_wysokosci
    for i in pole:
        if i in szerokosc:
            x = dajWspolrzedna(szerokosc.index(i))
        elif i in wysokosc:
            y = dajWspolrzedna(wysokosc.index(i))
    return {
        'x': x,
        'y': y
    }


def dajWspolrzedna(i):
    return (50+(i*100))


def zmienListeWspolrzednychNaPola(lista_wspolrzednych):
    ret = []
    for wspolrzedne in lista_wspolrzednych:
        ret.append(zmienWspolrzedneNaPole(wspolrzedne['x'], wspolrzedne['y']))
    return ret


def zmienWspolrzedneNaPole(x, y):
    plansza = Plansza()
    pole = plansza.lista_szerokosci[dajIndexPola(x)]
    pole += plansza.lista_wysokosci[dajIndexPola(y)]
    return pole


def dajIndexPola(wspolrzedna):
    return int(((wspolrzedna - 50)/100))


def myszNadObiektem(obiekt):
    krawedzie_pola = dajPunktyGranicznePola(obiekt)
    if (games.mouse.x >= krawedzie_pola['lewa'] and
            games.mouse.x <= krawedzie_pola['prawa'] and
            games.mouse.y <= krawedzie_pola['gorna'] and
            games.mouse.y >= krawedzie_pola['dolna']):
        return True
    else:
        return False


def dajPunktyGranicznePola(obiekt):
    return {
        'prawa': obiekt.pozycja_x + 49,
        'lewa': obiekt.pozycja_x - 49,
        'gorna': obiekt.pozycja_y + 49,
        'dolna': obiekt.pozycja_y - 49
    }


def czyWszpolrzedneWPolu(x, y):
    if (x >= 0 and
            x <= games.screen.width and
            y >= 0 and
            y <= games.screen.height):
        return True
    else:
        return False
