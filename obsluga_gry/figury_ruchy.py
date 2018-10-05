#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .listy_planszy import Plansza

from copy import deepcopy


class RuchFigur(object):
    def __init__(self):
        plansza = Plansza()

        self.figury_wagi = {
            'pion': 1,
            'skoczek': 3,
            'goniec': 3,
            'wieza': 4.5,
            'hetman': 8,
            'krol': None,
        }

        self.figury_pola_startowe = {
            'biale': {
                'pion': [znak + '2' for znak in plansza.lista_szerokosci],
                'skoczek': ['b1', 'g1'],
                'goniec': ['c1', 'f1'],
                'wieza': ['a1', 'h1'],
                'hetman': ['d1'],
                'krol': ['e1'],
            },
            'czarne': {
                'pion': [znak + '7' for znak in plansza.lista_szerokosci],
                'skoczek': ['b8', 'g8'],
                'goniec': ['c8', 'f8'],
                'wieza': ['a8', 'h8'],
                'hetman': ['d8'],
                'krol': ['e8'],
            },
        }

        self.pola_figur_w_trakcie_gry = deepcopy(self.figury_pola_startowe)

    def ruch(self, start, stop, czyj_ruch):
        if self.czy_w_planszy(stop):
            figury_ktorych_ruch = self.pola_figur_w_trakcie_gry.get(czyj_ruch)
            if czyj_ruch == 'biale':
                self.sprawdz_bicie('czarne')
            else:
                self.sprawdz_bicie('biale')
            figura_pole = self.daj_figure_i_pole(start, figury_ktorych_ruch)
            if not figura_pole.get('blad'):
                pola_poruszonej_figury = self.pola_figur_w_trakcie_gry.get(figura_pole.get('figura'))
                figury_ktorych_ruch[figura_pole.get('figura')] = self.zmien_pola(
                    stop, pola_poruszonej_figury, figura_pole)

    def czyWPlanszy(self, pozycja):
        i = 0
        for i in pozycja:
            if i in self.plansza.lista_szerokosci or i in self.plansza.lista_dlugosci:
                i += 1
        if i == 2:
            return True
        else:
            return False

    def sprawdzBicie(self, kolor, stop):
        pozycje_przeciwnikow = self.pola_figur_w_trakcie_gry.get(kolor)
        pozycja_w_biciu = self.dajFigureIPole(stop, pozycje_przeciwnikow)
        if pozycja_w_biciu:
            bicie = pozycje_przeciwnikow.get(pozycja_w_biciu('figura'))
            bicie.pop[pozycja_w_biciu('pozycja_pola')]

    def dajFigurePole(self, start, figury_pola):
        for figura in self.figury_wagi.keys():
            pola_figury = figury_pola.get(figura)
            if start in pola_figury:
                return self.sprawdzPole(pola_figury, start)

    def sprawdzPole(self, pola_figury, start):
        for i, pole in enumerate(pola_figury):
            if pole == start:
                return {
                    'figura': figura,
                    'pozycja_pola': i,
                }
        return None

    def zmienPola(self, stop, pola_poruszonej_figury, figura_pole):
        pola_poruszonej_figury[figura_pole.get('pozycja_pola')] = stop
        return pola_poruszonej_figury
