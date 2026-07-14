# Plan wdrożenia sklepu — krok po kroku

> Dokładny plan uruchomienia PixelPędzel od zera do pierwszej sprzedaży.
> Zaznaczaj `[x]` przy zrobionych krokach.

---

## Faza 0 — Przygotowanie (1–2 dni)

- [ ] Wybierz i kup **domenę** (np. `pixelpedzel.pl`) — u dowolnego rejestratora (OVH, home.pl, nazwa.pl).
- [ ] Załóż **osobny adres e-mail** firmowy: `kontakt@pixelpedzel.pl` (często w pakiecie z domeną).
- [ ] Załóż konto **GitHub** (jeśli nie masz) — do hostowania kodu.
- [ ] Zdecyduj o formie działalności: **działalność nierejestrowana** na start (patrz `14-platnosci-nierejestrowana.md`).

## Faza 1 — Publikacja strony (1 dzień)

- [ ] Wgraj projekt na **Vercel** lub **Netlify** (darmowy plan) — instrukcja w `README.md`.
- [ ] Podepnij **domenę** do hostingu.
- [ ] Podmień `[adres-strony]` na swoją domenę w `index.html` (JSON-LD), `sitemap.xml`, `robots.txt`.
- [ ] Podłącz **formularz zamówień** (Formspree) — podmień `FORM_ID`.
- [ ] Uzupełnij dane firmy: e-mail, social media w stopce; pola `[...]` w `regulamin.html` i `polityka-prywatnosci.html`.
- [ ] Sprawdź stronę na telefonie i komputerze (klik przez wszystkie sekcje).

## Faza 2 — Płatności (1 dzień)

- [ ] **Na absolutny start:** włącz tryb ręczny — konto bankowe + BLIK na telefon (bez formalności). Strona już to obsługuje.
- [ ] **Gdy pojawią się zamówienia:** skonfiguruj **Stripe** (karta + BLIK + Przelewy24) — instrukcja w `README.md` i `docs/09-platnosci.md`.
- [ ] Przetestuj płatność testową kartą Stripe.

## Faza 3 — Dostawca druku (2–3 dni)

- [ ] Wybierz drukarnię (POD/dropshipping) — patrz `02-model-druku.md`.
- [ ] Zamów **2–3 próbne wydruki** różnych stylów i rozmiarów.
- [ ] Oceń jakość: kolory, ostrość, napięcie płótna, opakowanie, czas dostawy.
- [ ] Ustal finalne koszty druku i wpisz je do `03-cennik-i-marze.md`.

## Faza 4 — Proces i narzędzia (1–2 dni)

- [ ] Przetestuj przeróbki AI dla każdego stylu — zapisz „przepisy" (patrz `05-narzedzia-ai.md`).
- [ ] Przygotuj **arkusz zamówień** (Google Sheets) wg wzoru z `04-proces-realizacji.md`.
- [ ] Przygotuj **szablony wiadomości** (potwierdzenie, podgląd, wysyłka) — gotowce w `04`.
- [ ] Ustal dane do płatności ręcznej (nr konta, numer BLIK).

## Faza 5 — Portfolio i marketing (3–5 dni)

- [ ] Stwórz **5–8 realnych przykładów** przeróbek (własne zdjęcia / za zgodą znajomych).
- [ ] Zrób zdjęcia/mockupy gotowych obrazów (masz gotowe w `assets/mockups/`).
- [ ] Załóż profile **Instagram + TikTok** (bio, link, 6–9 postów startowych) — patrz `10-social-media.md`.
- [ ] Przygotuj **promocję startową** (kod `START20`).

## Faza 6 — Start sprzedaży 🚀

- [ ] Ogłoś start wśród znajomych i rodziny (pierwsze zamówienia + feedback).
- [ ] Opublikuj pierwszy Reels z transformacją.
- [ ] Zbieraj opinie po każdej realizacji.
- [ ] Po 5–10 zamówieniach: włącz płatną reklamę na najlepszy kreatyw.

---

## Definicja „gotowości do startu" (Launch checklist)

Sklep jest gotowy, gdy:
1. ✅ Strona działa pod własną domeną i wygląda dobrze na telefonie.
2. ✅ Formularz zamówień dochodzi na Twój e-mail.
3. ✅ Masz sposób przyjęcia płatności (choćby ręczny).
4. ✅ Masz sprawdzoną drukarnię i znasz realne koszty.
5. ✅ Masz „przepisy" na każdy oferowany styl.
6. ✅ Masz portfolio i profil w social media.
7. ✅ Regulamin i polityka prywatności są uzupełnione.

> Pełną, klikalną wersję startu znajdziesz w pliku **`START-TUTAJ.md`**.
