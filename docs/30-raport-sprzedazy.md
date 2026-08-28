# Raport sprzedaży — jak go włączyć

Cotygodniowy raport ze Stripe: ile zamówień, jaki przychód, jak wypada
w porównaniu z poprzednim okresem.

## Dlaczego przez GitHub Actions

Sieć sesji Claude'a przepuszcza **wyłącznie GitHuba** — `api.stripe.com`
i `api.vercel.com` są zablokowane polityką egress. Klucz API nic by nie zmienił,
bo blokada jest na poziomie sieci, nie uwierzytelnienia.

Dlatego zapytanie leci z infrastruktury GitHuba, a Claude czyta wynik z logu
przebiegu. **Klucz nigdy nie trafia do rozmowy.**

## Konfiguracja (jednorazowo, ~5 minut)

### 1. Zrób klucz ograniczony w Stripe

Stripe → **Developers** → **API keys** → **Create restricted key**

Nazwa: `Raport GitHub Actions`

Uprawnienia — ustaw **Read** tylko dla:
- **Charges** (to jedyne, czego skrypt używa)

Cała reszta: **None**. Takim kluczem nie da się pobrać pieniędzy ani zmienić
niczego na koncie — nawet gdyby wyciekł.

### 2. Wklej do GitHub Secrets

Settings → Secrets and variables → **Actions** → **New repository secret**

- Nazwa: `STRIPE_RESTRICTED_KEY`
- Wartość: klucz ze Stripe (zaczyna się od `rk_`)

### 3. Odpal

Actions → **Raport sprzedazy (Stripe)** → **Run workflow**

Potem chodzi sam w poniedziałki o 9:00.

## Gdzie zobaczysz wynik

W przebiegu, w sekcji **Summary** — tabelka z liczbami. Ten sam tekst jest
w logu zadania, więc Claude odczyta go bez Twojego udziału.

## Czego raport NIE zapisuje

Niczego w repozytorium. Kwoty przychodu zostają w logu przebiegu i nie
wchodzą do historii gita.

Bez sekretu workflow nie zgłasza błędu — kończy się spokojnie i pisze,
czego brakuje. Nie będzie Cię zasypywał powiadomieniami o awarii.

## Vercel Analytics

Osobna sprawa i **nie mam pewności, czy Twój plan to udostępnia** — Analytics
API bywa zarezerwowane dla planów płatnych. Najprościej sprawdzisz sam:
panel Vercela → projekt → zakładka **Analytics**. Jeśli widzisz tam dane,
to na razie wystarczy zrzut ekranu.
