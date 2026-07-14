# Automatyczne płatności — jak to działa

> Sklep przyjmuje płatności online przez **Stripe Checkout**: karta, **BLIK**
> i **Przelewy24** (waluta PLN). Bez własnego serwera — wystarczy funkcja
> serverless na Vercel lub Netlify. Konfiguracja krok po kroku: `README.md`.

---

## Przepływ płatności

```
Klient w konfiguratorze: styl + rozmiar + zdjęcie + dane
        │  klik „Zamawiam i płacę"
        ▼
1. Zapis zamówienia (+ zdjęcie) → Formspree (e-mail do Ciebie)
        │
        ▼
2. Frontend woła /api/create-checkout-session (funkcja serverless)
        │   funkcja liczy cenę PO STRONIE SERWERA i tworzy sesję Stripe
        ▼
3. Przekierowanie na bezpieczną stronę płatności Stripe
        │   klient płaci: karta / BLIK / Przelewy24
        ▼
4. Sukces → powrót na /podziekowanie.html
   Anulowanie → powrót do konfiguratora
        │
        ▼
5. Płatność widoczna w panelu Stripe (z metadanymi: styl, rozmiar, klient)
```

## Dlaczego cena jest liczona na serwerze

W plikach `api/create-checkout-session.js` oraz
`netlify/functions/create-checkout-session.js` znajduje się obiekt `PRICES`
(ceny w groszach). **Nie ufamy cenie z przeglądarki** — gdyby ktoś zmanipulował
stronę, i tak zapłaci właściwą kwotę wyliczoną przez serwer. Dlatego przy każdej
zmianie cennika trzeba zaktualizować `PRICES` również tutaj (patrz README).

## Tryb bezpieczny (gdy płatności nie są jeszcze skonfigurowane)

Jeśli brak zmiennej `STRIPE_SECRET_KEY`, funkcja zwraca kod `501`, a strona
**nie psuje się**: zamówienie zostaje zapisane w Formspree, a klient dostaje
komunikat o płatności ręcznej (przelew / BLIK). Możesz więc uruchomić sklep od
razu i dołączyć płatności online później.

## Metody płatności i waluta

- Waluta: **PLN**.
- Metody: `card`, `blik`, `p24` (Przelewy24). BLIK i P24 wymagają włączenia
  w panelu Stripe i działają tylko w PLN.
- Chcesz dodać/odjąć metodę? Zmień tablicę `payment_method_types` w obu funkcjach.

## Koszty Stripe

Stripe pobiera prowizję od transakcji (różną dla kart, BLIK i P24 — sprawdź
aktualny cennik Stripe dla Polski). Wlicz ją w marżę (`docs/03-cennik-i-marze.md`).

## Alternatywy dla Stripe

Jeśli wolisz krajowego operatora, logikę można przełożyć na:
- **Przelewy24**, **PayU**, **tpay** — popularne w PL, podobny model
  (utworzenie transakcji po stronie serwera + przekierowanie).

Stripe wybrano, bo w jednym miejscu daje karty + BLIK + P24, ma prosty Checkout
i darmowy start bez abonamentu (płacisz tylko prowizję od transakcji).

## Faktury / rozliczenia

- W panelu Stripe masz historię płatności do rozliczeń.
- Kwestie faktur i podatków ustal zgodnie z formą działalności
  (`docs/06-prawne-rodo.md`).

## Bezpieczeństwo

- Klucz `sk_...` trzymaj **wyłącznie** w zmiennych środowiskowych hostingu.
- Nigdy nie umieszczaj go w kodzie ani w repozytorium.
- Frontend nie zna klucza — komunikuje się tylko z Twoją funkcją serverless.
