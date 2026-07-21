#!/usr/bin/env python3
"""Szablon postu PRZED -> PO (metamorfoza zdjecie -> obraz) w stylu Quiet Heirloom.
Uzycie realne:
  make("before.jpg", "after.jpg", "Olej klasyczny", "Z jednego zdjęcia — dzieło.", "01", "out.png")
Tryb makiety (placeholder), gdy brak zdjec: podaj before/after = None.
Format feed 1080x1350. Fonty: Gloock / Outfit / Arsenal SC (polskie znaki OK)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT   = os.path.join(ROOT, "assets", "social")
FONTS = "/root/.claude/skills/canvas-design/canvas-fonts"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
CREAM = (238, 232, 222); INK = (24, 21, 18); GOLD = (196, 162, 96)
F_HEAD = os.path.join(FONTS, "Gloock-Regular.ttf")
F_KICK = os.path.join(FONTS, "ArsenalSC-Regular.ttf")
F_SUB  = os.path.join(FONTS, "Outfit-Regular.ttf")
def font(p,s): return ImageFont.truetype(p,s)

def text_ls(d,xy,t,f,fill,ls=0):
    x,y=xy
    for ch in t:
        d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+ls
    return x
def ls_w(d,t,f,ls=0): return sum(d.textlength(c,font=f)+ls for c in t)-(ls if t else 0)
def wrap(d,t,f,mw):
    ws,ls,cur=t.split(),[],""
    for w in ws:
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else:
            if cur: ls.append(cur)
            cur=w
    if cur: ls.append(cur)
    return ls

def panel(img_path, w, h, placeholder_label):
    if img_path:
        im = Image.open(img_path).convert("RGB")
        return ImageOps.fit(im,(w,h),method=Image.LANCZOS)
    # makieta
    im = Image.new("RGB",(w,h),(38,34,30))
    d=ImageDraw.Draw(im)
    # delikatna diagonalna tekstura
    for i in range(-h,w,26): d.line([(i,0),(i+h,h)],fill=(46,41,36),width=1)
    f=font(F_KICK,30)
    for k,ln in enumerate(placeholder_label):
        tw=ls_w(d,ln,f,4)
        text_ls(d,((w-tw)//2, h//2-30+k*44), ln, f, (170,160,146), 4)
    # ikonka ramki
    d.rectangle([w//2-34,h//2-96,w//2+34,h//2-44],outline=(150,140,126),width=2)
    return im

def make(before, after, style_label, headline, idx, out_name):
    im = Image.new("RGB",(W,H),CREAM)
    d  = ImageDraw.Draw(im,"RGBA")
    m  = 46
    # passe-partout
    d.rectangle([m,m,W-m-1,H-m-1],outline=(24,21,18,60),width=2)
    # N°
    f_idx=font(F_KICK,34)
    text_ls(d,(m+34,m+26),f"N° {idx}",f_idx,(24,21,18,180),3)
    d.line([(m+34,m+74),(m+34+150,m+74)],fill=(196,162,96,200),width=1)

    # --- HERO: dwa panele przed|po ---
    gx0,gy0 = m+34, m+96
    gx1,gy1 = W-m-34, m+96+690
    pw = (gx1-gx0-6)//2
    ph = gy1-gy0
    left  = panel(before, pw, ph, ["TWOJE", "ZDJĘCIE"])
    right = panel(after,  pw, ph, ["PO", "PRZERÓBCE"])
    im.paste(left,(gx0,gy0)); im.paste(right,(gx0+pw+6,gy0))
    # zlota linia podzialu
    d.rectangle([gx0+pw, gy0, gx0+pw+6, gy1], fill=(196,162,96,255))
    # ramka wokol hero
    d.rectangle([gx0,gy0,gx1-1,gy1-1],outline=(238,232,222,90),width=1)
    # etykiety PRZED / PO (pigulki)
    def pillbl(cx_center, ytop, label):
        f=font(F_KICK,30); tw=ls_w(d,label,f,4)
        pad=22; w=tw+pad*2; h=52; x0=cx_center-w/2
        d.rounded_rectangle([x0,ytop,x0+w,ytop+h],26,fill=(24,21,18,205))
        text_ls(d,(x0+pad,ytop+9),label,f,(238,232,222,255),4)
    pillbl(gx0+pw/2, gy1-70, "PRZED")
    pillbl(gx0+pw+6+pw/2, gy1-70, "PO")

    # --- BLOK TEKSTU ---
    padx=m+34
    y=H-m-40
    # marka
    f_b=font(F_HEAD,40); f_dom=font(F_SUB,32)
    bx=text_ls(d,(padx,y-52),"PixelPędzel",f_b,(24,21,18,255),1)
    d.text((bx+22,y-44),"·",font=f_dom,fill=(196,162,96,255))
    d.text((bx+46,y-44),"pixelpedzel.pl",font=f_dom,fill=(90,82,72,255))
    y-=92
    d.line([(padx,y),(W-m-34,y)],fill=(24,21,18,45),width=1); y-=30
    # sub = etykieta stylu + zachęta
    f_s=font(F_SUB,34)
    sub=f"Styl: {style_label}. Podgląd przed drukiem — płacisz, gdy Ci się spodoba."
    for ln in reversed(wrap(d,sub,f_s,W-2*padx)):
        y-=48; d.text((padx,y),ln,font=f_s,fill=(70,63,55,255))
    y-=22
    # headline
    f_h=font(F_HEAD,76)
    for ln in reversed(wrap(d,headline,f_h,W-2*padx)):
        y-=86; d.text((padx,y),ln,font=f_h,fill=(24,21,18,255))
    y-=18
    # kicker
    f_k=font(F_KICK,32); kick="METAMORFOZA"
    text_ls(d,(padx,y-40),kick,f_k,(196,162,96,255),5)
    d.line([(padx,y-56),(padx+90,y-56)],fill=(196,162,96,220),width=2)

    im.save(os.path.join(OUT,out_name),quality=94)
    print("OK", out_name)

if __name__ == "__main__":
    # makieta ukladu (bez zdjec)
    make(None, None, "Olej klasyczny", "Z jednego zdjęcia — dzieło.", "00", "compare-makieta.png")
