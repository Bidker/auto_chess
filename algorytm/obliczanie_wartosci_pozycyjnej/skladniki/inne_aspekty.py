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
        ],
        gra_srodkowa: [
            'obliczPunktyZaPozycje',
            'wzorLevego',
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

    @staticmethod
    def obliczPunktyZaPozycje(**kwargs):
        self = kwargs['self']
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

    @staticmethod
    def wzorLevego(**kwargs):
        self = kwargs['self']
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

        K = self._dajWartoscDlaRoszady()
        C = self._dajWartoscZaWrogiegoHetmana()

        return 20*D - (15*U + K*C)

    @staticmethod
    def sprawdzCzyMat(**kwargs):
        from obsluga_gry.warunki_wygranej import WarunkiWygranej

        ww = WarunkiWygranej()
        if ww.dajZagrozonegoKrola(zmien_wartosci=False) and ww.sprawdzCzyMat():
            return 20000

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
        if krol.czy_poruszona:
            return 20

        wieze = self.nsb.dajBierkiPoSlowieKluczowym(self.kolor+'_wieza')

        if wieze[0].czy_poruszona:
            return sprawdzPoPozycji(wieze[0])

        if wieze[1].czy_poruszona:
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
