#!/usr/bin/env python3
"""Druga partia reelsow — inne KATY, nie kolejne style.

Pierwsza partia (gen_reels.py) pokazywala metamorfozy: zdjecie -> obraz.
Osiem filmow zbudowanych na tym samym schemacie zaczyna wygladac tak samo,
a TikTok karze powtarzalnosc mocniej niz slaba jakosc. Ta partia dokłada
katy, ktorych tam nie bylo: obiekcja, poradnik, porownanie, proces, okazja.

Dwie nowe sceny lamia rytm poprzedniej serii:
  * text_card — plansza tekstowa, mocne otwarcie bez zdjecia,
  * split     — przed i po jednoczesnie, jedno pod drugim, bez przejscia.

Zasady te same co w gen_reels.py: bez adresu strony w kadrze, tekst tylko
w strefie bezpiecznej, zakonczenie pytaniem. Zrodla z uploads/final/,
czyli po usunieciu znaku wodnego.

Uzycie: python3 tools/gen_reels2.py [nazwa ...]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_reels import (  # noqa: E402
    W, H, SAFE_TOP, SAFE_BOT, CREAM, INK, GOLD, F_HEAD, F_KICK, F_SUB,
    U, font, wrap, center_ls, build, photo, wall, grid, end_card, pill,
)


def text_card(lines, kicker=None, dark=True):
    """Plansza tekstowa. Otwiera film bez zdjecia — inny rytm niz reszta serii."""
    bg, fg = (INK, (242, 238, 231)) if dark else (CREAM, (26, 23, 20))
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([50, 50, W - 51, H - 51], outline=GOLD + (200,), width=3)
    y = SAFE_TOP + 260
    if kicker:
        center_ls(d, y, kicker.upper(), font(F_KICK, 42), GOLD + (255,), 6)
        y += 120
    fh = font(F_HEAD, 96)
    for raw in lines:
        for ln in wrap(d, raw, fh, W - 200):
            x = (W - d.textlength(ln, font=fh)) // 2
            d.text((x, y), ln, font=fh, fill=fg + (255,))
            y += 108
        y += 18
    return im


def split(before_path, after_path, hook=None):
    """Przed i po jednoczesnie, jedno pod drugim. Bez przejscia — cale
    porownanie widac w jednej klatce, wiec dziala nawet przy szybkim scrollu."""
    im = Image.new("RGB", (W, H), CREAM)
    px = im.load()
    for y in range(H):
        t = y / H
        val = (int(238 - 26 * t), int(232 - 28 * t), int(222 - 30 * t))
        for x in range(W):
            px[x, y] = val
    d = ImageDraw.Draw(im, "RGBA")

    top = SAFE_TOP + (150 if hook else 40)
    ph = (SAFE_BOT - top - 26) // 2
    pw = W - 150
    for i, (p, lab) in enumerate(((before_path, "ZDJĘCIE"), (after_path, "OBRAZ"))):
        art = ImageOps.fit(Image.open(p).convert("RGB"), (pw, ph), method=Image.LANCZOS)
        y0 = top + i * (ph + 26)
        im.paste(art, (75, y0))
        d.rectangle([75, y0, 75 + pw - 1, y0 + ph - 1], outline=(210, 202, 190, 255), width=1)
        f = font(F_KICK, 36)
        tw = d.textlength(lab, font=f) + 52
        d.rounded_rectangle([90, y0 + 16, 90 + tw, y0 + 74], 29, fill=(20, 18, 16, 205))
        d.text((116, y0 + 28), lab, font=f, fill=CREAM + (255,))

    if hook:
        fh = font(F_HEAD, 86)
        y = SAFE_TOP + 20
        for ln in wrap(d, hook, fh, W - 180):
            x = (W - d.textlength(ln, font=fh)) // 2
            d.text((x, y), ln, font=fh, fill=(26, 23, 20, 255))
            y += 96
    return im


def reels():
    return {
    # 9. Obiekcja — najczestsze pytanie w wiadomosciach, wiec i najlepszy hook.
    "reel-a-jak-sie-nie-spodoba": (
        [text_card(["„A jak mi się", "nie spodoba?"], kicker="Pytacie o to najczęściej"),
         photo(f"{U}/para3-przed.jpg", label="1. WYSYŁASZ ZDJĘCIE"),
         photo(f"{U}/para3-olej-clean.png", label="2. POKAZUJĘ PROJEKT"),
         text_card(["Nie spodoba się —", "nie płacisz."], dark=False),
         end_card("Co byś wysłał?", "Napisz w komentarzu.")],
        [2.8, 2.2, 2.4, 2.6, 2.6], ["fade", "wipeleft", "fade", "fade"],
        [None, "in", "out", None, None]),

    # 10. Poradnik — format najczesciej zapisywany, a zapisy licza sie
    # w rankingu wyzej niz polubienia.
    "reel-jakie-zdjecie": (
        [text_card(["Jakie zdjęcie", "się nadaje?"], kicker="Zanim wyślesz"),
         photo(f"{U}/para3-przed.jpg", label="OSTRE, DOBRE ŚWIATŁO"),
         photo(f"{U}/para1-przed.jpg", label="TWARZE DOBRZE WIDOCZNE"),
         photo(f"{U}/para3-olej-clean.png", label="I TAKI WYCHODZI EFEKT"),
         end_card("Masz takie zdjęcie?", "Napisz, co byś wybrał.")],
        [2.6, 2.4, 2.4, 2.6, 2.6], ["fade", "fade", "fade", "fade"],
        [None, "in", "out", "in", None]),

    # 11. Stare zdjecia — inna grupa docelowa niz pary: dzieci szukajace
    # prezentu dla rodzicow i dziadkow.
    "reel-stare-zdjecie": (
        [photo(f"{U}/para4-przed.jpg", hook="Zdjęcia z albumu\nzostają w albumie."),
         split(f"{U}/para4-przed.jpg", f"{U}/para4-szkic-clean.png"),
         wall(f"{U}/para4-szkic-clean.png"),
         end_card("Masz takie zdjęcie\nw szufladzie?", "Napisz w komentarzu.")],
        [3.0, 3.2, 2.6, 2.8], ["fade", "fade", "fade"], ["in", None, "in", None]),

    # 12. Porownanie — atakuje realna alternatywe (plakat z sieciowki),
    # a nie konkurencje. Latwiejszy przekaz niz "jestesmy lepsi".
    "reel-plakat-vs-obraz": (
        [text_card(["Plakat z sieciówki", "wisi u trzech", "znajomych."]),
         grid([f"{U}/para3-olej-clean.png", f"{U}/para3-witraz-clean.png",
               f"{U}/para3-wektor-clean.png", f"{U}/para3-cyberpunk-clean.png"],
              caption="Twoje zdjęcie · cztery style"),
         text_card(["Twój obraz", "nie wisi u nikogo."], dark=False),
         end_card("Które byś powiesił?", "Napisz numer w komentarzu.")],
        [2.8, 4.0, 2.6, 2.6], ["fade", "fade", "fade"], [None, None, None, None]),

    # 13. Poradnik wnetrzarski — trafia do ludzi, ktorzy urzadzaja dom,
    # a nie szukaja prezentu. Inna intencja, inna widownia.
    "reel-do-jakiego-wnetrza": (
        [text_card(["Jaki styl", "do jakiego wnętrza?"], kicker="Ściągawka"),
         wall(f"{U}/para3-olej-clean.png", caption="Do salonu — olej"),
         wall(f"{U}/para3-wektor-clean.png", caption="Do biura — wektor"),
         wall(f"{U}/para3-cyberpunk-clean.png", caption="Do pokoju nastolatka"),
         end_card("Jaką masz ścianę?", "Opisz w komentarzu, podpowiem styl.")],
        [2.6, 2.4, 2.4, 2.4, 2.8], ["fade", "fade", "fade", "fade"],
        [None, "in", "out", "in", None]),

    # 14. Proces — pokazuje, ze za obrazem stoi czlowiek, a nie automat.
    "reel-proces": (
        [photo(f"{U}/para1-przed.jpg", hook="Co się dzieje\npo wysłaniu\nzdjęcia?"),
         split(f"{U}/para1-przed.jpg", f"{U}/para1-bajka3d-clean.png"),
         wall(f"{U}/para1-bajka3d-clean.png", caption="I ląduje u Ciebie na ścianie"),
         end_card("Chcesz zobaczyć\nswoje zdjęcie?", "Napisz w komentarzu.")],
        [3.0, 3.2, 2.6, 2.8], ["fade", "fade", "fade"], ["in", None, "in", None]),

    # 15. Okazja — urodziny wypadaja caly rok, wiec film nie traci aktualnosci
    # jak wakacje czy sezon slubny.
    "reel-urodziny": (
        [text_card(["Urodziny za tydzień.", "Znowu perfumy?"]),
         photo(f"{U}/para2-przed.jpg", label="ICH ZDJĘCIE"),
         photo(f"{U}/para2-komiks-clean.png", label="PO · KOMIKS"),
         wall(f"{U}/para2-komiks-clean.png"),
         end_card("Komu kupujesz\nw tym miesiącu?", "Oznacz tę osobę.")],
        [2.6, 2.2, 2.4, 2.6, 2.8], ["fade", "wipeleft", "fade", "fade"],
        [None, "in", "out", "in", None]),

    # 16. Obiekcja cenowa — mowi o cenie bez pokazywania cennika w kadrze,
    # bo plansza z cenami czyta sie jak reklama.
    "reel-ile-kosztuje": (
        [text_card(["„Pewnie kosztuje", "majątek."], kicker="Druga obiekcja"),
         split(f"{U}/para3-przed.jpg", f"{U}/para3-witraz-clean.png"),
         text_card(["Tyle, co porządna", "kolacja we dwoje.", "Tylko zostaje", "na lata."], dark=False),
         end_card("Zgadnij, ile.", "Napisz kwotę w komentarzu 👇")],
        [2.8, 3.2, 3.2, 2.6], ["fade", "fade", "fade"], [None, None, None, None]),
    }


def main():
    want = set(sys.argv[1:])
    made = 0
    for name, args in reels().items():
        if want and name not in want:
            continue
        build(name, *args)
        made += 1
    print(f"\nGotowe: {made} filmow -> assets/video/")


if __name__ == "__main__":
    main()
