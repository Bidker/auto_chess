#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .config import lista_szerokosci, lista_wysokosci
from util.narzedzia_pol import zmienWspolrzedneNaPole, wyznaczWspolrzednePoPozycji, czyWszpolrzedneWPolu
from util.narzedzia_pol import zmienListeWspolrzednychNaPola, zmienListePolNaWspolrzedne
from util.narzedzia_pol import zmienListePolNaWspolrzedneZeSprawdzeniem, zmienListeWspolrzednychNaPolaZeSprawdzeniem
from util.narzedzia_figur import NarzedziaSzukaniaBierek


class MozliwoscRuchuBierki(object):
    def __init__(self):
        self.narz_szukania_bierek = NarzedziaSzukaniaBierek()
        self.pola_zajete_bialymi = self.stworzZajetePola('biale')
        self.pola_zajete_czarnymi = self.stworzZajetePola('czarne')

    def stworzZajetePola(self, kolor):
        pola = []
        figury = self.narz_szukania_bierek.dajSlownikZajetychPol()[kolor]
        for figura in figury.keys():
            pola.extend(figury[figura])
        return pola

    def sprawdzMozliweRuchy(self, obiektBierki):
        if 'bialy' in obiektBierki.nazwa:
            self.pola_przecinikow = self.pola_zajete_czarnymi
            self.pola_sojusznikow = self.pola_zajete_bialymi
        else:
            self.pola_przecinikow = self.pola_zajete_bialymi
            self.pola_sojusznikow = self.pola_zajete_czarnymi

        if 'pion' in obiektBierki.nazwa:
            return self.ruchDlaPiona(obiektBierki)
        elif 'skoczek' in obiektBierki.nazwa:
            return self.ruchDlaSkoczka(obiektBierki)
        elif 'goniec' in obiektBierki.nazwa:
            return self.ruchPoprzeczny(obiektBierki)
        elif 'wieza' in obiektBierki.nazwa:
            return self.ruchKrzyzowy(obiektBierki)
        elif 'hetman' in obiektBierki.nazwa:
            return self.ruchHetmana(obiektBierki)
        elif 'krol' in obiektBierki.nazwa:
            return self.ruchDlaKrola(obiektBierki)

    def ruchDlaPiona(self, obiektBierki):
        mozliwe_ruchy = []
        ilosc_ruchow = range(1, 2) if obiektBierki.czy_poruszona else range(1, 3)

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
        mozliwe_ruchy = zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy)
        mozliwe_ruchy = self.sprawdzCzyZawadzaPrzeciwnik(mozliwe_ruchy)
        return {
            'ruch': zmienListePolNaWspolrzedne(self.sprawdzCzyZawadza(mozliwe_ruchy)),
            'bicie': self.dodajPionomBicie(obiektBierki, mozliwe_ruchy),
        }

    def dodajPionomBicie(self, obiektPiona, ruchy):
        pole_piona = zmienWspolrzedneNaPole(obiektPiona.pozycja_x, obiektPiona.pozycja_y)
        pola_atakowane = self.dajBiciePionow(pole_piona, obiektPiona.nazwa)
        pola_atakowane = self.sprawdzCzyBicieNaPolach(pola_atakowane, obiektPiona)
        lista_wspolrzednych = []
        for pole in pola_atakowane:
            lista_wspolrzednych.append(wyznaczWspolrzednePoPozycji(pole))
        return lista_wspolrzednych

    def dajBiciePionow(self, pole_piona, nazwaPiona):
        pola_atakowane = []
        for i in pole_piona:
            if i in lista_szerokosci:
                pola_atakowane.extend(self.ustawSzerokoscBiciaOJeden(i))
            elif i in lista_wysokosci:
                pola_atakowane = self.ustawWysokoscBiciaOJeden(i, pola_atakowane, nazwaPiona)
        return pola_atakowane

    def ruchDlaSkoczka(self, obiektSkoczka):
        pole_skoczka = zmienWspolrzedneNaPole(obiektSkoczka.pozycja_x, obiektSkoczka.pozycja_y)
        mozliwe_ruchy = self.przygotujRuchySKoczka(pole_skoczka)
        mozliwe_ruchy = self.sprawdzCzyKucowiZawadza(mozliwe_ruchy)

        ret = []
        for ruch in mozliwe_ruchy:
            ret.append(wyznaczWspolrzednePoPozycji(ruch))

        return self.ograniczSkoczkaOBicie(ret)

    def przygotujRuchySKoczka(self, pole_skoczka):
        mozliwe_ruchy = []
        lista_przygotowawcza = []
        for wspolrzedna in pole_skoczka:
            lista_przygotowawcza.extend(self.dajPozycjeOddalonaODwaWiecej(wspolrzedna))
            lista_przygotowawcza.extend(self.dajPozycjeOddalonaODwaMniej(wspolrzedna))
        mozliwe_ruchy.extend(self.stworzPozycjeDlaSkoczka(lista_przygotowawcza, pole_skoczka))
        return mozliwe_ruchy

    def dajPozycjeOddalonaODwaWiecej(self, znak):
        ret = []
        if znak in lista_wysokosci and znak not in ('1', '2'):
            ret.append(lista_wysokosci[(lista_wysokosci.index(znak) + 2)])
        elif znak in lista_szerokosci and znak not in ('g', 'h'):
            ret.append(lista_szerokosci[(lista_szerokosci.index(znak) + 2)])
        return ret

    def dajPozycjeOddalonaODwaMniej(self, znak):
        ret = []
        if znak in lista_wysokosci and znak not in ('7', '8'):
            ret.append(lista_wysokosci[(lista_wysokosci.index(znak) - 2)])
        elif znak in lista_szerokosci and znak not in ('a', 'b'):
            ret.append(lista_szerokosci[(lista_szerokosci.index(znak) - 2)])
        return ret

    def stworzPozycjeDlaSkoczka(self, lista_przygotowawcza, pole_skoczka):
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
                if index != 7:
                    ret.append(lista_szerokosci[index+1] + znak)
                if index != 0:
                    ret.append(lista_szerokosci[index-1] + znak)
        return ret

    def sprawdzCzyKucowiZawadza(self, mozliwe_ruchy):
        ret = []
        for pole in zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy):
            if pole not in self.pola_sojusznikow:
                ret.append(pole)
        return ret

    def ruchHetmana(self, obiektHetmana):
        pole_krzyzowe = self.ruchKrzyzowy(obiektHetmana)
        pole_poprzeczne = self.ruchPoprzeczny(obiektHetmana)
        return {
            'ruch': pole_krzyzowe['ruch'] + pole_poprzeczne['ruch'],
            'bicie': pole_krzyzowe['bicie'] + pole_poprzeczne['bicie'],
        }

    def ruchDlaKrola(self, obiektKrola):
        ruch_krzyzowy = self.ruchKrzyzowy(obiektKrola)
        ruch_poprzeczny = self.ruchPoprzeczny(obiektKrola)
        mozliwy_ruch = self.wykreslPolaBitePrzezPrzeciwnikow(obiektKrola, ruch_poprzeczny['ruch']+ruch_krzyzowy['ruch'])
        mozliwe_bicie = self.wykreslPolaBitePrzezPrzeciwnikow(
            obiektKrola, ruch_poprzeczny['bicie']+ruch_krzyzowy['bicie'])
        return {
            'ruch': mozliwy_ruch,
            'bicie': mozliwe_bicie,
        }

    def ruchPoprzeczny(self, obiektBierki):
        poprzeczne_prawy_dol = []
        poprzeczne_lewa_gora = []
        poprzeczne_prawa_gora = []
        poprzeczne_lewy_dol = []

        if 'krol' in obiektBierki.nazwa:
            ilosc_ruchow = range(1, 2)
        else:
            ilosc_ruchow = range(1, 8)

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

        lista_ruchow = [poprzeczne_prawy_dol, poprzeczne_lewa_gora, poprzeczne_prawa_gora, poprzeczne_lewy_dol]
        return self.koncoweMozliwosciProstegoRuchu(lista_ruchow)

    def koncoweMozliwosciProstegoRuchu(self, lista_ruchow):
        mozliwe_bicie = []
        ret = []
        for ruch_kierunkowy in lista_ruchow:
            mozliwy_ruch = zmienListeWspolrzednychNaPola(ruch_kierunkowy)
            mozliwy_ruch = self.sprawdzCzyZawadza(mozliwy_ruch)
            mozliwy_ruch.append('zaslepka')
            dlugosc = len(mozliwy_ruch)
            mozliwy_ruch = self.sprawdzCzyZawadzaPrzeciwnik(mozliwy_ruch, 1)
            if dlugosc != len(mozliwy_ruch):
                mozliwe_bicie.append(mozliwy_ruch.pop())
            else:
                mozliwy_ruch.pop()
            ret.extend(mozliwy_ruch)

        return {
            'ruch': zmienListePolNaWspolrzedne(ret),
            'bicie': zmienListePolNaWspolrzedne(mozliwe_bicie),
        }

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

        lista_ruchow = [prosto_prawo, prosto_gora, prosto_lewo, prosto_dol]
        return self.koncoweMozliwosciProstegoRuchu(lista_ruchow)

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

    def sprawdzCzyZawadza(self, mozliwe_ruchy):
        for index, pole in enumerate(zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy)):
            if pole in self.pola_sojusznikow:
                mozliwe_ruchy = mozliwe_ruchy[:index]
        return mozliwe_ruchy

    def sprawdzCzyZawadzaPrzeciwnik(self, mozliwe_ruchy, dodaj_do_indexu=0):
        for index, pole in enumerate(zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy)):
            if pole in self.pola_przecinikow:
                mozliwe_ruchy = mozliwe_ruchy[:(index+dodaj_do_indexu)]
        return mozliwe_ruchy

    def ustawSzerokoscBiciaOJeden(self, liera_planszy):
        ret = []
        index = lista_szerokosci.index(liera_planszy)
        if liera_planszy != 'a':
            ret.append(lista_szerokosci[index - 1])
        if liera_planszy != 'h':
            ret.append(lista_szerokosci[index + 1])
        return ret

    def ustawWysokoscBiciaOJeden(self, cyfra_planszy, pola_atakowane, nazwa_bierki):
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
        figury_pola = self.narz_szukania_bierek.dajSlownikZajetychPol()[kolor_przecinikow]
        for bierka, pola_bierki in figury_pola.items():
            if bierka == 'pion':
                mozliwe_ruchy = self.wykreslPolaBitePrzezPiona(mozliwe_ruchy, pola_bierki, kolor_przecinikow)
            elif bierka == 'skoczek':
                mozliwe_ruchy = self.wykreslPolaBitePrzezSkoczka(mozliwe_ruchy, pola_bierki)
            elif bierka in ('goniec', 'hetman', 'krol'):
                mozliwe_ruchy = self.wykreslPolaBitePoprzecznie(mozliwe_ruchy, pola_bierki, bierka, kolor_przecinikow)
            elif bierka in ('wieza', 'hetman', 'krol'):
                mozliwe_ruchy = self.wykreslPolaBiteKrzyzowo(mozliwe_ruchy, pola_bierki, bierka, kolor_przecinikow)

        mozliwe_ruchy = zmienListePolNaWspolrzedneZeSprawdzeniem(mozliwe_ruchy)
        return mozliwe_ruchy

    def wykreslPolaBitePrzezPiona(self, mozliwe_ruchy, pola_bierki, kolor_przecinikow):
        mozliwe_ruchy = zmienListeWspolrzednychNaPola(mozliwe_ruchy)
        pola_atakowane = []
        for pole in pola_bierki:
            if kolor_przecinikow == 'biale':
                pola_atakowane.extend(self.dajBiciePionow(pole, 'bialy pion'))
            else:
                pola_atakowane.extend(self.dajBiciePionow(pole, 'czarny pion'))
        return [pole_ruchu for pole_ruchu in mozliwe_ruchy if pole_ruchu not in pola_atakowane]

    def wykreslPolaBitePrzezSkoczka(self, mozliwe_ruchy, pola_skoczka):
        pola_atakowane = []
        for pole in pola_skoczka:
            pola_atakowane.extend(self.przygotujRuchySKoczka(pole))
        return [pole_ruchu for pole_ruchu in mozliwe_ruchy if pole_ruchu not in pola_atakowane]

    def wykreslPolaBitePoprzecznie(self, mozliwe_ruchy, pola_bierki, bierka, kolor_przecinikow):
        with self.narz_szukania_bierek.szukanieBierki(bierka, kolor_przecinikow) as obiekt:
            pola_atakowane = self.ruchPoprzeczny(obiekt)
            return [pole for pole in mozliwe_ruchy if pole not in pola_atakowane]

    def wykreslPolaBiteKrzyzowo(self, mozliwe_ruchy, pola_bierki, bierka, kolor_przecinikow):
        with self.narz_szukania_bierek.szukanieBierki(bierka, kolor_przecinikow) as obiekt:
            pola_atakowane = self.ruchKrzyzowy(obiekt)
            return [pole for pole in mozliwe_ruchy if pole not in pola_atakowane]

    def ograniczSkoczkaOBicie(self, pola_ruchu):
        pola_bicia = []
        pola_ruchu = zmienListeWspolrzednychNaPolaZeSprawdzeniem(pola_ruchu)
        for pole in pola_ruchu[:]:
            if pole in self.pola_przecinikow:
                pola_bicia.append(pole)
                pola_ruchu.remove(pole)
        return {
            'ruch': zmienListePolNaWspolrzedne(pola_ruchu),
            'bicie': zmienListePolNaWspolrzedne(pola_bicia),
        }
