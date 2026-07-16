# Samodzielny druk na płótnie + workflow w Gemini

> Dwie rzeczy w jednym: (A) co potrzebujesz, żeby **drukować obrazy samemu**,
> (B) jak krok po kroku robić przeróbki w **Gemini** i przygotować plik do druku.

---

# A. Samodzielny druk na płótnie — co jest potrzebne

> **Szczerze na start:** własny druk **nie opłaca się przy małej sprzedaży**.
> Sprzęt to wydatek rzędu kilku–kilkunastu tys. zł + nauka. Do momentu, aż masz
> stałe kilkadziesiąt zamówień miesięcznie, **taniej i bezpieczniej zlecać druk**
> zewnętrznej drukarni (patrz `02-model-druku.md`). Poniżej masz jednak pełną
> listę, gdybyś chciał wejść w druk własny później.

## Co musisz mieć

1. **Drukarka wielkoformatowa (atramentowa, pigmentowa)**
   - Do rozmiaru 60 cm szerokości potrzebujesz drukarki min. **24 cale (61 cm)**.
   - **Atrament pigmentowy** (nie „dye") — trwalszy, odporniejszy na UV, lepszy na płótno.
   - Przykładowe serie: **Epson SureColor** (np. P700/P900 A2, lub serie rolkowe),
     **Canon imagePROGRAF**. Koszt: od ~3 000 zł (A2) do kilkunastu tys. zł (rolki).

2. **Płótno do druku (media)**
   - Role **canvas do druku atramentowego** (poli-bawełna, matowe, ~340–400 g/m²).

3. **Blejtramy (ramy)** + montaż
   - Drewniane listwy w Twoich rozmiarach (30×40, 40×50, 50×70, 60×90),
     do samodzielnego złożenia.

4. **Narzędzia do naciągania płótna**
   - **Szczypce do płótna** (canvas pliers), **zszywacz tapicerski** + zszywki,
     nożyk/gilotyna do przycięcia.

5. **Zabezpieczenie wydruku (opcjonalnie, zalecane)**
   - **Laminat/werniks w sprayu** do płótna — chroni przed wilgocią, otarciami i UV.

6. **Zarządzanie kolorem**
   - **Profile ICC** dla Twojego płótna + atramentu (żeby kolory na wydruku
     zgadzały się z ekranem). To najważniejsza i najtrudniejsza część — wymaga
     kalibracji i prób.

7. **Miejsce i czas** — stół roboczy, przestrzeń na suszenie, pakowanie.

## Orientacyjny koszt wejścia
- Drukarka A2 pigmentowa: ~3 000–6 000 zł · rolkowa 61 cm: ~8 000–15 000+ zł
- Atramenty + płótno + blejtramy + narzędzia + werniks: ~1 000–3 000 zł na start
- **Razem realnie: ~5 000–18 000 zł** + nauka i próby.

## Kiedy przejść na druk własny?
Policz to prosto: jeśli **oszczędność na 1 obrazie** (koszt druku zewnętrznego −
koszt własny) × liczba zamówień w miesiącu **przewyższa ratę/amortyzację sprzętu
i Twój czas** — wtedy warto. Zwykle to **60–100+ zamówień/mies.**

**Rekomendacja:** start = druk zlecany (POD/lokalna drukarnia). Druk własny =
opcja na później, gdy będzie wolumen.

---

# B. Workflow w Gemini — przeróbki krok po kroku

> Robisz zdjęcia w **Gemini** — super, to wygodne i szybkie. Oto jak
> ułożyć z tego powtarzalny proces realizacji zamówienia.

## Krok po kroku (dla każdego zamówienia)

1. **Wgraj zdjęcie klienta** do Gemini (to, które przysłał).
2. **Wpisz polecenie** stylu (gotowce niżej). Dopisz zawsze prośbę o
   **zachowanie podobieństwa twarzy** i **kadr pionowy**.
3. **Iteruj** — jeśli twarz się zmieniła albo styl za słaby/za mocny, popraw
   polecenie („zachowaj rysy twarzy z oryginału", „mniej/bardziej stylizacji").
4. **Pobierz** najlepszą wersję.
5. **Powiększ do druku** (upscaling — patrz niżej), bo wygenerowany plik bywa
   za mały na duże płótno.
6. **Wyślij klientowi podgląd do akceptacji** (dopiero po „tak" idzie do druku).
7. Po akceptacji przygotuj plik pod wymagania drukarni i zleć druk.

## Gotowe polecenia (prompty) per styl

> Wklejaj wraz ze zdjęciem. Możesz pisać po polsku lub angielsku — angielski
> często daje stabilniejszy efekt.

- **Olejny Klasyk:** „Zamień to zdjęcie w klasyczny obraz olejny — widoczne
  pociągnięcia pędzla, bogata tekstura farby, ciepłe światło galeryjne. Zachowaj
  rysy twarzy i kompozycję z oryginału. Format pionowy."
- **Van Gogh:** „Przekształć w obraz w stylu Vincenta van Gogha — wirujące,
  ekspresyjne pociągnięcia pędzla, intensywne błękity i żółcie. Zachowaj
  rozpoznawalność osób."
- **Akwarela:** „Delikatna akwarela — miękkie, rozmyte barwy, zacieki, dużo
  światła i powietrza. Zachowaj twarze i pozy."
- **Neon Cyberpunk:** „Futurystyczna sceneria cyberpunk, neony w odcieniach
  fioletu, różu i cyjanu, filmowy klimat sci-fi. Zachowaj postacie z oryginału."
- **Szkic Ołówkiem:** „Realistyczny szkic ołówkiem, delikatne cieniowanie,
  odcienie grafitu, biało-czarny. Zachowaj rysy twarzy."
- **Pastelowe Marzenie:** „Miękka, baśniowa ilustracja pastelowa, ciepłe barwy,
  romantyczny klimat. Zachowaj twarze i kompozycję."
- **Bajkowy 3D:** „Styl animowanego filmu 3D, ciepłe filmowe światło, bajkowa
  sceneria. Zachowaj rozpoznawalność osób."
- **Komiks Pop-art:** „Styl komiksu pop-art, wyraziste kontury, rastrowe cienie,
  żywe kolory. Zachowaj twarze."
- **Klockowy Świat:** „Scena zbudowana z kolorowych plastikowych klocków, render
  3D, nasycone barwy. Zachowaj rozpoznawalne postacie."

> Zapisuj swoje najlepsze wersje promptów w osobnym pliku — to Twoja „książka
> przepisów", z czasem coraz lepsza.

## Ważne: rozdzielczość do druku (upscaling)

Gemini często zwraca obraz ~1024–2048 px. To **za mało** na duże płótno.
Potrzebna rozdzielczość (przy 150 DPI):

| Rozmiar | Potrzebne px (ok.) |
|---|---|
| 30×40 cm | ~1770 × 2360 |
| 40×50 cm | ~2360 × 2950 |
| 50×70 cm | ~2950 × 4130 |
| 60×90 cm | ~3540 × 5310 |

**Rozwiązanie — powiększ obraz „upscalerem" AI** przed drukiem:
- **Upscayl** — darmowy program na komputer (Windows/Mac), powiększa 2×/4×.
- Lub dowolny inny upscaler online.

Zrób tak: Gemini → pobierz → Upscayl (powiększ ×4) → gotowy plik do druku.

## Przygotowanie pliku pod drukarnię

- **Proporcje:** nasze rozmiary to 3:4 (pion). Jeśli klient wybrał „poziom" lub
  „kwadrat" — dostosuj kadr.
- **DPI:** min. 150 (lepiej 300) w docelowym rozmiarze — stąd upscaling.
- **Format:** zwykle wysokiej jakości JPG lub PNG (sprawdź wymagania drukarni).
- **Kolory:** sRGB lub CMYK — zależnie od tego, czego wymaga drukarnia.
- **Spad (bleed):** zostaw margines na zawinięcie płótna, jeśli drukarnia tego
  wymaga (zwykle 2–4 cm z każdej strony).

## Zachowanie twarzy — najważniejsza zasada
AI potrafi „upiększyć" lub zmienić twarz. Dlatego:
- zawsze dopisuj „zachowaj rysy twarzy z oryginału",
- porównaj efekt z oryginałem,
- **zawsze** wysyłaj klientowi podgląd do akceptacji przed drukiem (masz to
  wpisane w proces i regulamin).

## Licencja / komercyjne użycie
Sprawdź aktualny regulamin Gemini/Google pod kątem **komercyjnego wykorzystania**
wygenerowanych obrazów. Warunki bywają aktualizowane — upewnij się, że możesz
sprzedawać efekty.
