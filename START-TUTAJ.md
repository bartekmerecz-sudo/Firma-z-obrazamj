# 🚀 START TUTAJ — jak odpalić PixelPędzel

> Ten plik to Twój przewodnik „od zera do online". Rób po kolei — zajmie ok. 1 dnia.
> Szczegóły każdego kroku znajdziesz w linkowanych dokumentach.

---

## ✅ Krok 1 — Opublikuj stronę online (15–30 min)

Najprościej przez **Vercel** (obsługuje też automatyczne płatności):

1. Wejdź na [vercel.com](https://vercel.com) i zaloguj się przez GitHub.
2. „Add New → Project" → wybierz repozytorium `Firma-z-obrazamj`.
3. Kliknij **Deploy**. Po chwili strona działa pod adresem `...vercel.app`.

> Alternatywa bez konta GitHub: [app.netlify.com/drop](https://app.netlify.com/drop)
> — przeciągnij folder projektu. (Uwaga: metoda „drop" nie uruchamia płatności
> automatycznych — do tego połącz repozytorium.)

## ✅ Krok 2 — Podepnij domenę (30 min + propagacja)

1. Kup domenę (np. `pixelpedzel.pl`) u rejestratora (OVH / home.pl / nazwa.pl).
2. W Vercel/Netlify: „Domains" → dodaj swoją domenę i ustaw wskazane rekordy DNS
   u rejestratora.
3. Poczekaj na propagację (zwykle do kilku godzin).

## ✅ Krok 3 — Podłącz formularz zamówień (10 min)

1. Załóż konto na [formspree.io](https://formspree.io), utwórz formularz.
2. Skopiuj **Form ID** i podmień `FORM_ID` w `index.html`
   (`action="https://formspree.io/f/FORM_ID"`).
3. Wyślij testowe zamówienie i potwierdź e-mail od Formspree.

## ✅ Krok 4 — Uzupełnij swoje dane (20 min)

- Stopka `index.html`: e-mail, Instagram, Facebook.
- `regulamin.html` i `polityka-prywatnosci.html`: pola `[...]` (imię/nazwa,
  adres, kontakt). Patrz `docs/06-prawne-rodo.md`.
- SEO: podmień `[adres-strony]` na swoją domenę w `index.html` (bloki JSON-LD),
  `sitemap.xml`, `robots.txt`.

## ✅ Krok 5 — Ustaw płatności (na start bez formalności)

- **Teraz:** przyjmuj **przelew + BLIK** na konto (najlepiej osobne). Strona już
  to obsługuje — bez konfiguracji. Zero formalności.
- **Za kilka zamówień:** dołącz **Stripe** (karta + BLIK + Przelewy24) — instrukcja
  w `README.md` (sekcja 💳).
- Szczegóły przy działalności nierejestrowanej: `docs/14-platnosci-nierejestrowana.md`.

## ✅ Krok 6 — Załatw druk (2–3 dni)

1. Wybierz drukarnię (POD) — `docs/02-model-druku.md`.
2. Zamów **2–3 próbne wydruki**, oceń jakość.
3. Wpisz realne koszty do `docs/03-cennik-i-marze.md`.

## ✅ Krok 7 — Przygotuj proces i portfolio (2–4 dni)

- Przetestuj przeróbki dla stylów, zapisz „przepisy" — `docs/05-narzedzia-ai.md`.
- Załóż **arkusz zamówień** i przygotuj **szablony wiadomości** — `docs/04-proces-realizacji.md`.
- Stwórz **5–8 przykładów** do portfolio (masz gotowe mockupy w `assets/mockups/`).

## ✅ Krok 8 — Odpal marketing i sprzedaż 🎉

1. Załóż **Instagram + TikTok** (bio, link, 6–9 postów) — `docs/10-social-media.md`.
2. Ogłoś start znajomym z kodem `START20` (−20%).
3. Wrzuć pierwszy **Reels z transformacją**.
4. Zbieraj opinie i oznaczenia po każdej realizacji.
5. Po 5–10 zamówieniach — włącz małą reklamę na najlepszy filmik.

---

## 🎯 Test „czy jestem gotowy"

- [ ] Strona działa pod moją domeną, dobrze wygląda na telefonie.
- [ ] Formularz zamówień dochodzi na mój e-mail.
- [ ] Mam sposób przyjęcia płatności (choćby przelew/BLIK).
- [ ] Mam sprawdzoną drukarnię i znam koszty.
- [ ] Mam „przepisy" na oferowane style.
- [ ] Mam portfolio i profil social.
- [ ] Regulamin i polityka prywatności uzupełnione.

Wszystko odhaczone? **Gratulacje — możesz przyjmować pierwsze zamówienia!** 🎨

---

## 📚 Gdzie szukać czego

| Temat | Plik |
|---|---|
| Cały plan działania firmy | `docs/15-plan-dzialania-firmy.md` |
| Plan wdrożenia (szczegóły) | `docs/11-plan-wdrozenia.md` |
| Plan marketingowy | `docs/12-plan-marketingowy.md` |
| Pozyskiwanie klientów | `docs/13-pozyskiwanie-klientow.md` |
| Płatności (nierejestrowana) | `docs/14-platnosci-nierejestrowana.md` |
| Model druku | `docs/02-model-druku.md` |
| Ceny i marże | `docs/03-cennik-i-marze.md` |
| Proces realizacji | `docs/04-proces-realizacji.md` |
| Narzędzia AI | `docs/05-narzedzia-ai.md` |
| Prawo i RODO | `docs/06-prawne-rodo.md` |
| Social media | `docs/10-social-media.md` |
| Opisy produktów | `docs/08-opisy-produktow.md` |
| Konfiguracja techniczna | `README.md` |
