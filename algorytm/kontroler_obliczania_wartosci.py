#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .faza_gry import FazaGry
from .ocena_materialna import dajWartoscMaterialna
from .pseudoposuniecia import wykonajPseudoruch, wykonajPseudobicie, wykonajPseudoroszade
from .obliczanie_wartosci_pozycyjnej.kontroler import dajWartoscPozycyjna
from tools.narzedzia_figur import NarzedziaSzukaniaBierek
from tools.narzedzia_pol import zmienWspolrzedneNaPole
from obsluga_gry.warunki_wygranej import WarunkiWygranej
from obsluga_gry.config import warunki_czarne


def uruchomAlgorytm():
    from obsluga_gry.figury_mozliwosc_ruchu import MozliwoscRuchuBierki

    nsb = NarzedziaSzukaniaBierek()
    lst_wartosci = []
    # sa trzymane w liscie slownikow, gdzie wartosc bedze wartoscia ruchu, bierka, pozycja wspolrzednymi i typ ruchu

    def zapiszWartosci(bierka, ruch, typ):
        wartosc_pozycyjna = dajWartoscPozycyjna()
        wartosc_materialna = dajWartoscMaterialna()
        lst_wartosci.append({
            'wartosc': wartosc_pozycyjna+wartosc_materialna,
            'bierka': bierka,
            'wspolrzedne': ruch,
            'typ_ruchu': typ,
        })

    def wybierzIWykonajNajlepszyRuch():
        lst_wartosci.sort(key=lambda x: x['wartosc'], reverse=True)
        bierka = lst_wartosci[0]['bierka']
        wspolrzedne = lst_wartosci[0]['wspolrzedne']
        typ = lst_wartosci[0]['typ_ruchu']
        pole = zmienWspolrzedneNaPole(x=wspolrzedne['x'], y=wspolrzedne['y'])

        if typ == 'ruch':
            bierka.zmienUstawienieBierki(wspolrzedne, pole)
        elif typ == 'bicie':
            bita_bierka = nsb.dajBierkePoPolu(pole)
            bita_bierka.zbita()
            bierka.zmienUstawienieBierki(wspolrzedne, pole)
        elif typ == 'roszada':
            bierka.wykonajRoszade(wspolrzedne, pole)

        ww = WarunkiWygranej()
        ww.sprawdzWarunkiWygranej()

    fg = FazaGry()
    fg.sprawdzFazeGry()
    lst_brk_cz = nsb.dajBierkiPoSlowieKluczowym(warunki_czarne)

    import datetime
    czas = datetime.datetime.now()

    for bierka in lst_brk_cz:
        mrb = MozliwoscRuchuBierki(bierka)
        mozliwe_ruchy = mrb.sprawdzMozliweRuchy()

        for ruch in mozliwe_ruchy['ruch']:
            with wykonajPseudoruch(bierka, ruch):
                zapiszWartosci(bierka, ruch, 'ruch')
        for ruch in mozliwe_ruchy['bicie']:
            with wykonajPseudobicie(bierka, ruch):
                zapiszWartosci(bierka, ruch, 'bicie')
        for ruch in mozliwe_ruchy.get('roszada', []):
            with wykonajPseudoroszade(bierka, ruch):
                zapiszWartosci(bierka, ruch, 'roszada')

    wybierzIWykonajNajlepszyRuch()

    koniec = datetime.datetime.now() - czas
    print('koniec = ', str(koniec))
