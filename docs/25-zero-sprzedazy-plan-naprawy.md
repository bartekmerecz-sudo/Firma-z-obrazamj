# Sprzedaż zerowa — diagnoza i plan naprawy

Data: 29.07.2026. Ten dokument mówi wprost, dlaczego nie ma sprzedaży
i co konkretnie z tym zrobić. Bez owijania.

---

## 1. Diagnoza — gdzie naprawdę jest problem

Sprawdziłem system po kolei:

| Element | Stan |
|---|---|
| Strona pixelpedzel.pl | ✅ działa |
| Płatności Stripe | ✅ podpięte |
| Robot publikujący | ✅ działa, publikuje codziennie |
| Treści (posty, filmy) | ✅ ~50 gotowych |
| **Obserwujący na Facebooku** | ❌ **0** |
| **Ruch na stronie** | ❌ bliski zeru |
| **Sprzedaż** | ❌ **0** |

**Problem nie jest techniczny.** Wszystko działa. Problem jest jeden:

> **Publikujemy codziennie do pustej sali.**

Strona firmowa z 0 obserwujących ma zasięg organiczny bliski **zeru**.
Facebook nie pokazuje postów nowej strony nikomu, kto jej nie obserwuje.
Robot wrzuca świetny post → widzi go 0–3 osoby → 0 wejść na stronę → 0 sprzedaży.

To nie jest wina treści. To jest **brak dystrybucji**.

### Prosta matematyka
Żeby zrobić 1 sprzedaż, potrzeba ok. **100–200 wejść** na stronę
(konwersja 0,5–1% to norma w tej branży na starcie).

Dziś mamy ~0 wejść. Czyli nie brakuje nam „lepszego posta" — brakuje **ludzi**.

### Czy robot jest więc bezużyteczny?
Nie. Ale pełni **inną rolę, niż myśleliśmy**:
- ❌ nie jest kanałem pozyskiwania klientów (nie dowozi ludzi),
- ✅ jest **witryną sklepową** — gdy ktoś trafi na profil z innego miejsca,
  widzi żywą, prowadzoną stronę z portfolio, a nie martwe konto.

Zostawiamy go włączonego. Ale ruch musimy przyprowadzić **skądinąd**.

---

## 2. Skąd wziąć pierwszych ludzi (kolejność wg skuteczności)

### 🥇 1. Grupy na Facebooku — najmocniejsza darmowa dźwignia
Grupy mają to, czego nie ma Twoja strona: **gotową publiczność**.
Jedna grupa prezentowa to 50–200 tys. osób.

**Grupy, w które warto wejść (wyszukaj po nazwie):**
- „Pomysł na prezent" / „Prezenty DIY i handmade"
- „Rękodzieło polskie" / „Handmade Polska"
- „Panny młode 2026" / „Ślub i wesele" (sezon!)
- „Mamy z [Twoje miasto]" / grupy lokalne Pabianice, Łódź
- „Dekoracja wnętrz / Wnętrza inspiracje"

**Zasada nr 1: nie wklejaj reklamy.** Grupy banują linki i suchą sprzedaż.
Działa **pokazanie efektu** i historia.

**Gotowy post do grup (skopiuj i wklej):**

> Zaczynam swoją małą pracownię — zamieniam zdjęcia w obrazy na płótnie.
>
> To zdjęcie pary z wakacji zamieniłem w obraz olejny [wstaw grafikę PRZED→PO].
>
> Szukam pierwszych 5 osób, które chciałyby taki obraz ze swojego zdjęcia —
> robię ze zniżką, bo buduję portfolio. Proszę tylko o zdjęcie obrazu
> na ścianie i szczerą opinię.
>
> Projekt pokazuję przed drukiem — jak się nie spodoba, nie płacicie.
> Piszcie w komentarzu albo prywatnie 🙂

Do tego **załącz grafikę** `post-oferta-start.png` albo metamorfozę PRZED→PO.

**Ile:** 2–3 grupy dziennie, nie więcej (inaczej Facebook uzna to za spam).
**Kiedy:** wieczorem 19:00–21:00, wtedy ludzie scrollują.

---

### 🥈 2. Twój prywatny profil — pierwsi klienci są tu
Prywatny profil ma **realny zasięg** (znajomi widzą Twoje posty).
Strona firmowa nie ma. To brutalne, ale prawdziwe.

**Zrób jeden szczery post na swoim profilu:**

> Nie pisałem o tym wcześniej, ale od jakiegoś czasu robię coś swojego.
>
> Zamieniam zdjęcia ludzi w obrazy na płótnie — olej, szkic, komiks, witraż.
> Wysyłacie zdjęcie, ja robię projekt, pokazuję Wam ZANIM cokolwiek zapłacicie.
> Nie spodoba się — nie płacicie.
>
> Szukam pierwszych 5 osób. Będzie taniej, bo buduję portfolio.
> Jak macie zdjęcie, które szkoda trzymać w telefonie — piszcie.
>
> A jak nie potrzebujecie, ale znacie kogoś przed rocznicą/ślubem —
> będę wdzięczny za podanie dalej 🙏

Realnie: **z tego posta wychodzą 1–3 pierwsze zamówienia.** To standard.

---

### 🥉 3. Marketplace + OLX — ludzie, którzy JUŻ szukają prezentu
To ruch z intencją zakupową — najlepszy jaki jest.

- **Facebook Marketplace** — wystaw jako „Obraz na płótnie ze zdjęcia — personalizowany".
  Darmowe, lokalne, ludzie tam szukają.
- **OLX** — kategoria „Dom i ogród → Wyposażenie → Dekoracje". Wystaw 3–4 ogłoszenia
  z różnymi stylami (olej, szkic, komiks) — każde łapie inne wyszukiwanie.

Użyj gotowych mockupów z `assets/mockups/`.

---

### 4. TikTok — jedyna platforma z darmowym zasięgiem dla nowych kont
Facebook nowego konta nie pokaże nikomu. **TikTok pokaże.**
Masz 18 gotowych filmów w `assets/video/` — leżą niewykorzystane.

- Wrzucaj **ręcznie z telefonu** (API TikToka wymaga zatwierdzenia firmy — odpada).
- 1 film dziennie, najlepiej metamorfozy PRZED→PO (`tt-metamorfoza-*.mp4`).
- Opis krótki + hashtagi: `#prezent #obraznaplotnie #metamorfoza #rekodzielo`
  (bez `#fyp` — nie działa i wygląda spamersko).
- ⛔ **Wyłącz „Treści promocyjne"** przy publikacji — to jest powód ▷ 0
  na dotychczasowych filmach. Szczegóły: `docs/26` i `docs/27`.

Jeden film, który „chwyci", potrafi dać więcej ruchu niż miesiąc postów na FB.

---

### 5. Reklama płatna — dopiero na końcu
**Nie odpalaj reklam, dopóki nie masz ani jednej opinii.** Spalisz budżet.

Kiedy będziesz mieć 3–5 zrealizowanych zamówień ze zdjęciami:
- budżet **30 zł/dzień przez 5 dni** (150 zł na test),
- cel: „Wiadomości" albo „Ruch na stronie",
- grupa: kobiety 25–45, Polska, zainteresowania: prezenty, rękodzieło, dekoracja wnętrz,
- kreacja: metamorfoza PRZED→PO (najlepiej klikany format).

---

## 3. Największy blokada: zero dowodu społecznego

Postaw się na miejscu klienta. Wchodzi na profil i widzi:
- 0 obserwujących,
- 0 opinii,
- 0 zdjęć od prawdziwych klientów.

**Nikt nie da 200 zł firmie, która nie ma ani jednego klienta.**
To błędne koło: nie ma opinii → nie ma sprzedaży → nie ma opinii.

**Jedyny sposób, żeby je przerwać: pierwsze 3–5 obrazów zrób prawie za darmo.**

Traktuj to jako **koszt marketingu, nie stratę**:
- koszt wydruku 30×40 to ok. 30–40 zł,
- w zamian dostajesz: zdjęcie obrazu na ścianie + opinię + osobę, która Cię poleci,
- 5 takich = 150–200 zł „inwestycji" i **komplet materiału, który sprzedaje za Ciebie**.

Zacznij od rodziny i znajomych — ich zdjęcia, ich ściany, ich opinie.

---

## 4. Plan na najbliższe 14 dni (konkret)

**Tydzień 1 — zdobądź pierwszych 5 klientów**
| Dzień | Zadanie | Czas |
|---|---|---|
| 1 | Post na prywatnym profilu (tekst wyżej) | 10 min |
| 2 | Dołącz do 8–10 grup FB (prezenty, ślub, lokalne) | 20 min |
| 3 | Pierwszy post w 2 grupach + grafika oferty | 15 min |
| 4 | Wystaw 3 ogłoszenia na OLX + Marketplace | 30 min |
| 5 | Post w kolejnych 2 grupach | 15 min |
| 6 | Zrób 2 obrazy dla rodziny/znajomych — za darmo | — |
| 7 | Zdjęcia tych obrazów NA ŚCIANIE + poproś o opinię | 15 min |

**Tydzień 2 — zamień dowód w sprzedaż**
| Dzień | Zadanie |
|---|---|
| 8 | Wrzuć zdjęcia klientów + opinie na profil (to teraz Twój najmocniejszy content) |
| 9–14 | 1 TikTok dziennie z `assets/video/` + 2 grupy dziennie |
| 14 | Podsumowanie: ile wejść, ile wiadomości, ile zamówień |

**Cel na 14 dni: 5 zrealizowanych obrazów i 3 opinie.** Nie „100 obserwujących".
Obserwujący nie płacą. Klienci płacą.

---

## 5. Czego NIE robić

- ❌ Nie dorzucaj kolejnych postów na stronę firmową licząc, że „w końcu chwyci".
  Przy 0 obserwujących 100. post ma taki sam zasięg jak 1.
- ❌ Nie kupuj obserwujących / polubień. Zabija zasięg i wiarygodność.
- ❌ Nie odpalaj reklam bez opinii. Wyrzucone pieniądze.
- ❌ Nie czekaj na „idealny moment". Sezon ślubny jest TERAZ, wakacje kończą się
  za miesiąc — oba hooki działają tylko przez chwilę.

---

## 6. Co już zrobione po stronie systemu

- ✅ Dodane **8 nowych postów sprzedażowych** (nie „ładny styl", tylko:
  oferta startowa, brak ryzyka, cennik, jak to działa, ankieta, wakacje, ślub, prezent).
- ✅ Ustawione jako **pierwsze w kolejce** — od 30.07 idą właśnie one.
- ✅ Grafiki gotowe w `assets/social/` — możesz je też wrzucać ręcznie do grup.
- ✅ Robot działa, kolejka pełna do 12.09.

Reszta jest po Twojej stronie — i szczerze: **te 30 minut dziennie w grupach
zrobi dla sprzedaży więcej niż wszystko, co dotąd zbudowaliśmy w kodzie.**
