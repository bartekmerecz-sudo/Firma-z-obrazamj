#!/usr/bin/env python3
"""Piata partia — kampania "pierwszy klient".

Od lipca poszlo ponad piecdziesiat postow i nie ma ani jednego zamowienia.
Dosypywanie kolejnych postow o stylach tego nie odwroci, bo problem nie lezy
w tresci, tylko w zasiegu i w braku powodu, zeby napisac WLASNIE TERAZ.

Te trzy posty sa zbudowane wokol jednej rzeczy, ktorej wczesniej nie bylo:
pracownia dziala, wiec projekt da sie pokazac tego samego dnia. To zamienia
mgliste "napisz do mnie" w konkretna obietnice z terminem.

  1. darmowy projekt dzis   — obietnica, ktora teraz da sie dotrzymac
  2. Pabianice              — lokalnie, z odbiorem osobistym
  3. pierwszy klient        — uczciwie o tym, ze jeszcze nikogo nie bylo

Post nr 3 mowi wprost, ze firma nie ma jeszcze klientow. To brzmi ryzykownie,
ale alternatywa jest gorsza: udawanie dorobku, ktorego nie ma, konczy sie
zmyslonymi opiniami — a tych nie wystawiamy.

Uzycie: python3 tools/gen_posty_start.py [nazwa ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_posty_jesien import (W, H, GOLD, ZLOTO_CIEMNE, font, center_ls,
                              base, brand, kicker, akapit, lista, cta,
                              headline, OUT)
from fonty import F_KICK, F_SUB


def p_darmowy_projekt():
    """Rdzen kampanii. Pracownia pozwala dotrzymac terminu 'dzis'."""
    bg, d = base(dark=True)
    kicker(d, 150, "BEZ ZALICZKI", dark=True)
    headline(d, 262, ["Wyślij zdjęcie", "rano —", "projekt zobaczysz", "wieczorem."], 76, dark=True)
    akapit(d, 720, [
        "Za darmo. Bez zamówienia, bez zaliczki,",
        "bez zobowiązania.",
        "",
        "Spodoba się — drukuję. Nie spodoba się —",
        "rozchodzimy się i nic nie płacisz.",
    ], 36, dark=True, lh=50)
    cta(d, 1010, "Napisz: PROJEKT", dark=True)
    brand(d, dark=True)
    return bg, "post-darmowy-projekt.png"


def p_pabianice():
    """Lokalnie. Jednoosobowa pracownia bez opinii wygrywa najpierw u sasiadow."""
    bg, d = base()
    kicker(d, 150, "PABIANICE I OKOLICE")
    headline(d, 262, ["Jestem stąd.", "Możesz odebrać", "osobiście."], 86)
    y = lista(d, 620, [
        "Bez kuriera i bez czekania na paczkę.",
        "Obraz obejrzysz na żywo przed zapłatą.",
        "Łódź i okolice — dowiozę sam.",
    ], 36)
    akapit(d, y + 30, [
        "Prezent na ostatnią chwilę? Lokalnie",
        "da się zdążyć tam, gdzie kurier już nie.",
    ], 34, lh=46)
    cta(d, 1010, "Napisz do mnie")
    brand(d)
    return bg, "post-pabianice.png"


def p_pierwszy_klient():
    """Uczciwie o braku dorobku. Zamiast udawac — zaproponowac uklad."""
    bg, d = base()
    kicker(d, 150, "SZCZERZE")
    headline(d, 262, ["Nikt u mnie", "jeszcze nie", "zamówił."], 92)
    akapit(d, 640, [
        "Ruszyłem niedawno i nie mam się czym",
        "pochwalić — poza tym, co sam zrobiłem.",
        "",
        "Więc proponuję układ: pierwsze trzy obrazy",
        "robię za pół ceny. W zamian proszę o zdjęcie",
        "gotowego obrazu na Waszej ścianie",
        "i szczerą opinię — także jeśli będzie kiepska.",
    ], 34, lh=48)
    cta(d, 1030, "Napisz: PIERWSZY")
    brand(d)
    return bg, "post-pierwszy-klient.png"


BUILDERS = [p_darmowy_projekt, p_pabianice, p_pierwszy_klient]


def main():
    chce = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for b in BUILDERS:
        img, nazwa = b()
        if chce and nazwa not in chce:
            continue
        img.save(os.path.join(OUT, nazwa), quality=95)
        print("  +", nazwa)
        n += 1
    print(f"\nGotowe: {n} postow -> assets/social/")


if __name__ == "__main__":
    main()
