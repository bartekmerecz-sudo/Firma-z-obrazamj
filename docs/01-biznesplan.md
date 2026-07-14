# Biznesplan — PixelPędzel

> Personalizowane obrazy na płótnie tworzone z jednego zdjęcia klienta,
> przerobionego w wybranym stylu artystycznym.

---

## 1. Streszczenie

**PixelPędzel** to mikro-biznes e-commerce działający w modelu
*print-on-demand* (druk na zamówienie). Klient przesyła **jedno zdjęcie**,
wybiera styl (olej, Van Gogh, cyberpunk, szkic, pastel, wektor, mozaika, LEGO)
i rozmiar płótna. My przerabiamy zdjęcie, wysyłamy podgląd do akceptacji,
drukujemy na płótnie i wysyłamy kurierem.

**Dlaczego to działa:**
- Wysoka wartość emocjonalna (prezent, pamiątka, dekoracja) → klient płaci za
  *personalizację*, nie za sam wydruk.
- Niskie koszty wejścia — brak magazynu, druk zlecany zewnętrznie.
- Produkt cyfrowo-fizyczny: marża w dużej mierze pochodzi z Twojej pracy nad
  grafiką, a nie z materiałów.

## 2. Model biznesowy

| Element | Opis |
|---|---|
| **Co sprzedajemy** | Obraz na płótnie = przeróbka zdjęcia + druk |
| **Kto kupuje** | Pary (rocznice, walentynki, zaręczyny), rodzice (portrety rodzinne, dzieci), właściciele zwierząt, prezenty last-minute |
| **Kanał** | Własna strona (ten projekt) + Instagram/Facebook + (docelowo) Allegro/Etsy |
| **Płatność** | Na start: formularz + przelew/BLIK. Docelowo: Stripe/Przelewy24 |
| **Realizacja** | Druk zlecany do zewnętrznej drukarni (dropshipping/POD) — patrz `02-model-druku.md` |

## 3. Analiza rynku

- **Konkurencja:** sklepy z fotoobrazami (Colorland, Fotoobraz, Fabryka Obrazów)
  sprzedają "gołe" wydruki zdjęć. Twoja przewaga = **przeróbka artystyczna
  w unikalnym stylu**, której oni nie oferują.
- **Trend:** rosnąca popularność grafiki generatywnej / "AI art" jako prezentu.
  Ludzie chcą efektu "wow", ale nie umieją zrobić go sami.
- **Nisza:** personalizowany prezent premium w cenie 129–299 zł — słodki punkt
  między tanią gadżeciarnią a drogim malarstwem na zamówienie.

## 4. Grupa docelowa (persony)

1. **Kasia, 27 lat** — szuka oryginalnego prezentu na rocznicę dla chłopaka.
   Budżet 150–250 zł. Kanał: Instagram.
2. **Marek, 34 lata** — chce portret rodzinny na ścianę w salonie. Ceni jakość.
   Budżet 250–300 zł. Kanał: Google / Facebook.
3. **Ania, 22 lata** — prezent last-minute, styl cyberpunk/pop-art dla brata
   gracza. Budżet ~130 zł. Kanał: TikTok/Instagram.

## 5. Przewaga konkurencyjna

- Unikalne, rozpoznawalne style (spójna estetyka marki).
- Podgląd przed drukiem = niskie ryzyko dla klienta = wyższa konwersja.
- Silna warstwa wizualna marki (paleta beż/grafit/złoto, "premium").

## 6. Koszty startu (szacunkowo)

| Pozycja | Koszt na start |
|---|---|
| Domena `.pl` (np. pixelpedzel.pl) | ~15–80 zł/rok |
| Hosting strony (Netlify/Vercel/GitHub Pages) | **0 zł** |
| Formularz (Formspree) | 0 zł (plan darmowy) / ~9 USD/mies. za pliki |
| Narzędzia AI do przeróbek | 0–100 zł/mies. (patrz `05-narzedzia-ai.md`) |
| Logo/branding | 0 zł (mamy) |
| Pierwsze próbne wydruki (testy jakości) | ~100–200 zł |
| **RAZEM start** | **~150–400 zł** |

To biznes, który realnie startuje za cenę kilku wydruków.

## 7. Prognoza przychodu (przykład ostrożny)

Założenia: średnia wartość zamówienia (AOV) ~185 zł, marża ~60% (patrz
`03-cennik-i-marze.md`).

| Miesiąc | Zamówienia | Przychód | Zysk (~60%) |
|---|---|---|---|
| 1 (start, znajomi + IG) | 5 | 925 zł | ~555 zł |
| 3 | 15 | 2 775 zł | ~1 665 zł |
| 6 | 30 | 5 550 zł | ~3 330 zł |
| 12 | 60 | 11 100 zł | ~6 660 zł |

To scenariusz side-businessu. Skalowanie w górę = płatne reklamy + Allegro/Etsy.

## 8. Kamienie milowe (roadmapa)

- [ ] **Tydzień 1:** uruchomić stronę online (domena + Formspree), wybrać dostawcę druku, zamówić 2–3 próbne wydruki.
- [ ] **Tydzień 2:** dopracować proces przeróbek dla każdego stylu, zebrać 3–5 realnych przykładów "przed/po".
- [ ] **Tydzień 3:** założyć profil Instagram + Facebook, opublikować portfolio.
- [ ] **Tydzień 4:** pierwsza kampania (znajomi, rodzina, promocja startowa −20%).
- [ ] **Miesiąc 2–3:** wejście na Allegro/Etsy, pierwsze płatne reklamy.
- [ ] **Miesiąc 3+:** podpięcie automatycznych płatności (Stripe/Przelewy24).

## 9. Ryzyka i jak je ograniczyć

| Ryzyko | Ograniczenie |
|---|---|
| Słaba jakość zdjęcia od klienta | Jasne wytyczne + akceptacja podglądu przed drukiem |
| Reklamacja jakości druku | Współpraca ze sprawdzoną drukarnią, testy próbne |
| Prawa autorskie do zdjęć | Regulamin: klient oświadcza, że ma prawa do zdjęcia |
| Sezonowość (walentynki, święta) | Budowanie oferty na rocznice/urodziny przez cały rok |
| Zależność od 1 narzędzia AI | Utrzymywać 2 alternatywy dla każdego stylu |

---

**Następne dokumenty:**
- `02-model-druku.md` — jak i gdzie drukować (rekomendacja)
- `03-cennik-i-marze.md` — ceny, koszty, marże
- `04-proces-realizacji.md` — obsługa zamówienia krok po kroku
- `05-narzedzia-ai.md` — czym przerabiać zdjęcia
- `06-prawne-rodo.md` — formalności, regulamin, RODO
- `07-marketing.md` — jak zdobyć pierwszych klientów
