#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QWidget
from wyswietlenie_grafik.screen import rozpocznijGre
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class ImageWidget(QWidget):
    def __init__(self, surface, parent=None):
        super(ImageWidget,self).__init__(parent)
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QtGui.QImage(self.data, w, h, QtGui.QImage.Format_RGB32)

class OknoGlowne(QMainWindow):
    def __init__(self,surface,parent=None):
        super(OknoGlowne, self).__init__(parent)
        self.setCentralWidget(ImageWidget(surface))

    def interfejs(self, surface):
        self.konfiguracjaOkna('Auto-chess by Bida', surface)
        rozpocznijGre()
        self.stworzMenu()

    def konfiguracjaOkna(self, tytulOkna, surface):
        w = surface.get_width()
        h = surface.get_height()
        self.image = QtGui.QImage(self.data, w, h, QtGui.QImage.Format_RGB32)
        self.setWindowTitle(tytulOkna)

    def stworzMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Otwarcia')
        helpMenu = mainMenu.addMenu('&Pomoc')

    def closeEvent(self, event):
        odpowiedz = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno opuścić program?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        self.sprawdzWyborWyjscia(odpowiedz, event)

    def keyPressEvent(self, wydarzenie):
        if wydarzenie.key() == Qt.Key_Escape:
            self.koniec()

    def koniec(self):
        self.close()

    def sprawdzWyborWyjscia(self, odp, event):
        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    import sys

    surface = rozpocznijGre()

    aplikacja = QApplication(sys.argv)
    okno = OknoGlowne(surface)
    okno.show()
    sys.exit(aplikacja.exec_())
