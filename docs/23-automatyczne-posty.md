# Robot do automatycznych postów (Facebook / Instagram)

Masz gotowy system, który **sam publikuje posty codziennie** — bez Twojego komputera.
Działa w chmurze (GitHub Actions, za darmo). Ty tylko raz go podłączasz.

## ⚠️ Co da się zautomatyzować (szczerze)
- ✅ **Facebook (strona/fanpage)** — pełna automatyzacja. Działa dla Twojej własnej
  strony bez skomplikowanej weryfikacji.
- ✅ **Instagram (konto Business)** — też się da, ale wymaga więcej ustawień (konto
  firmowe połączone ze stroną FB). Opcjonalne.
- ❌ **TikTok** — **nie da się** za darmo automatycznie (API TikToka wymaga
  zatwierdzenia firmy). TikToki wrzucaj ręcznie z telefonu (masz gotowe filmy).

> Uwaga: robot publikuje na **stronę na Facebooku (fanpage)**, nie na prywatny profil.
> Jeśli masz tylko profil prywatny — załóż darmową Stronę (Fanpage).

---

## Jak to działa (w skrócie)
1. Plan postów jest w pliku `automation/queue.json` (data + tekst + zdjęcie/wideo).
2. Codziennie o ustalonej godzinie GitHub sam uruchamia robota (`automation/post.py`).
3. Robot bierze post zaplanowany na dziś i publikuje go przez oficjalne API Meta.

Pliki (zdjęcia/wideo) robot bierze z Twojej strony `pixelpedzel.pl` — dlatego muszą
tam być wgrane (są, bo publikujemy je razem z tym systemem).

---

## Podłączenie — krok po kroku (jednorazowo, ~20 min)

### A. Załóż aplikację Meta i zdobądź token
1. Wejdź na **developers.facebook.com** → zaloguj się → **My Apps** → **Create App**.
   Wybierz typ **Business**. Nazwij np. „PixelPedzel Poster". Zostaw ją w trybie
   **Development** (nie musisz przechodzić weryfikacji, żeby postować na SWOJĄ stronę).
2. Wejdź w **Tools → Graph API Explorer**.
3. Po prawej wybierz swoją aplikację, a przy „User or Page" wybierz **Get Page
   Access Token** i wskaż swoją stronę.
4. W polu uprawnień dodaj: `pages_manage_posts`, `pages_read_engagement`
   (dla Instagrama dodatkowo: `instagram_basic`, `instagram_content_publish`).
5. Kliknij **Generate Access Token** i zatwierdź. Skopiuj token.

> Ten token jest krótki (wygasa). Zamień go na **długożyciowy (60 dni)**:
> w Graph API Explorer użyj narzędzia **Access Token Debugger** (Tools → Debug),
> wklej token → **Extend Access Token**. Skopiuj przedłużony.
> Co ~2 miesiące trzeba go odświeżyć (przypomnę w kalendarzu).

### B. Zdobądź ID strony
- W Graph API Explorer wpisz zapytanie `me?fields=id,name` z tokenem strony —
  zwróci **ID strony** (ciąg cyfr). Skopiuj.
- (Instagram, opcjonalnie) `me?fields=instagram_business_account` → dostaniesz `IG_USER_ID`.

### C. Wklej sekrety do GitHuba
1. Wejdź na swój repozytorium na GitHubie → **Settings** → **Secrets and variables**
   → **Actions** → **New repository secret**.
2. Dodaj:
   - `FB_PAGE_ID` = ID Twojej strony
   - `FB_PAGE_TOKEN` = przedłużony token strony
   - (opcjonalnie) `IG_USER_ID` = ID konta Instagram Business
   - (opcjonalnie) `SITE_BASE_URL` = `https://pixelpedzel.pl` (domyślnie i tak to jest)

### D. Włącz i przetestuj
1. Zakładka **Actions** w repozytorium → włącz workflow, jeśli poprosi.
2. Wybierz **Auto-post (Facebook / Instagram)** → **Run workflow** → w polu
   „Test bez publikacji" wpisz **1** → uruchom. To test — pokaże, co by wrzucił,
   ale nic nie opublikuje.
3. Jeśli test przechodzi — gotowe. Od jutra robot publikuje sam codziennie.

---

## Codzienne używanie

**Nic nie musisz robić** — robot działa sam. Ale możesz:

- **Zmienić godzinę publikacji:** w pliku `.github/workflows/auto-post.yml` zmień
  `cron: "0 9 * * *"` (to 11:00 w Polsce latem). Np. `0 16 * * *` = 18:00.
- **Dodać kolejne tygodnie postów:** uruchom generator (w repo lub poproś mnie):
  `python3 automation/generate_queue.py 2026-08-19 28` → tworzy plan na 28 dni od tej daty.
- **Zmienić treść postów:** edytuj `automation/content.py` i wygeneruj plan na nowo.
- **Włączyć Instagram:** ustaw sekret `IG_USER_ID` (reszta działa automatycznie).

## Ważne / bezpieczeństwo
- **Nie wysyłaj mi tokenów ani haseł.** Wklejasz je tylko do sekretów GitHuba —
  ja ich nie widzę i nie potrzebuję.
- Token strony wygasa ~co 60 dni — trzeba go odświeżyć (punkt A). Wpisz sobie
  przypomnienie co 6–8 tygodni.
- Jeśli robot zgłosi błąd, zajrzyj w **Actions → ostatni bieg → logi**. Najczęstszy
  powód: wygasły token (odśwież) albo plik nie jest jeszcze na `pixelpedzel.pl`.

## Co jest w środku (dla ciekawych)
- `automation/content.py` — teksty postów + przypisane pliki.
- `automation/generate_queue.py` — tworzy harmonogram `queue.json`.
- `automation/queue.json` — gotowy plan (data → post).
- `automation/post.py` — robot, który publikuje dzisiejszy post.
- `.github/workflows/auto-post.yml` — codzienny wyzwalacz (cron).
