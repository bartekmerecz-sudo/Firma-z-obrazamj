# Narzędzia AI — jak przerabiać zdjęcia na style

> To jest serce produktu: powtarzalna, wysokiej jakości przeróbka zdjęcia
> w każdym z naszych stylów. Cel: mając jedno zdjęcie klienta, uzyskać
> spójny, "wow" efekt w wybranym stylu — w kilka minut.

> ⚠️ **Licencje:** zanim użyjesz danego narzędzia komercyjnie, sprawdź jego
> regulamin (Terms of Service) pod kątem **prawa do komercyjnego wykorzystania
> wygenerowanych obrazów**. Warunki bywają różne i zmieniają się w czasie.

---

## Podejście ogólne: image-to-image

Kluczowa technika to **image-to-image** (obraz → obraz), nie tekst → obraz.
Podajesz zdjęcie klienta jako bazę i sterujesz stylem, zachowując kompozycję,
twarze i pozy. Dwa parametry, które kontrolują "ile zostaje z oryginału":

- **Siła zmiany / denoising** — niska = blisko oryginału, wysoka = mocno
  przestylizowane. Dla portretów par zwykle warto zostać bliżej oryginału,
  żeby twarze były rozpoznawalne.
- **Prompt stylu** — opis docelowego stylu (patrz gotowce niżej).

## Rodzaje narzędzi (do wyboru / porównania)

1. **Modele generatywne z trybem obrazu** (np. narzędzia typu ChatGPT/Gemini
   z generacją obrazów, Midjourney z funkcją odniesienia do obrazu) — szybkie,
   dobra jakość, mało konfiguracji.
2. **Stable Diffusion** (lokalnie lub w chmurze, np. przez ComfyUI/Automatic1111)
   — najwięcej kontroli: image-to-image + **ControlNet** (trzyma pozę/kontury) +
   modele stylowe (LoRA). Najlepsze do powtarzalności i zachowania twarzy.
3. **Wyspecjalizowane aplikacje** do konkretnych efektów (np. "photo to painting",
   "cartoonizer") — proste, ale mniej kontroli i spójności marki.

**Rekomendacja:** na start jedno wygodne narzędzie generatywne dla szybkości.
Gdy wolumen rośnie i zależy Ci na powtarzalności (te same style, zachowane
twarze) — przejdź na Stable Diffusion + ControlNet.

## Gotowe kierunki promptów per styl

> Traktuj to jako bazę — dopracuj pod wybrane narzędzie i zapisz swoje najlepsze
> "przepisy".

- **Olejny Klasyk** — `classical oil painting, visible brush strokes, rich
  impasto texture, warm gallery lighting, museum quality, realistic portrait`
- **Gwiaździsty Van Gogh** — `in the style of Vincent van Gogh, swirling
  expressive brushstrokes, post-impressionism, vivid blues and yellows,
  starry-night energy`
- **Neon Cyberpunk** — `cyberpunk sci-fi, neon lights, purple pink cyan glow,
  futuristic city, blade-runner mood, cinematic`
- **Szkic Ołówkiem** — `detailed pencil sketch, graphite drawing, soft shading,
  fine hatching, black and white, artistic paper texture`
- **Pastelowe Marzenie** — `soft pastel illustration, dreamy warm colors,
  storybook art, gentle gradients, cozy romantic atmosphere`
- **Nowoczesny Wektor** — `flat vector illustration, clean geometric shapes,
  minimal modern design, bold color blocks`
- **Mozaika Witrażowa** — `stained glass mosaic, thousands of colored glass
  tiles, leaded outlines, luminous`
- **Klockowy Świat (LEGO)** — `made of plastic building bricks, 3D toy blocks,
  colorful, pop-art, studio render`

## Zasada zachowania twarzy (ważne dla portretów!)

Klient chce rozpoznać siebie/bliskich. Dlatego:
- Trzymaj **niższą siłę przekształcenia** dla twarzy.
- Rozważ ControlNet (kontury/pozy) w Stable Diffusion.
- Zawsze wysyłaj **podgląd do akceptacji** przed drukiem (patrz proces, dok. 04).

## Przygotowanie pliku do druku

Po zaakceptowaniu podglądu przygotuj plik pod wymagania drukarni:
- **Rozdzielczość:** upscaling do min. 150–300 DPI w docelowym rozmiarze
  (np. 60×90 cm @ 150 DPI ≈ 3543×5315 px). Użyj narzędzia do powiększania AI
  (upscaler), jeśli wygenerowany obraz jest mniejszy.
- **Proporcje:** dopasuj do rozmiaru płótna (30×40, 40×50, 50×70, 60×90 —
  wszystkie 3:4). Kadruj świadomie, zostaw margines na zawinięcie (bleed).
- **Kolory:** zapisz w profilu wymaganym przez drukarnię (sRGB lub CMYK).
- **Format:** zwykle wysokiej jakości JPG/PNG lub TIFF.

## Kontrola powtarzalności (żeby marka wyglądała spójnie)

- Zapisuj **dokładne ustawienia** (prompt, siła, seed) dla każdego stylu w
  osobnym pliku "przepisów".
- Trzymaj bibliotekę udanych realizacji jako referencję.
- Dla każdego stylu miej **2 narzędzia** (podstawowe + zapasowe), gdyby jedno
  przestało działać lub zmieniło warunki.
