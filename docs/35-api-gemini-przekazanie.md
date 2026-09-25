# Gemini API — wszystko, co trzeba wiedzieć, żeby podpiąć to gdzie indziej

Dokument do przekazania: opisuje całą integrację generowania obrazów, żeby dało
się ją wpiąć w inne narzędzie bez zgadywania.

> **Klucza tu nie ma i nie będzie.** Jest wyłącznie w zmiennych środowiskowych
> na Vercelu. Nie wklejaj go na czat, do repozytorium ani do żadnego dokumentu.

---

## Co to właściwie jest

**Google Gemini API** (Generative Language API), tryb obraz→obraz: wysyłamy
zdjęcie plus opis stylu, dostajemy obraz w tym stylu z zachowaną twarzą.

| | |
|---|---|
| Endpoint | `https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent` |
| Model | `gemini-2.5-flash-image` (podmienialny zmienną `GEMINI_MODEL`) |
| Metoda | `POST` |
| Uwierzytelnianie | nagłówek `x-goog-api-key: <klucz>` |
| Rozliczenie | **przedpłata** — patrz niżej, to jest najczęstsza pułapka |

---

## Rozliczenie — przeczytaj, zanim zaczniesz debugować

Gemini API ma **własną pulę środków przedpłaconych**. To **nie to samo** co
darmowe kredyty Google Cloud.

Można mieć w konsoli Google Cloud tysiąc złotych darmowych środków i mimo to
dostawać błąd o braku pieniędzy — i tak właśnie było przy uruchamianiu.

- Doładowanie: **ai.studio/projects** → projekt → rozliczenia
- Projekt klucza: **Default Gemini Project**, ID `gen-lang-client-0300028860`
- Ten projekt musi mieć podpięte konto rozliczeniowe **i** środki przedpłacone

Darmowy poziom **nie obejmuje generowania obrazów** — pierwsze wywołanie
kończy się wtedy błędem 429 z zerowym limitem. Czekanie nic nie daje.

---

## Kształt żądania

```json
{
  "contents": [{
    "role": "user",
    "parts": [
      { "inline_data": { "mime_type": "image/jpeg", "data": "<base64 bez prefiksu data:>" } },
      { "text": "<prompt>" }
    ]
  }],
  "generationConfig": {
    "imageConfig": { "aspectRatio": "3:4", "imageSize": "2K" }
  }
}
```

### Pułapka: `imageConfig` bywa odrzucane

Nie każda wersja API zna te pola. Gdy ich nie zna, odrzuca **całe żądanie**
błędem 400 — nie ignoruje po cichu.

Dlatego próbujemy po kolei trzy konfiguracje i schodzimy niżej dopiero wtedy,
gdy 400 wspomina o `imageConfig`, `aspectRatio` lub `imageSize`:

1. `{ aspectRatio, imageSize }`
2. `{ aspectRatio }` — **proporcje są ważniejsze niż rozdzielczość**, bo obraz
   idzie na płótno o konkretnym kształcie
3. brak `generationConfig` w ogóle

Kod: `api/generate.js`, funkcja `generuj()`.

### Rozmiar wejścia

Zdjęcie zmniejszamy **w przeglądarce** do 1536 px dłuższego boku, JPEG jakość
0.92. Dwa powody: funkcje serverless na Vercelu mają limit 4,5 MB na żądanie,
a zdjęcie z telefonu potrafi mieć 8 MB. Model i tak pracuje na ~1024 px.

Kod: `js/pracownia.js`, funkcja `przygotuj()`.

---

## Kształt odpowiedzi

```json
{ "candidates": [{
    "finishReason": "STOP",
    "content": { "parts": [
      { "inlineData": { "mimeType": "image/png", "data": "<base64>" } }
    ]}
}]}
```

Trzy rzeczy, które trzeba obsłużyć, bo zdarzają się realnie:

- pola przychodzą raz jako `inlineData`, raz jako `inline_data` — sprawdzamy oba
- `finishReason` inne niż `STOP`/`MAX_TOKENS` znaczy, że model **odmówił**
  (najczęściej zdjęcia dzieci albo osoby uznane za publiczne)
- model potrafi odpowiedzieć **tekstem zamiast obrazem** — wtedy w `parts`
  nie ma w ogóle `inlineData`

---

## Katalog błędów

Każdy z tych trafił się naprawdę przy uruchamianiu.

| Kod | Co znaczy | Co zrobić |
|---|---|---|
| `400` + `API key not valid` | zły klucz | skopiować ponownie z AI Studio |
| `400` + `Unknown name "imageConfig"` | stara wersja API | powtórzyć bez tego pola |
| **`402`** | **wyczerpana przedpłata Gemini API** | doładować na ai.studio/projects — kredyty Google Cloud tego nie pokrywają |
| `403` | klucz bez dostępu do modelu | sprawdzić płatności w projekcie |
| `404` | model o tej nazwie nie istnieje | ustawić `GEMINI_MODEL` na aktualną nazwę |
| `429` + `quota_limit_value: 0` | darmowy poziom nie obejmuje obrazów | włączyć płatności; czekanie nie pomoże |
| `429` bez zerowego limitu | przekroczone tempo | odczekać minutę |

---

## Zmienne środowiskowe (Vercel → Settings → Environment Variables)

| Nazwa | Wymagana | Do czego |
|---|---|---|
| `GEMINI_API_KEY` | tak | klucz z AI Studio |
| `PRACOWNIA_HASLO` | tak | hasło do `/pracownia.html`, sprawdzane po stronie serwera |
| `GEMINI_MODEL` | nie | podmiana modelu bez ruszania kodu |
| `LIMIT_NA_ZADANIE` | nie | ile stylów naraz, domyślnie 4 — bezpiecznik kosztowy |
| `GEMINI_API_BASE` | nie | podstawienie adresu; używane tylko w testach |

**Zmienne wchodzą dopiero po Redeployu.** Samo zapisanie nic nie zmienia.

---

## Jakie mamy logi

**Żadnych własnych.** `api/generate.js` nie loguje nic — ani zapytań, ani
błędów, ani kosztów. To była świadoma decyzja (przez funkcję przechodzą zdjęcia
klientów), ale znaczy tyle, że historii nie ma.

Co jest dostępne:

| Źródło | Co zawiera | Jak długo |
|---|---|---|
| Kafelek w przeglądarce | pełny komunikat błędu, na bieżąco | do odświeżenia strony |
| Vercel → projekt → Logs | wywołania funkcji, nieprzechwycone wyjątki | krótko, zależnie od planu |
| ai.studio → projekt → Usage | liczba wywołań i zużycie środków | historia po stronie Google |
| GitHub Actions → auto-post | logi robota publikującego na Facebooku | 90 dni |

**Czego nie ma:** ile kosztowało jedno zamówienie, ile razy klient prosił
o poprawkę, które style wybierane są najczęściej. Żeby to mieć, trzeba dołożyć
zapis — a wtedy trzeba zdecydować, gdzie ma trafiać, bo dotyczy zdjęć klientów.

---

## Pliki

| Plik | Rola |
|---|---|
| `api/_style.js` | 13 stylów i ich prompty — **jedyne** miejsce do zmiany |
| `api/generate.js` | rozmowa z Google, hasło, limity, tłumaczenie błędów |
| `netlify/functions/generate.js` | przejściówka formatu, jedna logika |
| `pracownia.html`, `js/pracownia.js` | interfejs, zmniejszanie zdjęcia, DPI pod wynikiem |
| `tests/pracownia.test.js` | `npm test` — 16 testów na podstawionym Google, za darmo |

Prompty są **po stronie serwera**. Przeglądarka wysyła sam identyfikator stylu,
więc nikt ich nie podejrzy ani nie podmieni na własne i nie zrobi sobie
z naszego klucza darmowego generatora czegokolwiek.

---

## Co dorzucić, podpinając to do innego bota

1. **Własny klucz albo ten sam.** Ten sam znaczy wspólną pulę przedpłaty —
   jeden bot może ją wyczerpać drugiemu. Osobny projekt to osobny licznik.
2. **Prompty.** Skopiuj `api/_style.js`. Część o zachowaniu twarzy (`PODSTAWA`)
   decyduje o tym, czy klient rozpozna siebie — bez niej model robi ładny
   obraz przypadkowej osoby.
3. **Drabinkę prób.** Bez niej integracja przewróci się przy pierwszej zmianie
   wersji API po stronie Google.
4. **Zmniejszanie zdjęcia przed wysłaniem.** Inaczej połowa zdjęć z telefonu
   odbije się o limit żądania.
5. **Bezpiecznik kosztowy.** U nas 4 style na żądanie. Bot bez limitu wyczerpie
   przedpłatę w kilka minut.
6. **Powiększanie.** Model zwraca około megapiksela. Na wydruk 30×40 cm to
   około 73 DPI przy progu 150 — trzeba osobnego kroku (u nas Upscayl ×4,
   ręcznie).
