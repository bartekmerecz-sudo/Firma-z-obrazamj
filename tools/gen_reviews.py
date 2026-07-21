#!/usr/bin/env python3
"""Generator filmikow w stylu recenzji klienta (UGC) na TikTok/Reels.
Buduje sceny jako klatki PNG (PIL), skleja w pionowe wideo 1080x1920 (ffmpeg).
Nie wymaga internetu. Czcionki: DejaVu (polskie znaki)."""
import os, subprocess, textwrap, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "assets", "video")
TMP  = os.path.join(ROOT, "tools", "_frames")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
# Paleta marki
BEIGE   = (245, 239, 230)
GRAPH   = (43, 43, 43)
GOLD    = (201, 162, 75)
GOLD_D  = (184, 134, 11)
WHITE   = (255, 255, 255)
CREAM   = (250, 246, 240)

FSERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSANS    = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSANS_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(path, size): return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_center(draw, lines, fnt, cx, y, fill, lh=1.25, shadow=None):
    asc, desc = fnt.getmetrics()
    step = int((asc + desc) * lh)
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        x = cx - w/2
        if shadow:
            draw.text((x+2, y+2), ln, font=fnt, fill=shadow)
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y

def cover(img, w, h):
    return ImageOps.fit(img, (w, h), method=Image.LANCZOS)

def bg_blur(img_path):
    """Rozmyte, przyciemnione tlo z obrazka na cala klatke."""
    im = Image.open(img_path).convert("RGB")
    im = cover(im, W, H).filter(ImageFilter.GaussianBlur(38))
    ov = Image.new("RGB", (W, H), GRAPH)
    return Image.blend(im, ov, 0.55)

def rounded(img, rad):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0,0,img.size[0],img.size[1]], rad, fill=255)
    out = img.convert("RGBA"); out.putalpha(mask); return out

def stars(draw, cx, y, size=64, n=5):
    s = "★ ★ ★ ★ ★"
    f = font(FSANS_B, size)
    w = draw.textlength(s, font=f)
    draw.text((cx - w/2, y), s, font=f, fill=GOLD, )
    return y + size + 10

def pill(draw, cx, y, text, fnt, pad=(26,12), fill=GOLD, tc=WHITE):
    tw = draw.textlength(text, font=fnt)
    asc, desc = fnt.getmetrics(); th = asc+desc
    w = tw + pad[0]*2; h = th + pad[1]*2
    x0 = cx - w/2
    draw.rounded_rectangle([x0, y, x0+w, y+h], (h//2), fill=fill)
    draw.text((x0+pad[0], y+pad[1]), text, font=fnt, fill=tc)
    return y + h

# ---------- SCENY ----------
def scene_hook(path_img, hook_top, hook_big):
    im = bg_blur(path_img); d = ImageDraw.Draw(im)
    f_top = font(FSANS_B, 44); f_big = font(FSERIF_B, 96)
    ln1 = wrap(d, hook_top, f_top, W-160)
    y = 300
    y = draw_center(d, ln1, f_top, W/2, y, GOLD)
    y += 30
    ln2 = wrap(d, hook_big, f_big, W-140)
    draw_center(d, ln2, f_big, W/2, y, WHITE, lh=1.15, shadow=(0,0,0))
    # doln y wskazowka
    f_s = font(FSANS, 38)
    tip = "przesuwaj ➝ zobacz efekt"
    tw = d.textlength(tip, font=f_s)
    d.text((W/2-tw/2, H-190), tip, font=f_s, fill=(230,230,230))
    return im

def scene_reveal(path_img, caption):
    im = bg_blur(path_img); d = ImageDraw.Draw(im)
    # obraz w ramce (mockup jest 1080x1350 -> pokazujemy duzo)
    art = Image.open(path_img).convert("RGB")
    aw = 900
    art = cover(art, aw, int(aw*1.25))
    frame = Image.new("RGB", (art.size[0]+36, art.size[1]+36), WHITE)
    frame.paste(art, (18,18))
    fr = rounded(frame, 22)
    fx = (W - fr.size[0])//2; fy = 300
    # cien
    sh = Image.new("RGBA",(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.rounded_rectangle([fx+10,fy+22,fx+fr.size[0]+10,fy+fr.size[1]+22],22,fill=(0,0,0,120))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    im = Image.alpha_composite(im.convert("RGBA"), sh).convert("RGB")
    im.paste(fr, (fx,fy), fr)
    d = ImageDraw.Draw(im)
    f_c = font(FSANS_B, 46)
    ln = wrap(d, caption, f_c, W-160)
    draw_center(d, ln, f_c, W/2, fy+fr.size[1]+60, WHITE, shadow=(0,0,0))
    return im

def scene_review(path_img, quote, name, place):
    im = bg_blur(path_img); d = ImageDraw.Draw(im)
    # karta recenzji
    cw, ch = W-140, 900
    cx0 = (W-cw)//2; cy0 = 380
    card = Image.new("RGB",(cw,ch), CREAM)
    cd = ImageDraw.Draw(card)
    # gwiazdki
    ys = 70
    ss = "★ ★ ★ ★ ★"; fs = font(FSANS_B, 60)
    sw = cd.textlength(ss, font=fs); cd.text(((cw-sw)/2, ys), ss, font=fs, fill=GOLD)
    ys += 110
    # cudzyslow
    fq = font(FSERIF_B, 130); cd.text((50, ys-30), "“", font=fq, fill=(210,196,170))
    # cytat
    f_q = font(FSERIF_B, 52)
    ql = wrap(cd, quote, f_q, cw-130)
    yq = ys+40
    for ln in ql:
        w = cd.textlength(ln, font=f_q); cd.text(((cw-w)/2, yq), ln, font=f_q, fill=GRAPH); yq += 74
    # podpis
    yq += 30
    f_n = font(FSANS_B, 44); nm = name
    w = cd.textlength(nm, font=f_n); cd.text(((cw-w)/2, yq), nm, font=f_n, fill=GRAPH); yq += 60
    f_p = font(FSANS, 34)
    w = cd.textlength(place, font=f_p); cd.text(((cw-w)/2, yq), place, font=f_p, fill=(120,120,120))
    fr = rounded(card, 28)
    im = im.convert("RGBA"); im.paste(fr,(cx0,cy0),fr)
    im = im.convert("RGB"); d = ImageDraw.Draw(im)
    # plakietka zweryfikowana
    f_v = font(FSANS_B, 32)
    pill(d, W/2, cy0-30, "✓ Zamówienie zrealizowane", f_v, fill=GOLD_D)
    return im

def scene_cta():
    im = Image.new("RGB",(W,H), GRAPH); d = ImageDraw.Draw(im)
    # zlota ramka
    d.rounded_rectangle([60,60,W-60,H-60], 30, outline=GOLD, width=4)
    f_e = font(FSANS_B, 40)
    tt = "PIXELPĘDZEL"
    w = d.textlength(tt, font=f_e); d.text((W/2-w/2, 360), tt, font=f_e, fill=GOLD)
    f_h = font(FSERIF_B, 92)
    ln = wrap(d, "Zamień swoje zdjęcie w obraz", f_h, W-220)
    y = draw_center(d, ln, f_h, W/2, 470, WHITE, lh=1.12)
    y += 40
    f_s = font(FSANS, 46)
    ln2 = wrap(d, "Zobaczysz projekt przed drukiem. Płacisz, gdy Ci się spodoba.", f_s, W-260)
    y = draw_center(d, ln2, f_s, W/2, y, (225,225,225), lh=1.4)
    y += 60
    f_c = font(FSANS_B, 40)
    pill(d, W/2, y, "-20% kodem  START20", f_c, fill=GOLD, tc=GRAPH);
    # domena na dole
    f_d = font(FSANS_B, 56)
    dm = "pixelpedzel.pl"
    w = d.textlength(dm, font=f_d); d.text((W/2-w/2, H-260), dm, font=f_d, fill=GOLD)
    f_l = font(FSANS, 38); lk="kliknij link w bio ↑"
    w = d.textlength(lk, font=f_l); d.text((W/2-w/2, H-180), lk, font=f_l, fill=(200,200,200))
    return im

def build(name, scenes, durs, fade=0.45):
    """scenes: list[PIL.Image]; durs: sekundy na scene. Sklejanie z xfade."""
    paths=[]
    for i,s in enumerate(scenes):
        p=os.path.join(TMP,f"{name}_{i}.png"); s.save(p); paths.append(p)
    fps=30
    # zbuduj filtr xfade
    inputs=[]
    for p,dl in zip(paths,durs):
        inputs += ["-loop","1","-t",str(dl),"-i",p]
    n=len(paths)
    fc=[];
    for i in range(n):
        fc.append(f"[{i}:v]scale={W}:{H},setsar=1,fps={fps}[v{i}]")
    # lancuch xfade
    prev="v0"; off=0.0
    chain=[]
    cum=durs[0]
    for i in range(1,n):
        off = cum - fade
        out=f"x{i}"
        chain.append(f"[{prev}][v{i}]xfade=transition=fade:duration={fade}:offset={off:.3f}[{out}]")
        prev=out
        cum += durs[i]-fade
    filt=";".join(fc+chain)
    outp=os.path.join(OUT,f"{name}.mp4")
    cmd=[FFMPEG,"-y",*inputs,"-filter_complex",filt,"-map",f"[{prev}]",
         "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast","-r",str(fps),outp]
    subprocess.run(cmd, check=True, capture_output=True)
    print("OK", outp, round(os.path.getsize(outp)/1024), "KB, dlugosc ~", round(cum,1),"s")

# ---------- KONKRETNE FILMY ----------
def main():
    M = lambda f: os.path.join(ROOT,"assets","mockups",f)

    # 1. Rocznica — olej klasyczny
    build("tt-recenzja-rocznica",
        [ scene_hook(M("olej-klasyczny.png"), "Zamówiłam obraz z naszego zdjęcia", "Mąż się popłakał."),
          scene_reveal(M("olej-klasyczny.png"), "Nasze zdjęcie z wakacji → obraz olejny"),
          scene_review(M("olej-klasyczny.png"),
              "Bałam się, że wyjdzie kicz. A dostałam prawdziwe dzieło. Twarze oddane idealnie, jakość obłędna.",
              "Kasia", "rocznica ślubu · Łódź"),
          scene_cta() ],
        [2.6, 2.8, 4.2, 3.2])

    # 2. Zaręczyny — szkic olowkiem
    build("tt-recenzja-zareczyny",
        [ scene_hook(M("szkic-olowek.png"), "Prezent na zaręczyny", "Nie uwierzycie w efekt."),
          scene_reveal(M("szkic-olowek.png"), "Jedno zdjęcie → ręcznie dopracowany szkic"),
          scene_review(M("szkic-olowek.png"),
              "Zamówione w sobotę, podgląd w poniedziałek, poprawki tego samego dnia. Wisi nad łóżkiem, patrzymy codziennie.",
              "Ola", "zaręczyny · Warszawa"),
          scene_cta() ],
        [2.6, 2.8, 4.2, 3.2])

    # 3. Prezent dla mamy — akwarela
    build("tt-recenzja-mama",
        [ scene_hook(M("akwarela.png"), "Prezent dla mamy na urodziny", "Płakała ze szczęścia."),
          scene_reveal(M("akwarela.png"), "Wspólne zdjęcie → delikatna akwarela"),
          scene_review(M("akwarela.png"),
              "Szukałam czegoś innego niż perfumy. To był strzał w dziesiątkę. Mama nie może przestać patrzeć.",
              "Marta", "prezent dla mamy · Kraków"),
          scene_cta() ],
        [2.6, 2.8, 4.2, 3.2])

    # 4. Van Gogh na scianie — sceptyk
    build("tt-recenzja-vangogh",
        [ scene_hook(M("van-gogh.png"), "Bałem się, że AI zepsuje twarze", "Efekt mnie zaskoczył."),
          scene_reveal(M("van-gogh.png"), "Nasza fotka → styl Van Gogha na ścianie"),
          scene_review(M("van-gogh.png"),
              "Myślałem, że będzie sztucznie. A wyszło lepiej niż na zdjęciu. Każdy gość pyta, skąd to mam.",
              "Piotr", "dekoracja salonu · Wrocław"),
          scene_cta() ],
        [2.6, 2.8, 4.2, 3.2])

if __name__ == "__main__":
    main()
