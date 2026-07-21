#!/usr/bin/env python3
"""Filmy promocyjne PRZED -> PO (metamorfoza zdjecie->dzielo) na TikTok/Reels.
Pionowe 1080x1920. Reveal przez wipe (ffmpeg xfade). Styl Quiet Heirloom:
Gloock/Outfit/ArsenalSC, cieple scrimy, hairline ramka, zlote akcenty."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "assets", "video")
TMP  = os.path.join(ROOT, "tools", "_vframes")
FONTS= "/root/.claude/skills/canvas-design/canvas-fonts"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
CREAM=(238,232,222); INK=(20,18,16); GOLD=(196,162,96)
F_HEAD=os.path.join(FONTS,"Gloock-Regular.ttf")
F_KICK=os.path.join(FONTS,"ArsenalSC-Regular.ttf")
F_SUB =os.path.join(FONTS,"Outfit-Regular.ttf")
F_SUBB=os.path.join(FONTS,"Outfit-Bold.ttf")
def font(p,s): return ImageFont.truetype(p,s)

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
def text_ls(d,xy,t,f,fill,ls=0):
    x,y=xy
    for ch in t: d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+ls
    return x
def ls_w(d,t,f,ls=0): return sum(d.textlength(c,font=f)+ls for c in t)-(ls if t else 0)
def center_ls(d,y,t,f,fill,ls=0):
    x=(W-ls_w(d,t,f,ls))//2; text_ls(d,(x,y),t,f,fill,ls); return x

def grad_v(top_h, bot_h, top_a=210, bot_a=235):
    """maska ciemnosci: gora i dol."""
    m=Image.new("L",(1,H),0)
    for y in range(H):
        a=0
        if y<top_h: a=int(top_a*(1-y/top_h)**1.3)
        if y>H-bot_h:
            t=(y-(H-bot_h))/bot_h; a=max(a,int(bot_a*(t*t*(3-2*t))))
        m.putpixel((0,y),a)
    return m.resize((W,H))

def frame(img_path, kicker, label, hook=None):
    im=ImageOps.fit(Image.open(img_path).convert("RGB"),(W,H),method=Image.LANCZOS)
    sc=grad_v(int(H*0.34), int(H*0.30))
    im=Image.composite(Image.new("RGB",(W,H),INK), im, sc)
    d=ImageDraw.Draw(im,"RGBA")
    m=40
    d.rectangle([m,m,W-m-1,H-m-1],outline=(238,232,222,140),width=2)
    # gora: kicker + hook
    if kicker:
        fk=font(F_KICK,40); center_ls(d,90,kicker.upper(),fk,(196,162,96,255),6)
    if hook:
        fh=font(F_HEAD,96); lns=wrap(d,hook,fh,W-180); y=150
        for ln in lns:
            x=(W-d.textlength(ln,font=fh))//2
            d.text((x+2,y+2),ln,font=fh,fill=(0,0,0,160)); d.text((x,y),ln,font=fh,fill=(240,235,227,255)); y+=104
    # dol: pigulka label + marka
    if label:
        fl=font(F_KICK,44); tw=ls_w(d,label,fl,4); pad=34; w=tw+pad*2; h=76; x0=(W-w)//2; y0=H-300
        d.rounded_rectangle([x0,y0,x0+w,y0+h],38,fill=(20,18,16,215))
        text_ls(d,(x0+pad,y0+14),label,fl,(238,232,222,255),4)
    fb=font(F_HEAD,52); dom=font(F_SUB,38)
    bt="PixelPędzel"; bx=(W-(d.textlength(bt,font=fb)+ d.textlength("  ·  pixelpedzel.pl",font=dom)))//2
    x=text_ls(d,(bx,H-190),bt,fb,(238,232,222,255),1)
    d.text((x+16,H-176),"·  pixelpedzel.pl",font=dom,fill=(210,196,160,255))
    return im.convert("RGB")

def cta():
    im=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([50,50,W-50-1,H-50-1],outline=(196,162,96,255),width=3)
    center_ls(d,360,"PIXELPĘDZEL",font(F_KICK,46),(196,162,96,255),8)
    fh=font(F_HEAD,92); y=470
    for ln in ["Zamień swoje","zdjęcie w dzieło."]:
        x=(W-d.textlength(ln,font=fh))//2; d.text((x,y),ln,font=fh,fill=(240,235,227,255)); y+=104
    fs=font(F_SUB,44); y+=20
    for ln in ["Zobaczysz projekt przed drukiem.","Płacisz, gdy Ci się spodoba."]:
        x=(W-d.textlength(ln,font=fs))//2; d.text((x,y),ln,font=fs,fill=(214,207,196,255)); y+=58
    # pigulka kod
    fc=font(F_KICK,44); lab="-20% KODEM START20"; tw=ls_w(d,lab,fc,4); pad=36; w=tw+pad*2; hh=82; x0=(W-w)//2; y+=50
    d.rounded_rectangle([x0,y,x0+w,y+hh],40,fill=(196,162,96,255)); text_ls(d,(x0+pad,y+16),lab,fc,(20,18,16,255),4)
    fd=font(F_HEAD,64); dm="pixelpedzel.pl"; d.text(((W-d.textlength(dm,font=fd))//2,H-320),dm,font=fd,fill=(196,162,96,255))
    fl=font(F_SUB,40); lk="kliknij link w bio ↑"; d.text(((W-d.textlength(lk,font=fl))//2,H-230),lk,font=fl,fill=(200,192,178,255))
    return im

def build(name, frames, durs, trans):
    """frames: list PIL; durs: sek na scene; trans: lista przejsc miedzy scenami."""
    paths=[]
    for i,s in enumerate(frames):
        p=os.path.join(TMP,f"{name}_{i}.png"); s.save(p); paths.append(p)
    fps=30; fade=0.6
    inputs=[]
    for p,dl in zip(paths,durs): inputs+=["-loop","1","-t",str(dl),"-i",p]
    n=len(paths); fc=[f"[{i}:v]scale={W}:{H},setsar=1,fps={fps}[v{i}]" for i in range(n)]
    prev="v0"; cum=durs[0]; chain=[]
    for i in range(1,n):
        off=cum-fade; out=f"x{i}"
        chain.append(f"[{prev}][v{i}]xfade=transition={trans[i-1]}:duration={fade}:offset={off:.3f}[{out}]")
        prev=out; cum+=durs[i]-fade
    outp=os.path.join(OUT,f"{name}.mp4")
    subprocess.run([FFMPEG,"-y",*inputs,"-filter_complex",";".join(fc+chain),
        "-map",f"[{prev}]","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast","-r",str(fps),outp],
        check=True,capture_output=True)
    print("OK",name+".mp4", round(os.path.getsize(outp)/1024),"KB, ~",round(cum,1),"s")

def main():
    U=os.path.join(ROOT,"assets","uploads")
    # Film 1: para przy zielonej scianie -> wektor -> bajka 3D
    build("tt-metamorfoza-wektor3d",
      [ frame(f"{U}/para1-przed.jpg","1 zdjęcie, różne style","PRZED", hook="Zwykłe zdjęcie?"),
        frame(f"{U}/para1-wektor-clean.png",None,"PO · WEKTOR"),
        frame(f"{U}/para1-bajka3d-clean.png",None,"PO · BAJKOWY 3D"),
        cta() ],
      [2.4,2.4,2.6,3.0], ["wipeleft","wipeleft","fade"])
    # Film 2: para na pomoscie -> komiks -> lego
    build("tt-metamorfoza-komikslego",
      [ frame(f"{U}/para2-przed.jpg","1 zdjęcie, różne style","PRZED", hook="A może dzieło?"),
        frame(f"{U}/para2-komiks-clean.png",None,"PO · POP-ART"),
        frame(f"{U}/para2-lego-clean.png",None,"PO · KLOCKI"),
        cta() ],
      [2.4,2.4,2.6,3.0], ["wipeleft","wipeleft","fade"])

if __name__=="__main__":
    main()
