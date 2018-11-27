#! /usr/bin/env python3
# -*- coding: utf-8 -*-


warunki_biale = 'bialy'
warunki_czarne = 'czarny'

lista_szerokosci = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
lista_wysokosci = ['8', '7', '6', '5', '4', '3', '2', '1']

szerokosc_ekranu = 800
wysokosc_ekranu = szerokosc_ekranu
szerokosc_pola = szerokosc_ekranu/8
srodek_pola = szerokosc_pola/2

slownik_bierek = {
    'pion': [],
    'skoczek': [],
    'goniec': [],
    'wieza': [],
    'hetman': [],
    'krol': [],
}

figury_pola_startowe = {
    warunki_biale: {
        'pion': [znak + '2' for znak in lista_szerokosci],
        'skoczek': ['b1', 'g1'],
        'goniec': ['c1', 'f1'],
        'wieza': ['a1', 'h1'],
        'hetman': ['d1'],
        'krol': ['e1'],
    },
    warunki_czarne: {
        'pion': [znak + '7' for znak in lista_szerokosci],
        'skoczek': ['b8', 'g8'],
        'goniec': ['c8', 'f8'],
        'wieza': ['a8', 'h8'],
        'hetman': ['d8'],
        'krol': ['e8'],
    },
}

figury_wagi = {
    'pion': 1,
    'skoczek': 3,
    'goniec': 3,
    'wieza': 4.5,
    'hetman': 8,
    'krol': None,
}
