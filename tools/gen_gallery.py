#!/usr/bin/env python3
"""Generuje grafiki galerii i suwakow porownania z assets/uploads/final/.

Powod: pliki w assets/gallery/ mialy 341x512 px, a karty renderuja sie
na ekranach retina do ~560-880 px szerokosci. Efekt: widoczne rozmycie.
Oryginaly (1586x2376) daja ostry obraz po przeskalowaniu.

UWAGA: czytamy z podkatalogu final/, a nie wprost z uploads/. Surowe rendery
maja w prawym dolnym rogu znak wodny generatora; usuwa go
tools/strip_watermark.py. Po dorzuceniu nowego renderu do assets/uploads/
najpierw odpal strip_watermark.py, dopiero potem ten skrypt.

Wyjscie (kadr 3:4, zgodny z .card__img i .compare w css/style.css):
  assets/gallery/<styl>.jpg      700x933   (1x)
  assets/gallery/<styl>@2x.jpg   1400x1866 (2x, retina)

Uzycie: python3 tools/gen_gallery.py
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "assets", "uploads", "final")
OUT = os.path.join(ROOT, "assets", "gallery")

# styl w galerii -> plik zrodlowy w assets/uploads/
STYLE_SOURCES = {
    "olej-klasyczny": "para3-olej-clean.png",
    "van-gogh":       "para4-vangogh-clean.png",
    "cyberpunk":      "para3-cyberpunk-clean.png",
    "szkic-olowek":   "para4-szkic-clean.png",
    "wektor":         "para3-wektor-clean.png",
    "mozaika":        "para3-witraz-clean.png",
    "lego":           "para2-lego-clean.png",
    "komiks":         "para2-komiks-clean.png",
    "bajka-3d":       "para1-bajka3d-clean.png",
}

# suwaki „zdjecie -> obraz". Ta sama para na obu klatkach, inaczej
# podpis „to samo ujecie" bylby nieprawdziwy.
COMPARES = {
    "compare-a-przed": "para3-przed.jpg",
    "compare-a-po":    "para3-olej-clean.png",
    "compare-b-przed": "para1-przed.jpg",
    "compare-b-po":    "para1-bajka3d-clean.png",
}

WIDTH_1X = 700
ASPECT = 3 / 4          # szerokosc / wysokosc


def crop_34(im):
    """Kadruje do 3:4. Nadmiar wysokosci tnie 40% od gory, 60% od dolu —
    twarze na portretach sa zwykle powyzej srodka."""
    w, h = im.size
    target_h = w / ASPECT
    if target_h <= h:
        excess = h - target_h
        top = excess * 0.4
        return im.crop((0, int(top), w, int(top + target_h)))
    target_w = h * ASPECT
    left = (w - target_w) / 2
    return im.crop((int(left), 0, int(left + target_w), h))


def emit(src_path, out_stem):
    im = Image.open(src_path).convert("RGB")
    im = crop_34(im)
    for suffix, width, quality in (("", WIDTH_1X, 86), ("@2x", WIDTH_1X * 2, 80)):
        h = round(width / ASPECT)
        out = os.path.join(OUT, f"{out_stem}{suffix}.jpg")
        im.resize((width, h), Image.LANCZOS).save(
            out, "JPEG", quality=quality, optimize=True, progressive=True
        )
        print(f"  {os.path.basename(out):28} {width}x{h}  {os.path.getsize(out)//1024} kB")


def main():
    os.makedirs(OUT, exist_ok=True)
    missing = []
    print("Galeria:")
    for stem, src in STYLE_SOURCES.items():
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            missing.append(src)
            continue
        emit(p, stem)

    print("\nSuwaki porownania:")
    for stem, src in COMPARES.items():
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            missing.append(src)
            continue
        emit(p, stem)

    if missing:
        print("\nBRAK plikow zrodlowych:")
        for m in missing:
            print("  -", m)

    print(
        "\nUwaga: akwarela, kubizm, pastel i superbohater nie maja zrodla\n"
        "w assets/uploads/ — zostaja w starej rozdzielczosci 341x512.\n"
        "Zeby je poprawic, trzeba wyrenderowac te 4 style z para1-4-przed.jpg."
    )


if __name__ == "__main__":
    main()
