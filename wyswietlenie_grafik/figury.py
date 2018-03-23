class Figury(object):
    def __init__(self, figura, pozycja):
        figura = figura
        wspolrzedne = self.wyznacz_wspolrzedne_po_pozycji(pozycja)
        ikona = self.nadaj_ikone(figura, pozycja)
        czy_poruszona = False
        czy_zbita = False


    def wyznacz_wspolrzedne_po_pozycji(self, pozycja):
        wspolrzedne = {}
        for i in pozycja:
            if i in szerekosc:
                wspolrzedne['szerokosc'] = self.daj_wspolrzedne(szerokosc.index(i))
            else:
                wspolrzedne['wysokosc'] = self.daj_wspolrzedne(wysokosc.index(i))
        return wspolrzedne

    def daj_wspolrzedne(self, i):
        return (49+((i-1)*99))

    def nadaj_ikone(self):
        nazwa_ikony = 'Grafiki/'
        nazwa_ikony += self.sprawdz_kolor_po_pozycji() + '_'
        nazwa_ikony += self.figura + '.jpg'
        return nazwa_ikony

    def sprawdz_kolor_po_pozycji(self):
        if self.pozycja.get('wysokosc') > 200:
            kolor = 'czarny'
        else:
            kolor = 'bialy'
        return kolor

    def poruszona(self):
        self.czy_poruszona = True

    def zbita(self):
        self.czy_zbita = True
