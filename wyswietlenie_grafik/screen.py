from livewires import games
from .tworzenie_figur import pokaz_figury

def rozpocznijGre():
    games.init(screen_width = 793, screen_height = 798, fps = 50)
    wall_image = games.load_image("Grafiki/chess.jpg", False)

    pokaz_figury()
    games.screen.background = wall_image

    games.screen.mainloop()
