#!/usr/bin/env python3
"""Filmy: (1) 'na prezent' — okazje + obraz jako prezent, (2) realistyczny obraz
na plotnie (galeryjny wrap + faktura plotna + cien na scianie). Styl Quiet Heirloom."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_compare_video as G
from PIL import Image, ImageDraw, ImageOps, ImageFilter

W, H = G.W, G.H
GOLD=(196,162,96); INK=(24,21,18)
font=G.font; text_ls=G.text_ls; center_ls=G.center_ls; wrap=G.wrap
F_HEAD=G.F_HEAD; F_KICK=G.F_KICK; F_SUB=G.F_SUB
U=os.path.join(G.ROOT,"assets","uploads")

def wall_bg(warm=True):
    col=Image.new("RGB",(1,H)); p=col.load()
    for y in range(H):
        t=y/H; p[0,y]=(int(236-34*t),int(230-36*t),int(220-38*t))
    return col.resize((W,H))

def canvas_print(img_path, w, h, depth=20):
    """Realistyczny galeryjny wrap: front + boczna krawedz (glebia) + faktura plotna."""
    front=ImageOps.fit(Image.open(img_path).convert("RGB"),(w,h),Image.LANCZOS)
    # faktura plotna (szybki szum -> delikatny splot)
    tex=Image.effect_noise((w,h),14).convert("RGB")
    front=Image.blend(front, tex, 0.05)
    # blok z glebia: ciemniejszy front przesuniety w prawo-dol = grubosc plotna
    side=front.point(lambda p:int(p*0.55))
    canvas=Image.new("RGBA",(w+depth,h+depth),(0,0,0,0))
    canvas.paste(side,(depth,depth))
    canvas.paste(front,(0,0))
    return canvas

def place_on_wall(bg, canvas_rgba, cx, cy):
    cw,ch=canvas_rgba.size; x=cx-cw//2; y=cy-ch//2
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.rounded_rectangle([x+14,y+26,x+cw+14,y+ch+26],8,fill=(30,24,18,150))
    bg=Image.alpha_composite(bg.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(24)))
    bg.alpha_composite(canvas_rgba,(x,y))
    return bg.convert("RGB")

def brand(d, dark_wall=False):
    fb=font(F_HEAD,52); dom=font(F_SUB,38)
    col=(40,34,28,255) if not dark_wall else (238,232,222,255)
    bt="PixelPędzel"; bx=(W-(d.textlength(bt,font=fb)+d.textlength("  ·  pixelpedzel.pl",font=dom)))//2
    x=text_ls(d,(bx,H-200),bt,fb,col,1)
    d.text((x+16,H-186),"·  pixelpedzel.pl",font=dom,fill=(150,120,70,255))

def scene_wall(img_path, kicker):
    bg=wall_bg()
    cv=canvas_print(img_path, 660, 880, depth=22)
    bg=place_on_wall(bg, cv, W//2, 720)
    d=ImageDraw.Draw(bg,"RGBA")
    fk=font(F_KICK,42); center_ls(d,190,kicker.upper(),fk,GOLD,6)
    d.line([(W//2-70,246),(W//2+70,246)],fill=(196,162,96,220),width=2)
    brand(d)
    return bg

def scene_occasions():
    bg=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(bg,"RGBA")
    d.rectangle([50,50,W-50-1,H-50-1],outline=(196,162,96,255),width=3)
    center_ls(d,300,"IDEALNY PREZENT NA",font(F_KICK,42),GOLD,6)
    fh=font(F_HEAD,86); items=["Rocznicę ślubu","Urodziny","Dzień Matki","Święta","Ślub i zaręczyny"]
    y=470
    for it in items:
        tw=d.textlength(it,font=fh); x=(W-tw)//2
        d.ellipse([x-46,y+30,x-22,y+54],fill=(196,162,96,255))
        d.text((x,y),it,font=fh,fill=(240,235,227,255)); y+=118
    brand(d, dark_wall=True)
    return bg

def scene_gift(img_path):
    """Obraz na plotnie z 'metka prezentowa'."""
    bg=wall_bg()
    cv=canvas_print(img_path, 600, 800, depth=20)
    bg=place_on_wall(bg, cv, W//2, 700)
    d=ImageDraw.Draw(bg,"RGBA")
    fk=font(F_KICK,42); center_ls(d,180,"PREZENT, KTÓRY ZOSTAJE NA LATA",font(F_KICK,38),GOLD,4)
    d.line([(W//2-70,232),(W//2+70,232)],fill=(196,162,96,220),width=2)
    # metka prezentowa (sznurek + kartonik)
    tagx,tagy=W//2+250,470
    d.line([(W//2+120,410),(tagx,tagy)],fill=(120,100,60,255),width=3)
    d.rounded_rectangle([tagx-70,tagy,tagx+70,tagy+96],10,fill=(248,244,238,255),outline=(196,162,96,255),width=2)
    d.ellipse([tagx-8,tagy+10,tagx+8,tagy+26],outline=(150,120,70,255),width=2)
    fdla=font(F_KICK,26); wd=G.ls_w(d,"DLA",fdla,4); text_ls(d,(tagx-wd//2,tagy+34),"DLA",fdla,(120,100,70,255),4)
    ff=font(F_HEAD,40); w=d.textlength("Ciebie",font=ff); d.text((tagx-w//2,tagy+58),"Ciebie",font=ff,fill=(40,34,28,255))
    brand(d)
    return bg

def main():
    # FILM 1: NA PREZENT
    G.build("tt-na-prezent",
      [ G.frame(f"{U}/para4-vangogh-clean.png","Szukasz prezentu?","", hook="Nie wiesz, co kupić?"),
        scene_occasions(),
        scene_gift(f"{U}/para3-olej-clean.png"),
        G.cta() ],
      [2.5, 3.4, 3.0, 3.0], ["fade","fade","fade"])
    # FILM 2: REALISTYCZNIE NA PLOTNIE (showcase)
    G.build("tt-na-scianie",
      [ scene_wall(f"{U}/para3-olej-clean.png","Tak wygląda u Ciebie w domu"),
        scene_wall(f"{U}/para4-vangogh-clean.png","Prawdziwy obraz na płótnie"),
        scene_wall(f"{U}/para3-cyberpunk-clean.png","Gotowy do powieszenia"),
        G.cta() ],
      [2.8, 2.8, 2.8, 3.0], ["fade","fade","fade"])

if __name__=="__main__":
    main()
