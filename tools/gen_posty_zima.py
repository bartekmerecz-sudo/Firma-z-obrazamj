#!/usr/bin/env python3
"""Szosta partia — styczen, luty, marzec 2027.

Kolejka konczyla sie 31 grudnia, a zaraz po swietach wypadaja dwie z najlepszych
okazji prezentowych w roku wlasnie dla obrazu ze zdjecia:

  * Dzien Babci i Dziadka (21-22 stycznia) — dziadkowie maja wszystko i niczego
    nie potrzebuja, wiec pamiatka bije kazdy przedmiot;
  * Walentynki (14 lutego) — wspolne zdjecie pary to dokladnie ten prezent.

Do tego Dzien Kobiet i luka postswiateczna, gdy ludzie maja jeszcze prezentowy
nastroj, ale juz nie maja pomyslow.

Posty sezonowe maja okna (czwarty element wpisu w content.py) i wchodza do
rotacji tylko w swoim terminie. Okno zaczyna sie na DWA TYGODNIE przed data —
przy realizacji 3-7 dni roboczych plus wysylka ktos, kto zobaczy post 20
stycznia, juz nie zdazy na 21.

Uzycie: python3 tools/gen_posty_zima.py [nazwa ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

from gen_posty_jesien import (W, H, CREAM, GOLD, ZLOTO_CIEMNE, font, center_ls,
                              base, brand, kicker, akapit, lista, cta,
                              headline, canvas_on_wall, paste_canvas, OUT, U)
from fonty import F_KICK, F_SUB


# Stopka z nazwa marki siedzi na stalej wysokosci H-132. Tekst musi skonczyc
# sie nad nia, inaczej podpis wchodzi na logo — przy pierwszym podejsciu
# wchodzil. Liczymy wiec uklad od dolu, a nie od gory.
STOPKA_Y = H - 160


def na_scianie(plik, kicker_txt, naglowek, podpis, wys=610, cy=540):
    """Wspolny uklad: obraz na scianie u gory, tekst pod nim.

    Posty czysto typograficzne czytaja sie dobrze, ale w kanale wygladaja jak
    cytaty. Co drugi sezonowy post pokazuje wiec sam produkt."""
    src = os.path.join(U, plik)
    bg = Image.new("RGB", (W, H), CREAM)
    if os.path.exists(src):
        bg = paste_canvas(bg, canvas_on_wall(src, 600, wys, 18), W // 2, cy)
    d = ImageDraw.Draw(bg, "RGBA")
    d.rectangle([44, 44, W - 45, H - 45], outline=(196, 162, 96, 190), width=3)
    center_ls(d, 128, kicker_txt, font(F_KICK, 38), ZLOTO_CIEMNE, 6)

    # Obraz musi zmiescic sie MIEDZY kickerem a tekstem. Przy pierwszym
    # podejsciu zachodzil raz na jedno, raz na drugie, wiec sprawdzamy oba
    # brzegi zamiast dobierac liczby na oko.
    gorny_brzeg_obrazu = cy - wys // 2 - 18
    assert gorny_brzeg_obrazu > 190, (
        f"obraz zaslania kicker: zaczyna sie na {gorny_brzeg_obrazu}")

    wys_naglowka = len(naglowek) * 66
    wys_podpisu = len(podpis) * 44
    y0 = STOPKA_Y - wys_naglowka - wys_podpisu - 14
    dolny_brzeg_obrazu = cy + wys // 2 + 18
    assert y0 > dolny_brzeg_obrazu, (
        f"tekst zachodzi na obraz: start {y0}, obraz konczy sie {dolny_brzeg_obrazu}")

    y = headline(d, y0, naglowek, 54)
    akapit(d, y + 14, podpis, 32, lh=44)
    brand(d)
    return bg


def p_dzien_babci():
    """Najsilniejsza okazja w calym roku dla tego produktu."""
    return na_scianie(
        "para4-szkic-clean.png", "21–22 STYCZNIA",
        ["Dziadkowie mają wszystko.", "Poza sobą na ścianie."],
        ["Stare zdjęcie ślubne, wakacje sprzed lat,",
         "Wy razem z nimi — zrobię z tego obraz.",
         "Zamów do 14 stycznia, żeby zdążyć."],
    ), "post-dzien-babci.png"


def p_walentynki():
    return na_scianie(
        "para3-olej-clean.png", "WALENTYNKI",
        ["Wasze zdjęcie.", "Nie kolejna maskotka."],
        ["Jedno wspólne zdjęcie jako obraz na płótnie.",
         "Projekt pokazuję przed drukiem.",
         "Zamów do 6 lutego, żeby zdążyć na czas."],
    ), "post-walentynki.png"


def p_po_swietach():
    """Luka postswiateczna: nastroj prezentowy jest, pomyslow juz nie."""
    bg, d = base(dark=True)
    kicker(d, 150, "PO ŚWIĘTACH", dark=True)
    headline(d, 262, ["Ile z tych", "prezentów", "jeszcze pamiętasz?"], 82, dark=True)
    akapit(d, 700, [
        "Świeca się wypaliła, czekolada zniknęła,",
        "skarpetki poszły do szuflady.",
        "",
        "Obraz z Waszego zdjęcia wisi dalej.",
        "W styczniu nie ma kolejki — realizuję od ręki.",
    ], 36, dark=True, lh=50)
    cta(d, 1010, "Wyślij zdjęcie", dark=True)
    brand(d, dark=True)
    return bg, "post-po-swietach.png"


def p_nowy_rok():
    bg, d = base()
    kicker(d, 150, "NOWY ROK")
    headline(d, 262, ["Pusta ściana", "to nie", "minimalizm."], 92)
    akapit(d, 640, [
        "To zwykle odkładanie na potem.",
        "",
        "Zdjęcie macie od dawna — leży w telefonie",
        "razem z czterema tysiącami innych.",
        "Brakuje tylko jednej decyzji.",
    ], 36, lh=50)
    cta(d, 1010, "Zacznij od jednego zdjęcia")
    brand(d)
    return bg, "post-nowy-rok.png"


def p_dzien_kobiet():
    return na_scianie(
        "para4-vangogh-clean.png", "8 MARCA",
        ["Kwiaty zwiędną", "do piątku."],
        ["Obraz z Waszego wspólnego zdjęcia zostanie.",
         "Mama, żona, siostra, babcia — każda z nich",
         "ma zdjęcie, które zasługuje na ścianę."],
    ), "post-dzien-kobiet.png"


def p_zimowe_wieczory():
    """Wypelniacz bez okna — musi dzialac przez caly kwartal."""
    bg, d = base()
    kicker(d, 150, "STYCZEŃ")
    headline(d, 262, ["Ciemno o 16:00.", "Ściana pusta", "od lat."], 88)
    y = lista(d, 620, [
        "Jedno zdjęcie z telefonu — wystarczy.",
        "Projekt pokazuję, zanim cokolwiek zapłacisz.",
        "Od zdjęcia do ściany 3–7 dni.",
    ], 36)
    akapit(d, y + 30, [
        "Zimą i tak siedzicie w domu.",
        "Niech będzie na co patrzeć.",
    ], 34, lh=46)
    brand(d)
    return bg, "post-zimowe-wieczory.png"


BUILDERS = [p_dzien_babci, p_walentynki, p_po_swietach,
            p_nowy_rok, p_dzien_kobiet, p_zimowe_wieczory]


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
