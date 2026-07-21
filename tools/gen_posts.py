#!/usr/bin/env python3
"""Generator emocjonalnych grafik postowych PixelPedzel — poziom edytorialny.
Filozofia: „Quiet Heirloom" (tools/design-philosophy.md).
Passe-partout hairline + cieply gradient + ziarno + Gloock/Outfit/ArsenalSC.
Format feed 1080x1350. Wszystkie polskie znaki obslugiwane."""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK = os.path.join(ROOT, "assets", "mockups")
OUT  = os.path.join(ROOT, "assets", "social")
FONTS = "/root/.claude/skills/canvas-design/canvas-fonts"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
# Paleta „Quiet Heirloom"
CREAM  = (238, 232, 222)
CREAM2 = (208, 200, 188)
GOLD   = (196, 162, 96)
INK    = (24, 21, 18)      # cieply grafit do cienia

F_HEAD = os.path.join(FONTS, "Gloock-Regular.ttf")       # wysokokontrastowy serif
F_KICK = os.path.join(FONTS, "ArsenalSC-Regular.ttf")    # small caps do etykiet
F_SUB  = os.path.join(FONTS, "Outfit-Regular.ttf")       # czysty sans
F_SUBB = os.path.join(FONTS, "Outfit-Bold.ttf")
def font(p,s): return ImageFont.truetype(p,s)

def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t, font=fnt)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def text_ls(d, xy, text, fnt, fill, ls=0):
    """tekst z rozstrzeleniem (letter-spacing)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + ls
    return x

def ls_width(d, text, fnt, ls=0):
    return sum(d.textlength(ch, font=fnt)+ls for ch in text) - (ls if text else 0)

def grain(img, amount=8):
    """delikatne, monochromatyczne ziarno — analogowa faktura."""
    n = Image.new("L",(W,H))
    rnd = random.Random(7)
    px = bytearray(rnd.randint(128-amount,128+amount) for _ in range(W*H))
    n.putdata(bytes(px))
    n = n.convert("RGB")
    return Image.blend(img, n, 0.05)

def make(basename, kicker, headline, sub, idx, out_name):
    im = Image.open(os.path.join(MOCK, basename)).convert("RGB")
    im = ImageOps.fit(im, (W,H), method=Image.LANCZOS)

    # --- cieply gradient od dolu (smoothstep, bez pasm) ---
    top  = int(H*0.40); full = int(H*0.74)
    scrim = Image.new("L",(1,H),0)
    for y in range(H):
        if y<=top: v=0
        elif y>=full: v=248
        else:
            t=(y-top)/(full-top); v=int(248*(t*t*(3-2*t)))
        scrim.putpixel((0,y),v)
    scrim = scrim.resize((W,H))
    im = Image.composite(Image.new("RGB",(W,H),INK), im, scrim)

    # subtelne ziarno
    im = grain(im, 8)
    d = ImageDraw.Draw(im, "RGBA")

    # --- passe-partout: cienka linia jak w galerii ---
    m = 46
    d.rectangle([m, m, W-m-1, H-m-1], outline=(238,232,222,150), width=2)

    # --- znak kolekcjonerski „N° xx" (gora-lewo, w ramce) ---
    f_idx = font(F_KICK, 34)
    text_ls(d, (m+34, m+30), f"N° {idx}", f_idx, (238,232,222,205), ls=3)
    # hairline pionowy przy indeksie
    d.line([(m+34, m+78),(m+34+150, m+78)], fill=(196,162,96,180), width=1)

    # ---------- BLOK TEKSTU od dolu ----------
    padx = m + 34
    y = H - m - 40

    # sygnatura marki (najnizej)
    f_brand = font(F_HEAD, 40)
    f_dom   = font(F_SUB, 32)
    bx = text_ls(d, (padx, y-52), "PixelPędzel", f_brand, (238,232,222,255), ls=1)
    d.text((bx+22, y-44), "·", font=f_dom, fill=(196,162,96,255))
    d.text((bx+46, y-44), "pixelpedzel.pl", font=f_dom, fill=(208,200,188,255))
    y -= 92

    # hairline separator
    d.line([(padx, y),(W-m-34, y)], fill=(238,232,222,60), width=1)
    y -= 34

    # sub (jedno zdanie)
    if sub:
        f_s = font(F_SUB, 34)
        for ln in reversed(wrap(d, sub, f_s, W-2*padx)):
            y -= 48
            d.text((padx, y), ln, font=f_s, fill=(214,207,196,255))
        y -= 26

    # headline — Gloock, duzy, emocja
    f_h = font(F_HEAD, 82)
    hl = wrap(d, headline, f_h, W-2*padx)
    for ln in reversed(hl):
        y -= 92
        d.text((padx, y), ln, font=f_h, fill=(240,235,227,255))
    y -= 22

    # kicker — wersaliki rozstrzelone + hairline
    f_k = font(F_KICK, 32)
    kick = kicker.upper()
    text_ls(d, (padx, y-40), kick, f_k, (196,162,96,255), ls=5)
    kw = ls_width(d, kick, f_k, ls=5)
    d.line([(padx, y-56),(padx+min(kw,90), y-56)], fill=(196,162,96,220), width=2)

    im.convert("RGB").save(os.path.join(OUT, out_name), quality=94)
    print("OK", out_name)

POSTS = [
 ("olej-klasyczny.png", "Pamiątka na lata",
  "Niektórych chwil nie chcesz zapomnieć.",
  "Zamień swoje zdjęcie w obraz, który zostaje w domu i w sercu.",
  "01", "post-pamiatka.png"),
 ("szkic-olowek.png", "Prezent z sercem",
  "Powiedz „kocham” bez słów.",
  "Wasze zdjęcie jako ręcznie dopracowany obraz na płótnie.",
  "02", "post-kocham.png"),
 ("akwarela.png", "Zaręczyny · rocznica",
  "Ten moment, gdy padło „tak”.",
  "Zatrzymaj go na płótnie. Prezent, przy którym zakręci się łza.",
  "03", "post-zareczyny.png"),
 ("van-gogh.png", "Wasza historia",
  "Wasza historia zasługuje na ścianę.",
  "Nie kolejny plakat ze sklepu — Wasz obraz, jakiego nikt nie ma.",
  "04", "post-historia.png"),
 ("duo-galeria.png", "Dom z duszą",
  "Dom, który opowiada Waszą historię.",
  "Obrazy z Waszych zdjęć. Wy wybieracie chwile, my tworzymy dzieło.",
  "05", "post-dom.png"),
 ("cyberpunk.png", "Ty wybierasz styl",
  "Zwykłe zdjęcie? A może dzieło sztuki.",
  "17 stylów. Podgląd przed drukiem — płacisz, gdy Ci się spodoba.",
  "06", "post-styl.png"),
]

if __name__ == "__main__":
    for p in POSTS:
        make(*p)
