#!/usr/bin/env python3
"""Usuwa znak wodny generatora z renderow w assets/uploads/.

Problem: kazdy render ma w prawym dolnym rogu polprzezroczysta gwiazdke
(znak wodny Gemini), a para1-wektor dodatkowo wklejona pieczatke
"MODERN VECTOR / AV / ART PRINT" — obce logo, ktore nie jest nasze.
Na materiale sprzedazowym oba podwazaja wiarygodnosc.

Rozwiazanie: przyciecie dolnego pasa. Sprawdzone na wszystkich 20 plikach —
kazdy znak miesci sie w dolnych 250 px, wiec przyciecie CROP_BOTTOM usuwa go
niezaleznie od tla. Inpainting dawalby lepszy kadr, ale wykrycie gwiazdki
zawodzi na teksturach (pociagniecia pedzla, witraz), a niewykryty znak
na opublikowanym poscie kosztuje wiecej niz 10% wysokosci kadru.

Wejscie:  assets/uploads/*.png        (nietkniete, zostaja jako archiwum)
Wyjscie:  assets/uploads/final/*.png  (z tego generuja galerie i reelsy)

Skrypt jest idempotentny — czyta zawsze z oryginalow, nie z wlasnego wyjscia.

Uzycie: python3 tools/strip_watermark.py
"""
import os
import glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "uploads")
OUT = os.path.join(SRC, "final")

CROP_BOTTOM = 250   # px; zmierzone — najnizej polozony znak konczy sie ~220 px od dolu


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob(os.path.join(SRC, "*.png")))
    if not files:
        print("Brak plikow PNG w", SRC)
        return

    for f in files:
        name = os.path.basename(f)
        im = Image.open(f).convert("RGB")
        w, h = im.size
        if h <= CROP_BOTTOM + 100:
            print(f"  POMINIETO {name} — za niski ({h} px)")
            continue
        out = im.crop((0, 0, w, h - CROP_BOTTOM))
        p = os.path.join(OUT, name)
        out.save(p, "PNG", optimize=True)
        print(f"  {name:30} {w}x{h} -> {out.size[0]}x{out.size[1]}")

    # zdjecia zrodlowe (przed) sa prawdziwymi fotografiami — bez znaku wodnego,
    # kopiujemy bez zmian, zeby generatory czytaly wszystko z jednego katalogu
    for f in sorted(glob.glob(os.path.join(SRC, "*-przed.jpg"))):
        name = os.path.basename(f)
        Image.open(f).convert("RGB").save(
            os.path.join(OUT, name), "JPEG", quality=92, optimize=True
        )
        print(f"  {name:30} skopiowane bez zmian (fotografia, brak znaku)")

    print(f"\nGotowe -> {OUT}")
    print("Teraz: python3 tools/gen_gallery.py && python3 tools/gen_reels.py")


if __name__ == "__main__":
    main()
