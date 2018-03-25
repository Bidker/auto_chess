#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QWidget
from wyswietlenie_grafik.screen import rozpocznijGre
from PyQt5.QtCore import Qt
<<<<<<< HEAD
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

=======

class OknoGlowne(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
>>>>>>> c8849a5618a63435a98e92127312d4952823a0fd
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

<<<<<<< HEAD
=======
    def konfiguracjaOkna(self, tytulOkna):
          self.resize(793, 798)
          self.setWindowTitle(tytulOkna)


>>>>>>> c8849a5618a63435a98e92127312d4952823a0fd

if __name__ == '__main__':
    from okno_startowe.okno_startowe import OknoStartowe
    import sys

    surface = rozpocznijGre()

    aplikacja = QApplication(sys.argv)
<<<<<<< HEAD
    okno = OknoGlowne(surface)
=======
    okno = OknoStartowe()
>>>>>>> c8849a5618a63435a98e92127312d4952823a0fd
    okno.show()
    sys.exit(aplikacja.exec_())
