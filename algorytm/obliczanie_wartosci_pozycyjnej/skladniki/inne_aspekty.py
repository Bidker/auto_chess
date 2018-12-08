#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from tools.narzedzia_pol import zmienWspolrzedneNaPole
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.config import figury_pola_startowe, warunki_biale, warunki_czarne
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)
from .baza import BazowaKlasaWartosci


class InneAspekty(BazowaKlasaWartosci):

    funkcje_obliczajace_wartosc = {
        debiut: [
            'obliczPunktyZaPozycje',
            'wzorLevego',
            'sprawdzCzyMat',
        ],
        gra_srodkowa: [
            'obliczPunktyZaPozycje',
            'wzorLevego',
            'sprawdzCzyMat',
        ],
        wczesna_koncowka: [
            'obliczPunktyZaPozycje',
            'sprawdzCzyMat',
        ],
        koncowka: [
            'obliczPunktyZaPozycje',
            'sprawdzCzyMat',
        ],
        matowanie: [
            'sprawdzCzyMat',
        ],
    }

    def __init__(self, kolor):
        super(InneAspekty, self).__init__(kolor)
        self.lista_bierek = self.nsb.dajBierkiPoSlowieKluczowym(kolor)

    def obliczPunktyZaPozycje(self):
        wartosc = 0

        for bierka in self.lista_bierek:
            mrb = MozliwoscRuchuBierki(bierka)
            mozliwe_ruchy = mrb.sprawdzMozliweRuchy()
            for wspolrzedne in mozliwe_ruchy['ruch']+mozliwe_ruchy['bicie']:
                pole = zmienWspolrzedneNaPole(x=wspolrzedne['x'], y=wspolrzedne['y'])
                if pole in lista_pol_centralnych:
                    wartosc += 10
                wartosc += 3
        return wartosc

    def wzorLevego(self):
        hetman = self.nsb.dajBierkiPoSlowieKluczowym(self.kolor+'_hetman')

        D = 0
        U = 0
        for bierka in self.lista_bierek:
            if bierka.czy_poruszona and ('skoczek' in bierka.nazwa or 'goniec' in bierka.nazwa):
                D += 1
            if (
                len(hetman) and
                not bierka.czy_poruszona and
                ('skoczek' in bierka.nazwa or 'goniec' in bierka.nazwa or 'wieza' in bierka.nazwa)
            ):
                U += 1
        if not len(hetman) or not hetman[0].czy_poruszona:
            U = 0

        K = self._dajWartoscDlaRoszady()
        C = self._dajWartoscZaWrogiegoHetmana()

        return 20*D - (15*U + K*C)

    def sprawdzCzyMat(self):
        from obsluga_gry.warunki_wygranej import WarunkiWygranej

        ww = WarunkiWygranej(self.kolor)
        if ww.dajZagrozonegoKrola(zmien_wartosci=False):
            if ww.sprawdzCzyMat():
                # mniejsza od 0 ponieważ sprawdzenie czy ruch dał mata dopiero przy sprawdzeniu kolejnego półruchu
                return -20000

        return 0

    def _dajWartoscDlaRoszady(self):
        from algorytm.obliczanie_wartosci_pozycyjnej.kontroler import KontrolerWartosciPozycyjnych

        def sprawdzPoPozycji(wieza):
            if 'a' in wieza.pozycja:
                return 5
            else:
                return 10

        if KontrolerWartosciPozycyjnych.roszada_wykonana[self.kolor]:
            return 0

        krol = self.nsb.dajBierkiPoSlowieKluczowym(self.kolor+'_krol')[0]
        wieze = self.nsb.dajBierkiPoSlowieKluczowym(self.kolor+'_wieza')

        if krol.czy_poruszona or not len(wieze):
            return 20

        if len(wieze) == 2 and not wieze[0].czy_poruszona and not wieze[1].czy_poruszona:
            return 3

        if wieze[0].czy_poruszona:
            return sprawdzPoPozycji(wieze[0])

        if len(wieze) == 2 and wieze[1].czy_poruszona:
            return sprawdzPoPozycji(wieze[1])

        return 20

    def _dajWartoscZaWrogiegoHetmana(self):
        kolor_wroga = warunki_biale if self.kolor == warunki_czarne else warunki_czarne
        bierki_wroga = self.nsb.dajBierkiPoSlowieKluczowym(kolor_wroga)

        C = 0
        for bierka in bierki_wroga:
            if 'hetman' in bierka.nazwa:
                return 8
            if 'skoczek' in bierka.nazwa or 'goniec' in bierka.nazwa or 'wieza' in bierka.nazwa:
                C += 1
        return C
