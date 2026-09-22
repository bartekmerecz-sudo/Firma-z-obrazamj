#!/usr/bin/env python3
"""Reelsy PRZED -> PO na TikToka/Reels. Pionowe 1080x1920.

Czym rozni sie od gen_compare_video.py (starsza generacja):
  * BEZ adresu strony wypalonego w kadrze — TikTok czyta to jako probe
    wyprowadzenia ruchu poza platforme. Link zostaje wylacznie w bio.
  * Tekst tylko w strefie bezpiecznej (gora 150 px, dol 480 px sa
    zaslaniane przez UI TikToka: opis, przyciski, nick).
  * Powolny zoom (Ken Burns) zamiast statycznej grafiki — statyczny kadr
    z animowanym tekstem algorytm klasyfikuje jako baner reklamowy.
  * Hook rozstrzyga sie do 3 sekundy i dziala przy wylaczonym dzwieku.
  * Konca nie zamyka cennik ani kod rabatowy, tylko pytanie —
    komentarze podbijaja zasieg mocniej niz kliniecie w link.

Uzycie: python3 tools/gen_reels.py [nazwa-filmu ...]
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
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
SAFE_TOP, SAFE_BOT = 150, H - 480      # strefy zaslaniane przez UI TikToka
CREAM, INK, GOLD = (238, 232, 222), (20, 18, 16), (196, 162, 96)
F_HEAD = os.path.join(FONTS, "Gloock-Regular.ttf")
F_KICK = os.path.join(FONTS, "ArsenalSC-Regular.ttf")
F_SUB = os.path.join(FONTS, "Outfit-Regular.ttf")


def font(p, s):
    return ImageFont.truetype(p, s)


def wrap(d, t, f, mw):
    ws, ls, cur = t.split(), [], ""
    for w in ws:
        s = (cur + " " + w).strip()
        if d.textlength(s, font=f) <= mw:
            cur = s
        else:
            if cur:
                ls.append(cur)
            cur = w
    if cur:
        ls.append(cur)
    return ls


def ls_w(d, t, f, sp=0):
    return sum(d.textlength(c, font=f) + sp for c in t) - (sp if t else 0)


def text_ls(d, xy, t, f, fill, sp=0):
    x, y = xy
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + sp
    return x


def center_ls(d, y, t, f, fill, sp=0):
    text_ls(d, ((W - ls_w(d, t, f, sp)) // 2, y), t, f, fill, sp)


def scrim(top_h, bot_h, top_a=205, bot_a=170):
    """Przyciemnienie gory i dolu, zeby bialy tekst byl czytelny na kazdym zdjeciu."""
    m = Image.new("L", (1, H), 0)
    for y in range(H):
        a = 0
        if y < top_h:
            a = int(top_a * (1 - y / top_h) ** 1.3)
        if y > H - bot_h:
            t = (y - (H - bot_h)) / bot_h
            a = max(a, int(bot_a * (t * t * (3 - 2 * t))))
        m.putpixel((0, y), a)
    return m.resize((W, H))


def pill(d, y, label, fs=44, bg=(20, 18, 16, 215), fg=CREAM):
    f = font(F_KICK, fs)
    tw = ls_w(d, label, f, 4)
    pad = 34
    w = tw + pad * 2
    h = fs + 32
    x0 = (W - w) // 2
    d.rounded_rectangle([x0, y, x0 + w, y + h], h // 2, fill=bg)
    text_ls(d, (x0 + pad, y + 14), label, f, fg + (255,) if len(fg) == 3 else fg, 4)


def photo(img_path, hook=None, label=None):
    """Kadr pelnoekranowy ze zdjeciem/obrazem. Tekst wylacznie w strefie bezpiecznej."""
    im = ImageOps.fit(Image.open(img_path).convert("RGB"), (W, H), method=Image.LANCZOS)
    im = Image.composite(Image.new("RGB", (W, H), INK), im, scrim(int(H * 0.30), int(H * 0.26)))
    d = ImageDraw.Draw(im, "RGBA")
    if hook:
        fh = font(F_HEAD, 92)
        y = SAFE_TOP + 40
        for ln in wrap(d, hook, fh, W - 170):
            x = (W - d.textlength(ln, font=fh)) // 2
            d.text((x + 2, y + 3), ln, font=fh, fill=(0, 0, 0, 170))
            d.text((x, y), ln, font=fh, fill=(242, 238, 231, 255))
            y += 102
    if label:
        pill(d, SAFE_BOT - 110, label)
    return im.convert("RGB")


def wall(img_path, caption="Na płótnie, u Ciebie na ścianie"):
    """Gotowy obraz w ramie na ciepłym tle — pokazuje produkt, nie plik."""
    bg = Image.new("RGB", (W, H), CREAM)
    px = bg.load()
    for y in range(H):
        t = y / H
        val = (int(238 - 40 * t), int(232 - 42 * t), int(222 - 44 * t))
        for x in range(W):
            px[x, y] = val
    cw, ch = 620, 828
    art = ImageOps.fit(Image.open(img_path).convert("RGB"), (cw, ch), method=Image.LANCZOS)
    fr = Image.new("RGB", (cw + 38, ch + 38), (250, 248, 244))
    fr.paste(art, (19, 19))
    fx, fy = (W - fr.size[0]) // 2, 470
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [fx + 16, fy + 30, fx + fr.size[0] + 16, fy + fr.size[1] + 30], 10, fill=(40, 32, 26, 150)
    )
    bg = Image.alpha_composite(bg.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(26))).convert("RGB")
    bg.paste(fr, (fx, fy))
    d = ImageDraw.Draw(bg, "RGBA")
    d.rectangle([fx, fy, fx + fr.size[0] - 1, fy + fr.size[1] - 1], outline=(210, 202, 190, 255), width=1)
    fk = font(F_KICK, 40)
    center_ls(d, SAFE_TOP + 90, caption.upper(), fk, GOLD + (255,), 6)
    d.line([(W // 2 - 70, SAFE_TOP + 152), (W // 2 + 70, SAFE_TOP + 152)], fill=GOLD + (220,), width=2)
    return bg


def grid(paths, caption="Jedno zdjęcie · cztery style"):
    bg = Image.new("RGB", (W, H), CREAM)
    px = bg.load()
    for y in range(H):
        t = y / H
        val = (int(238 - 30 * t), int(232 - 32 * t), int(222 - 34 * t))
        for x in range(W):
            px[x, y] = val
    d = ImageDraw.Draw(bg, "RGBA")
    fk = font(F_KICK, 42)
    center_ls(d, SAFE_TOP + 40, caption.upper(), fk, GOLD + (255,), 6)
    d.line([(W // 2 - 70, SAFE_TOP + 104), (W // 2 + 70, SAFE_TOP + 104)], fill=GOLD + (220,), width=2)
    gap, gx0, gy0 = 24, 110, SAFE_TOP + 170
    cw = (W - 2 * gx0 - gap) // 2
    ch = int(cw * 1.32)
    for i, (p, (x, y)) in enumerate(zip(paths, [(gx0, gy0), (gx0 + cw + gap, gy0),
                                                (gx0, gy0 + ch + gap), (gx0 + cw + gap, gy0 + ch + gap)]), 1):
        art = ImageOps.fit(Image.open(p).convert("RGB"), (cw, ch), method=Image.LANCZOS)
        fr = Image.new("RGB", (cw + 16, ch + 16), (250, 248, 244))
        fr.paste(art, (8, 8))
        bg.paste(fr, (x - 8, y - 8))
        d.rectangle([x - 8, y - 8, x + cw + 7, y + ch + 7], outline=(210, 202, 190, 255), width=1)
        # numer kafelka — karta koncowa prosi o odpowiedz numerem, wiec musi byc widoczny
        fn = font(F_KICK, 46)
        r = 34
        cx, cy = x + 26, y + 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 18, 16, 225))
        n = str(i)
        d.text((cx - d.textlength(n, font=fn) / 2, cy - 30), n, font=fn, fill=CREAM + (255,))
    return bg


def end_card(question="Które zdjęcie\nby u Ciebie zawisło?",
             sub="Napisz w komentarzu — podpowiem, jaki styl pasuje."):
    """Zamkniecie pytaniem, nie oferta. Bez adresu i bez kodu rabatowego."""
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([50, 50, W - 51, H - 51], outline=GOLD + (255,), width=3)
    fh = font(F_HEAD, 94)
    y = 560
    for ln in question.split("\n"):
        x = (W - d.textlength(ln, font=fh)) // 2
        d.text((x, y), ln, font=fh, fill=(242, 238, 231, 255))
        y += 108
    fs = font(F_SUB, 42)
    y += 40
    for ln in wrap(d, sub, fs, W - 220):
        x = (W - d.textlength(ln, font=fs)) // 2
        d.text((x, y), ln, font=fs, fill=(206, 198, 186, 255))
        y += 56
    center_ls(d, SAFE_BOT - 60, "PIXELPĘDZEL", font(F_KICK, 44), GOLD + (255,), 8)
    return im


def build(name, scenes, durs, trans, zooms=None):
    """scenes: PIL; durs: sek; trans: przejscia; zooms: 'in'/'out'/None na scene."""
    fps, fade = 30, 0.55
    paths = []
    for i, s in enumerate(scenes):
        p = os.path.join(TMP, f"{name}_{i}.png")
        s.save(p)
        paths.append(p)
    zooms = zooms or [None] * len(scenes)

    inputs = []
    for p, dl in zip(paths, durs):
        inputs += ["-loop", "1", "-t", str(dl), "-i", p]

    fc = []
    for i, (dl, z) in enumerate(zip(durs, zooms)):
        if z:
            # skalowanie w gore przed zoompan usuwa drganie kadru
            n = max(1, int(round(dl * fps)))
            if z == "in":
                expr = f"min(zoom+{0.10/n:.6f},1.10)"
            else:
                expr = f"if(eq(on,0),1.10,max(zoom-{0.10/n:.6f},1.0))"
            fc.append(
                f"[{i}:v]scale={W*2}:{H*2},zoompan=z='{expr}':d={n}:"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={fps},"
                f"setsar=1[v{i}]"
            )
        else:
            fc.append(f"[{i}:v]scale={W}:{H},setsar=1,fps={fps}[v{i}]")

    prev, cum, chain = "v0", durs[0], []
    for i in range(1, len(paths)):
        off = cum - fade
        out = f"x{i}"
        chain.append(
            f"[{prev}][v{i}]xfade=transition={trans[i-1]}:duration={fade}:offset={off:.3f}[{out}]"
        )
        prev, cum = out, cum + durs[i] - fade

    outp = os.path.join(OUT, f"{name}.mp4")
    subprocess.run(
        [FFMPEG, "-y", *inputs, "-filter_complex", ";".join(fc + chain), "-map", f"[{prev}]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
         "-movflags", "+faststart", "-r", str(fps), outp],
        check=True, capture_output=True)
    print(f"OK  {name}.mp4  {os.path.getsize(outp)//1024} kB  ~{cum:.1f}s")


# ---------------------------------------------------------------- filmy
def reels():
    return {
    # 1. Hook konkretny: liczba + strata. Najmocniejszy material (starsze malzenstwo).
    "reel-lata-razem": (
        [photo(f"{U}/para4-przed.jpg", hook="Tyle lat razem.\nI ani jednego\nzdjęcia na ścianie."),
         photo(f"{U}/para4-vangogh-clean.png", label="TO SAMO ZDJĘCIE"),
         wall(f"{U}/para4-vangogh-clean.png"),
         end_card("Czyje zdjęcie\nzasługuje na ścianę?", "Napisz w komentarzu, komu byś taki zrobił.")],
        [3.0, 2.6, 2.8, 3.0], ["wipeleft", "fade", "fade"], ["in", "out", "in", None]),

    # 2. Hook „strata": zdjecie ktore zostalo w telefonie.
    "reel-zostalo-w-telefonie": (
        [photo(f"{U}/para3-przed.jpg", hook="To zdjęcie leżało\nw telefonie\ndwa lata."),
         photo(f"{U}/para3-olej-clean.png", label="PO · OLEJ"),
         wall(f"{U}/para3-olej-clean.png"),
         end_card("Masz takie zdjęcie\nw telefonie?", "Napisz w komentarzu, z czego byś zrobił obraz.")],
        [3.0, 2.6, 2.8, 3.0], ["wipeleft", "fade", "fade"], ["in", "out", "in", None]),

    # 3. Format ankiety — najlepiej zbiera komentarze, a komentarze podbijaja zasieg.
    "reel-ktory-styl": (
        [photo(f"{U}/para3-przed.jpg", hook="Jedno zdjęcie.\nCztery style.\nKtóry wybierasz?"),
         grid([f"{U}/para3-olej-clean.png", f"{U}/para3-witraz-clean.png",
               f"{U}/para3-wektor-clean.png", f"{U}/para3-cyberpunk-clean.png"]),
         end_card("1, 2, 3 czy 4?", "Napisz numer w komentarzu.")],
        [2.8, 4.2, 2.8], ["fade", "fade"], ["in", None, None]),

    # 4. Kontrast: zwykle studyjne zdjecie -> bajka 3D. Efekt „nie poznasz".
    "reel-jak-z-bajki": (
        [photo(f"{U}/para1-przed.jpg", hook="Zwykłe zdjęcie\nz sesji."),
         photo(f"{U}/para1-bajka3d-clean.png", label="PO · BAJKOWY 3D"),
         photo(f"{U}/para1-wektor-clean.png", label="PO · WEKTOR"),
         end_card("Bajka czy wektor?", "Napisz, który lepszy.")],
        [2.6, 2.5, 2.5, 2.8], ["wipeleft", "wipeleft", "fade"], ["in", "out", "in", None]),

    # 5. Prezent — konkretna sytuacja zamiast ogolnika „fajny prezent".
    "reel-prezent-klocki": (
        [photo(f"{U}/para2-przed.jpg", hook="Zrobiłem im obraz\nz klocków."),
         photo(f"{U}/para2-lego-clean.png", label="PO · KLOCKI"),
         photo(f"{U}/para2-komiks-clean.png", label="PO · KOMIKS"),
         wall(f"{U}/para2-lego-clean.png"),
         end_card("Komu byś taki\nprezent zrobił?", "Oznacz tę osobę w komentarzu.")],
        [2.6, 2.4, 2.4, 2.6, 2.8], ["wipeleft", "wipeleft", "fade", "fade"],
        ["in", "out", "in", "out", None]),

    # 6. Witraz — najbardziej „nieoczywisty" efekt, dobry na zaskoczenie.
    "reel-witraz": (
        [photo(f"{U}/para3-przed.jpg", hook="Nie sądziłem,\nże wyjdzie z tego\nwitraż."),
         photo(f"{U}/para3-witraz-clean.png", label="PO · WITRAŻ"),
         wall(f"{U}/para3-witraz-clean.png"),
         end_card("Który styl\nchcesz zobaczyć?", "Napisz w komentarzu.")],
        [3.0, 2.6, 2.8, 2.8], ["wipeleft", "fade", "fade"], ["in", "out", "in", None]),

    # 7. Szkic — spokojny, „pamiatkowy" ton. Inny rejestr niz reszta.
    "reel-szkic-pamiatka": (
        [photo(f"{U}/para4-przed.jpg", hook="Zdjęcie sprzed lat.\nOłówkiem."),
         photo(f"{U}/para4-szkic-clean.png", label="PO · SZKIC OŁÓWKIEM"),
         wall(f"{U}/para4-szkic-clean.png"),
         end_card("Czyje zdjęcie\nbyś tak przerobił?", "Napisz w komentarzu.")],
        [2.8, 2.6, 2.8, 2.8], ["wipeleft", "fade", "fade"], ["in", "out", "in", None]),

    # 8. Cyberpunk — najmocniejszy wizualnie kontrast, pod mlodsza widownie.
    "reel-cyberpunk": (
        [photo(f"{U}/para3-przed.jpg", hook="Ze zdjęcia z plaży\ndo neonowego\nmiasta."),
         photo(f"{U}/para3-cyberpunk-clean.png", label="PO · CYBERPUNK"),
         wall(f"{U}/para3-cyberpunk-clean.png"),
         end_card("Twój styl:\nklasyka czy neon?", "Napisz w komentarzu.")],
        [2.8, 2.6, 2.8, 2.8], ["wipeleft", "fade", "fade"], ["in", "out", "in", None]),
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
