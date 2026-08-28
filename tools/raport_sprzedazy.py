#!/usr/bin/env python3
"""Raport sprzedazy ze Stripe — uruchamiany przez GitHub Actions.

Po co przez Actions, a nie wprost: siec tej sesji przepuszcza wylacznie
GitHuba (api.stripe.com jest zablokowane politykia egress). Zapytanie
wychodzi wiec z infrastruktury GitHuba, klucz siedzi w GitHub Secrets
i nigdy nie trafia do rozmowy.

Wynik idzie na stdout (czytelne z logu przebiegu) oraz do podsumowania
zadania. CELOWO nic nie zapisujemy w repozytorium — kwoty przychodu nie
maja po co siedziec w historii gita.

Wymaga sekretu STRIPE_RESTRICTED_KEY: klucz ograniczony, uprawnienia
tylko do odczytu (Stripe -> Developers -> API keys -> Restricted key).
Brak sekretu nie jest bledem — skrypt konczy sie zerem i mowi, czego brakuje.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.stripe.com/v1"
KEY = os.environ.get("STRIPE_RESTRICTED_KEY", "").strip()
DAY = 86400


def get(path, params):
    url = f"{API}/{path}?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def charges_since(ts):
    """Pobiera wszystkie obciazenia od znacznika czasu, ze stronicowaniem."""
    out, after = [], None
    while True:
        p = {"created[gte]": ts, "limit": 100}
        if after:
            p["starting_after"] = after
        d = get("charges", p)
        out += d.get("data", [])
        if not d.get("has_more"):
            return out
        after = out[-1]["id"]


def podsumuj(charges, od, do):
    ok = [c for c in charges
          if od <= c["created"] < do and c.get("paid") and c.get("status") == "succeeded"]
    kwota = sum(c["amount"] - c.get("amount_refunded", 0) for c in ok) / 100
    return len(ok), kwota


def main():
    if not KEY:
        print("Brak sekretu STRIPE_RESTRICTED_KEY — pomijam raport.")
        print("Dodaj go w: Settings -> Secrets and variables -> Actions.")
        print("Klucz zrob jako Restricted key z uprawnieniami tylko do odczytu.")
        return 0

    now = int(time.time())
    try:
        charges = charges_since(now - 60 * DAY)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        print(f"Stripe odrzucil zapytanie: HTTP {e.code}")
        print(body)
        if e.code in (401, 403):
            print("\nTo zwykle znaczy, ze klucz jest nieaktualny albo nie ma "
                  "uprawnienia do odczytu obciazen (charges: read).")
        return 1

    okresy = [("7 dni", 7), ("30 dni", 30)]
    linie = ["# Raport sprzedazy (Stripe)", ""]
    linie.append("| Okres | Zamowien | Przychod | Srednia | Poprzedni okres |")
    linie.append("|---|---:|---:|---:|---:|")

    for nazwa, dni in okresy:
        n, kwota = podsumuj(charges, now - dni * DAY, now)
        pn, pkwota = podsumuj(charges, now - 2 * dni * DAY, now - dni * DAY)
        srednia = f"{kwota / n:.0f} zl" if n else "—"
        if pn or pkwota:
            zmiana = f"{pn} zam. / {pkwota:.0f} zl"
        else:
            zmiana = "brak danych"
        linie.append(f"| {nazwa} | {n} | {kwota:.0f} zl | {srednia} | {zmiana} |")

    n30, _ = podsumuj(charges, now - 30 * DAY, now)
    linie += ["", f"Obciazen pobranych z ostatnich 60 dni: {len(charges)}"]
    if n30 == 0:
        linie += ["", "**Zero zamowien w 30 dni.** Problemem nie jest strona ani "
                      "tresci, tylko liczba osob, ktore w ogole na nia trafiaja."]

    raport = "\n".join(linie)
    print(raport)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(raport + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
