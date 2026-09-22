#!/usr/bin/env python3
"""Trzecia partia reelsow — styl "szybkie ciecie".

Dwie poprzednie serie mialy ten sam charakter: elegancki serif, spokojne
przenikanie 0,55 s, scena po 2,5-3 s. To wyglada jak reklama marki premium
i dobrze dziala na Facebooku, ale na TikToku przegrywa pierwsze sekundy.

Ta seria jest celowo inna:
  * napisy slowo po slowie (karaoke) — dominujacy jezyk TikToka, czyta sie
    je przy wylaczonym dzwieku, a algorytm indeksuje tekst na ekranie;
  * ciecia co 1,2-1,8 s zamiast 2,5-3 s;
  * gruby, zwezony krój (Big Shoulders) zamiast serifu — czytelny na
    miniaturze i na slabym telefonie;
  * skok zoomu na ciecie zamiast przenikania;
  * zolty akcent na slowie kluczowym.

Napisy renderujemy w PIL jako przezroczyste warstwy i nakladamy filtrem
overlay z okienkiem czasowym. Filtr drawtext odpada — ffmpeg dostarczony
z imageio-ffmpeg jest zbudowany bez libfreetype i tego filtru nie ma.

Uzycie: python3 tools/gen_reels3.py [nazwa ...]
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "video")
TMP = os.path.join(ROOT, "tools", "_vframes")
U = os.path.join(ROOT, "assets", "uploads", "final")
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from fonty import FONTS   # wspolny lokalizator fontow, patrz tools/fonty.py
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
SAFE_TOP, SAFE_BOT = 150, H - 480
F_BOLD = os.path.join(FONTS, "BigShoulders-Bold.ttf")   # ma polskie znaki
GOLD = "#F0C24B"
FPS = 30

CAP_SIZE = 96          # wysokosc napisu
CAP_Y = 1180           # nad strefa UI TikToka
LINE_H = 112
MAX_LINE_PX = W - 150


GOLD_RGB = (240, 194, 75)


def scene(img_path, darken=0.45):
    """Kadr pelnoekranowy, bez tekstu — napisy dokladamy pozniej filtrem."""
    im = ImageOps.fit(Image.open(img_path).convert("RGB"), (W, H), method=Image.LANCZOS)
    # przyciemnienie dolu, zeby biale napisy mialy kontrast na kazdym zdjeciu
    ov = Image.new("L", (1, H), 0)
    for y in range(H):
        a = 0
        if y > H * 0.52:
            t = (y - H * 0.52) / (H * 0.48)
            a = int(255 * darken * (t ** 1.2))
        ov.putpixel((0, y), a)
    im = Image.composite(Image.new("RGB", (W, H), (10, 9, 8)), im, ov.resize((W, H)))
    return im


def layout(words, font):
    """Dzieli slowa na linie i liczy pozycje x — potrzebne, bo drawtext
    nie umie zawijac tekstu ani centrowac wielu slow naraz."""
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    space = d.textlength(" ", font=font)
    lines, cur, curw = [], [], 0.0
    for w in words:
        ww = d.textlength(w, font=font)
        add = ww if not cur else ww + space
        if curw + add > MAX_LINE_PX and cur:
            lines.append((cur, curw))
            cur, curw = [w], ww
        else:
            cur.append(w)
            curw += add
    if cur:
        lines.append((cur, curw))

    placed = []
    for li, (ws, tw) in enumerate(lines):
        x = (W - tw) / 2
        for w in ws:
            ww = d.textlength(w, font=font)
            placed.append((w, x, li))
            x += ww + space
    return placed, len(lines)


def karaoke(name, idx, text, t0, t1, accent=()):
    """Renderuje kazde slowo jako osobna przezroczysta warstwe 1080x1920.
    Zwraca [(sciezka, poczatek, koniec)] — slowa pojawiaja sie po kolei
    i zostaja do konca swojej kwestii."""
    font = ImageFont.truetype(F_BOLD, CAP_SIZE)
    words = text.split()
    placed, nlines = layout(words, font)
    y0 = CAP_Y - (nlines - 1) * LINE_H / 2
    per = (t1 - t0) / max(len(words), 1)
    out = []
    for i, (w, x, li) in enumerate(placed):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        col = GOLD_RGB if w.strip(".,!?").lower() in accent else (255, 255, 255)
        d.text((x, y0 + li * LINE_H), w, font=font, fill=col + (255,),
               stroke_width=8, stroke_fill=(0, 0, 0, 220))
        p = os.path.join(TMP, f"{name}_c{idx}_{i}.png")
        layer.save(p)
        out.append((p, t0 + i * per, t1))
    return out


def build(name, shots, caps):
    """shots: [(sciezka, sekundy, 'in'/'out'/None)]
       caps:  [(tekst, start, koniec, (slowa_na_zolto,))]"""
    paths = []
    for i, (p, _, _) in enumerate(shots):
        f = os.path.join(TMP, f"{name}_b{i}.png")
        scene(p).save(f)
        paths.append(f)

    # WAZNE: sceny podajemy jako POJEDYNCZA klatke, bez -loop. Parametr d
    # w zoompan liczy klatki wyjsciowe na kazda klatke wejsciowa — przy
    # zapetlonym wejsciu pierwsza scena rozciaga sie na dziesiatki sekund
    # i wypycha reszte poza material.
    inputs = []
    for f in paths:
        inputs += ["-i", f]

    fc = []
    for i, (_, dur, z) in enumerate(shots):
        n = max(1, int(round(dur * FPS)))
        # skok zoomu — mocniejszy niz w poprzednich seriach (12% zamiast 10%)
        if z == "in":
            expr = f"min(zoom+{0.12/n:.6f},1.12)"
        elif z == "out":
            expr = f"if(eq(on,0),1.12,max(zoom-{0.12/n:.6f},1.0))"
        else:
            expr = "1.0"
        fc.append(f"[{i}:v]scale={W*2}:{H*2},zoompan=z='{expr}':d={n}"
                  f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}"
                  f",setsar=1[v{i}]")

    # twarde ciecia zamiast przenikania — stad concat, nie xfade
    fc.append("".join(f"[v{i}]" for i in range(len(shots)))
              + f"concat=n={len(shots)}:v=1:a=0[base]")

    total = sum(s[1] for s in shots)
    layers = []
    for ci, (t, a, b, acc) in enumerate(caps):
        layers += karaoke(name, ci, t, a, b, acc)

    n_shots = len(shots)
    for p, _, _ in layers:
        inputs += ["-loop", "1", "-t", str(total), "-i", p]

    prev = "base"
    for j, (_, a, b) in enumerate(layers):
        src = n_shots + j
        tag = f"o{j}"
        fc.append(f"[{prev}][{src}:v]overlay=enable='between(t,{a:.2f},{b:.2f})'[{tag}]")
        prev = tag

    outp = os.path.join(OUT, f"{name}.mp4")
    subprocess.run(
        [FFMPEG, "-y", *inputs, "-filter_complex", ";".join(fc),
         "-map", f"[{prev}]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart",
         "-r", str(FPS), "-t", str(total), outp],
        check=True, capture_output=True)
    print(f"OK  {name}.mp4  {os.path.getsize(outp)//1024} kB  ~{total:.1f}s")


P = lambda n: os.path.join(U, n)


def reels():
    return {
    # Kazdy film: ciecie co ~1,5 s, napis konczy sie razem ze scena.
    "bold-ile-lat": (
        [(P("para4-przed.jpg"), 1.6, "in"),
         (P("para4-vangogh-clean.png"), 1.6, "out"),
         (P("para4-szkic-clean.png"), 1.5, "in"),
         (P("para4-vangogh-clean.png"), 2.0, "out")],
        [("Ile lat jesteście razem", 0.2, 1.6, ("razem",)),
         ("I ile zdjęć wisi na ścianie", 1.7, 3.2, ("zdjęć",)),
         ("Właśnie", 3.3, 4.7, ("właśnie",)),
         ("Wyślij mi jedno", 4.8, 6.6, ("jedno",))]),

    "bold-telefon": (
        [(P("para3-przed.jpg"), 1.5, "in"),
         (P("para3-olej-clean.png"), 1.5, "out"),
         (P("para3-witraz-clean.png"), 1.4, "in"),
         (P("para3-cyberpunk-clean.png"), 2.0, "out")],
        [("Masz 4000 zdjęć w telefonie", 0.2, 1.5, ("4000",)),
         ("Zobaczysz je jeszcze kiedyś", 1.6, 3.0, ("kiedyś",)),
         ("Wybierz jedno", 3.1, 4.4, ("jedno",)),
         ("Reszta to moja robota", 4.5, 6.4, ("moja",))]),

    "bold-prezent": (
        [(P("para2-przed.jpg"), 1.5, "in"),
         (P("para2-lego-clean.png"), 1.5, "out"),
         (P("para2-komiks-clean.png"), 1.5, "in"),
         (P("para2-lego-clean.png"), 1.9, "out")],
        [("Perfumy się skończą", 0.2, 1.5, ("skończą",)),
         ("Świeca zgaśnie", 1.6, 3.0, ("zgaśnie",)),
         ("To zostaje na ścianie", 3.1, 4.6, ("zostaje",)),
         ("Na lata", 4.7, 6.4, ("lata",))]),

    "bold-nie-placisz": (
        [(P("para3-przed.jpg"), 1.4, "in"),
         (P("para3-olej-clean.png"), 1.5, "out"),
         (P("para3-wektor-clean.png"), 1.4, "in"),
         (P("para3-olej-clean.png"), 1.9, "out")],
        [("Wysyłasz mi zdjęcie", 0.2, 1.4, ("zdjęcie",)),
         ("Robię projekt i pokazuję", 1.5, 2.9, ("pokazuję",)),
         ("Nie spodoba się", 3.0, 4.3, ("nie",)),
         ("Nie płacisz ani złotówki", 4.4, 6.2, ("złotówki",))]),

    "bold-ktory": (
        [(P("para3-olej-clean.png"), 1.4, "in"),
         (P("para3-witraz-clean.png"), 1.4, "out"),
         (P("para3-wektor-clean.png"), 1.4, "in"),
         (P("para3-cyberpunk-clean.png"), 2.2, "out")],
        [("Jeden", 0.2, 1.4, ("jeden",)),
         ("Dwa", 1.5, 2.8, ("dwa",)),
         ("Trzy", 2.9, 4.2, ("trzy",)),
         ("Cztery. Który wybierasz", 4.3, 6.4, ("który",))]),

    "bold-babcia": (
        [(P("para4-przed.jpg"), 1.6, "in"),
         (P("para4-szkic-clean.png"), 1.6, "out"),
         (P("para4-vangogh-clean.png"), 1.5, "in"),
         (P("para4-szkic-clean.png"), 2.0, "out")],
        [("Dziadkowie mają wszystko", 0.2, 1.6, ("wszystko",)),
         ("I niczego nie potrzebują", 1.7, 3.2, ("niczego",)),
         ("Poza jednym", 3.3, 4.7, ("jednym",)),
         ("Sobą na ścianie", 4.8, 6.7, ("ścianie",))]),
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
