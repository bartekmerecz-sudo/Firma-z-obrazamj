/**
 * PixelPedzel — pracownia: zdjecie wchodzi, obraz w wybranym stylu wychodzi.
 *
 * To jest narzedzie WEWNETRZNE. Nie ma linku ze strony, jest wykluczone
 * w robots.txt i chronione haslem. Publiczny generator oznaczalby, ze kazdy
 * robi sobie obraz za nasze pieniadze i nie ma juz powodu, zeby zamowic.
 *
 * Wymagane zmienne srodowiskowe (Vercel -> Settings -> Environment Variables):
 *   GEMINI_API_KEY     klucz z Google AI Studio (PLATNY projekt, patrz docs/32)
 *   PRACOWNIA_HASLO    haslo do strony /pracownia.html
 * Opcjonalne:
 *   GEMINI_MODEL       domyslnie gemini-2.5-flash-image
 *   LIMIT_NA_ZADANIE   ile stylow naraz, domyslnie 4 (kazdy to osobna oplata)
 *
 * GET  /api/generate            -> lista stylow do zbudowania formularza
 * POST /api/generate            -> generowanie (wymaga hasla)
 */

const { PROPORCJE, zbudujPrompt, listaDlaUI } = require("./_style.js");

// GEMINI_API_BASE pozwala podstawic wlasny adres — uzywane do testow
// (tests/pracownia.test.js), zeby dalo sie sprawdzic cala sciezke bez
// wydawania pieniedzy na prawdziwe generowanie.
const API = process.env.GEMINI_API_BASE ||
  "https://generativelanguage.googleapis.com/v1beta/models";
const MODEL = process.env.GEMINI_MODEL || "gemini-2.5-flash-image";
const LIMIT = parseInt(process.env.LIMIT_NA_ZADANIE || "4", 10);
// Vercel odrzuca zadania powyzej 4,5 MB wlasnym, nieczytelnym bledem. Nasz
// limit jest nizszy, zeby komunikat byl zrozumialy. Po zmniejszeniu zdjecia
// w przegladarce realnie wychodzi 200-500 kB, wiec to tylko bezpiecznik.
const MAX_BAJTOW = 4 * 1024 * 1024;

/** Porownanie odporne na czas — haslo krotkie, ale nic nie kosztuje. */
function hasloOk(podane, prawdziwe) {
  if (typeof podane !== "string" || podane.length !== prawdziwe.length) return false;
  let r = 0;
  for (let i = 0; i < prawdziwe.length; i++) r |= podane.charCodeAt(i) ^ prawdziwe.charCodeAt(i);
  return r === 0;
}

/**
 * Jedno wywolanie modelu. Zwraca {obraz, mime} albo rzuca bledem z czytelnym
 * komunikatem po polsku — te komunikaty ogladamy potem w przegladarce.
 */
async function generuj(klucz, dane, mime, prompt, proporcje, bezImageConfig) {
  const body = {
    contents: [{
      role: "user",
      parts: [
        { inline_data: { mime_type: mime, data: dane } },
        { text: prompt },
      ],
    }],
  };
  // Nowsze wersje API przyjmuja wymuszenie proporcji. Starsze odrzucaja cale
  // zadanie z bledem 400, dlatego przy takim bledzie probujemy jeszcze raz bez
  // tego pola, zamiast pokazywac uzytkownikowi czerwony komunikat.
  if (!bezImageConfig) {
    body.generationConfig = { imageConfig: { aspectRatio: proporcje } };
  }

  const r = await fetch(`${API}/${MODEL}:generateContent`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": klucz },
    body: JSON.stringify(body),
  });

  if (!r.ok) {
    const tekst = await r.text();
    if (r.status === 400 && !bezImageConfig && /imageConfig|aspectRatio|generationConfig/i.test(tekst)) {
      return generuj(klucz, dane, mime, prompt, proporcje, true);
    }
    if (r.status === 400 && /API key not valid/i.test(tekst))
      throw new Error("Klucz GEMINI_API_KEY jest nieprawidłowy.");
    // 402 = wyczerpana przedplata. Gemini API rozlicza sie osobna pula
    // srodkow, ktorej NIE pokrywaja darmowe kredyty Google Cloud — latwo
    // uznac, ze cos jest zepsute, skoro w konsoli widac tysiac zlotych.
    if (r.status === 402)
      throw new Error(
        "Skończyły się środki przedpłaty na Gemini API. Doładuj je na ai.studio/projects " +
        "(to osobna pula niż darmowe kredyty Google Cloud — te jej nie pokrywają).");
    if (r.status === 403)
      throw new Error("Klucz nie ma dostępu do tego modelu. Sprawdź, czy projekt w Google ma włączone płatności.");
    if (r.status === 404)
      throw new Error(`Model „${MODEL}" nie istnieje pod tym kluczem. Ustaw zmienną GEMINI_MODEL na aktualną nazwę.`);
    if (r.status === 429) {
      // 429 przy pierwszej probie to najczesciej nie "za szybko", tylko zerowy
      // limit darmowego poziomu na ten model — czekanie tego nie naprawi.
      // Pokazujemy wiec, na co konkretnie Google sie powoluje.
      const zerowy = /quota_limit_value[^0-9]*"?0"?|limit: 0|FreeTier/i.test(tekst);
      const szczegol = (tekst.match(/"?(?:quotaId|quota_id|quotaMetric|quota_metric)"?\s*:\s*"([^"]+)"/) || [])[1];
      throw new Error(
        (zerowy
          ? `Darmowy poziom nie obejmuje generowania obrazów modelem „${MODEL}". Czekanie nic nie da — trzeba włączyć płatności w projekcie Google albo wskazać inny model zmienną GEMINI_MODEL.`
          : "Limit zapytań chwilowo wyczerpany. Odczekaj minutę i spróbuj ponownie.") +
        (szczegol ? ` (Google podaje limit: ${szczegol})` : ""));
    }
    throw new Error(`Błąd Google (${r.status}): ${tekst.slice(0, 300)}`);
  }

  const j = await r.json();
  const kand = j.candidates && j.candidates[0];

  // Model potrafi odmowic zamiast zwrocic obraz — najczesciej przy zdjeciach
  // dzieci albo przy czyms, co uzna za wizerunek osoby publicznej.
  if (!kand) throw new Error("Model nic nie zwrócił. Spróbuj innego zdjęcia.");
  if (kand.finishReason && !["STOP", "MAX_TOKENS"].includes(kand.finishReason)) {
    throw new Error(`Model odmówił (${kand.finishReason}). Zwykle pomaga inne zdjęcie albo inny styl.`);
  }

  const czesci = (kand.content && kand.content.parts) || [];
  const obraz = czesci.find((p) => p.inlineData || p.inline_data);
  if (!obraz) {
    const tekst = czesci.map((p) => p.text).filter(Boolean).join(" ");
    throw new Error(tekst ? `Model odpowiedział tekstem zamiast obrazem: ${tekst.slice(0, 200)}`
                          : "Model nie zwrócił obrazu.");
  }
  const dd = obraz.inlineData || obraz.inline_data;
  return { obraz: dd.data, mime: dd.mimeType || dd.mime_type || "image/png" };
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  // Celowo bez naglowkow CORS: to narzedzie wewnetrzne, wiec brak zgody na
  // wywolania z obcego hosta jest tu poprawnym zachowaniem.
  res.setHeader("X-Robots-Tag", "noindex, nofollow");

  if (req.method === "GET") {
    // Mowimy wprost, KTOREJ zmiennej brakuje. "Nie jest skonfigurowane" nie
    // odroznia literowki w nazwie od zmiennej dodanej tylko do srodowiska
    // Preview, a to sa zupelnie inne poprawki. Zadnej wartosci nie zdradzamy.
    const brakuje = ["GEMINI_API_KEY", "PRACOWNIA_HASLO"]
      .filter((n) => !process.env[n]);
    return res.status(200).json({
      style: listaDlaUI(),
      limit: LIMIT,
      model: MODEL,
      skonfigurowane: brakuje.length === 0,
      brakuje,
    });
  }
  if (req.method !== "POST") return res.status(405).json({ blad: "Metoda niedozwolona." });

  const klucz = process.env.GEMINI_API_KEY;
  const haslo = process.env.PRACOWNIA_HASLO;
  if (!klucz || !haslo) {
    return res.status(501).json({
      blad: "Pracownia nie jest skonfigurowana. Brakuje GEMINI_API_KEY albo PRACOWNIA_HASLO w ustawieniach hostingu.",
    });
  }

  let body;
  try {
    body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
  } catch (e) {
    return res.status(400).json({ blad: "Nieczytelne dane." });
  }

  if (!hasloOk(body.haslo, haslo)) {
    return res.status(401).json({ blad: "Złe hasło." });
  }

  const { zdjecie, mime, orientacja, uwagi } = body;

  // Podglad promptu — nic nie generuje i nic nie kosztuje. Sluzy za wyjscie
  // awaryjne: gdy API Google lezy, mozna wkleic prompt do Gemini recznie
  // i dokonczyc zamowienie bez czekania, az wszystko wroci.
  if (body.podglad_promptu) {
    const id = (Array.isArray(body.style) ? body.style : [])[0];
    const prompt = zbudujPrompt(id, orientacja, uwagi);
    if (!prompt) return res.status(400).json({ blad: "Nieznany styl." });
    return res.status(200).json({ prompt });
  }

  if (!zdjecie || typeof zdjecie !== "string")
    return res.status(400).json({ blad: "Brak zdjęcia." });
  if (zdjecie.length > MAX_BAJTOW)
    return res.status(413).json({ blad: "Zdjęcie za duże. Przeglądarka powinna je była zmniejszyć — odśwież stronę." });
  if (!/^image\/(jpeg|png|webp)$/.test(mime || ""))
    return res.status(400).json({ blad: "Obsługiwane formaty: JPG, PNG, WEBP." });

  const wybrane = (Array.isArray(body.style) ? body.style : []).slice(0, LIMIT);
  if (!wybrane.length) return res.status(400).json({ blad: "Nie wybrano żadnego stylu." });

  const proporcje = PROPORCJE[orientacja] || PROPORCJE.pion;

  // Rownolegle, ale kazdy styl osobno — jeden nieudany nie przewraca reszty.
  const wyniki = await Promise.all(wybrane.map(async (id) => {
    const prompt = zbudujPrompt(id, orientacja, uwagi);
    if (!prompt) return { styl: id, blad: "Nieznany styl." };
    try {
      const { obraz, mime: m } = await generuj(klucz, zdjecie, mime, prompt, proporcje, false);
      return { styl: id, obraz, mime: m };
    } catch (e) {
      return { styl: id, blad: e.message };
    }
  }));

  const udane = wyniki.filter((w) => w.obraz).length;
  return res.status(udane ? 200 : 502).json({ wyniki, udane });
};
