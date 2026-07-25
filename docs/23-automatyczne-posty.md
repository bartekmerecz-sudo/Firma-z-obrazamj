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

### A. Załóż aplikację Meta i zdobądź TRWAŁY token strony

> **WAŻNE (to najczęstsza przyczyna, że robot przestaje działać):** token strony
> wzięty prosto z Graph API Explorer **wygasa po kilku godzinach/dniach** — i wtedy
> robot zgłasza błąd `OAuthException` („Cannot call API for app… on behalf of user…").
> Żeby token **nigdy nie wygasał**, trzeba zrobić 2 kroki: najpierw przedłużyć
> **token użytkownika** do 60 dni, a dopiero z niego pobrać **token strony** —
> taki token strony jest **bezterminowy**. Poniżej dokładnie jak.

1. Wejdź na **developers.facebook.com** → **My Apps** → **Create App** (typ
   **Business**, nazwa np. „PixelPedzel Poster"). Zostaw tryb **Development**.
   Zapisz sobie **App ID** i **App Secret** (Settings → Basic → „Show" przy secret).
2. Wejdź w **Tools → Graph API Explorer**. Po prawej wybierz swoją aplikację.
3. Przy „User or Page" wybierz **User Token** (na razie użytkownika, nie strony).
   W „Permissions" dodaj: `pages_show_list`, `pages_manage_posts`,
   `pages_read_engagement` (dla Instagrama dodatkowo `instagram_basic`,
   `instagram_content_publish`). Kliknij **Generate Access Token** i zatwierdź
   wszystkie zgody. Skopiuj ten token — to **krótki token użytkownika**.
4. **Przedłuż token użytkownika do 60 dni.** W przeglądarce otwórz (podmień 3 rzeczy):
   ```
   https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=KROTKI_TOKEN
   ```
   Dostaniesz JSON z `access_token` — to **długi token użytkownika (60 dni)**. Skopiuj go.
5. **Pobierz bezterminowy token strony.** W przeglądarce otwórz:
   ```
   https://graph.facebook.com/v21.0/me/accounts?access_token=DLUGI_TOKEN_UZYTKOWNIKA
   ```
   Zobaczysz listę swoich stron. Przy swojej stronie skopiuj wartość `access_token`
   **oraz** `id`. **Ten token strony nie wygasa** (dopóki nie zmienisz hasła FB ani
   nie cofniesz zgód aplikacji). To jest token do sekretu `FB_PAGE_TOKEN`, a `id`
   do `FB_PAGE_ID`.

> Nie chcesz kombinować z URL-ami? Alternatywa: w Graph API Explorer wygeneruj token
> użytkownika (krok 3), kliknij ikonę **„i"** obok tokenu → **Open in Access Token Tool**
> → **Extend Access Token** (to daje długi token użytkownika), wróć do Explorera,
> wklej długi token, wpisz zapytanie `me/accounts` i skopiuj `access_token` strony.

### B. ID strony
- **ID strony** masz już z kroku A5 (`id` obok tokenu strony w `me/accounts`).
- (Instagram, opcjonalnie) w Graph API Explorer wpisz `PAGE_ID?fields=instagram_business_account`
  z tokenem strony → dostaniesz `IG_USER_ID`.

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
- Jeśli token strony zdobyłeś sposobem z sekcji A (najpierw **długi token
  użytkownika**, potem `me/accounts`), token strony **jest bezterminowy** — nic
  nie musisz odświeżać. Przestaje działać tylko, gdy zmienisz hasło do Facebooka
  albo cofniesz zgody aplikacji.
- Jeśli robot zgłosi błąd, zajrzyj w **Actions → ostatni bieg → logi**. Robot sam
  napisze diagnozę. Najczęstszy powód: **niewłaściwy / krótki token** (`OAuthException`,
  „Cannot call API… on behalf of user") — wygeneruj token jeszcze raz **całą** sekcją
  A (kroki 3→4→5), inaczej znów wygaśnie. Rzadziej: plik nie jest jeszcze na `pixelpedzel.pl`.

## Co jest w środku (dla ciekawych)
- `automation/content.py` — teksty postów + przypisane pliki.
- `automation/generate_queue.py` — tworzy harmonogram `queue.json`.
- `automation/queue.json` — gotowy plan (data → post).
- `automation/post.py` — robot, który publikuje dzisiejszy post.
- `.github/workflows/auto-post.yml` — codzienny wyzwalacz (cron).
