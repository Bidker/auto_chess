from obsluga_gry.listy_planszy import Plansza
from livewires import games
import pygame
import time

class Figury(games.Sprite):
    def __init__(self, figura, pozycja):
        self.wyznacz_wspolrzedne_po_pozycji(pozycja)
        self.nazwa = self.daj_nazwe(figura)
        self.ikona = self.nadaj_ikone()
        self.czy_poruszona = False
        self.czy_zbita = False
        self.stworzObraz()

    def wyznacz_wspolrzedne_po_pozycji(self, pozycja):
        plansza = Plansza()
        szerokosc = plansza.lista_szerokosci
        wysokosc = plansza.lista_dlugosci
        wspolrzedne = {}
        for i in pozycja:
            if i in szerokosc:
                index = szerokosc.index(i)
                self.pozycja_x = self.daj_wspolrzedne(index)
            elif i in wysokosc:
                index = wysokosc.index(i)
                self.pozycja_y = self.daj_wspolrzedne(index)

    def daj_wspolrzedne(self, i):
        return (49+(i*99))


    def daj_nazwe(self, figura):
        nazwa = figura
        kolor = self.sprawdz_kolor_po_pozycji()
        return kolor + '_' + nazwa


    def sprawdz_kolor_po_pozycji(self):
        if self.pozycja_y > 200:
            kolor = 'bialy'
        else:
            kolor = 'czarny'
        return kolor


    def nadaj_ikone(self):
        nazwa_ikony = 'wyswietlenie_grafik/Grafiki/'
        nazwa_ikony += self.nazwa + '.jpg'
        return nazwa_ikony

    def stworzObraz(self):
        obraz = games.load_image(self.ikona, True)
        super(Figury, self).__init__(
            image = obraz,
            x = self.pozycja_x,
            y = self.pozycja_y
        )


    def poruszona(self):
        self.czy_poruszona = True

    def zbita(self):
        self.czy_zbita = True

    def daj_punkty_graniczne_pola(self):
        return {
            'lewa': self.pozycja_x - 49,
            'prawa': self.pozycja_x + 49,
            'gorna': self.pozycja_y + 49,
            'dolna': self.pozycja_y - 49
        }

    def update(self):
        if games.mouse.is_pressed(0)==1:
            krawedzie_pola = self.daj_punkty_graniczne_pola()
            if (games.mouse.x >= krawedzie_pola['lewa'] and
                    games.mouse.x <= krawedzie_pola['prawa'] and
                    games.mouse.y <= krawedzie_pola['gorna'] and
                    games.mouse.y >= krawedzie_pola['dolna'] and
                    'bialy' in self.nazwa):

                print('x: %r, y: %r, nazwa: %r', self.pozycja_x, self.pozycja_y, self.nazwa)
                tlo_kliknietego = games.load_image('wyswietlenie_grafik/Grafiki/podswietlenie.jpg', True)
                podswietlenie = games.Sprite(
                    image = tlo_kliknietego,
                    x = self.pozycja_x,
                    y = self.pozycja_y
                )
                games.screen.add(podswietlenie)
                time.sleep(0.5)
