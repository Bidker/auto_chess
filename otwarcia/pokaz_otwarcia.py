# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from funkcje_wyswietlania import konfiguracjaOkna

class PokazOtwarcia(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        # tabelaryczny widok danych
        self.widok = QTableView()

        # główny układ okna ###
        ukladV = QVBoxLayout(self)
        ukladV.addWidget(self.widok)

        # właściwości widżetu ###
        konfiguracjaOkna(self, "Księga otwarć")
