#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget
from PyQt5.QtWidgets import QGridLayout, QPushButton
from wyswietlenie_grafik.screen import rozpocznijGre
from PyQt5.QtCore import Qt

class OknoGlowne(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def closeEvent(self, event):
        odpowiedz = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno opuścić program?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        self.sprawdzWyborWyjscia(odpowiedz, event)

    def keyPressEvent(self, wydarzenie):
        if wydarzenie.key() == Qt.Key_Escape:
            self.koniec()

    def sprawdzWyborWyjscia(self, odp, event):
        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def konfiguracjaOkna(self, tytulOkna):
          self.resize(793, 798)
          self.setWindowTitle(tytulOkna)



if __name__ == '__main__':
    from okno_startowe.okno_startowe import OknoStartowe
    import sys

    aplikacja = QApplication(sys.argv)
    okno = OknoStartowe()
    okno.show()
    sys.exit(aplikacja.exec_())
