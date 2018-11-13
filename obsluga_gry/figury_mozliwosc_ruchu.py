#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .config import lista_szerokosci, lista_wysokosci, warunki_biale, warunki_czarne
from tools.narzedzia_pol import zmienWspolrzedneNaPole, wyznaczWspolrzednePoPozycji, czyWszpolrzedneWPolu
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola, zmienListePolNaWspolrzedne
from tools.narzedzia_pol import zmienListePolNaWspolrzedneZeSprawdzeniem, zmienListeWspolrzednychNaPolaZeSprawdzeniem
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_matow import NarzedziaMatow
from tools.narzedzia_szachow import czyKrolWSzachu
from tools.narzedzia_wyznaczania_ruchow import NarzedziaWyznaczaniaRuchow


class MozliwoscRuchuBierki(object):

    def __init__(self, obiekt_bierki):
        self.narz_szukania_bierek = NarzedziaSzukaniaBierek()
        self.narz_wyznacz_ruchow = NarzedziaWyznaczaniaRuchow()

        self.obiekt_bierki = obiekt_bierki
        self.pola_zajete_bialymi = self.stworzZajetePola(warunki_biale)
        self.pola_zajete_czarnymi = self.stworzZajetePola(warunki_czarne)
        self.dajPolaSojusznikowIWrogow()

    def stworzZajetePola(self, kolor, wykluczenie=' '):
        pola = []
        figury = self.narz_szukania_bierek.dajSlownikZajetychPol()[kolor]
        for figura in figury.keys():
            if wykluczenie not in figura:
                pola.extend(figury[figura])
        return pola

    def dajPolaSojusznikowIWrogow(self):
        if warunki_biale in self.obiekt_bierki.nazwa:
            self.pola_przecinikow = self.pola_zajete_czarnymi
            self.pola_sojusznikow = self.pola_zajete_bialymi
        else:
            self.pola_przecinikow = self.pola_zajete_bialymi
            self.pola_sojusznikow = self.pola_zajete_czarnymi

    def dajPolaSojusznikowIWrogowBezKrola(self):
        if warunki_biale in self.obiekt_bierki.nazwa:
            self.pola_przecinikow = self.stworzZajetePola(warunki_czarne, 'krol')
            self.pola_sojusznikow = self.stworzZajetePola(warunki_biale, 'krol')
        else:
            self.pola_przecinikow = self.stworzZajetePola(warunki_biale, 'krol')
            self.pola_sojusznikow = self.stworzZajetePola(warunki_czarne, 'krol')

    def sprawdzMozliweRuchy(self, ograniczyc_szach=True):
        if 'pion' in self.obiekt_bierki.nazwa:
            ruch = self.ruchDlaPiona(self.obiekt_bierki)
        elif 'skoczek' in self.obiekt_bierki.nazwa:
            ruch = self.ruchDlaSkoczka(self.obiekt_bierki)
        elif 'goniec' in self.obiekt_bierki.nazwa:
            ruch = self.ruchPoprzeczny(self.obiekt_bierki)
        elif 'wieza' in self.obiekt_bierki.nazwa:
            ruch = self.ruchKrzyzowy(self.obiekt_bierki)
        elif 'hetman' in self.obiekt_bierki.nazwa:
            ruch = self.ruchHetmana(self.obiekt_bierki)
        elif 'krol' in self.obiekt_bierki.nazwa:
            ruch = self.ruchDlaKrola(self.obiekt_bierki)

        if ograniczyc_szach:
            if 'krol' not in self.obiekt_bierki.nazwa:
                ruch = self.sprawdzIOgraniczJesliSzach(ruch)
            else:
                ruch['roszada'] = self.dajRoszade(self.obiekt_bierki)
            ruch = self.dajRuchyBezSzachow(ruch, self.obiekt_bierki)

        return ruch

    def dajRoszade(self, obiekt_krola):
        mozliwa_roszada = self.dajPolaDoRoszady(obiekt_krola)
        mozliwa_roszada = self.wykreslPolaBitePrzezPrzeciwnikow(obiekt_krola, mozliwa_roszada)
        return zmienListePolNaWspolrzedne(mozliwa_roszada)

    def ruchDlaPiona(self, obiekt_bierki):
        mozliwe_ruchy = []
        ilosc_ruchow = range(1, 2) if obiekt_bierki.czy_poruszona else range(1, 3)

        for ruch in ilosc_ruchow:
            if warunki_biale in obiekt_bierki.nazwa:
                mozliwe_ruchy.append({
                    'x': obiekt_bierki.pozycja_x,
                    'y': obiekt_bierki.pozycja_y - 100*ruch
                })
            else:
                mozliwe_ruchy.append({
                    'x': obiekt_bierki.pozycja_x,
                    'y': obiekt_bierki.pozycja_y + 100*ruch
                })
        mozliwe_ruchy = zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy)
        mozliwe_ruchy = self.sprawdzCzyZawadzaPrzeciwnik(mozliwe_ruchy)
        # TODO Promocja
        return {
            'ruch': zmienListePolNaWspolrzedne(self.sprawdzCzyZawadza(mozliwe_ruchy)),
            'bicie': self.dodajPionomBicie(obiekt_bierki, mozliwe_ruchy),
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

        return self.ograniczSkoczkaOBicie([wyznaczWspolrzednePoPozycji(ruch) for ruch in mozliwe_ruchy])

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
        mozliwe_bicie = self.wykreslOslonieteBierki(obiektKrola, ruch_poprzeczny['bicie']+ruch_krzyzowy['bicie'])
        return {
            'ruch': mozliwy_ruch,
            'bicie': mozliwe_bicie,
        }

    def wykreslOslonieteBierki(self, obiektKrola, mozliwe_ruchy):
        for wspolrzedne in mozliwe_ruchy[:]:
            pole = zmienWspolrzedneNaPole(wspolrzedne['x'], wspolrzedne['y'])
            bierka = self.narz_szukania_bierek.dajBierkePoPolu(pole)
            if bierka and bierka.kryta:
                mozliwe_ruchy.remove(wspolrzedne)
        return mozliwe_ruchy

    def dajPolaDoRoszady(self, obiekt_krola):
        roszada = []
        szerokosc = '1' if warunki_biale in obiekt_krola.nazwa else '8'
        if self.narz_wyznacz_ruchow.czyMozliwaRoszadaDluga(obiekt_krola):
            roszada.append('c'+szerokosc)
        if self.narz_wyznacz_ruchow.czyMozliwaRoszadaKrotka(obiekt_krola):
            roszada.append('g'+szerokosc)
        return roszada

    def ruchPoprzeczny(self, obiekt_bierki):
        lista_ruchow = self.dajListyRuchowPoprzecznych(obiekt_bierki)
        return self.koncoweMozliwosciProstegoRuchu(lista_ruchow)

    def dajListyRuchowPoprzecznych(self, obiekt_bierki):
        poprzeczne_prawy_dol = []
        poprzeczne_lewa_gora = []
        poprzeczne_prawa_gora = []
        poprzeczne_lewy_dol = []

        ilosc_ruchow = range(1, 2) if 'krol' in obiekt_bierki.nazwa else range(1, 8)
        for ruch in ilosc_ruchow:
            poprzeczne_prawy_dol.extend(self.dajJedenMozliwyPoprzecznyWPrawyDol(ruch, obiekt_bierki))
            poprzeczne_lewa_gora.extend(self.dajJedenMozliwyPoprzecznyWLewaGore(ruch, obiekt_bierki))
            poprzeczne_prawa_gora.extend(self.dajJedenMozliwyPoprzecznyWPrawaGore(ruch, obiekt_bierki))
            poprzeczne_lewy_dol.extend(self.dajJedenMozliwyPoprzecznyWLewyDol(ruch, obiekt_bierki))

        return [poprzeczne_prawy_dol, poprzeczne_lewa_gora, poprzeczne_prawa_gora, poprzeczne_lewy_dol]

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

    def dajJedenMozliwyPoprzecznyWLewaGore(self, index, obiekt_bierki):
        x_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_x, index)
        y_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyPoprzecznyWPrawyDol(self, index, obiekt_bierki):
        x_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_x, index)
        y_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyPoprzecznyWPrawaGore(self, index, obiekt_bierki):
        x_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_x, index)
        y_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyPoprzecznyWLewyDol(self, index, obiekt_bierki):
        x_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_x, index)
        y_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_y, index)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def ruchKrzyzowy(self, obiekt_bierki):
        lista_ruchow = self.dajListyRuchowKrzyzowych(obiekt_bierki)
        return self.koncoweMozliwosciProstegoRuchu(lista_ruchow)

    def dajListyRuchowKrzyzowych(self, obiekt_bierki):
        prosto_prawo = []
        prosto_gora = []
        prosto_lewo = []
        prosto_dol = []

        ilosc_ruchow = range(1, 2) if 'krol' in obiekt_bierki.nazwa else range(1, 8)
        for ruch in ilosc_ruchow:
            prosto_prawo.extend(self.dajJedenMozliwyWPrawo(ruch, obiekt_bierki))
            prosto_gora.extend(self.dajJedenMozliwyWGore(ruch, obiekt_bierki))
            prosto_lewo.extend(self.dajJedenMozliwyWLewo(ruch, obiekt_bierki))
            prosto_dol.extend(self.dajJedenMozliwyWDol(ruch, obiekt_bierki))

        return [prosto_prawo, prosto_gora, prosto_lewo, prosto_dol]

    def dajJedenMozliwyWPrawo(self, ruch, obiekt_bierki):
        x_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_x, ruch)
        y_podswietlenia = obiekt_bierki.pozycja_y
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyWGore(self, ruch, obiekt_bierki):
        x_podswietlenia = obiekt_bierki.pozycja_x
        y_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_y, ruch)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyWLewo(self, ruch, obiekt_bierki):
        x_podswietlenia = self.zmniejszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_x, ruch)
        y_podswietlenia = obiekt_bierki.pozycja_y
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def dajJedenMozliwyWDol(self, ruch, obiekt_bierki):
        x_podswietlenia = obiekt_bierki.pozycja_x
        y_podswietlenia = self.zwiekszWspolrzednaOXSetekPx(obiekt_bierki.pozycja_y, ruch)
        return self.przypiszPozycjePodswietleniaJesliWPolu(x_podswietlenia, y_podswietlenia)

    def przypiszPozycjePodswietleniaJesliWPolu(self, x, y):
        if czyWszpolrzedneWPolu(x, y):
            return [{
                'x': x,
                'y': y
            }]
        return []

    def sprawdzCzyZawadza(self, mozliwe_ruchy, dodaj_do_indexu=0):
        for index, pole in enumerate(zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy)):
            if pole in self.pola_sojusznikow and index <= len(mozliwe_ruchy):
                mozliwe_ruchy = mozliwe_ruchy[:index+dodaj_do_indexu]
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
            if warunki_biale in nazwa_bierki and index != 0:
                pola_atakowane[j] = pole + lista_wysokosci[index - 1]
            elif warunki_czarne in nazwa_bierki and index != len(lista_wysokosci):
                pola_atakowane[j] = pole + lista_wysokosci[index + 1]
        return pola_atakowane

    def sprawdzCzyBicieNaPolach(self, pola_atakowane, obiekt_bierki):
        if warunki_biale in obiekt_bierki.nazwa:
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
        if warunki_biale in obiektKrola.nazwa:
            return self.wykreslPolaBitePrzez(warunki_czarne, mozliwe_ruchy)
        return self.wykreslPolaBitePrzez(warunki_biale, mozliwe_ruchy)

    def wykreslPolaBitePrzez(self, kolor_przecinikow, mozliwe_ruchy):
        figury_pola = self.narz_szukania_bierek.dajSlownikZajetychPol()[kolor_przecinikow]
        self.dajPolaSojusznikowIWrogowBezKrola()
        for bierka, pola_bierki in figury_pola.items():
            if bierka == 'pion':
                mozliwe_ruchy = self.wykreslPolaBitePrzezPiona(mozliwe_ruchy, pola_bierki, kolor_przecinikow)
            elif bierka == 'skoczek':
                mozliwe_ruchy = self.wykreslPolaBitePrzezSkoczka(mozliwe_ruchy, pola_bierki)
            if bierka in ('goniec', 'hetman', 'krol'):
                mozliwe_ruchy = self.wykreslPolaBitePoprzecznie(mozliwe_ruchy, pola_bierki)
            if bierka in ('wieza', 'hetman', 'krol'):
                mozliwe_ruchy = self.wykreslPolaBiteKrzyzowo(mozliwe_ruchy, pola_bierki)
        self.dajPolaSojusznikowIWrogow()

        mozliwe_ruchy = zmienListePolNaWspolrzedneZeSprawdzeniem(mozliwe_ruchy)
        return mozliwe_ruchy

    def wykreslPolaBitePrzezPiona(self, mozliwe_ruchy, pola_bierki, kolor_przecinikow):
        mozliwe_ruchy = zmienListeWspolrzednychNaPolaZeSprawdzeniem(mozliwe_ruchy)
        pola_atakowane = []
        for pole in pola_bierki:
            if warunki_biale in kolor_przecinikow:
                pola_atakowane.extend(self.dajBiciePionow(pole, 'bialy pion'))
            else:
                pola_atakowane.extend(self.dajBiciePionow(pole, 'czarny pion'))
        return [pole_ruchu for pole_ruchu in mozliwe_ruchy if pole_ruchu not in pola_atakowane]

    def wykreslPolaBitePrzezSkoczka(self, mozliwe_ruchy, pola_skoczka):
        pola_atakowane = []
        for pole in pola_skoczka:
            pola_atakowane.extend(self.przygotujRuchySKoczka(pole))
        return [pole_ruchu for pole_ruchu in mozliwe_ruchy if pole_ruchu not in pola_atakowane]

    def wykreslPolaBitePoprzecznie(self, mozliwe_ruchy, pola_bierki):
        ret = []
        for pole in pola_bierki:
            obiekt = self.narz_szukania_bierek.dajBierkePoPolu(pole)
            pola_atakowane = self.ruchPoprzeczny(obiekt)
            ret.extend(pola_atakowane['ruch'])
        ret = zmienListeWspolrzednychNaPola(ret)
        return [pole for pole in mozliwe_ruchy if pole not in ret]

    def wykreslPolaBiteKrzyzowo(self, mozliwe_ruchy, pola_bierki):
        ret = []
        for pole in pola_bierki:
            obiekt = self.narz_szukania_bierek.dajBierkePoPolu(pole)
            pola_atakowane = self.ruchKrzyzowy(obiekt)
            ret.extend(pola_atakowane['ruch'])
        ret = zmienListeWspolrzednychNaPola(ret)
        return [pole for pole in mozliwe_ruchy if pole not in ret]

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

    def sprawdzIOgraniczJesliSzach(self, pola):
        from .warunki_wygranej import WarunkiWygranej

        if WarunkiWygranej.zagrozony_krol and self.obiekt_bierki.kolor in WarunkiWygranej.zagrozony_krol.nazwa:
            return self.ograniczMozliwePola(pola)
        return pola

    def ograniczMozliwePola(self, pola):
        return {
            'ruch': self.dajMozliwyRuchWSzachu(pola['ruch']),
            'bicie': self.dajMozliwoscBiciaWSzachu(pola['bicie']),
        }

    def dajMozliwyRuchWSzachu(self, ruch):
        from .warunki_wygranej import WarunkiWygranej

        nm = NarzedziaMatow(WarunkiWygranej.bierka_bijaca)
        pola_biacej = nm.dajPolaBijacejDoKrola()
        return [i for i in ruch if i in pola_biacej]

    def dajMozliwoscBiciaWSzachu(self, bicie):
        from .warunki_wygranej import WarunkiWygranej

        nm = NarzedziaMatow(WarunkiWygranej.bierka_bijaca)
        return nm.dajPolaBijaceSzachujacego(bicie)

    def dajRuchyBezSzachow(self, mozliwe_ruchy, bierka):
        from obsluga_gry.kolejnosc_ruchu import KolejnoscRuchu

        nazwa_krola = KolejnoscRuchu.kolej_na + '_krol'
        krol = self.narz_szukania_bierek.dajBierkiPoSlowieKluczowym(nazwa_krola)[0]
        bazowe_wspolrzedne = {'x': bierka.pozycja_x, 'y': bierka.pozycja_y, 'pozycja': bierka.pozycja}

        for klucz in mozliwe_ruchy:
            for wspolrzedna in mozliwe_ruchy[klucz][:]:
                bierka.pozycja_x = wspolrzedna['x']
                bierka.pozycja_y = wspolrzedna['y']
                bierka.pozycja = zmienWspolrzedneNaPole(wspolrzedna['x'], wspolrzedna['y'])
                if czyKrolWSzachu(krol):
                    mozliwe_ruchy[klucz].remove(wspolrzedna)

        bierka.pozycja = bazowe_wspolrzedne['pozycja']
        bierka.pozycja_x = bazowe_wspolrzedne['x']
        bierka.pozycja_y = bazowe_wspolrzedne['y']

        return mozliwe_ruchy
