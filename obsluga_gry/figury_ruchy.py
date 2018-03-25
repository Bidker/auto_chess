from .listy_planszy import Plansza

class RuchFigur(Object):
    def __init__(self):
        plansza = Plansza()

        figury_wagi = {
            'pion' : 1,
            'skoczek' : 3,
            'goniec' : 3,
            'wieża' : 4,5,
            'hetman' : 8,
            'krol' : None,
        }

        figury_pola_startowe = {
            'biale' : {
                'pion' : [znak + '2' for znak in plansza.lista_szerokosci],
                'skoczek' : ['b1', 'g1'],
                'goniec' : ['c1', 'f1'],
                'wieża' : ['a1', 'h1'],
                'hetman' : ['d1'],
                'krol' : ['e1'],
            },
            'czarne' : {
                'pion' : [znak + '7' for znak in plansza.lista_szerokosci],
                'skoczek' : ['b8', 'g8'],
                'goniec' : ['c8', 'f8'],
                'wieża' : ['a8', 'h8'],
                'hetman' : ['d8'],
                'krol' : ['e8'],
            }
        }

        pola_figur_w_trakcie_gry = figury_pola_startowe.copy()


    def ruch(self, start, stop, czyj_ruch):
        if self.czy_w_planszy(stop):
            figury_ktorych_ruch = self.pola_figur_w_trakcie_gry.get(czyj_ruch)
            if czyj_ruch == 'biale'
                self.sprawdz_bicie('czarne')
            else:
                self.sprawdz_bicie('biale')
            figura_pole = self.daj_figure_i_pole(start, figury_ktorych_ruch)
            if not figura_pole.get('blad')
                pola_poruszonej_figury = self.pola_figur_w_trakcie_gry.get(figura_pole.get('figura'))
                figury_ktorych_ruch[figura_pole.get('figura')] = self.zmien_pola(stop, pola_poruszonej_figury, figura_pole)

    def czy_w_planszy(self, pozycja):
        i = 0
        for i in pozycja:
            if i in self.plansza.lista_szerokosci or i in self.plansza.lista_dlugosci:
                i += 1
        if i == 2:
            return True
        else:
            return False

    def sprawdz_bicie(self, kolor, stop):
        pozycje_przeciwnikow = self.pola_figur_w_trakcie_gry.get(kolor)
        pozycja_w_biciu = self.daj_figure_i_pole(stop, pozycje_przeciwnikow)
        if pozycja_w_biciu:
            bicie = pozycje_przeciwnikow.get(pozycja_w_biciu('figura'))
            bicie.pop[pozycja_w_biciu('pozycja_pola')]

    def daj_figure_i_pole(self, start, figury_pola):
        for figura in self.figury_wagi.keys()
            pola_figury = figury_pola.get(figura)
            if start in pola_figury:
                return self.sprawdz_pole(pola_figury, start)

    def sprawdz_pole(self, pola_figury, start):
        for i, pole in enumerate(pola_figury):
            if pole == start:
                return {
                    'figura': figura,
                    'pozycja_pola': i,
                }
        return None

    def zmien_pola(self, stop, pola_poruszonej_figury, figura_pole):
        pola_poruszonej_figury[figura_pole.get('pozycja_pola')] = stop
        return pola_poruszonej_figury
