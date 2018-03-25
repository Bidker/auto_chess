# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from main import OknoGlowne

class PokazOtwarcia(OknoGlowne):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        # tabelaryczny widok danych
        self.widok = QTableView()

        # główny układ okna ###
        ukladV = QVBoxLayout(self)
        ukladV.addWidget(self.widok)
        sel.show()
