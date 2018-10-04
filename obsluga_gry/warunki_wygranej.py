from .figury_ruchy import RuchFigur

ruchFigury = RuchFigur()


def sprawdzWarunkiWygranej(kolor):
    wszystkie_figury_koloru = ruchFigury.pola_figur_w_trakcie_gry.get(kolor)
    krol_koloru = wszystkie_figury_koloru.get('krol')
