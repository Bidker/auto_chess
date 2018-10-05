#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .figury_ruchy import RuchFigur
from narzedzia_pol import zmienWspolrzedneNaPole, wyznaczWspolrzednePoPozycji, czyWszpolrzedneWPolu, zmienListeWspolrzednychNaPola, zmienListePolNaWspolrzedne
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
        if 'biale' in obiektBierki.nazwa:
            self.pola_przecinikow = self.pola_zajete_czarnymi
        else:
            self.pola_przecinikow = self.pola_zajete_bialymi

        if 'pion' in obiektBierki.nazwa:
            pola = self.ruchDlaPiona(obiektBierki)
            return self.ograniczPionaOBicie(obiektBierki, pola)
        elif 'skoczek' in obiektBierki.nazwa:
            pola = self.ruchDlaSkoczka(obiektBierki)
            return self.ograniczSkoczkaOBicie(obiektBierki, pola)
        elif 'goniec' in obiektBierki.nazwa:
            pola = self.ruchPoprzeczny(obiektBierki)
            return self.ograniczGoncaOBicie(obiektBierki, pola)
        elif 'wieza' in obiektBierki.nazwa:
            pola = self.ruchKrzyzowy(obiektBierki)
            return self.ograniczWiezeOBicie(obiektBierki, pola)
        elif 'hetman' in obiektBierki.nazwa:
            pola = self.ruchKrzyzowy(obiektBierki)
            pola.extend(self.ruchPoprzeczny(obiektBierki))
            return self.ograniczHetmanaOBicie(obiektBierki, pola)
        elif 'krol' in obiektBierki.nazwa:
            pola = self.ruchDlaKrola(obiektBierki)
            return self.ograniczKrolaOBicie(obiektBierki, pola)

    def ruchDlaPiona(self, obiektBierki):
        mozliwe_ruchy = []
        plansza = self.plansza
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
            else:
                mozliwe_ruchy.append({
                    'x': obiektBierki.pozycja_x,
                    'y': obiektBierki.pozycja_y + 100*ruch
                })
        mozliwe_ruchy = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, mozliwe_ruchy)
        mozliwe_ruchy.extend(self.dodajPionomBicie(obiektBierki, mozliwe_ruchy))
        return mozliwe_ruchy

    def dodajPionomBicie(self, obiektPiona, ruchy):
        pole_piona = zmienWspolrzedneNaPole(obiektPiona.pozycja_x, obiektPiona.pozycja_y)
        pola_atakowane = self.dajBiciePionow(pole_piona, obiektPiona.nazwa)
        pola_atakowane = self.sprawdzCzyBicieNaPolach(pola_atakowane, obiektPiona)
        lista_wspolrzednych = []
        for pole in pola_atakowane:
            lista_wspolrzednych.append(wyznaczWspolrzednePoPozycji(pole))
        return lista_wspolrzednych

    def dajBiciePionow(self, pole_piona, nazwaPiona):
        plansza = self.plansza
        pola_atakowane = []
        for i in pole_piona:
            if i in plansza.lista_szerokosci:
                pola_atakowane.extend(self.ustawSzerokoscBiciaOJeden(i))
            elif i in plansza.lista_wysokosci:
                pola_atakowane = self.ustawWysokoscBiciaOJeden(i, pola_atakowane, nazwaPiona)
        return pola_atakowane

    def ruchDlaSkoczka(self, obiektSkoczka):
        lista_wysokosci = self.plansza.lista_wysokosci
        lista_szerokosci = self.plansza.lista_szerokosci

        pole_skoczka = zmienWspolrzedneNaPole(obiektSkoczka.pozycja_x, obiektSkoczka.pozycja_y)
        mozliwe_ruchy = self.przygotujRuchySKoczka(pole_skoczka)
        mozliwe_ruchy = self.sprawdzZaleznieOdKoloruCzyZawadzaKucowi(obiektSkoczka, mozliwe_ruchy)

        ret = []
        for ruch in mozliwe_ruchy:
            ret.append(wyznaczWspolrzednePoPozycji(ruch))

        return ret

    def przygotujRuchySKoczka(self, pole_skoczka):
        mozliwe_ruchy = []
        lista_przygotowawcza = []
        for wspolrzedna in pole_skoczka:
            lista_przygotowawcza.extend(self.dajPozycjeOddalonaODwaWiecej(wspolrzedna))
            lista_przygotowawcza.extend(self.dajPozycjeOddalonaODwaMniej(wspolrzedna))
        mozliwe_ruchy.extend(self.stworzPozycjeDlaSkoczka(lista_przygotowawcza, pole_skoczka))
        return mozliwe_ruchy

    def dajPozycjeOddalonaODwaWiecej(self, znak):
        lista_wysokosci = self.plansza.lista_wysokosci
        lista_szerokosci = self.plansza.lista_szerokosci
        ret = []
        if znak in lista_wysokosci and znak not in ('1', '2'):
            ret.append(lista_wysokosci[(lista_wysokosci.index(znak) + 2)])
        elif znak in lista_szerokosci and znak not in ('g', 'h'):
            ret.append(lista_szerokosci[(lista_szerokosci.index(znak) + 2)])
        return ret

    def dajPozycjeOddalonaODwaMniej(self, znak):
        lista_wysokosci = self.plansza.lista_wysokosci
        lista_szerokosci = self.plansza.lista_szerokosci
        ret = []
        if znak in lista_wysokosci and znak not in ('7', '8'):
            ret.append(lista_wysokosci[(lista_wysokosci.index(znak) - 2)])
        elif znak in lista_szerokosci and znak not in ('a', 'b'):
            ret.append(lista_szerokosci[(lista_szerokosci.index(znak) - 2)])
        return ret

    def stworzPozycjeDlaSkoczka(self, lista_przygotowawcza, pole_skoczka):
        lista_wysokosci = self.plansza.lista_wysokosci
        lista_szerokosci = self.plansza.lista_szerokosci
        ret = []

        for znak in lista_przygotowawcza:
            if znak in lista_szerokosci:
                index = lista_wysokosci.index(pole_skoczka[1])
                if index != 7:
                    ret.append(znak + lista_wysokosci[index+1])
                if index != 0:
                    ret.append(znak + lista_wysokosci[index-1])
            elif znak in lista_wysokosci:
                index = lista_szerokosci.index(pole_skoczka[0])
                if znak != 7:
                    ret.append(znak + lista_szerokosci[index-1])
                if znak != 0:
                    ret.append(znak + lista_szerokosci[index+1])
        return ret

    def sprawdzZaleznieOdKoloruCzyZawadzaKucowi(self, obiektSkoczka, mozliwe_ruchy):
        if 'bialy' in obiektSkoczka.nazwa:
            return self.sprawdzCzyKucowiZawadza(self.pola_zajete_bialymi, mozliwe_ruchy)
        else:
            return self.sprawdzCzyKucowiZawadza(self.pola_zajete_czarnymi, mozliwe_ruchy)

    def sprawdzCzyKucowiZawadza(self, sojusznicy, mozliwe_ruchy):
        ret = []
        for pole in mozliwe_ruchy:
            if pole not in sojusznicy:
                ret.append(pole)
        return ret

    def ruchDlaKrola(self, obiektKrola):
        mozliwy_ruch = self.ruchPoprzeczny(obiektKrola)
        mozliwy_ruch.extend(self.ruchKrzyzowy(obiektKrola))
        mozliwy_ruch = self.wykreslPolaBitePrzezPrzeciwnikow(obiektKrola, mozliwy_ruch)
        return mozliwy_ruch

    def ruchPoprzeczny(self, obiektBierki):
        poprzeczne_prawy_dol = []
        poprzeczne_lewa_gora = []
        poprzeczne_prawa_gora = []
        poprzeczne_lewy_dol = []

        if 'krol' not in obiektBierki.nazwa:
            ilosc_ruchow = range(1, 8)
        else:
            ilosc_ruchow = range(1, 2)
        ilosc_poprzednich_w_prawy_dol = None
        ilosc_poprzednich_w_lewa_gore = None
        ilosc_poprzednich_w_prawa_gore = None
        ilosc_poprzednich_w_lewy_dol = None

        for ruch in ilosc_ruchow:
            if ilosc_poprzednich_w_prawy_dol != len(poprzeczne_prawy_dol):
                ilosc_poprzednich_w_prawy_dol == len(poprzeczne_prawy_dol)
                poprzeczne_prawy_dol.extend(self.dajJedenMozliwyPoprzecznyWPrawyDol(ruch, obiektBierki))
            if ilosc_poprzednich_w_lewa_gore != len(poprzeczne_lewa_gora):
                ilosc_poprzednich_w_lewa_gore == len(poprzeczne_lewa_gora)
                poprzeczne_lewa_gora.extend(self.dajJedenMozliwyPoprzecznyWLewaGore(ruch, obiektBierki))
            if ilosc_poprzednich_w_prawa_gore != len(poprzeczne_prawa_gora):
                ilosc_poprzednich_w_prawa_gore == len(poprzeczne_prawa_gora)
                poprzeczne_prawa_gora.extend(self.dajJedenMozliwyPoprzecznyWPrawaGore(ruch, obiektBierki))
            if ilosc_poprzednich_w_lewy_dol != len(poprzeczne_lewy_dol):
                ilosc_poprzednich_w_lewy_dol == len(poprzeczne_lewy_dol)
                poprzeczne_lewy_dol.extend(self.dajJedenMozliwyPoprzecznyWLewyDol(ruch, obiektBierki))

        # poprzeczne_prawy_dol = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(poprzeczne_prawy_dol))
        # poprzeczne_lewa_gora = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(poprzeczne_lewa_gora))
        # poprzeczne_prawa_gora = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(poprzeczne_prawa_gora))
        # poprzeczne_lewy_dol = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(poprzeczne_lewy_dol))

        ret = poprzeczne_prawy_dol
        ret.extend(poprzeczne_lewa_gora)
        ret.extend(poprzeczne_prawa_gora)
        ret.extend(poprzeczne_lewy_dol)
        return ret

    def dajJedenMozliwyPoprzecznyWLewaGore(self, index, obiektBierki):
        x_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiektBierki.pozycja_x, index)
        y_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiektBierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyPoprzecznyWPrawyDol(self, index, obiektBierki):
        x_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiektBierki.pozycja_x, index)
        y_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiektBierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyPoprzecznyWPrawaGore(self, index, obiektBierki):
        x_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiektBierki.pozycja_x, index)
        y_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiektBierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyPoprzecznyWLewyDol(self, index, obiektBierki):
        x_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiektBierki.pozycja_x, index)
        y_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiektBierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def ruchKrzyzowy(self, obiektBierki):
        prosto_prawo = []
        prosto_gora = []
        prosto_lewo = []
        prosto_dol = []

        if 'krol' not in obiektBierki.nazwa:
            ilosc_ruchow = range(1, 8)
        else:
            ilosc_ruchow = range(1, 2)
        ilosc_poprzednich_prawo = None
        ilosc_poprzednich_gora = None
        ilosc_poprzednich_lewo = None
        ilosc_poprzednich_dol = None

        for ruch in ilosc_ruchow:
            prosto_prawo.extend(self.dajJedenMozliwyWPrawo(ruch, obiektBierki))
            prosto_gora.extend(self.dajJedenMozliwyWGore(ruch, obiektBierki))
            prosto_lewo.extend(self.dajJedenMozliwyWLewo(ruch, obiektBierki))
            prosto_dol.extend(self.dajJedenMozliwyWDol(ruch, obiektBierki))

        # prosto_prawo = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(prosto_prawo))
        # prosto_gora = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(prosto_gora))
        # prosto_lewo = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(prosto_lewo))
        # prosto_dol = self.sprawdzCzyZawadzaPoKolorze(obiektBierki, zmienListeWspolrzednychNaPola(prosto_lewo))

        ret = prosto_prawo
        ret.extend(prosto_gora)
        ret.extend(prosto_lewo)
        ret.extend(prosto_dol)
        return ret

    def dajJedenMozliwyWPrawo(self, ruch, obiektBierki):
        x_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiektBierki.pozycja_x, ruch)
        y_podswietlenia = obiektBierki.pozycja_y
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyWGore(self, ruch, obiektBierki):
        x_podswietlenia = obiektBierki.pozycja_x
        y_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiektBierki.pozycja_y, ruch)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyWLewo(self, ruch, obiektBierki):
        x_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiektBierki.pozycja_x, ruch)
        y_podswietlenia = obiektBierki.pozycja_y
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyWDol(self, ruch, obiektBierki):
        x_podswietlenia = obiektBierki.pozycja_x
        y_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiektBierki.pozycja_y, ruch)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def przypiszPozycjePodswietleniaJesliWPolu(self, x, y):
        if czyWszpolrzedneWPolu(x, y):
            return [{
                'x': x,
                'y': y
            }]
        else:
            return []

    def sprawdzCzyZawadzaPoKolorze(self, obiektBierki, mozliwe_ruchy):
        if 'bialy' in obiektBierki.nazwa:
            return self.sprawdzCzyZawadzaBialy(mozliwe_ruchy)
        else:
            return self.sprawdzCzyZawadzaCzarny(mozliwe_ruchy)

    def sprawdzCzyZawadzaBialy(self, mozliwe_ruchy):
        return self.sprawdzCzyZawadza(self.pola_zajete_bialymi, mozliwe_ruchy)

    def sprawdzCzyZawadzaCzarny(self, mozliwe_ruchy):
        return self.sprawdzCzyZawadza(self.pola_zajete_czarnymi, mozliwe_ruchy)

    def sprawdzCzyZawadza(self, pola_sojucznikow, mozliwe_ruchy):
        for index, pole in enumerate(mozliwe_ruchy):
            if pole in pola_sojucznikow:
                mozliwe_ruchy = mozliwe_ruchy[:index]
        return mozliwe_ruchy

    def ustawSzerokoscBiciaOJeden(self, liera_planszy):
        ret = []
        lista_szerokosci = self.plansza.lista_szerokosci
        index = lista_szerokosci.index(liera_planszy)
        if liera_planszy != 'a':
            ret.append(lista_szerokosci[index - 1])
        if liera_planszy != 'h':
            ret.append(lista_szerokosci[index + 1])
        return ret

    def ustawWysokoscBiciaOJeden(self, cyfra_planszy, pola_atakowane, nazwa_bierki):
        lista_wysokosci = self.plansza.lista_wysokosci
        index = lista_wysokosci.index(cyfra_planszy)
        for j, pole in enumerate(pola_atakowane):
            if 'bialy' in nazwa_bierki and index != 0:
                pola_atakowane[j] = pole + lista_wysokosci[index - 1]
            elif 'czarny' in nazwa_bierki and index != len(lista_wysokosci):
                pola_atakowane[j] = pole + lista_wysokosci[index + 1]
        return pola_atakowane

    def sprawdzCzyBicieNaPolach(self, pola_atakowane, obiektBierki):
        if 'bialy' in obiektBierki.nazwa:
            return self.sprawdzBicieNa(self.pola_zajete_czarnymi, pola_atakowane)
        else:
            return self.sprawdzBicieNa(self.pola_zajete_bialymi, pola_atakowane)

    def sprawdzBicieNa(self, pola_przeciwnika, pola_atakowane):
        ret = []
        for pole in pola_atakowane:
            if pole in pola_przeciwnika:
                ret.append(pole)
        return ret

    def zmniejszWspolrzednaOXSetekPx(self, wspolrzedna, x):
        return wspolrzedna - x*100

    def zwiekszWspolrzednaOXSetekPx(self, wspolrzedna, x):
        return wspolrzedna + x*100

    def wykreslPolaBitePrzezPrzeciwnikow(self, obiektKrola, mozliwe_ruchy):
        if 'bialy' in obiektKrola.nazwa:
            return self.wykreslPolaBitePrzez('czarne', mozliwe_ruchy)
        else:
            return self.wykreslPolaBitePrzez('biale', mozliwe_ruchy)

    def wykreslPolaBitePrzez(self, kolor_przecinikow, mozliwe_ruchy):
        figury_pola = self.ruchFigury.pola_figur_w_trakcie_gry.get(kolor_przecinikow)

        mozliwe_ruchy = zmienListeWspolrzednychNaPola(mozliwe_ruchy)
        for bierka, pola_bierki in figury_pola.items():
            if bierka == 'pion':
                mozliwe_ruchy = self.wykreslPolaBitePrzezPiona(mozliwe_ruchy, pola_bierki, kolor_przecinikow)
            elif bierka == 'skoczek':
                mozliwe_ruchy = self.wykreslPolaBitePrzezSkoczka(mozliwe_ruchy, pola_bierki)
            elif bierka in ('goniec', 'hetman', 'krol'):
                mozliwe_ruchy = self.wykreslPolaBitePoprzecznie(mozliwe_ruchy, pola_bierki, bierka)
            # elif bierka in ('wieza', 'hetman', 'krol'):
                #mozliwe_ruchy = self.wykreslPolaBiteKrzyzowo(mozliwe_ruchy, pola_bierki, bierka)

        mozliwe_ruchy = zmienListePolNaWspolrzedne(mozliwe_ruchy)

        return mozliwe_ruchy

    def wykreslPolaBitePrzezPiona(self, mozliwe_ruchy, pola_bierki, kolor_przecinikow):
        pola_atakowane = []
        for pole in pola_bierki:
            if kolor_przecinikow == 'biale':
                pola_atakowane.extend(self.dajBiciePionow(pole, 'bialy pion'))
            else:
                pola_atakowane.extend(self.dajBiciePionow(pole, 'czarny pion'))

        return self.wykreslAtakowanePola(mozliwe_ruchy, pola_atakowane)

    def wykreslPolaBitePrzezSkoczka(self, mozliwe_ruchy, pola_skoczka):
        pola_atakowane = []
        for pole in pola_skoczka:
            pola_atakowane.extend(self.przygotujRuchySKoczka(pole))
        return self.wykreslAtakowanePola(mozliwe_ruchy, pola_atakowane)

    def wykreslPolaBitePoprzecznie(self, mozliwe_ruchy, pola_bierki, bierka):
        # if bierka == 'krol':
        return mozliwe_ruchy

        # TODO: wykreslanie pol dla innych bierek, ograniczenie przez bicie, roszada

    def wykreslAtakowanePola(self, mozliwe_ruchy, pola_atakowane):
        return [pole_ruchu for pole_ruchu in mozliwe_ruchy if pole_ruchu not in pola_atakowane]

    def ograniczPionaOBicie(self, obiektPiona, pola):
        return pola

    def ograniczSkoczkaOBicie(self, obiektSkoczka, pola):
        return pola

    def ograniczGoncaOBicie(self, obiektGonca, pola):
        return pola

    def ograniczWiezeOBicie(self, obiektWiezy, pola):
        return pola

    def ograniczHetmanaOBicie(self, obiektHetmana, pola):
        return pola

    def ograniczKrolaOBicie(self, obiektKrola, pola):
        return pola
