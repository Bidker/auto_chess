from .figury_ruchy import RuchFigur
from narzedzia_pol import zmienWspolrzedneNaPole, wyznaczWspolrzednePoPozycji
from .listy_planszy import Plansza

class MozliwoscRuchuBierki(object):
    def __init__(self):
        self.ruchFigury = RuchFigur()
        self.pola_zajete_bialymi = self.stworzZajetePola('biale')
        self.pola_zajete_czarnymi = self.stworzZajetePola('czarne')
        self.plansza = Plansza()

    def stworzZajetePola(self, kolor):
        pola = []
        figury = self.ruchFigury.pola_figur_w_trakcie_gry.get(kolor)
        for figura in figury.keys():
            pola.extend(figury.get(figura))
        return pola

    def sprawdzMozliweRuchy(self, obiektBierki):
        if 'pion' in obiektBierki.nazwa:
            return self.ruchDlaPiona(obiektBierki)
        elif 'skoczek' in obiektBierki.nazwa:
            return self.ruchDlaSkoczka(obiektBierki)
        elif 'goniec' in obiektBierki.nazwa:
            return self.ruchPoprzeczny(obiektBierki)
        elif 'wieża' in obiektBierki.nazwa:
            return self.ruchKrzyzowy(obiektBierki)
        elif 'hetman' in obiektBierki.nazwa:
            return self.ruchKrzyzowy(obiektBierki).extend(self.ruchPoprzeczny(obiektBierki))
        elif 'krol' in obiektBierki.nazwa:
            return self.ruchDlaKrola(obiektBierki)

    def ruchDlaPiona(self, obiektBierki):
        mozliwe_ruchy = []
        plansza = Plansza()
        if not obiektBierki.czy_poruszona:
            ilosc_ruchow = range(1, 3)
        else:
            ilosc_ruchow = range(1, 2)

        for ruch in ilosc_ruchow:
            if 'bialy' in obiektBierki.nazwa:
                mozliwe_ruchy.append({
                        'x': obiektBierki.pozycja_x,
                        'y': obiektBierki.pozycja_y - 100*ruch
                })
                mozliwe_ruchy.extend(self.dodajBialymPionomBicie(obiektBierki, mozliwe_ruchy))
            else:
                mozliwe_ruchy.append({
                        'x': obiektBierki.pozycja_x,
                        'y': obiektBierki.pozycja_y + 100*ruch
                })
        return mozliwe_ruchy

    def dodajBialymPionomBicie(self, obiektPiona, ruchy):
        pole_piona = zmienWspolrzedneNaPole(obiektPiona.pozycja_x, obiektPiona.pozycja_y)
        pola_bicia = []
        plansza = Plansza()
        for i in pole_piona:
            if i in plansza.lista_szerokosci:
                index = plansza.lista_szerokosci.index(i)
                if i != 'a':
                    pola_bicia.append(plansza.lista_szerokosci[index + 1])
                if i!= 'h':
                    pola_bicia.append(plansza.lista_szerokosci[index - 1])
            elif i in plansza.lista_wysokosci:
                index = plansza.lista_wysokosci.index(i)
                for j, pole in enumerate(pola_bicia):
                    pola_bicia[j] = pole + plansza.lista_wysokosci[index + 1]
        print(pola_bicia)
        lista_wspolrzednych = []
        for pole in pola_bicia:
            lista_wspolrzednych.append(wyznaczWspolrzednePoPozycji(pole))
        return lista_wspolrzednych

    def ruchDlaSkoczka(self, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchPoprzeczny(self, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchKrzyzowy(self, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchDlaKrola(self, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch
