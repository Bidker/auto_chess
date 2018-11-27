#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .faza_gry import FazaGry
from .ocena_materialna import dajWartoscMaterialna
from .pseudoposuniecia import wykonajPseudoruch, wykonajPseudobicie, wykonajPseudoroszade
from .obliczanie_wartosci_pozycyjnej.kontroler import dajWartoscPozycyjna
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from obsluga_gry.config import warunki_czarne


def uruchomAlgorytm():
    from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki
    # TU_BEDA_TRZYMANE_DANE
    # trzeba przemyslec strukture do najlepszego jej przeszukania

    def zapiszWartosci():
        wartosc_pozycyjna = dajWartoscPozycyjna()
        wartosc_materialna = dajWartoscMaterialna()
        # tu będą zapisywane dane

    def wybierzIWykonajNajlepszyRuch():
        # tu będą wybierane dane
        pass

    fg = FazaGry()
    fg.sprawdzFazeGry()
    nsb = NarzedziaSzukaniaBierek()
    lst_brk_cz = nsb.dajBierkiPoSlowieKluczowym(warunki_czarne)

    import datetime
    czas = datetime.datetime.now()

    for bierka in lst_brk_cz:
        mrb = MozliwoscRuchuBierki(bierka)
        mozliwe_ruchy = mrb.sprawdzMozliweRuchy()

        for ruch in mozliwe_ruchy['ruch']:
            with wykonajPseudoruch(bierka, ruch):
                zapiszWartosci()
        for ruch in mozliwe_ruchy['bicie']:
            with wykonajPseudobicie(bierka, ruch):
                zapiszWartosci()
        for ruch in mozliwe_ruchy.get('roszada', []):
            with wykonajPseudoroszade(bierka, ruch):
                zapiszWartosci()

    wybierzIWykonajNajlepszyRuch()

    koniec = datetime.datetime.now() - czas
    print('koniec = ', str(koniec))
