#!/usr/bin/env python3
"""Jedno miejsce, w ktorym szukamy fontow Quiet Heirloom.

Sciezka do katalogu z fontami byla wpisana na sztywno w pieciu generatorach
naraz. Kiedy skill canvas-design zmienil lokalizacje, wszystkie piec przestalo
dzialac tego samego dnia i trzeba bylo poprawiac je pojedynczo. Dlatego teraz
kazdy generator importuje FONTS stad, a lista kandydatow jest jedna.
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Font, po ktorym poznajemy, ze katalog jest tym wlasciwym.
PROBKA = "Gloock-Regular.ttf"

KANDYDACI = [
    os.environ.get("CANVAS_FONTS", ""),          # awaryjnie: wskaz recznie
    "/mnt/skills/examples/canvas-design/canvas-fonts",
    "/root/.claude/skills/canvas-design/canvas-fonts",
    os.path.join(ROOT, ".claude", "skills", "canvas-design", "canvas-fonts"),
    os.path.join(ROOT, "assets", "fonts"),
]


def znajdz_fonty():
    kand = [k for k in KANDYDACI if k]
    kand += sorted(glob.glob("/root/.claude/skills/*/canvas-design/canvas-fonts"))
    kand += sorted(glob.glob("/mnt/skills/*/canvas-design/canvas-fonts"))
    for k in kand:
        if os.path.exists(os.path.join(k, PROBKA)):
            return k
    raise SystemExit(
        "Nie znalazlem fontow canvas-design (szukam " + PROBKA + ").\n"
        "Sprawdzone sciezki:\n  " + "\n  ".join(kand) + "\n"
        "Mozesz wskazac katalog recznie: CANVAS_FONTS=/sciezka python3 tools/...")


FONTS = znajdz_fonty()

F_HEAD = os.path.join(FONTS, "Gloock-Regular.ttf")     # naglowki, serif
F_KICK = os.path.join(FONTS, "ArsenalSC-Regular.ttf")  # kickery, kapitaliki
F_SUB = os.path.join(FONTS, "Outfit-Regular.ttf")      # tresc, bezszeryfowy
F_BOLD = os.path.join(FONTS, "BigShoulders-Bold.ttf")  # napisy na wideo

if __name__ == "__main__":
    print(FONTS)
