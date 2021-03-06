#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from obsluga_gry.config import slownik_bierek, warunki_biale, warunki_czarne
from .narzedzia_pol import naprawPole

from copy import deepcopy


class NarzedziaSzukaniaBierek(object):

    def __init__(self):
        from wyswietlenie_grafik.tworzenie_figur import ObiektyFigur
        of = ObiektyFigur()
        self.lista_obiektow = of.dajObiektyFigur()

    def dajZaznaczonaBierke(self):
        '''Funkcja zwraca bierkę nad którą został ostatnio wcisnięty klawisz myszy'''
        for bierka in self.lista_obiektow:
            if bierka.zaznaczony and not bierka.czy_zbita:
                return bierka

    def dajBierkePoPolu(self, pole, wiecej_niz_jeden=False):
        '''Zwraca bierkę która stoi na polu podanym w parametrze'''
        lst_brk = []
        for bierka in self.lista_obiektow:
            if naprawPole(bierka.pozycja) == naprawPole(pole) and not bierka.czy_zbita:
                if not wiecej_niz_jeden:
                    return bierka
                lst_brk.append(bierka)
        return lst_brk

    def dajSlownikZajetychPol(self):
        '''Zwraca słownik z kluczami 'czarny' i 'bialy' gdzie wartosciami są słowniki list '''
        slownik = {
            warunki_czarne: self.dajSlownikCzarnych(),
            warunki_biale: self.dajSlownikBialych(),
        }
        return slownik

    def dajSlownikBialych(self):
        '''Zwraca słownik białych bierek gdzie kluczami są figury, a wartosciami listy pól na których są'''
        return self._dajSlownikPozycji(warunki_biale)

    def dajSlownikCzarnych(self):
        '''Zwraca słownik czarnych bierek gdzie kluczami są figury, a wartosciami listy pól na których są'''
        return self._dajSlownikPozycji(warunki_czarne)

    def _dajSlownikPozycji(self, kolor):
        slownik = deepcopy(slownik_bierek)
        index = len(kolor) + 1

        for bierka in self.lista_obiektow:
            if kolor in bierka.nazwa:
                slownik[bierka.nazwa[index:]].append(bierka.pozycja)
        return slownik

    def dajBierkiPoSlowieKluczowym(self, slowo):
        return [bierka for bierka in self.lista_obiektow if slowo in bierka.nazwa]

    def dajNieruszoneBierkiBezKroli(self):
        return [bierka for bierka in self.lista_obiektow if not bierka.czy_poruszona and 'krol' not in bierka.nazwa]

    def dajBierkiBezKroli(self):
        return [bierka for bierka in self.lista_obiektow if 'krol' not in bierka.nazwa]

    def dajBierkeZKolumnyPoSlowieKluczowym(self, slowo_kluczowe, kolumna):
        lst_bierek = []
        for bierka in self.lista_obiektow:
            if slowo_kluczowe in bierka.nazwa and kolumna in bierka.pozycja:
                lst_bierek.append(bierka)
        return lst_bierek

    def dajBierkiZPolPoSlowie(self, slowo_kluczowe, lst_pol):
        lst_bierek = []
        for bierka in self.lista_obiektow:
            if slowo_kluczowe in bierka.nazwa and bierka.pozycja in lst_pol:
                lst_bierek.append(bierka)
        return lst_bierek

    def dajBierkiZListyNazw(self, lista_nazw):
        return [bierka for bierka in self.lista_obiektow if bierka.nazwa in lista_nazw]
