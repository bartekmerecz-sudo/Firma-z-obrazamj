/**
 * PixelPedzel — style i prompty w JEDNYM miejscu.
 *
 * Prompty siedza po stronie serwera, nie w przegladarce. Dwa powody:
 *  1. Sa efektem wielu podejsc i nie ma powodu, zeby ktokolwiek mogl je
 *     podejrzec przez "pokaz zrodlo strony".
 *  2. Przegladarka wysyla tylko identyfikator stylu, wiec nikt nie podmieni
 *     promptu na wlasny i nie zrobi sobie z naszego klucza API darmowego
 *     generatora czegokolwiek.
 *
 * Te same prompty w wersji do recznego wklejenia sa w docs/24-prompty-gemini.md.
 * Zmieniasz tutaj — popraw tez tam, zeby sie nie rozjechalo.
 */

// Dopisywane do KAZDEGO promptu. To jest ta czesc, ktora decyduje o tym, czy
// klient rozpozna na obrazie siebie, a nie przypadkowa osobe.
const PODSTAWA =
  " Keep the exact facial features, likeness and proportions of the people" +
  " from the original photo — same faces, same hair, same expressions." +
  " Ultra high detail, print-ready." +
  " No text, no watermark, no logo, no signature, no border, no frame.";

const STYLE = [
  {
    id: "olej",
    nazwa: "Olej klasyczny",
    opis: "Ciepły, galeryjny. Najbezpieczniejszy wybór na prezent.",
    prompt:
      "Transform this photo into a classic oil painting — visible thick brush" +
      " strokes, rich impasto texture, warm gallery lighting, museum quality.",
  },
  {
    id: "vangogh",
    nazwa: "Van Gogh",
    opis: "Wirujące pociągnięcia pędzla, mocne błękity i żółcie.",
    prompt:
      "Transform this photo into a painting in the style of Vincent van Gogh —" +
      " swirling expressive brushstrokes, thick impasto, vivid blues and yellows," +
      " post-impressionist starry mood.",
  },
  {
    id: "szkic",
    nazwa: "Szkic ołówkiem",
    opis: "Czarno-biały, spokojny. Dobrze znosi słabsze zdjęcia.",
    prompt:
      "Transform this photo into a realistic graphite pencil sketch — soft" +
      " shading, fine hand-drawn lines, black and white, subtle paper texture.",
  },
  {
    id: "akwarela",
    nazwa: "Akwarela",
    opis: "Lekka, rozmyta, dużo światła. Ładnie do sypialni.",
    prompt:
      "Transform this photo into a delicate watercolor painting — soft washes," +
      " bleeding colors, lots of light and airy white space, romantic mood.",
  },
  {
    id: "komiks",
    nazwa: "Komiks pop-art",
    opis: "Grube kontury, rastry, nasycone kolory.",
    prompt:
      "Transform this photo into a pop-art comic illustration — bold ink" +
      " outlines, halftone dots, vivid saturated colors, vintage comic-book style.",
  },
  {
    id: "witraz",
    nazwa: "Witraż",
    opis: "Czarne ołowiane linie i świecące szkło.",
    prompt:
      "Transform this photo into a stained-glass mosaic — bold black outlines" +
      " dividing luminous colored glass pieces, glowing backlit effect.",
  },
  {
    id: "lego",
    nazwa: "Klocki",
    opis: "Hit u dzieci i na prezent dla faceta.",
    prompt:
      "Transform this photo into a scene built entirely from colorful plastic" +
      " building bricks, 3D toy render, minifigure-style characters, saturated" +
      " colors, playful set.",
  },
  {
    id: "bajka3d",
    nazwa: "Bajkowy 3D",
    opis: "Klimat filmu animowanego. Najlepszy do zdjęć z dziećmi.",
    prompt:
      "Transform this photo into a 3D animated movie style — Pixar-like" +
      " characters, soft cinematic lighting, cute rounded features, warm" +
      " storybook scene.",
  },
  {
    id: "wektor",
    nazwa: "Wektor",
    opis: "Płaski, graficzny, nowoczesny. Dobry do biura.",
    prompt:
      "Transform this photo into a modern flat vector illustration — clean" +
      " minimal shapes, flat colors, simple stylized faces, contemporary" +
      " editorial poster look, plain solid background.",
  },
  {
    id: "pastel",
    nazwa: "Pastelowe marzenie",
    opis: "Miękkie, ciepłe światło, klimat książki dla dzieci.",
    prompt:
      "Transform this photo into a soft dreamy pastel illustration — gentle" +
      " warm colors, delicate soft light, romantic storybook mood.",
  },
  {
    id: "cyberpunk",
    nazwa: "Cyberpunk",
    opis: "Neony, fiolet i cyjan. Do pokoju nastolatka.",
    prompt:
      "Transform this photo into a cinematic cyberpunk scene — glowing neon" +
      " lights in purple, pink and cyan, futuristic sci-fi atmosphere, moody" +
      " rim lighting.",
  },
  {
    id: "kubizm",
    nazwa: "Kubizm",
    opis: "Kanciaste plany, inspiracja Picassem. Nisza, ale sprzedaje się drogo.",
    prompt:
      "Transform this photo into a geometric cubist painting — fragmented" +
      " angular planes, bold abstract shapes, Picasso-inspired multi-perspective" +
      " composition.",
  },
  {
    id: "superbohater",
    nazwa: "Superbohater",
    opis: "Plakat filmowy. Prezent dla chłopaka albo taty.",
    prompt:
      "Transform this photo into an epic superhero comic and cinematic style —" +
      " dramatic heroic lighting, dynamic comic-book rendering, bold colors," +
      " movie-poster energy.",
  },
];

const ORIENTACJE = {
  pion: "Vertical 3:4 portrait composition.",
  poziom: "Horizontal 4:3 landscape composition.",
  kwadrat: "Square 1:1 composition.",
};

const PROPORCJE = { pion: "3:4", poziom: "4:3", kwadrat: "1:1" };

/** Sklada finalny prompt. `dopisek` to pole "uwagi" z formularza. */
function zbudujPrompt(idStylu, orientacja, dopisek) {
  const s = STYLE.find((x) => x.id === idStylu);
  if (!s) return null;
  const kadr = ORIENTACJE[orientacja] || ORIENTACJE.pion;
  // Uwagi klienta ida NA KONIEC — model traktuje pozniejsze instrukcje jako
  // doprecyzowanie wczesniejszych, wiec "wiecej zimnych kolorow" ma szanse
  // zadzialac, a nie zostac przykryte przez opis stylu.
  const extra = (dopisek || "").trim().slice(0, 400);
  return s.prompt + " " + kadr + PODSTAWA + (extra ? " " + extra : "");
}

/** Lista dla przegladarki — bez promptow. */
function listaDlaUI() {
  return STYLE.map(({ id, nazwa, opis }) => ({ id, nazwa, opis }));
}

module.exports = { STYLE, PROPORCJE, zbudujPrompt, listaDlaUI };
