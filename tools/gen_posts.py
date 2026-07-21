#!/usr/bin/env python3
"""Generator emocjonalnych grafik postowych PixelPedzel (feed FB/IG, 1080x1350).
Pelne zdjecie + delikatny scrim u dolu + emocjonalny naglowek + CTA marki.
Zasady: sprzedajemy EMOCJE i MOMENT, nie produkt. Jeden przekaz na grafike."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK = os.path.join(ROOT, "assets", "mockups")
OUT  = os.path.join(ROOT, "assets", "social")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
GOLD   = (201, 162, 75)
WHITE  = (245, 245, 242)
FSERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSERIF   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FSANS    = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSANS_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
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

def make(basename, eyebrow, headline, sub, out_name):
    im = Image.open(os.path.join(MOCK, basename)).convert("RGB")
    im = ImageOps.fit(im, (W,H), method=Image.LANCZOS)
    # scrim: przezroczysty u gory -> gladki ramp -> pelna ciemnosc u dolu
    top  = int(H*0.42)   # do tego miejsca zdjecie czyste
    full = int(H*0.72)   # od tego miejsca pelna ciemnosc (miejsce na tekst)
    scrim = Image.new("L",(1,H),0)
    for y in range(H):
        if y <= top: v = 0
        elif y >= full: v = 255
        else:
            t = (y-top)/(full-top)
            v = int(255*(t*t*(3-2*t)))   # smoothstep, bez szwu
        scrim.putpixel((0,y), v)
    scrim = scrim.resize((W,H))
    dark = Image.new("RGB",(W,H),(20,18,16))
    im = Image.composite(dark, im, scrim)
    d = ImageDraw.Draw(im)

    # blok tekstu od dolu
    pad = 80
    y = H - 90
    # CTA / marka (najnizej)
    f_brand = font(FSANS_B, 34)
    brand = "PixelPędzel  ·  pixelpedzel.pl"
    d.text((pad, y-6), brand, font=f_brand, fill=GOLD)
    y -= 70
    # sub
    if sub:
        f_sub = font(FSANS, 34)
        for ln in reversed(wrap(d, sub, f_sub, W-2*pad)):
            y -= 46
            d.text((pad, y), ln, font=f_sub, fill=(225,222,215))
        y -= 18
    # headline (emocja)
    f_h = font(FSERIF_B, 72)
    hl = wrap(d, headline, f_h, W-2*pad)
    for ln in reversed(hl):
        y -= 86
        d.text((pad, y), ln, font=f_h, fill=WHITE)
    y -= 14
    # eyebrow (mala zlota etykieta)
    f_e = font(FSANS_B, 30)
    d.text((pad, y-40), eyebrow.upper(), font=f_e, fill=GOLD)
    # zlota kreska nad eyebrow
    d.rectangle([pad, y-58, pad+70, y-54], fill=GOLD)

    im.save(os.path.join(OUT, out_name), quality=92)
    print("OK", out_name)

POSTS = [
 ("olej-klasyczny.png", "Pamiątka na lata",
  "Niektórych chwil nie chcesz zapomnieć.",
  "Zamień swoje zdjęcie w obraz, który zostaje w domu i w sercu.",
  "post-pamiatka.png"),
 ("szkic-olowek.png", "Prezent z sercem",
  "Powiedz „kocham” bez słów.",
  "Wasze zdjęcie jako ręcznie dopracowany obraz na płótnie.",
  "post-kocham.png"),
 ("akwarela.png", "Zaręczyny · rocznica",
  "Ten moment, gdy padło „tak”.",
  "Zatrzymaj go na płótnie. Prezent, przy którym zakręci się łza.",
  "post-zareczyny.png"),
 ("van-gogh.png", "Wasza historia",
  "Wasza historia zasługuje na ścianę.",
  "Nie kolejny plakat ze sklepu — Wasz obraz, jakiego nikt nie ma.",
  "post-historia.png"),
 ("duo-galeria.png", "Dom z duszą",
  "Dom, który opowiada Waszą historię.",
  "Obrazy z Waszych zdjęć. Wy wybieracie chwile, my tworzymy dzieło.",
  "post-dom.png"),
 ("cyberpunk.png", "Ty wybierasz styl",
  "Zwykłe zdjęcie? A może dzieło sztuki.",
  "17 stylów do wyboru. Podgląd przed drukiem — płacisz, gdy Ci się spodoba.",
  "post-styl.png"),
]

if __name__ == "__main__":
    for p in POSTS:
        make(*p)
