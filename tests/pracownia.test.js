/**
 * Test calej sciezki pracowni BEZ placenia za generowanie.
 *
 * Podstawiamy pod GEMINI_API_BASE wlasny serwer, ktory udaje Google i oddaje
 * male, rozpoznawalne obrazki. Sprawdzamy to, co latwo zepsuc i trudno
 * zauwazyc golym okiem: haslo, limit stylow, zachowanie przy czesciowej
 * awarii i ponowienie zadania bez pola imageConfig.
 *
 * Uruchomienie:  node tests/pracownia.test.js
 */
const http = require("http");
const assert = require("assert");

const PIKSEL_PNG =
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==";

let zapytania = [];

const OBRAZ_OK = {
  kod: 200,
  tresc: { candidates: [{ finishReason: "STOP", content: { parts: [
    { inlineData: { mimeType: "image/png", data: PIKSEL_PNG } }] } }] },
};

/* Jeden serwer na caly przebieg, zachowanie przelaczane zmienna `tryb`.
   Wczesniej kazdy scenariusz dostawal wlasny serwer na tym samym porcie —
   close() jest asynchroniczne, wiec kolejny listen() bywal wyscigiem i test
   oblewal, chociaz kod produkcyjny byl w porzadku. */
let tryb = () => OBRAZ_OK;

const serwer = http.createServer((req, res) => {
  let raw = "";
  req.on("data", (c) => (raw += c));
  req.on("end", () => {
    const body = JSON.parse(raw || "{}");
    zapytania.push({ url: req.url, klucz: req.headers["x-goog-api-key"], body });
    const odp = tryb(req, body);
    res.statusCode = odp.kod;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify(odp.tresc));
  });
});

function wywolaj(handler, body) {
  return new Promise((ok) => {
    let kod = 200, wynik = null;
    const res = {
      setHeader() {},
      status(c) { kod = c; return this; },
      json(o) { wynik = o; ok({ kod, tresc: wynik }); return this; },
      end() { ok({ kod, tresc: wynik }); return this; },
    };
    handler({ method: "POST", headers: {}, body: JSON.stringify(body) }, res);
  });
}

const zdjecie = { zdjecie: PIKSEL_PNG, mime: "image/png", orientacja: "pion" };

(async function () {
  const testy = [];
  const test = (nazwa, fn) => testy.push([nazwa, fn]);

  // ---------------------------------------------------------------- testy
  test("złe hasło nie dochodzi do Google", async (handler) => {
    zapytania = [];
    const r = await wywolaj(handler, { ...zdjecie, haslo: "zle", style: ["olej"] });
    assert.strictEqual(r.kod, 401);
    assert.strictEqual(zapytania.length, 0, "przy złym haśle nie wolno wołać API");
  });

  test("dobre hasło generuje obraz", async (handler) => {
    zapytania = [];
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    assert.strictEqual(r.kod, 200);
    assert.strictEqual(r.tresc.udane, 1);
    assert.strictEqual(r.tresc.wyniki[0].styl, "olej");
    assert.ok(r.tresc.wyniki[0].obraz, "brak obrazu w odpowiedzi");
    assert.strictEqual(zapytania[0].klucz, "klucz-testowy");
  });

  test("limit stylów obcina nadmiar", async (handler) => {
    zapytania = [];
    // LIMIT_NA_ZADANIE ustawione nizej na 2, prosimy o 4
    const r = await wywolaj(handler, {
      ...zdjecie, haslo: "tajne",
      style: ["olej", "szkic", "witraz", "lego"],
    });
    assert.strictEqual(r.tresc.wyniki.length, 2, "limit nie zadziałał");
    assert.strictEqual(zapytania.length, 2, "zapłaciliśmy za więcej niż limit");
  });

  test("uwagi trafiają na koniec promptu", async (handler) => {
    zapytania = [];
    await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"], uwagi: "ZNACZNIK" });
    const tekst = zapytania[0].body.contents[0].parts[1].text;
    assert.ok(tekst.endsWith("ZNACZNIK"), "uwagi muszą być na końcu: " + tekst.slice(-60));
  });

  test("nieznany styl nie przewraca reszty", async (handler) => {
    zapytania = [];
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej", "nie-ma-takiego"] });
    assert.strictEqual(r.tresc.udane, 1);
    const zly = r.tresc.wyniki.find((w) => w.styl === "nie-ma-takiego");
    assert.ok(zly.blad, "nieznany styl powinien mieć błąd");
  });

  // ---------------------------------------------------------------- start
  await new Promise((r) => serwer.listen(0, r));
  const port = serwer.address().port;

  process.env.GEMINI_API_BASE = `http://127.0.0.1:${port}`;
  process.env.GEMINI_API_KEY = "klucz-testowy";
  process.env.PRACOWNIA_HASLO = "tajne";
  process.env.LIMIT_NA_ZADANIE = "2";
  const handler = require("../api/generate.js");

  let bledy = 0;
  const sprawdz = async (nazwa, fn) => {
    try { await fn(); console.log("  ok   " + nazwa); }
    catch (e) { bledy++; console.log("  BLAD " + nazwa + "\n       " + e.message); }
  };

  for (const [nazwa, fn] of testy) await sprawdz(nazwa, () => fn(handler));

  // Starsze wersje API odrzucaja pole imageConfig. Funkcja ma wtedy sprobowac
  // jeszcze raz bez niego, zamiast pokazac blad.
  await sprawdz("przy starym API schodzi do gołego żądania", async () => {
    zapytania = [];
    tryb = (req, body) => body.generationConfig
      ? { kod: 400, tresc: { error: { message: 'Unknown name "imageConfig"' } } }
      : OBRAZ_OK;
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    assert.strictEqual(zapytania.length, 3, "drabinka ma trzy szczeble");
    assert.strictEqual(r.tresc.udane, 1, "ostatnia próba miała się udać");
  });

  // Gdy API nie zna samego imageSize, nie wolno przy okazji zgubic proporcji —
  // kadr 3:4 jest wazniejszy niz rozdzielczosc, bo obraz idzie na plotno.
  await sprawdz("nieobsługiwany rozmiar nie gubi proporcji", async () => {
    zapytania = [];
    tryb = (req, body) => {
      const ic = body.generationConfig && body.generationConfig.imageConfig;
      if (ic && ic.imageSize)
        return { kod: 400, tresc: { error: { message: 'Unknown name "imageSize"' } } };
      return OBRAZ_OK;
    };
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    assert.strictEqual(zapytania.length, 2, "miały wystarczyć dwie próby");
    const druga = zapytania[1].body.generationConfig.imageConfig;
    assert.strictEqual(druga.aspectRatio, "3:4", "proporcje miały zostać");
    assert.ok(!druga.imageSize, "rozmiar miał zniknąć");
    assert.strictEqual(r.tresc.udane, 1);
  });

  // Rozdzielczosc wybrana w formularzu ma faktycznie dojsc do Google.
  await sprawdz("wybrany rozmiar trafia do żądania", async () => {
    zapytania = [];
    tryb = () => OBRAZ_OK;
    await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"], rozmiar: "4K" });
    assert.strictEqual(zapytania[0].body.generationConfig.imageConfig.imageSize, "4K");
  });

  await sprawdz("nieznany rozmiar wraca do domyślnego", async () => {
    zapytania = [];
    tryb = () => OBRAZ_OK;
    await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"], rozmiar: "999K" });
    assert.strictEqual(zapytania[0].body.generationConfig.imageConfig.imageSize, "2K");
  });

  // Odmowa modelu (np. przy zdjeciu dziecka) ma dac czytelny komunikat, nie 500.
  await sprawdz("odmowa modelu daje czytelny komunikat", async () => {
    tryb = () => ({ kod: 200, tresc: { candidates: [{ finishReason: "SAFETY", content: { parts: [] } }] } });
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    assert.strictEqual(r.kod, 502);
    assert.match(r.tresc.wyniki[0].blad, /odmówił/);
  });

  // Zly klucz to najczestszy blad przy pierwszym uruchomieniu — komunikat musi
  // mowic, co poprawic, a nie wypluwac surowy JSON od Google.
  await sprawdz("zły klucz API daje zrozumiały komunikat", async () => {
    tryb = () => ({ kod: 400, tresc: { error: { message: "API key not valid. Please pass a valid API key." } } });
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    assert.match(r.tresc.wyniki[0].blad, /GEMINI_API_KEY/);
  });

  // Jeden styl padl, drugi wyszedl — klient ma dostac to, co sie udalo.
  await sprawdz("częściowa awaria oddaje to, co wyszło", async () => {
    let n = 0;
    tryb = () => (++n === 1 ? { kod: 429, tresc: { error: {} } } : OBRAZ_OK);
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej", "szkic"] });
    assert.strictEqual(r.kod, 200, "skoro coś wyszło, to nie jest błąd całego żądania");
    assert.strictEqual(r.tresc.udane, 1);
    assert.ok(r.tresc.wyniki.some((w) => /Limit zapytań/.test(w.blad || "")));
  });

  // 429 ma dwa zupelnie rozne znaczenia i musza dac rozne komunikaty:
  // zerowy limit darmowego poziomu (czekanie nic nie da) kontra chwilowe
  // przekroczenie tempa (czekanie pomoze).
  await sprawdz("429 z zerowym limitem mówi o płatnościach", async () => {
    tryb = () => ({ kod: 429, tresc: { error: { message: "Quota exceeded",
      details: [{ quotaId: "GenerateRequestsPerDayPerProjectPerModel-FreeTier",
                  quota_limit_value: "0" }] } } });
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    const b = r.tresc.wyniki[0].blad;
    assert.match(b, /Darmowy poziom/, "powinno wskazywać na darmowy poziom: " + b);
    assert.match(b, /FreeTier/, "powinno cytować limit podany przez Google");
    assert.doesNotMatch(b, /Odczekaj/, "czekanie tu nic nie da, nie sugerujmy tego");
  });

  await sprawdz("429 bez zerowego limitu proponuje odczekać", async () => {
    tryb = () => ({ kod: 429, tresc: { error: { message: "Too many requests" } } });
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    assert.match(r.tresc.wyniki[0].blad, /Odczekaj/);
  });

  // 402 zdarzyl sie realnie przy pierwszym uruchomieniu i wygladal jak usterka,
  // bo w konsoli Google widac bylo tysiac zlotych darmowych kredytow.
  await sprawdz("402 kieruje do doładowania przedpłaty", async () => {
    tryb = () => ({ kod: 402, tresc: { error: { code: 402,
      message: "Your prepayment credits are depleted.", status: "RESOURCE_EXHAUSTED" } } });
    const r = await wywolaj(handler, { ...zdjecie, haslo: "tajne", style: ["olej"] });
    const b = r.tresc.wyniki[0].blad;
    assert.match(b, /przedpłaty/);
    assert.match(b, /ai\.studio/);
    assert.doesNotMatch(b, /RESOURCE_EXHAUSTED/, "nie pokazujemy surowego JSON-a");
  });

  serwer.close();
  console.log(bledy ? `\n${bledy} testow nie przeszlo` : "\nWszystkie testy przeszly");
  process.exit(bledy ? 1 : 0);
})();
