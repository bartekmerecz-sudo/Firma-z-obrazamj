#!/usr/bin/env python3
"""Robot publikujacy PixelPedzel.
Czyta queue.json, znajduje posty na DZIS (strefa Europe/Warsaw) i publikuje je
na Facebooku (strona) oraz opcjonalnie na Instagramie — przez oficjalne API Meta.

Uruchamiany automatycznie codziennie przez GitHub Actions.

Sekrety (ustawiane w GitHub -> Settings -> Secrets):
  FB_PAGE_ID      – ID Twojej strony na Facebooku (wymagane)
  FB_PAGE_TOKEN   – dlugozyciowy token strony (wymagane)
  IG_USER_ID      – ID konta Instagram Business (opcjonalne)
  SITE_BASE_URL   – adres, spod ktorego serwowane sa pliki (domyslnie https://pixelpedzel.pl)

Tryb testowy bez publikacji:  DRY_RUN=1 python3 automation/post.py
Wymuszenie konkretnej daty:   POST_DATE=2026-07-22 python3 automation/post.py
"""
import json, os, sys, time, urllib.request, urllib.parse

API = "https://graph.facebook.com/v21.0"
HERE = os.path.dirname(os.path.abspath(__file__))

DRY = os.environ.get("DRY_RUN", "0") == "1"
BASE = (os.environ.get("SITE_BASE_URL") or "https://pixelpedzel.pl").rstrip("/")
PAGE_ID = os.environ.get("FB_PAGE_ID", "")
PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN", "")
IG_ID = os.environ.get("IG_USER_ID", "")


def today_warsaw():
    if os.environ.get("POST_DATE"):
        return os.environ["POST_DATE"]
    try:
        from zoneinfo import ZoneInfo
        from datetime import datetime
        return datetime.now(ZoneInfo("Europe/Warsaw")).date().isoformat()
    except Exception:
        from datetime import datetime, timezone, timedelta
        return (datetime.now(timezone.utc) + timedelta(hours=2)).date().isoformat()


def http_post(url, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def http_get(url, params):
    q = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{url}?{q}", timeout=60) as r:
        return json.loads(r.read().decode())


def media_url(path):
    return f"{BASE}/{path.lstrip('/')}"


# ---------- FACEBOOK ----------
def fb_post(item):
    url_media = media_url(item["media"])
    if item["type"] == "image":
        res = http_post(f"{API}/{PAGE_ID}/photos", {
            "url": url_media, "message": item["text"], "access_token": PAGE_TOKEN})
    else:
        res = http_post(f"{API}/{PAGE_ID}/videos", {
            "file_url": url_media, "description": item["text"], "access_token": PAGE_TOKEN})
    print("  [FB] ok:", res)


# ---------- INSTAGRAM ----------
def ig_post(item):
    url_media = media_url(item["media"])
    if item["type"] == "image":
        cont = http_post(f"{API}/{IG_ID}/media", {
            "image_url": url_media, "caption": item["text"], "access_token": PAGE_TOKEN})
    else:
        cont = http_post(f"{API}/{IG_ID}/media", {
            "media_type": "REELS", "video_url": url_media,
            "caption": item["text"], "access_token": PAGE_TOKEN})
    cid = cont["id"]
    # wideo trzeba poczekac az sie przetworzy
    for _ in range(20):
        st = http_get(f"{API}/{cid}", {"fields": "status_code", "access_token": PAGE_TOKEN})
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            raise RuntimeError(f"IG przetwarzanie bledne: {st}")
        time.sleep(15)
    res = http_post(f"{API}/{IG_ID}/media_publish", {
        "creation_id": cid, "access_token": PAGE_TOKEN})
    print("  [IG] ok:", res)


def main():
    with open(os.path.join(HERE, "queue.json"), encoding="utf-8") as f:
        queue = json.load(f)
    day = today_warsaw()
    due = [x for x in queue if x["date"] == day]
    print(f"Dzis: {day} | postow na dzis: {len(due)} | DRY_RUN={DRY}")
    if not due:
        print("Brak postow na dzis. Koniec.")
        return

    if not DRY and (not PAGE_ID or not PAGE_TOKEN):
        print("BLAD: brak FB_PAGE_ID / FB_PAGE_TOKEN. Ustaw sekrety w GitHub.")
        sys.exit(1)

    errors = 0
    for item in due:
        print(f"- {item['type']}: {item['media']}")
        print(f"  tekst: {item['text'][:70]}...")
        if DRY:
            print("  (DRY_RUN — nie publikuje, tylko podglad)")
            print("  media_url:", media_url(item["media"]))
            continue
        try:
            if "facebook" in item["platforms"]:
                fb_post(item)
            if "instagram" in item["platforms"] and IG_ID:
                ig_post(item)
        except Exception as e:
            errors += 1
            print("  BLAD publikacji:", e)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
