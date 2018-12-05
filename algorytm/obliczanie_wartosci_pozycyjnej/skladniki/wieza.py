#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .baza import BazowaKlasaWartosci
from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
from obsluga_gry.config import warunki_biale, warunki_czarne
from tools.narzedzia_pol import zmienListeWspolrzednychNaPola, dajOdlegloscMiedzyPolami
from algorytm.stale_wartosci import (
    debiut,
    gra_srodkowa,
    wczesna_koncowka,
    koncowka,
    matowanie,
    lista_pol_centralnych,
)


class Wieza(BazowaKlasaWartosci):
    funkcje_obliczajace_wartosc = {
        debiut: [
            'sprawdzOtwartaLinie',
            'mobilnoscWiezy',
        ],
        gra_srodkowa: [
            'sprawdzOtwartaLinie',
            'bliskoscWrogiegoKrola',
            'mobilnoscWiezy',
        ],
        wczesna_koncowka: [
            'bliskoscWrogiegoKrola',
            'mobilnoscWiezy',
        ],
        koncowka: [
            'bliskoscWrogiegoKrola',
            'mobilnoscWiezy',
        ],
        matowanie: [],
    }

    def __init__(self, kolor):
        super(Wieza, self).__init__(kolor)
        self.lista_wiez = self.nsb.dajBierkiPoSlowieKluczowym(kolor+'_wieza')

    def sprawdzOtwartaLinie(self):
        wartosc = 0
        kolor_wrogow = warunki_biale if warunki_czarne in self.kolor else warunki_czarne

        for wieza in self.lista_wiez:
            mrb = MozliwoscRuchuBierki(wieza)
            ruchy_wiezy = mrb.dajListyRuchowKrzyzowych(wieza)

            for lst_wsporzdnch in ruchy_wiezy:
                lst_pozycji = zmienListeWspolrzednychNaPola(lst_wsporzdnch)
                lst_pozycji.sort()
                przerwana_petla = False

                for pozycja in lst_pozycji:
                    bierka = self.nsb.dajBierkePoPolu(pozycja)

                    if bierka:
                        if bierka.nazwa == kolor_wrogow+'_pion':
                            wartosc += 4
                            przerwana_petla = True
                            break
                        elif bierka.nazwa == self.kolor+'pion':
                            przerwana_petla = True
                            break

                if not przerwana_petla and len(lst_pozycji):
                    wartosc += 10
        return wartosc

    def bliskoscWrogiegoKrola(self):
        wartosc = 0
        kolor_wroga = warunki_biale if warunki_czarne in self.kolor else warunki_czarne

        wrogi_krol = self.nsb.dajBierkiPoSlowieKluczowym(kolor_wroga+'_krol')[0]
        for wieza in self.lista_wiez:
            wartosc += dajOdlegloscMiedzyPolami(wrogi_krol.pozycja, wieza.pozycja)

        return 2*wartosc

    def mobilnoscWiezy(self):
        wartosc = 0
        for wieza in self.lista_wiez:
            mrb = MozliwoscRuchuBierki(wieza)
            # ruch = mrb.wyznacz ruch
        return wartosc
