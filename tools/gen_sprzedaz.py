#!/usr/bin/env python3
"""Posty SPRZEDAZOWE (nie "ladny styl", tylko: zdejmij obiekcje i daj powod do zakupu).
Styl Quiet Heirloom, format feed 1080x1350.

Dotychczasowe posty pokazywaly STYLE. Te posty odpowiadaja na realne blokady zakupu:
  - "nie wiem czy wyjdzie"      -> podglad przed zaplata
  - "nie wiem ile kosztuje"     -> jawny cennik
  - "nie wiem jak to dziala"    -> 3 kroki
  - "nikt tego nie kupil"       -> oferta zalozycielska (pierwsi klienci)
  - "nie mam okazji"            -> sezon (wakacje, sluby)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import gen_compare as G

W, H = G.W, G.H
CREAM, INK, GOLD = G.CREAM, G.INK, G.GOLD
font, text_ls, ls_w, wrap = G.font, G.text_ls, G.ls_w, G.wrap
F_HEAD, F_KICK, F_SUB = G.F_HEAD, G.F_KICK, G.F_SUB
OUT = G.OUT
ROOT = G.ROOT
# final/, nie uploads/ — surowe rendery maja w rogu znak wodny generatora.
U = os.path.join(ROOT, "assets", "uploads", "final")


def center_ls(d, y, t, f, fill, ls=0):
    tw = ls_w(d, t, f, ls)
    return text_ls(d, ((W - tw) // 2, y), t, f, fill, ls)


def base(dark=False):
    bg = Image.new("RGB", (W, H), INK if dark else CREAM)
    d = ImageDraw.Draw(bg, "RGBA")
    edge = (196, 162, 96, 255) if dark else (196, 162, 96, 190)
    d.rectangle([44, 44, W - 45, H - 45], outline=edge, width=3)
    return bg, d


def brand(d, dark=False):
    fb, fd = font(F_HEAD, 44), font(F_SUB, 30)
    col = (238, 232, 222, 255) if dark else (40, 34, 28, 255)
    t = "PixelPędzel"
    tw = ls_w(d, t, fb, 1) + d.textlength("  ·  pixelpedzel.pl", font=fd)
    x = text_ls(d, ((W - tw) // 2, H - 132), t, fb, col, 1)
    d.text((x + 14, H - 120), "·  pixelpedzel.pl", font=fd, fill=(160, 130, 78, 255))


def rule(d, y, w=80):
    d.line([(W // 2 - w, y), (W // 2 + w, y)], fill=(196, 162, 96, 230), width=2)


def headline(d, y, lines, size=88, dark=False):
    f = font(F_HEAD, size)
    col = (240, 235, 227, 255) if dark else (24, 21, 18, 255)
    for ln in lines:
        center_ls(d, y, ln, f, col, 0)
        y += int(size * 1.22)
    return y


def canvas_on_wall(img_path, w, h, depth=18):
    front = ImageOps.fit(Image.open(img_path).convert("RGB"), (w, h), Image.LANCZOS)
    tex = Image.effect_noise((w, h), 14).convert("RGB")
    front = Image.blend(front, tex, 0.05)
    side = front.point(lambda p: int(p * 0.55))
    cv = Image.new("RGBA", (w + depth, h + depth), (0, 0, 0, 0))
    cv.paste(side, (depth, depth))
    cv.paste(front, (0, 0))
    return cv


def paste_canvas(bg, cv, cx, cy):
    cw, ch = cv.size
    x, y = cx - cw // 2, cy - ch // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [x + 12, y + 22, x + cw + 12, y + ch + 22], 8, fill=(30, 24, 18, 130))
    bg = Image.alpha_composite(bg.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(22)))
    bg.alpha_composite(cv, (x, y))
    return bg.convert("RGB")


# ---------------------------------------------------------------- POSTY

def p_oferta_start():
    """Post nr 1 dla firmy bez klientow: oferta zalozycielska."""
    bg, d = base(dark=True)
    center_ls(d, 150, "OFERTA ZAŁOŻYCIELSKA", font(F_KICK, 40), GOLD, 6)
    rule(d, 214)
    headline(d, 268, ["Szukam 5 osób,", "które chcą swój", "obraz taniej."], 92, dark=True)
    fs = font(F_SUB, 38)
    body = ["Startuję z pracownią i buduję portfolio.", "Pierwsze 5 zamówień realizuję",
            "ze zniżką — w zamian proszę o zdjęcie", "obrazu na Waszej ścianie i szczerą opinię."]
    y = 700
    for ln in body:
        tw = d.textlength(ln, font=fs)
        d.text(((W - tw) // 2, y), ln, font=fs, fill=(214, 208, 198, 255)); y += 54
    d.rounded_rectangle([220, 950, W - 220, 1060], 10, fill=(196, 162, 96, 255))
    fb = font(F_SUB, 40)
    t = "Napisz: CHCĘ"
    d.text(((W - d.textlength(t, font=fb)) // 2, 978), t, font=fb, fill=(24, 21, 18, 255))
    brand(d, dark=True)
    return bg, "post-oferta-start.png"


def p_bez_ryzyka():
    """Zdejmuje najwieksza obiekcje: 'a jak mi sie nie spodoba?'"""
    bg, d = base()
    center_ls(d, 150, "BEZ RYZYKA", font(F_KICK, 40), GOLD, 6)
    rule(d, 214)
    headline(d, 276, ["Najpierw", "zobacz obraz.", "Potem zapłać."], 94)
    fs = font(F_SUB, 38)
    pts = ["Przysyłasz zdjęcie — za darmo.",
           "Robię projekt i pokazuję Ci podgląd.",
           "Nie podoba się? Nie płacisz. Koniec.",
           "Podoba się? Dopiero wtedy drukuję."]
    y = 740
    for p in pts:
        d.ellipse([150, y + 14, 168, y + 32], fill=(196, 162, 96, 255))
        d.text((196, y), p, font=fs, fill=(52, 46, 38, 255)); y += 66
    brand(d)
    return bg, "post-bez-ryzyka.png"


def p_cennik():
    bg, d = base()
    center_ls(d, 150, "CENNIK", font(F_KICK, 40), GOLD, 6)
    rule(d, 214)
    headline(d, 274, ["Ile to kosztuje?"], 92)
    rows = [("30 × 40 cm", "129 zł"), ("40 × 50 cm", "169 zł"),
            ("50 × 70 cm", "229 zł"), ("60 × 90 cm", "299 zł")]
    fr, fp = font(F_SUB, 46), font(F_HEAD, 50)
    y = 470
    for name, price in rows:
        d.text((176, y), name, font=fr, fill=(52, 46, 38, 255))
        pw = d.textlength(price, font=fp)
        d.text((W - 176 - pw, y - 4), price, font=fp, fill=(24, 21, 18, 255))
        y += 86
        d.line([(176, y - 16), (W - 176, y - 16)], fill=(196, 162, 96, 110), width=1)
    fs = font(F_SUB, 36)
    for k, ln in enumerate(["Projekt i podgląd — gratis.",
                            "Dostawa 15 zł · od 250 zł gratis.",
                            "Płacisz dopiero gdy zaakceptujesz projekt."]):
        tw = d.textlength(ln, font=fs)
        d.text(((W - tw) // 2, 880 + k * 52), ln, font=fs, fill=(96, 86, 72, 255))
    brand(d)
    return bg, "post-cennik.png"


def p_jak_dziala():
    bg, d = base()
    center_ls(d, 150, "JAK TO DZIAŁA", font(F_KICK, 40), GOLD, 6)
    rule(d, 214)
    headline(d, 274, ["Trzy kroki", "do obrazu."], 92)
    steps = [("01", "Wysyłasz zdjęcie", "Telefonem, e-mailem — jak wygodnie."),
             ("02", "Wybierasz styl", "13 stylów: olej, komiks, szkic, witraż…"),
             ("03", "Odbierasz obraz", "Gotowy na płótnie, do powieszenia.")]
    fn, ft, fd_ = font(F_HEAD, 62), font(F_SUB, 44), font(F_SUB, 33)
    y = 560
    for num, title, desc in steps:
        d.text((172, y - 6), num, font=fn, fill=(196, 162, 96, 255))
        d.text((286, y), title, font=ft, fill=(24, 21, 18, 255))
        d.text((286, y + 54), desc, font=fd_, fill=(102, 92, 78, 255))
        y += 148
    brand(d)
    return bg, "post-jak-dziala.png"


def p_wakacje():
    """Sezonowy hak: lipiec/sierpien — powrot z wakacji."""
    src = os.path.join(U, "para3-olej-clean.png")
    bg = Image.new("RGB", (W, H), CREAM)
    if os.path.exists(src):
        bg = paste_canvas(bg, canvas_on_wall(src, 600, 740, 18), W // 2, 590)
    d = ImageDraw.Draw(bg, "RGBA")
    d.rectangle([44, 44, W - 45, H - 45], outline=(196, 162, 96, 190), width=3)
    center_ls(d, 128, "PO WAKACJACH", font(F_KICK, 38), GOLD, 6)
    headline(d, 1012, ["1200 zdjęć w telefonie.", "Jedno zasługuje na ścianę."], 56)
    brand(d)
    return bg, "post-wakacje.png"


def p_slub():
    src = os.path.join(U, "para1-wektor-clean.png")
    bg = Image.new("RGB", (W, H), CREAM)
    if os.path.exists(src):
        bg = paste_canvas(bg, canvas_on_wall(src, 600, 740, 18), W // 2, 590)
    d = ImageDraw.Draw(bg, "RGBA")
    d.rectangle([44, 44, W - 45, H - 45], outline=(196, 162, 96, 190), width=3)
    center_ls(d, 128, "SEZON ŚLUBNY", font(F_KICK, 38), GOLD, 6)
    headline(d, 1012, ["Prezent ślubny, którego", "nie schowają do szafy."], 56)
    brand(d)
    return bg, "post-slub.png"


def p_ktory_styl():
    """Post na ZAANGAZOWANIE — komentarze podbijaja zasieg."""
    bg, d = base(dark=True)
    center_ls(d, 140, "PYTANIE DO WAS", font(F_KICK, 40), GOLD, 6)
    rule(d, 204)
    headline(d, 258, ["Który styl", "wybralibyście", "dla siebie?"], 92, dark=True)
    opts = [("A", "Olej klasyczny"), ("B", "Pop-art komiks"),
            ("C", "Szkic ołówkiem"), ("D", "Witraż")]
    fl, ft = font(F_HEAD, 56), font(F_SUB, 44)
    y = 720
    for letter, name in opts:
        d.ellipse([182, y - 6, 246, y + 58], outline=(196, 162, 96, 255), width=3)
        lw = d.textlength(letter, font=fl)
        d.text((214 - lw / 2, y - 4), letter, font=fl, fill=(196, 162, 96, 255))
        d.text((292, y + 4), name, font=ft, fill=(226, 220, 210, 255))
        y += 96
    fs = font(F_SUB, 34)
    t = "Napiszcie literę w komentarzu"
    d.text(((W - d.textlength(t, font=fs)) // 2, 1128), t, font=fs, fill=(170, 160, 146, 255))
    brand(d, dark=True)
    return bg, "post-ktory-styl.png"


def p_prezent_last():
    bg, d = base(dark=True)
    center_ls(d, 160, "NA PREZENT", font(F_KICK, 40), GOLD, 6)
    rule(d, 224)
    headline(d, 300, ["Kwiaty zwiędną.", "Perfumy się skończą.", "Obraz zostanie."], 86, dark=True)
    fs = font(F_SUB, 38)
    for k, ln in enumerate(["Rocznica · urodziny · ślub · Dzień Matki",
                            "Nie masz pomysłu? Weź bon —", "obdarowany sam wybierze zdjęcie i styl."]):
        tw = d.textlength(ln, font=fs)
        d.text(((W - tw) // 2, 880 + k * 56), ln, font=fs, fill=(214, 208, 198, 255))
    brand(d, dark=True)
    return bg, "post-prezent-argument.png"


BUILDERS = [p_oferta_start, p_bez_ryzyka, p_cennik, p_jak_dziala,
            p_wakacje, p_slub, p_ktory_styl, p_prezent_last]


def main():
    os.makedirs(OUT, exist_ok=True)
    for b in BUILDERS:
        img, name = b()
        img.save(os.path.join(OUT, name), quality=95)
        print("  +", name)


if __name__ == "__main__":
    main()
