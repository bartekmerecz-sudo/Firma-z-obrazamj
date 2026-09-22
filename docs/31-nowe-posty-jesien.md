# Nowa partia postów — jesień / sezon prezentowy

Osiem grafik, wszystkie już w kolejce automatu. Nie musisz nic wrzucać ręcznie
na Facebooka — robot je opublikuje sam. Ta strona mówi **co poszło, kiedy
i po co**, plus gdzie te same pliki wykorzystać poza Facebookiem.

---

## Dlaczego akurat te osiem

Kolejka miała już posty stylowe (PRZED→PO), cennik, „bez ryzyka" i „jak to
działa". Brakowało czterech rzeczy, na których realnie urywa się rozmowa
z klientem:

| Blokada klienta | Post |
|---|---|
| „Chyba mam za słabe zdjęcie" | `post-ktore-zdjecie` |
| „Kto to w ogóle robi, czy to nie hurtownia" | `post-kto-to-robi` |
| „Co ja właściwie dostanę, jakiś plik?" | `post-co-dostajesz` |
| „Ile to potrwa" | `post-ile-trwa` |
| Brak okazji / brak terminu | `post-swieta-termin` |
| Nieruszony segment | `post-pies` |
| Za mała wartość zamówienia | `post-dwa-obrazy` |
| Inny hak niż zwykły „prezent" | `post-rocznica` |

---

## Harmonogram — co i kiedy leci

| Data | Plik |
|---|---|
| 24.09 | `post-ktore-zdjecie.png` |
| 26.09 | `post-kto-to-robi.png` |
| 27.09 | `post-co-dostajesz.png` |
| 29.09 | `post-pies.png` |
| 02.10 | `post-ile-trwa.png` |
| 03.10 | `post-dwa-obrazy.png` |
| 05.10 | `post-rocznica.png` |
| 04.11 → 07.12 | `post-swieta-termin.png` — sześć razy, co tydzień |

Kolejka sięga **31 grudnia**. Ciągłość jest zapewniona, nic nie trzeba
dosypywać przed Nowym Rokiem.

---

## Dwa posty wymagają Twojej reakcji

Te dwa proszą o odpowiedź w komentarzu. Jeśli nikt nie odpisze przez pierwszą
godzinę, **skomentuj sam z prywatnego profilu** — post bez ani jednego
komentarza Facebook pokazuje kilkunastu osobom i na tym koniec.

- **`post-pies`** — „Napiszcie PIES albo KOT w komentarzu"
- **`post-dwa-obrazy`** — „Opiszcie ścianę, podpowiem"

**Obietnica z posta o psach jest zobowiązaniem.** Napisane jest: *pierwsze trzy
zwierzaki za pół ceny w zamian za zdjęcie obrazu na ścianie*. Jak ktoś się
zgłosi — trzeba dowieźć, inaczej zostaje ślad w komentarzach.

---

## `post-swieta-termin` — sprawdź datę, zanim poleci

Post mówi **„zamawiam do 12 grudnia"**. Pierwszy raz idzie 4 listopada, więc
masz sześć tygodni, żeby to zweryfikować u drukarni. Jeśli termin jest inny,
popraw w dwóch miejscach i przegeneruj:

1. `tools/gen_posty_jesien.py` → `p_swieta_termin()` — tekst na grafice
2. `automation/content.py` → wpis `post-swieta-termin.png` — treść posta

```bash
python3 tools/gen_posty_jesien.py
cd automation && ZACHOWAJ=1 python3 generate_queue.py 2026-11-01 61
```

Podany termin, którego nie dowieziesz, boli bardziej niż brak terminu.

---

## Gdzie jeszcze użyć tych plików

**OLX i Marketplace** — `post-co-dostajesz.png` wrzuć jako ostatnie zdjęcie
w ogłoszeniu. Odpowiada na pytanie, które i tak padnie na czacie.

**Grupy na Facebooku** — `post-ktore-zdjecie.png` to jedyny z tej ósemki, który
przejdzie w grupach zakazujących reklam. Jest poradnikiem, nie ofertą. Wrzuć go
bez linku, a adres podaj dopiero w komentarzu, jak ktoś zapyta.

**TikTok** — te grafiki są pionowe 4:5, nie 9:16. Nie nadają się bez przerobienia.
Rozpiska filmów jest osobno, w `docs/28-tiktok-harmonogram.md`.

---

## Jak zrobić kolejną partię

```bash
python3 tools/gen_posty_jesien.py              # same grafiki
```

Potem dopisz wpisy w `automation/content.py` i przegeneruj kolejkę:

```bash
cd automation
ZACHOWAJ=1 OD_POSTU=post-nazwa-nowego python3 generate_queue.py 2027-01-01 90
```

- `ZACHOWAJ=1` — nie kasuje historii tego, co już poszło
- `OD_POSTU=` — rotacja rusza od wskazanej grafiki. **Bez tego nowe posty czekają
  w kolejce za całą resztą nawet miesiąc** — dopisane są na końcu listy.

Post sezonowy (np. na Dzień Matki) dopisz z czwartym elementem:

```python
("image", "assets/social/post-dzien-matki.png",
 "treść...",
 ("2027-05-01", "2027-05-25")),
```

Taki post leci **tylko w swoim oknie** i w tym okresie ma pierwszeństwo przed
zwykłą rotacją — nie częściej niż co 7 dni.
