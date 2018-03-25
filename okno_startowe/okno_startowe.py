#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main import OknoGlowne
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget
from PyQt5.QtWidgets import QGridLayout, QPushButton
from wyswietlenie_grafik.screen import rozpocznijGre
from otwarcia.pokaz_otwarcia import PokazOtwarcia
from PyQt5.QtCore import Qt

class OknoStartowe(OknoGlowne):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()

    def interfejs(self):
        listaPrzyciskowMenu = self.stworzPrzyciski()
        ukladT = self.dodajPrzyciskiDoWidgetu(listaPrzyciskowMenu)
        self.setLayout(ukladT)
        self.podepnijObslugePrzyciskow(listaPrzyciskowMenu)
        self.konfiguracjaOkna("Auto szachy")

    def stworzPrzyciski(self):
        zacznijGreBtn = QPushButton("&Zacznij gre", self)
        dodajDoKsiegiOtwarcBtn = QPushButton("&Dodaj nowe otwarcie", self)
        zobaczOtwarciaBtn = QPushButton("&Przeglądaj dostępne otwacia", self)
        wyjdzBtn = QPushButton("&Wyjdź", self)
        wyjdzBtn.resize(wyjdzBtn.sizeHint())
        return [zacznijGreBtn, dodajDoKsiegiOtwarcBtn, zobaczOtwarciaBtn, wyjdzBtn]

    def dodajPrzyciskiDoWidgetu(self, listaPrzyciskow):
        ukladT = QGridLayout()
        j = 0
        for i, przycisk in enumerate(listaPrzyciskow):
            if (i % 3) == 0:
                j = j + 1
            ukladT.addWidget(przycisk, 0, i)
        return ukladT

    def podepnijObslugePrzyciskow(self, listaPrzyciskow):
        zacznijGreBtn = listaPrzyciskow[0]
        dodajDoKsiegiOtwarcBtn = listaPrzyciskow[1]
        zobaczOtwarciaBtn = listaPrzyciskow[2]
        wyjdzBtn = listaPrzyciskow[3]
        self.przyciskZamknieciaProgramu(wyjdzBtn)
        self.przyciskPrzejdz(dodajDoKsiegiOtwarcBtn)
        self.przyciskPrzejdz(zobaczOtwarciaBtn)
        self.przyciskPrzejdz(zacznijGreBtn)

    def przyciskZamknieciaProgramu(self, przycisk):
        przycisk.clicked.connect(self.koniec)

    def koniec(self):
        self.close()

    def przyciskPrzejdz(self, przycisk):
        przycisk.clicked.connect(self.przejdz)

    def przejdz(self):
        nadawca = self.sender()
        if nadawca.text() == "&Dodaj nowe otwarcie":
            self.noweOtwarcie()
        elif nadawca.text() == "&Zacznij gre":
            self.rozpocznijGre()
        elif nadawca.text() == "&Przeglądaj dostępne otwacia":
            pokazOtwarcia = PokazOtwarcia()
            self.close()

    def rozpocznijGre(self):
        rozpocznijGre()

    def noweOtwarcie(self):
        self.pokazOtwarcia.setupUi()

    def pokazOtwarcia(self):
        self.pokazOtwarcia.setupUi()
