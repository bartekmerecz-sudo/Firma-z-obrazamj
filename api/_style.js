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

// Dla wariantow, ktore celowo zmieniaja poze i kompozycje. Zwykla PODSTAWA
// kaze trzymac "same expressions", co gryzie sie z prosba o profil albo
// postac w polu — model dostaje sprzeczne polecenia i wychodzi cos pomiedzy.
// Tu zostaje tylko to, co decyduje o rozpoznaniu osoby: twarz, wlosy, cera.
const PODSTAWA_POZA =
  " The person must stay clearly recognizable: keep the exact facial features," +
  " face shape, eye color, hair color and texture, skin tone and freckles from" +
  " the original photo. Pose, expression, clothing and setting change as" +
  " described above." +
  " Ultra high detail, print-ready." +
  " No text, no watermark, no logo, no signature, no border, no frame.";

// Dla stylow realistycznych. Modele maja sklonnosc do "upiekszania" twarzy:
// wyszczuplaja, wygladzaja skore, poprawiaja rysy pod jakis wzorzec. Przy
// portrecie konkretnej osoby to zabija podobienstwo — klientka ma zobaczyc
// przyjaciolke, nie modelke z reklamy. Stad osobne, mocniejsze zastrzezenie.
const PODSTAWA_REALIZM =
  " This is a portrait of a real, specific person and must look exactly like" +
  " her: keep the exact face shape, proportions, facial features, eye color," +
  " eyebrows, hair color and texture, natural skin texture and freckles from" +
  " the original photo. Do not slim, smooth, retouch or idealize the face." +
  " Pose, clothing and setting change as described above." +
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
    // Dodany 06.10 na prosbe pierwszej klientki. Opisujemy GATUNEK — slowianska
    // boginia w stroju ludowym — a nie konkretny obrazek, ktory przyslala jako
    // inspiracje. Kopiowanie cudzej pracy po pierwsze nie jest nasze, po drugie
    // model i tak lepiej trzyma sie opisu elementow niz "w stylu tego obrazka".
    //
    // Swiadomie BEZ malowanej ramki, chociaz inspiracja ja miala: na plotnie
    // brzegi zawijaja sie na blejtram, wiec ramka zostalaby obcieta z kazdej
    // strony. Zamiast niej motywy kwiatowe rozlozone po tle.
    id: "slowianka",
    nazwa: "Słowiańska bogini",
    opis: "Wianek, korale, złota aureola. Portret w stylu ludowej ikony.",
    // Ikona patrzy spokojnie prosto, a zwykla PODSTAWA kaze trzymac mine ze
    // zdjecia — przy usmiechnietym selfie to sprzeczne polecenia.
    podstawa: PODSTAWA_POZA,
    prompt:
      "Transform this photo into a Slavic goddess portrait painting in the style" +
      " of modern folk-mythology art — the person wearing a tall traditional" +
      " Slavic flower crown (wianek) made of poppies, sunflowers, cornflowers," +
      " wheat ears and wild herbs with long colorful woven ribbons; layered red" +
      " coral bead necklaces; an embroidered white linen folk blouse with puffed" +
      " sleeves and a laced vest with floral embroidery; a large flat gold-leaf" +
      " halo disc glowing behind the head; a deep saturated jewel-tone background" +
      " (crimson or forest green) with subtle painted folk floral motifs;" +
      " small gold crescent moon mark on the forehead; visible acrylic brush" +
      " strokes with gold leaf accents; frontal icon-like composition, calm" +
      " direct gaze, head and shoulders.",
  },
  // --- Warianty slowianskie: inne pozy i kompozycje -----------------------
  // Klientka chciala "cos w tym stylu", nie jedno konkretne ujecie. Zamiast
  // zmieniac Uwagi przy kazdej probie — cztery gotowe kompozycje do
  // zaznaczenia naraz, jedno klikniecie, cztery rozne propozycje.
  {
    id: "slowianka-profil",
    nazwa: "Słowiańska — profil",
    opis: "Ujęcie w trzech czwartych, włosy na wietrze, jaskółki.",
    podstawa: PODSTAWA_POZA,
    prompt:
      "Transform this photo into a Slavic goddess painting — three-quarter view," +
      " the woman turning her head to look over her shoulder, long hair flowing" +
      " in the wind with woven ribbons, a crown of red poppies, cornflowers and" +
      " wheat ears, red coral necklaces, embroidered folk blouse, swallows flying" +
      " around her, a large gold-leaf halo behind, deep crimson background with" +
      " subtle folk floral motifs, visible acrylic brush strokes and gold accents.",
  },
  {
    id: "slowianka-pole",
    nazwa: "Słowiańska — w polu",
    opis: "Postać do pasa wśród zbóż o zachodzie. Malarska scena, nie ikona.",
    podstawa: PODSTAWA_POZA,
    prompt:
      "Transform this photo into a romantic Slavic folk painting — the woman shown" +
      " from the waist up standing in a golden wheat field at sunset, holding an" +
      " armful of wildflowers and wheat, wearing a flower wreath with long" +
      " ribbons, a white embroidered linen dress and red coral beads, warm golden" +
      " light on her face and hair, soft painterly oil technique with gold leaf" +
      " accents in the sky.",
  },
  {
    id: "slowianka-kupala",
    nazwa: "Słowiańska — noc Kupały",
    opis: "Księżyc, świece, wianek na wodzie. Mroczna, mistyczna.",
    podstawa: PODSTAWA_POZA,
    prompt:
      "Transform this photo into a mystical Slavic Kupala Night painting — the" +
      " woman at a moonlit river at night holding a lit flower wreath with" +
      " candles, fireflies and glowing ferns around her, a silver crescent moon" +
      " on her forehead, a dark green and deep blue palette with warm candlelight" +
      " on her face, white embroidered dress, coral beads, painterly acrylic" +
      " technique with gold and silver leaf accents.",
  },
  {
    id: "slowianka-kokosznik",
    nazwa: "Słowiańska — kokosznik",
    opis: "Wysokie nakrycie głowy z kamieniami, szmaragdowe tło.",
    podstawa: PODSTAWA_POZA,
    prompt:
      "Transform this photo into a regal Slavic princess portrait painting —" +
      " the woman wearing a tall ornate kokoshnik headdress embroidered with" +
      " garnets, pearls and gold thread, surrounded by red apples, rowan berries" +
      " and green leaves, layered garnet bead necklaces, a dark green velvet" +
      " folk dress with gold embroidery, a gold-leaf circular halo behind her" +
      " head, emerald green background, head and shoulders, visible acrylic" +
      " brush strokes and gold accents.",
  },
  // --- Realizm --------------------------------------------------------------
  // Na prosbe: "bardziej w realizmie". Dwie drogi, bo "realistycznie" znaczy
  // dla roznych osob co innego — jedni mysla o zdjeciu, drudzy o obrazie.
  {
    id: "slowianka-foto",
    nazwa: "Słowiańska — fotorealizm",
    opis: "Jak sesja zdjęciowa w stroju ludowym. Najwierniejsza twarz.",
    podstawa: PODSTAWA_REALIZM,
    prompt:
      "Turn this photo into a photorealistic professional portrait photograph" +
      " of the same woman styled as a Slavic goddess — wearing a real lush" +
      " flower crown of fresh red poppies, sunflowers, cornflowers and wheat" +
      " ears with long silk ribbons, layered red coral bead necklaces, an" +
      " authentic hand-embroidered white linen folk blouse; soft natural window" +
      " light, warm golden tones, shallow depth of field with a softly blurred" +
      " meadow background, shot on a full-frame camera with an 85mm portrait" +
      " lens, real skin texture, head and shoulders.",
  },
  {
    id: "slowianka-realizm",
    nazwa: "Słowiańska — obraz realistyczny",
    opis: "Klasyczny portret olejny, jak dawni mistrzowie. Bez stylizacji.",
    podstawa: PODSTAWA_REALIZM,
    prompt:
      "Transform this photo into a realist oil portrait painting in the" +
      " tradition of 19th-century academic portrait painters — the woman" +
      " wearing a flower crown of poppies, cornflowers and wheat with ribbons," +
      " red coral beads and an embroidered folk blouse; accurate anatomy and" +
      " true-to-life proportions, subtle refined brushwork, soft chiaroscuro" +
      " lighting, warm muted earthy palette with a dark atmospheric background," +
      " museum-quality fine art, head and shoulders.",
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
  return s.prompt + " " + kadr + (s.podstawa || PODSTAWA) + (extra ? " " + extra : "");
}

/** Lista dla przegladarki — bez promptow. */
function listaDlaUI() {
  return STYLE.map(({ id, nazwa, opis }) => ({ id, nazwa, opis }));
}

module.exports = { STYLE, PROPORCJE, zbudujPrompt, listaDlaUI };
