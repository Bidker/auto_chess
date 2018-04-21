import time
from livewires import games

from obsluga_gry.listy_planszy import Plansza
from .mozliwy_ruch import MozliwyRuch

class Figury(games.Sprite):
    def __init__(self, figura, pozycja):
        self.wyznaczWspolrzednePoPozycji(pozycja)
        self.nazwa = self.dajNazwe(figura)
        self.ikona = self.nadajIkone()
        self.czy_poruszona = False
        self.czy_zbita = False
        self.stworzDuszka()

    def wyznaczWspolrzednePoPozycji(self, pozycja):
        plansza = Plansza()
        szerokosc = plansza.lista_szerokosci
        wysokosc = plansza.lista_dlugosci
        for i in pozycja:
            if i in szerokosc:
                index = szerokosc.index(i)
                self.pozycja_x = self.dajWspolrzedne(index)
            elif i in wysokosc:
                index = wysokosc.index(i)
                self.pozycja_y = self.dajWspolrzedne(index)

    def dajWspolrzedne(self, i):
        return (49+(i*99))


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
        self.czy_zbita = True

    def dajPunktyGranicznePola(self):
        return {
            'prawa': self.pozycja_x + 49,
            'lewa': self.pozycja_x - 49,
            'gorna': self.pozycja_y + 49,
            'dolna': self.pozycja_y - 49
        }

    def update(self):
        if games.mouse.is_pressed(0)==1:
            if self.czyMyszNadBialymObiektem():
                self.podswietlMozliweRuchy()

    def czyMyszNadBialymObiektem(self):
        krawedzie_pola = self.dajPunktyGranicznePola()
        if (games.mouse.x >= krawedzie_pola['lewa'] and
                games.mouse.x <= krawedzie_pola['prawa'] and
                games.mouse.y <= krawedzie_pola['gorna'] and
                games.mouse.y >= krawedzie_pola['dolna'] and
                'bialy' in self.nazwa):
            return True
        else:
            return False

    def podswietlMozliweRuchy(self):
        ruch = MozliwyRuch(self.pozycja_x, self.pozycja_y)
        games.screen.add(ruch)
