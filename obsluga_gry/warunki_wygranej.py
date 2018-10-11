#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from util.narzedzia_figur import NarzedziaSzukaniaBierek

narz_szukania_bierek = NarzedziaSzukaniaBierek()


def sprawdzWarunkiWygranej(kolor):
    wszystkie_figury_koloru = narz_szukania_bierek.dajSlownikZajetychPol()[kolor]
    krol_koloru = wszystkie_figury_koloru['krol']
