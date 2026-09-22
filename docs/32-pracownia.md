# Pracownia — generowanie obrazów bez wklejania promptów

Strona `pixelpedzel.pl/pracownia.html`. Wrzucasz zdjęcie od klienta, klikasz
style, dostajesz gotowe podglądy. Żadnego kopiowania promptów, żadnego
przeklikiwania się przez Gemini.

**To narzędzie jest tylko dla Ciebie.** Nie ma do niego linku ze strony, jest
wyłączone z wyszukiwarek i zamknięte hasłem. Publiczny generator znaczyłby,
że każdy robi sobie obraz za Twoje pieniądze i nie ma już po co zamawiać.

---

## Zanim zadziała — dwie rzeczy do zrobienia

Nie mogę tego zrobić za Ciebie, bo wymaga Twojego konta Google i Twojej karty.

### 1. Klucz do Google

1. Wejdź na **aistudio.google.com/apikey**
2. **Create API key** → wybierz projekt (albo utwórz nowy)
3. **Włącz płatności w tym projekcie.** Na darmowym poziomie Google potrafi
   dokładać do obrazów widoczny znaczek w rogu — dokładnie ten, przez który
   musieliśmy przerabiać reelsy i posty. Płatny projekt tego nie robi.
4. Skopiuj klucz

> **Sprawdź pierwszy wygenerowany obraz w powiększeniu, zanim wyślesz go
> klientowi.** Jeśli w rogu jest jakikolwiek znaczek — napisz, dodam
> automatyczne przycinanie, tak jak w `tools/strip_watermark.py`.
>
> Niezależnie od tego każdy obraz z Google ma w sobie **niewidoczny znacznik
> SynthID**. Gołym okiem tego nie widać i klient tego nie zobaczy, ale warto
> wiedzieć, że tak jest.

### 2. Wpisanie kluczy na Vercelu

Vercel → projekt pixelpedzel → **Settings** → **Environment Variables**.
Dodaj dwie pozycje i wybierz wszystkie trzy środowiska (Production, Preview,
Development):

| Nazwa | Wartość |
|---|---|
| `GEMINI_API_KEY` | klucz skopiowany z AI Studio |
| `PRACOWNIA_HASLO` | hasło, które sam wymyślisz — dowolne, byle nie „admin" |

Potem **Deployments → … → Redeploy**. Zmienne wchodzą dopiero przy nowym
wdrożeniu.

> **Nie wklejaj tych kluczy na czacie ani nigdzie indziej.** Wpisz je
> bezpośrednio na Vercelu. Klucz Google to Twoja karta — kto go ma, ten
> generuje na Twój rachunek.

---

## Jak się tego używa

1. Wejdź na `pixelpedzel.pl/pracownia.html`, wpisz hasło (raz na przeglądarkę)
2. **Wrzuć zdjęcie** — przeciągnij, kliknij albo **wklej Ctrl+V**.
   Wklejanie jest najszybsze: zdjęcia przychodzą na Messengerze, więc robisz
   zrzut ekranu i wklejasz, bez zapisywania pliku
3. **Zaznacz style** — do czterech naraz. Klientowi i tak lepiej pokazać trzy
   propozycje niż jedną
4. **Nazwa zamówienia** (opcjonalnie) — trafia do nazw pobieranych plików,
   np. `kowalska-rocznica-olej-2026-09-22.png`. Warto, gdy masz kilka zamówień
   naraz
5. **Uwagi** (opcjonalnie) — po angielsku działa lepiej. Np. `warmer colors`,
   `remove the people in the background`, `keep the dog`
6. **Generuj** → 15–40 sekund

### Potem

Wyniki mają około 1024 px. Na wydruk 30×40 to za mało — przepuść plik przez
**Upscayl ×4**, tak samo jak dotąd. Tego kroku pracownia nie zastępuje.

---

## Ile to kosztuje

Każdy styl to osobne płatne wywołanie. Przy stawkach rzędu kilku groszy za
obraz trzy style na zamówienie to grosze — ale **licznik biegnie przy każdym
kliknięciu „Generuj", także przy nieudanych próbach**.

Dlatego są dwa bezpieczniki:

- **maksymalnie 4 style na jedno kliknięcie.** Chcesz inaczej — dodaj na
  Vercelu zmienną `LIMIT_NA_ZADANIE` z inną liczbą
- **ustaw limit wydatków w Google Cloud Billing → Budgets & alerts.**
  Zrób to od razu, nie „kiedyś". Jeśli hasło wycieknie, to jedyna rzecz,
  która stoi między Tobą a rachunkiem

---

## Kiedy coś nie działa

Strona pokazuje konkretny powód przy każdym stylu osobno. Jeden styl może
paść, a reszta wyjdzie — dostajesz to, co się udało.

| Komunikat | Co zrobić |
|---|---|
| „Pracownia nie jest skonfigurowana" | brak zmiennych na Vercelu albo nie było redeploya |
| „Klucz GEMINI_API_KEY jest nieprawidłowy" | zły klucz — skopiuj ponownie z AI Studio |
| „Klucz nie ma dostępu do tego modelu" | płatności w projekcie Google nie są włączone |
| „Model … nie istnieje pod tym kluczem" | Google zmienił nazwę modelu — dodaj zmienną `GEMINI_MODEL` z aktualną |
| „Limit zapytań wyczerpany" | odczekaj minutę albo podnieś limit w AI Studio |
| „Model odmówił (SAFETY)" | zwykle zdjęcie dziecka albo osoby publicznej — inne zdjęcie lub inny styl |

Gdyby API Google leżało dłużej, jest wyjście awaryjne: zaznacz **jeden** styl
i kliknij **„Kopiuj prompt do Gemini"**. Dostajesz dokładnie ten sam prompt do
ręcznego wklejenia. Ten przycisk nic nie kosztuje.

---

## Dla mnie, na przyszłość

| Plik | Co robi |
|---|---|
| `api/_style.js` | 13 stylów i ich prompty — **jedyne** miejsce, gdzie je zmieniać |
| `api/generate.js` | rozmowa z Google, hasło, limity, obsługa błędów |
| `netlify/functions/generate.js` | przejściówka, gdyby hosting wrócił na Netlify |
| `pracownia.html` + `js/pracownia.js` | interfejs |
| `tests/pracownia.test.js` | `npm test` — sprawdza całą ścieżkę na udawanym Google, za darmo |

Prompty są po stronie serwera, nie w przeglądarce. Dzięki temu nikt ich nie
podejrzy przez „pokaż źródło" ani nie podmieni na własne i nie zrobi sobie
z naszego klucza darmowego generatora czegokolwiek.

Te same prompty w wersji do ręcznego wklejenia są w `docs/24-prompty-gemini.md`.
**Zmieniasz w jednym miejscu — popraw w drugim**, inaczej się rozjadą.

Zdjęcie jest zmniejszane do 1536 px **w przeglądarce**, przed wysłaniem.
Funkcje serverless mają limit wielkości żądania, a zdjęcie prosto z telefonu
potrafi mieć 8 MB. Model i tak pracuje na około 1024 px, więc nic na tym
nie tracimy.

---

## Czego to jeszcze nie robi

- **Nie upscale'uje.** Upscayl ×4 nadal ręcznie.
- **Nie zapisuje historii.** Zamkniesz kartę, wyniki przepadają — pobierz od
  razu to, co dobre.
- **Nie wysyła nic klientowi.** Pobierasz plik i wysyłasz sam.

Każdą z tych rzeczy da się dołożyć. Historia zamówień ma największy sens,
gdy zaczniesz mieć po kilka zamówień dziennie — wcześniej to zbędna maszyneria.
