# PixelPędzel 🎨

Sklep internetowy dla biznesu, który zamienia **jedno zdjęcie klienta** w
spersonalizowane dzieło sztuki w wybranym stylu i drukuje je na płótnie.

To repozytorium zawiera **działającą stronę sklepu** (HTML/CSS/JS, bez żadnego
build-a) oraz **kompletną dokumentację biznesową** potrzebną do uruchomienia
firmy.

---

## 📁 Co jest w środku

```
.
├── index.html                    # Strona sklepu (hero, style, konfigurator, cennik, FAQ)
├── regulamin.html                # Szablon regulaminu (do uzupełnienia)
├── polityka-prywatnosci.html     # Szablon polityki prywatności / RODO
├── podziekowanie.html            # Strona po udanej płatności
├── css/style.css                 # Style (paleta beż / grafit / złoto)
├── js/main.js                    # Konfigurator, kalkulacja ceny, zamówienie + płatność
├── assets/gallery/               # Przykłady stylów (galeria, 13 stylów)
├── api/
│   └── create-checkout-session.js       # Płatności Stripe (Vercel)
├── netlify/functions/
│   └── create-checkout-session.js       # Płatności Stripe (Netlify)
├── netlify.toml                  # Przekierowanie /api/* dla Netlify
├── package.json                  # Zależność: stripe
└── docs/                         # Dokumentacja biznesowa
    ├── 01-biznesplan.md
    ├── 02-model-druku.md         # Dropshipping vs własny druk (rekomendacja)
    ├── 03-cennik-i-marze.md
    ├── 04-proces-realizacji.md   # Obsługa zamówienia + szablony wiadomości
    ├── 05-narzedzia-ai.md        # Jak przerabiać zdjęcia na style
    ├── 06-prawne-rodo.md         # Formalności, regulamin, RODO
    ├── 07-marketing.md           # Jak zdobyć pierwszych klientów
    ├── 08-opisy-produktow.md     # Gotowe opisy sprzedażowe wszystkich stylów
    └── 09-platnosci.md           # Automatyczne płatności — jak działają
```

## 🚀 Jak zobaczyć stronę lokalnie

Nie wymaga instalacji. W katalogu projektu uruchom prosty serwer:

```bash
python3 -m http.server 8000
```

Następnie otwórz `http://localhost:8000` w przeglądarce.
(Można też po prostu otworzyć `index.html`, ale serwer lepiej obsługuje ścieżki.)

## 🌐 Jak opublikować w internecie (za darmo)

Strona jest w pełni statyczna, więc zadziała na każdym darmowym hostingu:

- **Vercel** — połącz repozytorium GitHub i „Deploy". ✅ Obsługuje automatyczne płatności (folder `api/`).
- **Netlify** — połącz repo lub przeciągnij folder na app.netlify.com/drop. ✅ Obsługuje płatności (`netlify/functions/`).
- **GitHub Pages** — Settings → Pages → wskaż branch. ⚠️ Tylko strona statyczna — **bez** automatycznych płatności (brak funkcji serwerowych; formularz zamówień działa, płatność w trybie ręcznym).

> Dla automatycznych płatności wybierz **Vercel** lub **Netlify** — obie mają darmowy plan.

Po publikacji podepnij własną domenę (np. `pixelpedzel.pl`).

## ⚙️ Konfiguracja formularza zamówień (WAŻNE)

Formularz używa [Formspree](https://formspree.io) — bez własnego backendu.

1. Załóż darmowe konto na formspree.io i utwórz nowy formularz.
2. Skopiuj swój **Form ID** (wygląda jak `xnqrdezw`).
3. W pliku `index.html` znajdź:
   ```html
   <form ... action="https://formspree.io/f/FORM_ID" ...>
   ```
   i zamień `FORM_ID` na swój identyfikator.
4. Wyślij testowe zamówienie i potwierdź pierwszy e-mail od Formspree.

> **Załączniki (zdjęcia):** przesyłanie plików przez formularz działa na
> **płatnych** planach Formspree. Na planie darmowym najprościej zbierać dane
> zamówienia, a klienta prosić o przesłanie zdjęcia w odpowiedzi na e-mail
> potwierdzający (strona już o tym informuje w konfiguratorze). Alternatywy:
> plan Formspree z załącznikami, albo osobny upload (np. link do WeTransfer /
> Google Drive od klienta).

## 💳 Konfiguracja automatycznych płatności (Stripe)

Płatności obsługuje [Stripe](https://stripe.com) przez funkcję serverless.
Klient płaci **kartą, BLIK-iem lub przez Przelewy24** (waluta PLN). Pełny opis
działania: `docs/09-platnosci.md`.

1. Załóż konto na stripe.com i (docelowo) przejdź weryfikację firmy.
2. W panelu Stripe włącz metody płatności **BLIK** i **Przelewy24 (P24)**
   (Settings → Payment methods).
3. Skopiuj **Secret key** (Developers → API keys). Zaczyna się od `sk_test_...`
   (tryb testowy) lub `sk_live_...` (tryb produkcyjny).
4. Ustaw go jako **zmienną środowiskową** `STRIPE_SECRET_KEY` na hostingu:
   - **Vercel:** Project → Settings → Environment Variables → dodaj `STRIPE_SECRET_KEY`.
   - **Netlify:** Site settings → Environment variables → dodaj `STRIPE_SECRET_KEY`.
5. Wdróż projekt (deploy). Zależność `stripe` z `package.json` zainstaluje się automatycznie.
6. **Test:** złóż zamówienie i zapłać testową kartą Stripe `4242 4242 4242 4242`
   (dowolna przyszła data i CVC). Sprawdź płatność w panelu Stripe.
7. Gdy wszystko działa — przełącz klucz na `sk_live_...`, by przyjmować realne wpłaty.

> **Bez skonfigurowanego klucza** strona nie „wywali się" — formularz zapisze
> zamówienie (Formspree), a klient dostanie informację o płatności ręcznej
> (przelew/BLIK). To bezpieczny tryb przejściowy.
>
> ⚠️ **Nigdy** nie wpisuj klucza `sk_...` do kodu ani nie commituj go do repo —
> wyłącznie jako zmienna środowiskowa na hostingu.

## ✏️ Co dostosować pod siebie

- **Dane kontaktowe** w stopce `index.html` (e-mail, social media).
- **Ceny i rozmiary** — pamiętaj o zsynchronizowaniu w **trzech** miejscach:
  `index.html` (konfigurator + cennik), `js/main.js` (`SHIPPING`, `FREE_SHIPPING_FROM`)
  oraz w funkcjach płatności `api/` i `netlify/functions/` (obiekt `PRICES` w groszach).
  Logika cen i marż: `docs/03`.
- **Style** — dodaj/edytuj karty w sekcji galerii i opcje w konfiguratorze.
- **Pola `[...]`** w `regulamin.html` i `polityka-prywatnosci.html` — uzupełnij
  swoimi danymi (patrz `docs/06-prawne-rodo.md`).
- **Numer konta / BLIK** — w szablonach wiadomości w `docs/04-proces-realizacji.md`.

## 🧭 Od czego zacząć (skrót)

1. Przeczytaj `docs/01-biznesplan.md` i `docs/02-model-druku.md`.
2. Wybierz drukarnię i zamów próbny wydruk (`docs/02`).
3. Opublikuj stronę + podłącz Formspree.
4. Zbuduj portfolio przykładów i profil na Instagramie (`docs/07-marketing.md`).
5. Uruchom promocję startową i zbierz pierwsze zamówienia.

---

> Ceny druku, konkretne firmy i szczegóły prawne w dokumentacji to **punkt
> wyjścia**, a nie wiążąca oferta ani porada prawna — zweryfikuj aktualne dane
> przed startem.
