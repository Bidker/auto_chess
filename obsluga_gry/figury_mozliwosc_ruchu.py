from .figury_ruchy import RuchFigur

class FiguryMozliwoscRuchu(Object):
    def __init__(self):
        self.ruchFigury = RuchFigur()
        self.zajete_pola = stworzZajetePola()

    def stworzZajetePola(self):
        pola = []
        biale_figury = self.ruchFigury.pola_figur_w_trakcie_gry.get('biale')
        czarne_figury = self.ruchFigury.pola_figur_w_trakcie_gry.get('czarne')
        for figura in biale_figury.keys():
            pola.extend(biale_figury.get(figura))
            pola.extend(czarne_figury.get(figura))
        return pola

    def sprawdzMozliweRuchy(self, obiektBierki, pozycja, kolor):
        if 'pion' in obiektBierki.nazwa:
            return self.ruchDlaPiona(pozycja, obiektBierki)
        elif 'skoczek' in obiektBierki.nazwa:
            return self.ruchDlaSkoczka(pozycja, obiektBierki)
        elif 'goniec' in obiektBierki.nazwa:
            return self.ruchPoprzeczny(pozycja, obiektBierki)
        elif 'wieża' in obiektBierki.nazwa:
            return self.ruchKrzyzowy(pozycja, obiektBierki)
        elif 'hetman' in obiektBierki.nazwa:
            return self.ruchKrzyzowy(pozycja, obiektBierki).extend(self.ruchPoprzeczny(pozycja, obiektBierki))
        elif 'krol' in obiektBierki.nazwa:
            return self.ruchDlaKrola(kpozycja, obiektBierki)

    def ruchDlaPiona(self, pozycja, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchDlaSkoczka(self, pozycja, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchPoprzeczny(self, pozycja, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchKrzyzowy(self, pozycja, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruchDlaKrola(self, pozycja, obiektBierki):
        mozliwy_ruch = []
        return mozliwy_ruch
