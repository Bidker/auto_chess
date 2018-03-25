from obsluga_gry.listy_planszy import Plansza

class Figury(object):
    def __init__(self, figura, pozycja):
        self.nazwa = figura
        self.wspolrzedne = self.wyznacz_wspolrzedne_po_pozycji(pozycja)
        self.ikona = self.nadaj_ikone()
        self.czy_poruszona = False
        self.czy_zbita = False


    def wyznacz_wspolrzedne_po_pozycji(self, pozycja):
        plansza = Plansza()
        szerokosc = plansza.lista_szerokosci
        wysokosc = plansza.lista_dlugosci
        wspolrzedne = {}
        for i in pozycja:
            if i in szerokosc:
                index = szerokosc.index(i) + 1
                wspolrzedne['szerokosc'] = self.daj_wspolrzedne(index)
            elif i in wysokosc:
                index = wysokosc.index(i) + 1
                wspolrzedne['wysokosc'] = self.daj_wspolrzedne(index)
        return wspolrzedne

    def daj_wspolrzedne(self, i):
        return (49+((i-1)*99))

    def nadaj_ikone(self):
        nazwa_ikony = 'wyswietlenie_grafik/Grafiki/'
        nazwa_ikony += self.sprawdz_kolor_po_pozycji() + '_'
        nazwa_ikony += self.nazwa + '.png'
        return nazwa_ikony

    def sprawdz_kolor_po_pozycji(self):
        if self.wspolrzedne.get('wysokosc') > 200:
            kolor = 'bialy'
        else:
            kolor = 'czarny'
        return kolor

    def poruszona(self):
        self.czy_poruszona = True

    def zbita(self):
        self.czy_zbita = True
