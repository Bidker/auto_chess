from .figury_ruchy import RuchFigur

class FiguryMozliwoscRuchu(Object):
    def __init__(self):
        ruchFigury = RuchFigury()
        zajete_pola = stworz_zajete_pola()

    def stworz_zajete_pola(self):
        pola = []
        biale_figury = self.ruchFigury.pola_figur_w_trakcie_gry.get('biale')
        czarne_figury = self.ruchFigury.pola_figur_w_trakcie_gry.get('czarne')
        for figura in biale_figury.keys():
            pola.extend(biale_figury.get(figura))
            pola.extend(czarne_figury.get(figura))
        return pola

    def sprawdz_mozliwe_ruchy(self, figura, pozycja, kolor):
        return self.sprawdz_mozliwe_ruchy_dla_figury(figura, pozycja, kolor)

    def sprawdz_mozliwe_ruchy_dla_figury(self, figura, pozycja, kolor):
        if figura == 'pion':
            return self.ruch_dla_piona(pozycja, kolor)
        elif figura == 'skoczek':
            return self.ruch_dla_skoczka(pozycja)
        elif figura == 'goniec':
            return self.ruch_poprzeczny(pozycja)
        elif figura == 'wieża':
            return self.ruch_krzyzowy(pozycja)
        elif figura == 'hetman':
            return self.ruch_krzyzowy(pozycja).extend(self.ruch_poprzeczny(pozycja))
        elif figura == 'krol':
            return self.ruch_dla_krola(kpozycja, kolor)

    def ruch_dla_piona(self, kolor, pozycja):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruch_dla_skoczka(self, pozycja):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruch_poprzeczny(self, pozycja):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruch_krzyzowy(self, pozycja):
        mozliwy_ruch = []
        return mozliwy_ruch

    def ruch_dla_krola(self, kolor, pozycja):
        mozliwy_ruch = []
        return mozliwy_ruch
