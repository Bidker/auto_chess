from livewires import games
from .tworzenie_figur import pokaz_figury

def rozpocznijGre():
    games.init(screen_width = 793, screen_height = 798, fps = 50)
    wall_image = games.load_image("wyswietlenie_grafik/Grafiki/chess.jpg", False)

    games.screen.background = wall_image
    obiekty_bierek = pokaz_figury(games)

    games.screen.mainloop()
