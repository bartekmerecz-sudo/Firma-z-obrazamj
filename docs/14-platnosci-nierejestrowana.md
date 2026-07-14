# Płatności na start — przy działalności nierejestrowanej

> ⚠️ **To nie jest porada prawna ani podatkowa.** Praktyczne wskazówki —
> zweryfikuj aktualny stan na biznes.gov.pl lub u księgowego. Limity i przepisy
> zmieniają się w czasie.

---

## O co chodzi z działalnością nierejestrowaną

W Polsce możesz legalnie sprzedawać **bez rejestracji firmy** (działalność
nierejestrowana), jeśli:
- Twój **miesięczny przychód** nie przekracza ustawowego limitu (limit jest
  powiązany z minimalnym wynagrodzeniem i **co roku rośnie** — sprawdź aktualną
  kwotę na biznes.gov.pl), oraz
- w ciągu ostatnich 60 miesięcy nie prowadziłeś działalności gospodarczej.

Obowiązki: prowadzisz **uproszczoną ewidencję sprzedaży** (choćby w arkuszu),
rozliczasz dochód w rocznym PIT, wystawiasz **rachunek** na żądanie klienta.
Po przekroczeniu limitu masz obowiązek zarejestrować JDG.

To idealny model na **przetestowanie biznesu bez formalności i kosztów ZUS**.

---

## Jak przyjmować płatności — drabinka (od najprostszego)

### Poziom 1 — Start bez formalności (dzień 1)
**Przelew na konto + BLIK na telefon.**
- Wystarczy Twoje **prywatne konto** (najlepiej załóż osobne, by oddzielić
  finanse firmowe — pomaga w ewidencji).
- Klient płaci przelewem lub BLIK-iem na numer telefonu po złożeniu zamówienia.
- **Strona już to obsługuje** — gdy płatności online nie są skonfigurowane,
  formularz zapisuje zamówienie, a klient dostaje info o płatności ręcznej.
- Zalety: zero kosztów, zero formalności, działa od ręki.
- Wady: ręczne sprawdzanie wpłat, mniej „profesjonalnie" niż płatność automatyczna.

> To w zupełności wystarczy na pierwsze tygodnie i pierwsze kilkanaście zamówień.

### Poziom 2 — Płatności automatyczne jako osoba fizyczna
Gdy chcesz automatyzacji i większej konwersji:
- **Stripe** pozwala zarejestrować się także jako **osoba fizyczna** (bez firmy) —
  podajesz dane osobowe i identyfikator podatkowy. Daje **kartę + BLIK +
  Przelewy24** w jednym. To rekomendowana ścieżka przy nierejestrowanej.
- Konfiguracja: patrz `README.md` (sekcja 💳) i `docs/09-platnosci.md`.
- Uwaga: operatorzy tacy jak **Przelewy24 / PayU / tpay** zwykle wymagają
  **zarejestrowanej działalności (NIP)** — dlatego na etapie nierejestrowanym
  najprościej postawić na Stripe albo pozostać przy płatności ręcznej.

### Poziom 3 — Po rejestracji JDG
Po przejściu na działalność gospodarczą otwierają się wszystkie opcje
(Przelewy24, PayU, tpay, integracje z fakturowaniem). Wtedy też rozważ kasę
fiskalną/zwolnienia — skonsultuj z księgowym.

---

## Rekomendacja

```
Tydzień 1–4:   Płatność ręczna (przelew + BLIK) — zero formalności, testujesz biznes
Miesiąc 2+:    Dołącz Stripe (jako osoba fizyczna) — automatyzacja, karta/BLIK/P24
Po przekroczeniu limitu / gdy „na poważnie":  rejestracja JDG + pełne integracje
```

---

## Ewidencja i „papierologia" (minimum)

- **Ewidencja sprzedaży:** arkusz z datą, kwotą i numerem kolejnym sprzedaży
  (możesz połączyć z arkuszem zamówień z `04-proces-realizacji.md`).
- **Rachunek:** wystaw na żądanie klienta (prosty dokument: sprzedawca, nabywca,
  data, przedmiot, kwota).
- **Rozliczenie podatku:** dochód (przychód − koszty) wykazujesz w rocznym PIT.
- **Konto:** osobne konto na wpłaty od klientów bardzo ułatwia liczenie przychodu
  i pilnowanie limitu.

## Pilnowanie limitu przychodu

- Sumuj przychód **narastająco w miesiącu**.
- Gdy zbliżasz się do limitu — zwolnij tempo lub przygotuj rejestrację JDG.
- Po przekroczeniu limitu masz ustawowy termin na rejestrację działalności.

## Uwaga o prawach konsumenta (dotyczy też nierejestrowanej)

Sprzedając konsumentom online, obowiązują Cię przepisy konsumenckie (regulamin,
informacja o braku zwrotu dla produktu personalizowanego, reklamacje) —
niezależnie od formy działalności. Szczegóły: `06-prawne-rodo.md`.
