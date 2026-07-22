# Prompty do Gemini — generowanie zdjęć w stylach PixelPędzel

Jak używać:
1. Wgraj zdjęcie do Gemini.
2. Skopiuj prompt danego stylu (niżej) i wklej razem ze zdjęciem.
3. Jeśli twarz się zmieni albo styl za słaby/za mocny — dopisz „zachowaj rysy twarzy
   z oryginału" / „mniej / bardziej stylizacji" i wygeneruj ponownie.
4. Pobierz najlepszą wersję → powiększ (Upscayl ×4) → gotowe do druku.

> Prompty są po angielsku — Gemini daje wtedy stabilniejszy efekt. Możesz je wklejać
> bez tłumaczenia.

---

## SZABLON UNIWERSALNY (podmieniasz tylko [STYL])

**PL:**
> Przekształć to zdjęcie w **[OPIS STYLU]**. Zachowaj dokładnie rysy twarzy,
> podobieństwo i proporcje osób z oryginału — te same twarze, włosy i wyraz.
> Kompozycja pionowa 3:4. Bardzo wysoka jakość, gotowe do druku.
> Bez tekstu, bez znaku wodnego, bez logo, bez podpisu.

**EN (zalecane):**
> Transform this photo into **[STYLE DESCRIPTION]**. Keep the exact facial features,
> likeness and proportions of the people from the original — same faces, same hair,
> same expressions. Vertical 3:4 portrait composition. Ultra high detail, print-ready.
> No text, no watermark, no logo, no signature.

Do każdego stylu niżej podmieniasz część **[STYLE DESCRIPTION]** na opis stylu.

---

## 13 STYLÓW — gotowe prompty (kopiuj-wklej całość)

**1. Olejny Klasyk**
> Transform this photo into a classic oil painting — visible thick brush strokes, rich impasto texture, warm gallery lighting, museum quality. Keep the exact faces, likeness and proportions from the original. Vertical 3:4. Print-ready, ultra detailed. No text, no watermark, no signature.

**2. Gwiaździsty Van Gogh**
> Transform this photo into a painting in the style of Vincent van Gogh — swirling expressive brushstrokes, thick impasto, vivid blues and yellows, post-impressionist starry mood. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**3. Neon Cyberpunk**
> Transform this photo into a cinematic cyberpunk scene — glowing neon lights in purple, pink and cyan, futuristic sci-fi atmosphere, moody rim lighting. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**4. Szkic Ołówkiem**
> Transform this photo into a realistic graphite pencil sketch — soft shading, fine hand-drawn lines, black and white, subtle paper texture. Keep the exact facial features and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**5. Pastelowe Marzenie**
> Transform this photo into a soft dreamy pastel illustration — gentle warm colors, delicate soft light, romantic storybook mood. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**6. Nowoczesny Wektor**
> Transform this photo into a modern flat vector illustration — clean minimal shapes, flat colors, simple stylized faces, contemporary editorial poster look, plain solid background. Keep recognizable likeness and hair. Vertical 3:4. Print-ready. No text, no watermark, no logo.

**7. Mozaika Witrażowa**
> Transform this photo into a stained-glass mosaic — bold black outlines dividing luminous colored glass pieces, glowing backlit effect. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**8. Klockowy Świat (LEGO)**
> Transform this photo into a scene built entirely from colorful plastic building bricks, 3D toy render, minifigure-style characters, saturated colors, playful set. Keep recognizable faces, hair and outfits. Vertical 3:4. Print-ready. No text, no watermark.

**9. Akwarela**
> Transform this photo into a delicate watercolor painting — soft washes, bleeding colors, lots of light and airy white space, romantic mood. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**10. Komiks Pop-art**
> Transform this photo into a pop-art comic illustration — bold ink outlines, halftone dots, vivid saturated colors, vintage comic-book style. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

**11. Bajkowy 3D**
> Transform this photo into a 3D animated movie style — Pixar-like characters, soft cinematic lighting, cute rounded features, warm storybook scene. Keep recognizable faces, hair and expressions. Vertical 3:4. Print-ready. No text, no watermark.

**12. Kubizm Geometryczny**
> Transform this photo into a geometric cubist painting — fragmented angular planes, bold abstract shapes, Picasso-inspired multi-perspective composition. Keep recognizable faces and features. Vertical 3:4. Print-ready. No text, no watermark.

**13. Superbohater**
> Transform this photo into an epic superhero comic / cinematic style — dramatic heroic lighting, dynamic comic-book rendering, bold colors, movie-poster energy. Keep the exact faces and likeness from the original. Vertical 3:4. Print-ready. No text, no watermark.

---

## Wskazówki (żeby wychodziło najlepiej)
- **Twarze:** zawsze porównaj efekt z oryginałem. Jeśli AI zmieniło twarz — dopisz
  „keep the exact face from the original, do not change facial features".
- **Kadr:** dla pary najlepiej zdjęcie w pionie, twarze dobrze widoczne, dobre światło.
- **Znak wodny Gemini:** czasem dodaje małą gwiazdkę w rogu — nie przejmuj się,
  przycinam ją przy robieniu postów.
- **Druk:** po wygenerowaniu powiększ w Upscayl ×4 (patrz `17-wlasny-druk-i-gemini.md`).
- **Do postów:** wrzuć oryginał + przeróbki do folderu `uploads/` na GitHubie,
  napisz mi który styl — zrobię gotowe posty i filmy PRZED → PO (mogę też pokazać
  obraz „na ścianie" jako wydruk na płótnie).
