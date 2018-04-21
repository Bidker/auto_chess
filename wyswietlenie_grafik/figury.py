import time
from livewires import games

from narzedzia_pol import myszNadObiektem, wyznaczWspolrzednePoPozycji
from .mozliwy_ruch import PodswietlMozliwyRuch
from obsluga_gry.listy_planszy import Plansza
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki

class Figury(games.Sprite):
    def __init__(self, figura, pozycja):
        wspolrzedne = wyznaczWspolrzednePoPozycji(pozycja)
        self.ustaw_x(wspolrzedne.get('x'))
        self.ustaw_y(wspolrzedne.get('y'))
        self.nazwa = self.dajNazwe(figura)
        self.ikona = self.nadajIkone()
        self.czy_poruszona = False
        self.stworzDuszka()

    def ustaw_x(self, x):
        self.pozycja_x = x

    def ustaw_y(self, y):
        self.pozycja_y = y

    def dajNazwe(self, figura):
        nazwa = figura
        kolor = self.sprawdzKolorPoPozycji()
        return kolor + '_' + nazwa


    def sprawdzKolorPoPozycji(self):
        if self.pozycja_y > 200:
            kolor = 'bialy'
        else:
            kolor = 'czarny'
        return kolor

    def nadajIkone(self):
        nazwa_ikony = 'wyswietlenie_grafik/Grafiki/'
        nazwa_ikony += self.nazwa + '.jpg'
        return nazwa_ikony

    def stworzDuszka(self):
        obraz = games.load_image(self.ikona)
        super(Figury, self).__init__(
            image = obraz,
            x = self.pozycja_x,
            y = self.pozycja_y
        )

    def poruszona(self):
        self.czy_poruszona = True

    def zbita(self):
        self.destroy()

    def update(self):
        if games.mouse.is_pressed(0)==1:
            if myszNadObiektem(self) and 'bialy' in self.nazwa:
                print('%s: x: %r, y: %r', self.nazwa, self.pozycja_x, self.pozycja_y)
                self.podswietlMozliweRuchy()

    def podswietlMozliweRuchy(self):
        mozliwoscRuchu = MozliwoscRuchuBierki()
        ruchy_do_podswietlenia = mozliwoscRuchu.sprawdzMozliweRuchy(self)
        podswietlony_ruch = []
        for i, wspolrzedne in enumerate(ruchy_do_podswietlenia):
            podswietlony_ruch.append(PodswietlMozliwyRuch(wspolrzedne))
            games.screen.add(podswietlony_ruch[i])
