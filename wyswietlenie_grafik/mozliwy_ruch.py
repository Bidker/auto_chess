from livewires import games

from obsluga_gry.listy_planszy import Plansza

class MozliwyRuch(games.Sprite):
    ikona = 'wyswietlenie_grafik/Grafiki/podswietlenie.jpg'

    def __init__(self, iks, igreg):
        self.pozycja_x = iks
        self.pozycja_y = igreg
        self.wybrane = False
        self.podswietlPole()

    def podswietlPole(self):
        obraz = games.load_image(MozliwyRuch.ikona, False)
        super(MozliwyRuch, self).__init__(
            image = obraz,
            x = self.pozycja_x,
            y = self.pozycja_y
        )
