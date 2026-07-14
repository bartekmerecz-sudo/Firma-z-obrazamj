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
├── css/style.css                 # Style (paleta beż / grafit / złoto)
├── js/main.js                    # Konfigurator, kalkulacja ceny, obsługa formularza
├── assets/gallery/               # Przykłady stylów (galeria)
└── docs/                         # Dokumentacja biznesowa
    ├── 01-biznesplan.md
    ├── 02-model-druku.md         # Dropshipping vs własny druk (rekomendacja)
    ├── 03-cennik-i-marze.md
    ├── 04-proces-realizacji.md   # Obsługa zamówienia + szablony wiadomości
    ├── 05-narzedzia-ai.md        # Jak przerabiać zdjęcia na style
    ├── 06-prawne-rodo.md         # Formalności, regulamin, RODO
    └── 07-marketing.md           # Jak zdobyć pierwszych klientów
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

- **Netlify** — przeciągnij folder na app.netlify.com/drop, gotowe w minutę.
- **Vercel** — połącz repozytorium GitHub i „Deploy".
- **GitHub Pages** — w ustawieniach repo: Settings → Pages → wskaż branch.

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

## ✏️ Co dostosować pod siebie

- **Dane kontaktowe** w stopce `index.html` (e-mail, social media).
- **Ceny i rozmiary** — w `index.html` (konfigurator + cennik) oraz w
  `js/main.js` (stałe `SHIPPING`, `FREE_SHIPPING_FROM`). Logika cen: `docs/03`.
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
