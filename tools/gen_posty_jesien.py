#!/usr/bin/env python3
"""Czwarta partia postow — jesien / sezon prezentowy.

Kolejka na Facebooku miala do tej pory trzy rodzaje postow: metamorfozy
(PRZED -> PO), posty stylowe i posty zdejmujace obiekcje (cennik, bez ryzyka,
jak to dziala). Brakowalo czterech rzeczy, ktore realnie decyduja o zamowieniu:

  1. "ktore zdjecie sie nada"  — najczestszy powod, dla ktorego rozmowa umiera
  2. "kto to w ogole robi"     — jednoosobowa pracownia to atut, nie wstyd
  3. "co dokladnie dostane"    — plotno, blejtram, zawieszki; rzecz, nie plik
  4. sezon                     — swieta maja twardy termin zamowienia

Dwa posty maja okno sezonowe (patrz automation/content.py) i nie pojda
w rotacje przed listopadem.

Kontrast: zloto (196,162,96) na kremie to 1,98:1 — nie przechodzi nawet dla
duzego tekstu. Na ciemnym tle to 7,52:1 i jest w porzadku. Dlatego na kremie
uzywamy ciemniejszego ZLOTO_CIEMNE (5,15:1), a zloto zostaje na tle atramentowym
i w elementach czysto dekoracyjnych.

Uzycie: python3 tools/gen_posty_jesien.py [nazwa ...]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

import gen_sprzedaz as S
from gen_sprzedaz import (W, H, CREAM, INK, GOLD, font, text_ls, wrap,
                          center_ls, base, brand, rule, headline,
                          canvas_on_wall, paste_canvas, OUT, U)
from fonty import F_HEAD, F_KICK, F_SUB

ZLOTO_CIEMNE = (125, 90, 18)      # #7d5a12 — 5,15:1 na kremie
TRESC_KREM = (52, 46, 38)
TRESC_CIEMNA = (214, 208, 198)


def kicker(d, y, tekst, dark=False):
    """Napis kapitalikami nad naglowkiem — na kremie w ciemniejszym zlocie."""
    center_ls(d, y, tekst, font(F_KICK, 40),
              GOLD if dark else ZLOTO_CIEMNE, 6)
    rule(d, y + 64)


def akapit(d, y, linie, size=38, dark=False, x=None, lh=54):
    f = font(F_SUB, size)
    col = TRESC_CIEMNA if dark else TRESC_KREM
    for ln in linie:
        if x is None:
            tw = d.textlength(ln, font=f)
            d.text(((W - tw) // 2, y), ln, font=f, fill=col + (255,))
        else:
            d.text((x, y), ln, font=f, fill=col + (255,))
        y += lh
    return y


def lista(d, y, punkty, size=38, dark=False, x=150, odstep=66):
    """Punktowana lista ze zlota kropka."""
    f = font(F_SUB, size)
    col = TRESC_CIEMNA if dark else TRESC_KREM
    kropka = GOLD if dark else ZLOTO_CIEMNE
    for p in punkty:
        d.ellipse([x, y + 14, x + 18, y + 32], fill=kropka + (255,))
        d.text((x + 46, y), p, font=f, fill=col + (255,))
        y += odstep
    return y


def cta(d, y, tekst, dark=False):
    """Przycisk — na kremie atrament, na ciemnym zloto. Oba przechodza normy."""
    tlo = (196, 162, 96, 255) if dark else (24, 21, 18, 255)
    napis = (24, 21, 18, 255) if dark else (238, 232, 222, 255)
    d.rounded_rectangle([220, y, W - 220, y + 110], 10, fill=tlo)
    f = font(F_SUB, 40)
    d.text(((W - d.textlength(tekst, font=f)) // 2, y + 28), tekst, font=f, fill=napis)


# ------------------------------------------------------------------ POSTY

def p_ktore_zdjecie():
    """Najczestszy powod, dla ktorego rozmowa sie urywa: "chyba mam slabe zdjecie"."""
    bg, d = base()
    kicker(d, 140, "PORADNIK")
    headline(d, 250, ["Które zdjęcie", "się nada?"], 92)
    y = lista(d, 505, [
        "Zwykłe, z telefonu — wystarczy.",
        "Twarze wyraźne, nie z drugiego końca plaży.",
        "Ostre. Rozmazanego nie naprawię.",
        "Im większy plik, tym lepiej.",
    ])
    y = akapit(d, y + 24, [
        "Zrzut ekranu z Instagrama albo zdjęcie",
        "zdjęcia — to jedyne, co odpada.",
        "",
        "Nie wiesz, czy Twoje się nada?",
        "Wyślij — sprawdzę i powiem wprost.",
    ], 36)
    brand(d)
    return bg, "post-ktore-zdjecie.png"


def p_kto_to_robi():
    """Jednoosobowa pracownia — w tej branzy to przewaga, nie brak."""
    bg, d = base(dark=True)
    kicker(d, 150, "KTO TO ROBI", dark=True)
    headline(d, 262, ["Za tym nie stoi", "firma.", "Stoję ja."], 90, dark=True)
    akapit(d, 700, [
        "Jedna osoba, Pabianice. Sam odbieram",
        "wiadomości, sam robię projekt, sam pakuję.",
        "",
        "Dlatego odpisuję tego samego dnia",
        "i dlatego nie przyjmuję stu zamówień naraz.",
    ], 38, dark=True)
    cta(d, 1010, "Napisz do mnie", dark=True)
    brand(d, dark=True)
    return bg, "post-kto-to-robi.png"


def p_co_dostajesz():
    """Ludzie kupuja rzecz, nie plik. Warto powiedziec, co przyjdzie kurierem."""
    bg, d = base()
    kicker(d, 140, "CO DOSTAJESZ")
    headline(d, 250, ["To nie jest", "plik do druku."], 88)
    y = lista(d, 480, [
        "Płótno naciągnięte na drewniany blejtram.",
        "Boki zadrukowane — wygląda z każdej strony.",
        "Zawieszka z tyłu, gotowa na gwóźdź.",
        "Zapakowane tak, żeby przeżyło kuriera.",
    ], 36)
    akapit(d, y + 30, [
        "Wyjmujesz z kartonu i wieszasz.",
        "Nic nie trzeba dokupować.",
    ], 36)
    cta(d, 1010, "Wyślij zdjęcie")
    brand(d)
    return bg, "post-co-dostajesz.png"


def p_pies():
    """Segment, ktorego dotad w ogole nie zaczepialismy.

    Swiadomie bez zdjecia obrazu: nie mam jeszcze ani jednego psa w portfolio,
    a podpisanie ludzkiego portretu naglowkiem o psach byloby scinaniem zakretu.
    Brak przykladu zamieniamy w powod, zeby ktos sie odezwal pierwszy.
    """
    bg, d = base(dark=True)
    kicker(d, 150, "NIE TYLKO LUDZIE", dark=True)
    headline(d, 262, ["Psa też zrobię.", "Kota też."], 92, dark=True)
    akapit(d, 620, [
        "Olej, szkic, komiks, klocki — każdy styl",
        "działa tak samo jak na portrecie.",
    ], 38, dark=True)
    akapit(d, 780, [
        "Uczciwie: nie mam jeszcze żadnego",
        "zwierzaka w portfolio. Pierwsze trzy",
        "robię za pół ceny — w zamian proszę",
        "o zdjęcie obrazu na Waszej ścianie.",
    ], 36, dark=True, lh=50)
    cta(d, 1010, "Napisz: PIES", dark=True)
    brand(d, dark=True)
    return bg, "post-pies.png"


def p_ile_trwa():
    """Obiekcja czasowa — i jednoczesnie przygotowanie gruntu pod swieta."""
    bg, d = base()
    kicker(d, 140, "ILE TO TRWA")
    headline(d, 250, ["Od zdjęcia", "do ściany:", "3–7 dni."], 92)
    kroki = [("24 h", "Pokazuję projekt"),
             ("1–2 dni", "Poprawki, jeśli trzeba"),
             ("2–4 dni", "Druk i wysyłka")]
    fn, ft = font(F_HEAD, 52), font(F_SUB, 40)
    y = 690
    for ile, co in kroki:
        d.text((176, y - 4), ile, font=fn, fill=ZLOTO_CIEMNE + (255,))
        d.text((420, y + 6), co, font=ft, fill=(24, 21, 18, 255))
        y += 108
        d.line([(176, y - 22), (W - 176, y - 22)], fill=(24, 21, 18, 45), width=1)
    akapit(d, y + 10, ["Zegar rusza, gdy przyjdzie zdjęcie.",
                       "Nie wcześniej."], 34, lh=46)
    brand(d)
    return bg, "post-ile-trwa.png"


def p_swieta_termin():
    """Sezonowy — okno listopad/grudzien. Termin robi z checi decyzje."""
    bg, d = base(dark=True)
    kicker(d, 150, "ŚWIĘTA", dark=True)
    headline(d, 262, ["Zamów do", "12 grudnia."], 96, dark=True)
    akapit(d, 640, [
        "Potem nie zdążę zrobić projektu,",
        "przyjąć poprawek i wydrukować",
        "przed Wigilią. Wolę powiedzieć teraz",
        "niż obiecać i nie dowieźć.",
    ], 38, dark=True)
    akapit(d, 900, ["Grudzień to jedyny miesiąc,",
                    "w którym zamykam listę wcześniej."], 34, dark=True, lh=46)
    cta(d, 1010, "Napisz: ŚWIĘTA", dark=True)
    brand(d, dark=True)
    return bg, "post-swieta-termin.png"


def p_dwa_obrazy():
    """Podbija wartosc zamowienia — dwa mniejsze zamiast jednego duzego."""
    a = os.path.join(U, "para3-olej-clean.png")
    b = os.path.join(U, "para4-szkic-clean.png")
    bg = Image.new("RGB", (W, H), CREAM)
    if os.path.exists(a) and os.path.exists(b):
        bg = paste_canvas(bg, canvas_on_wall(a, 380, 470, 14), 320, 520)
        bg = paste_canvas(bg, canvas_on_wall(b, 380, 470, 14), 760, 560)
    d = ImageDraw.Draw(bg, "RGBA")
    d.rectangle([44, 44, W - 45, H - 45], outline=(196, 162, 96, 190), width=3)
    center_ls(d, 128, "DWA ZAMIAST JEDNEGO", font(F_KICK, 38), ZLOTO_CIEMNE, 6)
    headline(d, 900, ["Dwa mniejsze obrazy", "robią ze ściany galerię."], 54)
    akapit(d, 1042, [
        "Dwa razy 30×40 to 258 zł — i darmowa dostawa.",
        "Możesz dać jedno zdjęcie w dwóch stylach",
        "albo dwa różne zdjęcia obok siebie.",
    ], 32, lh=46)
    brand(d)
    return bg, "post-dwa-obrazy.png"


def p_rocznica():
    """Jesien to sezon rocznic slubu — inny hak niz sam 'prezent'."""
    bg, d = base(dark=True)
    kicker(d, 150, "ROCZNICA", dark=True)
    headline(d, 262, ["Zdjęcie ze ślubu", "leży w pudełku", "od dwudziestu lat."], 80, dark=True)
    akapit(d, 720, [
        "Zeskanuj je telefonem i wyślij.",
        "Odtworzę je jako obraz na płótnie —",
        "tym razem na ścianie, nie w szafie.",
        "",
        "Stare i podniszczone też przyjmuję.",
    ], 38, dark=True)
    cta(d, 1010, "Wyślij zdjęcie", dark=True)
    brand(d, dark=True)
    return bg, "post-rocznica.png"


BUILDERS = [p_ktore_zdjecie, p_kto_to_robi, p_co_dostajesz, p_pies,
            p_ile_trwa, p_swieta_termin, p_dwa_obrazy, p_rocznica]


def main():
    chce = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    zrobione = 0
    for b in BUILDERS:
        img, name = b()
        if chce and name not in chce and b.__name__ not in chce:
            continue
        img.save(os.path.join(OUT, name), quality=95)
        print("  +", name)
        zrobione += 1
    print(f"\nGotowe: {zrobione} postow -> assets/social/")


if __name__ == "__main__":
    main()
