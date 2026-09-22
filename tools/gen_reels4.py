#!/usr/bin/env python3
"""Czwarta partia reelsow — kampania i sezony.

Wideo dowozi wyrazniej lepszy zasieg niz grafiki, wiec kolejka idzie teraz
w proporcji jeden do jednego i trzeba czym ja wypelnic. Ta partia nie dokłada
kolejnych filmow "o stylach" — kazdy ma za soba konkretna obietnice albo date:

  bold-projekt-dzis   rdzen kampanii: projekt tego samego dnia, za darmo
  bold-pabianice      lokalnie, z odbiorem osobistym
  bold-pierwszy       wprost o tym, ze firma nie ma jeszcze klientow
  bold-swieta         termin zamowien przed Wigilia
  bold-walentynki     14 lutego
  bold-dzien-babci    21-22 stycznia

Maszyneria (ciecia co ~1,5 s, napisy slowo po slowie, skok zoomu) jest ta sama
co w gen_reels3.py i stamtad importowana — filtr drawtext nie istnieje w tym
ffmpegu, wiec napisy renderuje PIL, a ffmpeg tylko je naklada.

Uzycie: python3 tools/gen_reels4.py [nazwa ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_reels3 import build, P, OUT


def reels():
    return {
    "bold-projekt-dzis": (
        [(P("para3-przed.jpg"), 1.4, "in"),
         (P("para3-olej-clean.png"), 1.5, "out"),
         (P("para3-witraz-clean.png"), 1.4, "in"),
         (P("para3-olej-clean.png"), 2.0, "out")],
        [("Wyślij zdjęcie rano", 0.2, 1.4, ("rano",)),
         ("Projekt zobaczysz wieczorem", 1.5, 3.0, ("wieczorem",)),
         ("Za darmo. Bez zaliczki", 3.1, 4.4, ("darmo",)),
         ("Nie spodoba się? Nie płacisz", 4.5, 6.3, ("nie",))]),

    "bold-pabianice": (
        [(P("para2-przed.jpg"), 1.4, "in"),
         (P("para2-komiks-clean.png"), 1.5, "out"),
         (P("para2-lego-clean.png"), 1.4, "in"),
         (P("para2-komiks-clean.png"), 2.0, "out")],
        [("Jestem z Pabianic", 0.2, 1.4, ("pabianic",)),
         ("Nie z hurtowni", 1.5, 2.9, ("hurtowni",)),
         ("Odbierzesz osobiście", 3.0, 4.4, ("osobiście",)),
         ("Obejrzysz, zanim zapłacisz", 4.5, 6.3, ("zanim",))]),

    "bold-pierwszy": (
        [(P("para1-przed.jpg"), 1.4, "in"),
         (P("para1-wektor-clean.png"), 1.5, "out"),
         (P("para1-bajka3d-clean.png"), 1.4, "in"),
         (P("para1-wektor-clean.png"), 2.1, "out")],
        [("Nikt u mnie jeszcze nie zamówił", 0.2, 1.7, ("nikt",)),
         ("Nie będę udawał", 1.8, 3.1, ("udawał",)),
         ("Pierwsze trzy za pół ceny", 3.2, 4.6, ("pół",)),
         ("Ktoś musi być pierwszy", 4.7, 6.4, ("pierwszy",))]),

    "bold-swieta": (
        [(P("para4-przed.jpg"), 1.4, "in"),
         (P("para4-vangogh-clean.png"), 1.5, "out"),
         (P("para4-szkic-clean.png"), 1.4, "in"),
         (P("para4-vangogh-clean.png"), 2.0, "out")],
        [("Do świąt zostało mniej niż myślisz", 0.2, 1.7, ("mniej",)),
         ("Zamówienia przyjmuję do 12 grudnia", 1.8, 3.3, ("grudnia",)),
         ("Potem nie zdążę", 3.4, 4.7, ("nie",)),
         ("Wolę powiedzieć teraz", 4.8, 6.3, ("teraz",))]),

    "bold-walentynki": (
        [(P("para3-przed.jpg"), 1.4, "in"),
         (P("para3-olej-clean.png"), 1.5, "out"),
         (P("para3-cyberpunk-clean.png"), 1.4, "in"),
         (P("para3-olej-clean.png"), 2.0, "out")],
        [("Znowu kupisz maskotkę", 0.2, 1.4, ("maskotkę",)),
         ("Albo pudełko czekoladek", 1.5, 2.9, ("czekoladek",)),
         ("Macie wspólne zdjęcie", 3.0, 4.4, ("wspólne",)),
         ("Powieście je na ścianie", 4.5, 6.3, ("ścianie",))]),

    "bold-dzien-babci": (
        [(P("para4-przed.jpg"), 1.5, "in"),
         (P("para4-szkic-clean.png"), 1.5, "out"),
         (P("para4-vangogh-clean.png"), 1.4, "in"),
         (P("para4-szkic-clean.png"), 2.0, "out")],
        [("Co kupić babci i dziadkowi", 0.2, 1.5, ("babci",)),
         ("Mają już wszystko", 1.6, 3.0, ("wszystko",)),
         ("Poza jednym", 3.1, 4.4, ("jednym",)),
         ("Sobą na ścianie", 4.5, 6.4, ("ścianie",))]),
    }


def main():
    chce = set(sys.argv[1:])
    n = 0
    for nazwa, args in reels().items():
        if chce and nazwa not in chce:
            continue
        build(nazwa, *args)
        n += 1
    print(f"\nGotowe: {n} filmow -> assets/video/")


if __name__ == "__main__":
    main()
