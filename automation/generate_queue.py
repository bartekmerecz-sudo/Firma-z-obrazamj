#!/usr/bin/env python3
"""Generuje harmonogram postow (queue.json): 1 post dziennie, rotacja z content.py.

Uzycie:
  python3 automation/generate_queue.py 2026-07-22 28
  (start = data pierwszego postu, 28 = liczba dni)

Domyslnie: start = jutro, 28 dni. Instagram wlaczamy, jesli chcesz (INSTAGRAM=1).
KROK_WIDEO ustawia, co ktory dzien idzie film (domyslnie 2).

ZACHOWAJ=1 dokleja z przodu wpisy z istniejacego queue.json, ktore juz sie
odbyly (data < start). Bez tego przegenerowanie kolejki w polowie sezonu
kasuje historie i robot nie wie, co juz poszlo.

Posty z oknem sezonowym (czwarty element wpisu w content.py) trafiaja tylko
w te dni, ktore mieszcza sie w oknie — i w swoim sezonie maja pierwszenstwo
przed zwykla rotacja, nie czesciej niz co ODSTEP_SEZON dni.

OD_POSTU=post-ktore-zdjecie ustawia, od ktorej grafiki rusza rotacja, a
OD_FILMU=bold-projekt-dzis to samo dla filmow. Przydaje sie po dopisaniu nowej
partii na koniec content.py: bez tego czekaja w kolejce za cala reszta nawet
miesiac.
"""
import json, os, sys
from datetime import date, timedelta
from content import POSTS

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    start = sys.argv[1] if len(sys.argv) > 1 else (date.today() + timedelta(days=1)).isoformat()
    days  = int(sys.argv[2]) if len(sys.argv) > 2 else 28
    post_time = os.environ.get("POST_TIME", "11:00")   # tylko informacyjnie
    with_ig   = os.environ.get("INSTAGRAM", "0") == "1"
    platforms = ["facebook"] + (["instagram"] if with_ig else [])

    y, m, dd = map(int, start.split("-"))
    d0 = date(y, m, dd)

    def okno(post):
        return post[3] if len(post) >= 4 and post[3] else None

    def pasuje(post, dzien):
        """Post bez okna leci zawsze; z oknem — tylko w swoim sezonie."""
        w = okno(post)
        return True if w is None else w[0] <= dzien.isoformat() <= w[1]

    # Co ktory dzien idzie film. Reelsy dowoza wyraznie lepszy zasieg niz
    # grafiki, wiec domyslnie co drugi dzien; KROK_WIDEO=3 wraca do poprzedniego
    # ukladu, a 0 wylacza filmy calkiem.
    krok_wideo = int(os.environ.get("KROK_WIDEO", "2"))
    images = [p for p in POSTS if p[0] == "image"]
    videos = [p for p in POSTS if p[0] == "video"]

    # Rotacja musi ruszyc tam, gdzie skonczyla poprzednia kolejka. Inaczej
    # przegenerowanie w polowie sezonu cofa nas na poczatek listy i nowo
    # dopisane posty czekaja na swoja kolej szesc tygodni.
    idx = {"image": 0, "video": 0}
    if os.environ.get("ZACHOWAJ") == "1":
        stary = os.path.join(HERE, "queue.json")
        if os.path.exists(stary):
            with open(stary, encoding="utf-8") as fh:
                for w in json.load(fh):
                    if w["date"] < start:
                        idx[w["type"]] = idx.get(w["type"], 0) + 1

    def ustaw_start(zmienna, pula, klucz, co):
        wzor = os.environ.get(zmienna, "")
        if not wzor:
            return
        trafione = [i for i, p in enumerate(pula) if wzor in p[1]]
        if not trafione:
            sys.exit(f"{zmienna}={wzor}: nie ma takiego pliku w content.py")
        idx[klucz] = trafione[0]
        print(f"Rotacja {co} rusza od: {pula[trafione[0]][1]}")

    ustaw_start("OD_POSTU", images, "image", "grafik")
    ustaw_start("OD_FILMU", videos, "video", "filmow")

    ODSTEP_SEZON = 7     # dni miedzy powtorzeniami postu sezonowego

    def wez(pula, dzien, klucz, ostatnio):
        """Najpierw sezon, potem zwykla rotacja.

        Post z oknem ma pierwszenstwo w swoim sezonie — inaczej przy puli
        czterdziestu grafik ogloszenie o terminie zamowien na swieta poszloby
        raz na caly listopad i grudzien. Powtarzamy go nie czesciej niz co
        ODSTEP_SEZON dni, zeby nie zalac nim tablicy."""
        dzis = dzien.toordinal()
        sezonowe = [p for p in pula if okno(p) and pasuje(p, dzien)
                    and dzis - ostatnio.get(p[1], -999) >= ODSTEP_SEZON]
        if sezonowe:
            return min(sezonowe, key=lambda p: ostatnio.get(p[1], -999))

        for _ in range(len(pula)):
            p = pula[idx[klucz] % len(pula)]
            idx[klucz] += 1
            if pasuje(p, dzien):
                return p
        return next((p for p in pula if pasuje(p, dzien)), pula[0])

    seq, ostatnio = [], {}
    for i in range(days):
        dzien = d0 + timedelta(days=i)
        film = videos and krok_wideo > 0 and i % krok_wideo == krok_wideo - 1
        pula, klucz = (videos, "video") if film else (images, "image")
        p = wez(pula, dzien, klucz, ostatnio)
        ostatnio[p[1]] = dzien.toordinal()
        seq.append(p)

    queue = []
    for i in range(days):
        typ, media, text = seq[i][:3]
        queue.append({
            "date": (d0 + timedelta(days=i)).isoformat(),
            "time": post_time,
            "type": typ,
            "media": media,
            "platforms": platforms,
            "text": text,
        })
    if os.environ.get("ZACHOWAJ") == "1":
        stary = os.path.join(HERE, "queue.json")
        if os.path.exists(stary):
            with open(stary, encoding="utf-8") as f:
                przeszle = [w for w in json.load(f) if w["date"] < start]
            queue = przeszle + queue
            print(f"Zachowano {len(przeszle)} wpisow sprzed {start}")

    out = os.path.join(HERE, "queue.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
    print(f"Zapisano {len(queue)} postow -> {out}")
    print(f"Od {queue[0]['date']} do {queue[-1]['date']} | platformy: {platforms}")

if __name__ == "__main__":
    main()
