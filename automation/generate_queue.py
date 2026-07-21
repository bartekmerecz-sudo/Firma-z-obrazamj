#!/usr/bin/env python3
"""Generuje harmonogram postow (queue.json): 1 post dziennie, rotacja z content.py.

Uzycie:
  python3 automation/generate_queue.py 2026-07-22 28
  (start = data pierwszego postu, 28 = liczba dni)

Domyslnie: start = jutro, 28 dni. Instagram wlaczamy, jesli chcesz (INSTAGRAM=1).
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
    queue = []
    for i in range(days):
        typ, media, text = POSTS[i % len(POSTS)]
        queue.append({
            "date": (d0 + timedelta(days=i)).isoformat(),
            "time": post_time,
            "type": typ,
            "media": media,
            "platforms": platforms,
            "text": text,
        })
    out = os.path.join(HERE, "queue.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
    print(f"Zapisano {len(queue)} postow -> {out}")
    print(f"Od {queue[0]['date']} do {queue[-1]['date']} | platformy: {platforms}")

if __name__ == "__main__":
    main()
