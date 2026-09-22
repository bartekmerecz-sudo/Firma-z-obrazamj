/* PixelPedzel — pracownia. Logika strony /pracownia.html.
 *
 * Calosc rozmowy z Google idzie przez /api/generate, zeby klucz API nigdy nie
 * trafil do przegladarki. Tutaj zostaje: przygotowanie zdjecia, formularz
 * i pokazanie wynikow.
 */
(function () {
  "use strict";

  var MAX_BOK = 1536;      // dluzszy bok po zmniejszeniu
  var KLUCZ_HASLA = "pixelpedzel-pracownia";

  var el = function (id) { return document.getElementById(id); };
  var panel = el("panel"), kartaHaslo = el("karta-haslo");
  var zdjecie = null;      // { dane: base64 bez prefiksu, mime, szer, wys, nazwa }
  var style = [], limit = 4;
  // Dopoki na hostingu nie ma klucza i hasla, nie ma czym generowac. Bez tej
  // flagi odswiezPrzycisk() wlaczalo przycisk z powrotem przy kazdym klikniecu
  // stylu i "Generuj" wygladal na gotowy, chociaz konczyl sie komunikatem.
  var gotowe = true;

  // ---------------------------------------------------------------- pomocnicze
  function pokazKomunikat(tekst, typ) {
    var k = el("komunikat");
    if (!tekst) { k.innerHTML = ""; return; }
    k.innerHTML = '<div class="komunikat komunikat--' + (typ || "info") + '"></div>';
    k.firstChild.textContent = tekst;
  }

  function slug(t) {
    return (t || "").toLowerCase().trim()
      .replace(/[ąàáâ]/g, "a").replace(/[ćç]/g, "c").replace(/[ęèéê]/g, "e")
      .replace(/ł/g, "l").replace(/ń/g, "n").replace(/[óòô]/g, "o")
      .replace(/[śş]/g, "s").replace(/[żź]/g, "z")
      .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  }

  /* Zmniejszamy zdjecie W PRZEGLADARCE. Dwa powody: funkcje serverless maja
     limit wielkosci zadania (u Vercela 4,5 MB), a zdjecie prosto z telefonu
     potrafi miec 8 MB. Poza tym model i tak pracuje na okolo 1024 px, wiec
     wysylanie wiekszego pliku to czekanie bez zysku na jakosci. */
  function przygotuj(plik) {
    return new Promise(function (ok, zle) {
      if (!/^image\/(jpeg|png|webp)$/.test(plik.type))
        return zle(new Error("To nie jest JPG, PNG ani WEBP."));
      var url = URL.createObjectURL(plik);
      var img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var skala = Math.min(1, MAX_BOK / Math.max(img.width, img.height));
        var w = Math.round(img.width * skala), h = Math.round(img.height * skala);
        var c = document.createElement("canvas");
        c.width = w; c.height = h;
        var ctx = c.getContext("2d");
        ctx.imageSmoothingQuality = "high";
        ctx.drawImage(img, 0, 0, w, h);
        var dataUrl = c.toDataURL("image/jpeg", 0.92);
        ok({
          dane: dataUrl.split(",")[1],
          mime: "image/jpeg",
          szer: w, wys: h,
          podglad: dataUrl,
          nazwa: plik.name || "zdjecie",
          oryginal: img.width + "×" + img.height,
        });
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        zle(new Error("Nie udało się otworzyć tego pliku."));
      };
      img.src = url;
    });
  }

  function ustawZdjecie(z) {
    zdjecie = z;
    el("podglad-img").src = z.podglad;
    el("podglad-meta").textContent =
      z.nazwa + " · " + z.oryginal + " → wysyłam " + z.szer + "×" + z.wys;
    el("podglad").hidden = false;
    el("strefa").hidden = true;
    odswiezPrzycisk();
  }

  function wyczyscZdjecie() {
    zdjecie = null;
    el("podglad").hidden = true;
    el("strefa").hidden = false;
    el("plik").value = "";
    odswiezPrzycisk();
  }

  function wybrane() {
    return Array.prototype.slice
      .call(document.querySelectorAll("#chipy input:checked"))
      .map(function (i) { return i.value; });
  }

  function odswiezPrzycisk() {
    var n = wybrane().length;
    el("generuj").disabled = !gotowe || !zdjecie || n === 0;
    el("generuj").textContent = n > 1 ? "Generuj " + n + " style" : "Generuj";
    el("kopiuj-prompt").hidden = !gotowe || n !== 1;
    // Limit jest po stronie serwera i tak, ale lepiej wygasic chipy, niz dac
    // klikac i dopiero potem powiedziec "nie".
    var maks = n >= limit;
    Array.prototype.forEach.call(document.querySelectorAll("#chipy input"), function (i) {
      i.disabled = maks && !i.checked;
    });
    el("licznik").textContent = "· wybrane " + n + " z " + limit;
  }

  // ---------------------------------------------------------------- formularz
  function zbudujChipy() {
    var box = el("chipy");
    box.innerHTML = "";
    style.forEach(function (s) {
      var lab = document.createElement("label");
      lab.className = "chip";
      lab.title = s.opis || "";
      var inp = document.createElement("input");
      inp.type = "checkbox"; inp.value = s.id;
      inp.addEventListener("change", odswiezPrzycisk);
      var sp = document.createElement("span");
      sp.textContent = s.nazwa;
      lab.appendChild(inp); lab.appendChild(sp);
      box.appendChild(lab);
    });
  }

  function podepnijZrzut() {
    var strefa = el("strefa"), plik = el("plik");
    strefa.addEventListener("click", function () { plik.click(); });
    strefa.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); plik.click(); }
    });
    plik.addEventListener("change", function () {
      if (plik.files && plik.files[0]) wczytaj(plik.files[0]);
    });
    ["dragenter", "dragover"].forEach(function (t) {
      strefa.addEventListener(t, function (e) {
        e.preventDefault(); strefa.classList.add("nad");
      });
    });
    ["dragleave", "drop"].forEach(function (t) {
      strefa.addEventListener(t, function (e) {
        e.preventDefault(); strefa.classList.remove("nad");
      });
    });
    strefa.addEventListener("drop", function (e) {
      var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      if (f) wczytaj(f);
    });
    // Wklejanie ze schowka — zdjecia najczesciej przychodza na Messengerze,
    // wiec zrzut ekranu i Ctrl+V jest szybsze niz zapisywanie pliku na dysk.
    document.addEventListener("paste", function (e) {
      if (panel.hidden) return;
      var items = (e.clipboardData && e.clipboardData.items) || [];
      for (var i = 0; i < items.length; i++) {
        if (items[i].type.indexOf("image/") === 0) {
          var f = items[i].getAsFile();
          if (f) { wczytaj(f); e.preventDefault(); return; }
        }
      }
    });
    el("usun").addEventListener("click", wyczyscZdjecie);
  }

  function wczytaj(f) {
    pokazKomunikat("");
    przygotuj(f).then(ustawZdjecie).catch(function (e) {
      pokazKomunikat(e.message, "blad");
    });
  }

  // ---------------------------------------------------------------- generowanie
  function szkielety(ids) {
    var box = el("wyniki");
    box.innerHTML = "";
    ids.forEach(function (id) {
      var s = style.filter(function (x) { return x.id === id; })[0] || { nazwa: id };
      var d = document.createElement("div");
      d.className = "wynik";
      d.id = "w-" + id;
      d.innerHTML = '<div class="szkielet"></div><div class="stopka">' +
                    '<span class="nazwa"></span><span class="meta">pracuję…</span></div>';
      d.querySelector(".nazwa").textContent = s.nazwa;
      box.appendChild(d);
    });
  }

  function pokazWynik(w) {
    var s = style.filter(function (x) { return x.id === w.styl; })[0] || { nazwa: w.styl };
    var d = el("w-" + w.styl);
    if (!d) return;
    if (w.blad) {
      d.className = "wynik pusty";
      d.textContent = s.nazwa + " — " + w.blad;
      return;
    }
    var nazwaPliku = [slug(el("zamowienie").value) || "pracownia", w.styl,
                      new Date().toISOString().slice(0, 10)].join("-") + ".png";
    d.innerHTML = "";
    var img = document.createElement("img");
    img.src = "data:" + w.mime + ";base64," + w.obraz;
    img.alt = s.nazwa;
    var stopka = document.createElement("div");
    stopka.className = "stopka";
    var nazwa = document.createElement("span");
    nazwa.className = "nazwa"; nazwa.textContent = s.nazwa;
    var a = document.createElement("a");
    a.className = "btn btn--maly"; a.textContent = "Pobierz";
    a.href = img.src; a.download = nazwaPliku;
    stopka.appendChild(nazwa); stopka.appendChild(a);
    d.appendChild(img); d.appendChild(stopka);
  }

  function generuj() {
    var ids = wybrane();
    if (!zdjecie || !ids.length) return;
    var btn = el("generuj");
    btn.disabled = true;
    pokazKomunikat("");
    el("status").textContent = "Generuję " + ids.length +
      (ids.length === 1 ? " styl…" : " style…") + " to zwykle 15–40 sekund.";
    szkielety(ids);

    fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        haslo: localStorage.getItem(KLUCZ_HASLA) || "",
        zdjecie: zdjecie.dane,
        mime: zdjecie.mime,
        style: ids,
        orientacja: el("orientacja").value,
        uwagi: el("uwagi").value,
      }),
    })
      .then(function (r) { return r.json().then(function (j) { return { r: r, j: j }; }); })
      .then(function (o) {
        if (o.r.status === 401) {
          localStorage.removeItem(KLUCZ_HASLA);
          zablokuj();
          throw new Error("Hasło przestało pasować — zaloguj się ponownie.");
        }
        if (!o.j.wyniki) throw new Error(o.j.blad || "Coś poszło nie tak.");
        o.j.wyniki.forEach(pokazWynik);
        var ile = o.j.udane || 0;
        el("status").textContent = ile + " z " + ids.length + " gotowe.";
        if (!ile) pokazKomunikat("Żaden styl nie wyszedł. Szczegóły przy kafelkach niżej.", "blad");
      })
      .catch(function (e) {
        el("wyniki").innerHTML = "";
        el("status").textContent = "";
        pokazKomunikat(e.message, "blad");
      })
      .then(function () { btn.disabled = false; odswiezPrzycisk(); });
  }

  // ---------------------------------------------------------------- haslo
  function odblokuj() {
    kartaHaslo.hidden = true;
    panel.hidden = false;
  }
  function zablokuj() {
    kartaHaslo.hidden = false;
    panel.hidden = true;
    el("haslo").value = "";
  }

  function start() {
    fetch("/api/generate")
      .then(function (r) { return r.json(); })
      .then(function (j) {
        style = j.style || [];
        limit = j.limit || 4;
        zbudujChipy();
        odswiezPrzycisk();
        if (!j.skonfigurowane) {
          kartaHaslo.hidden = true;
          panel.hidden = false;
          var brak = (j.brakuje || []).join(" i ") || "GEMINI_API_KEY i PRACOWNIA_HASLO";
          pokazKomunikat(
            "Hosting nie widzi zmiennej: " + brak + ". Sprawdź pisownię nazwy, " +
            "zaznaczenie środowiska Production i czy po zapisaniu był Redeploy — " +
            "instrukcja w docs/32.", "blad");
          gotowe = false;
          odswiezPrzycisk();
          return;
        }
        if (localStorage.getItem(KLUCZ_HASLA)) odblokuj();
      })
      .catch(function () {
        pokazKomunikat("Nie mogę pobrać listy stylów. Czy /api/generate jest wdrożone?", "blad");
      });

    el("wejdz").addEventListener("click", function () {
      var h = el("haslo").value;
      if (!h) return;
      localStorage.setItem(KLUCZ_HASLA, h);
      odblokuj();
    });
    el("haslo").addEventListener("keydown", function (e) {
      if (e.key === "Enter") el("wejdz").click();
    });
    el("wyloguj").addEventListener("click", function () {
      localStorage.removeItem(KLUCZ_HASLA);
      zablokuj();
    });
    el("generuj").addEventListener("click", generuj);
    el("kopiuj-prompt").addEventListener("click", function () {
      // Awaryjnie: gdy API nie dziala, chcemy miec czym wkleic do Gemini recznie.
      var id = wybrane()[0];
      fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          haslo: localStorage.getItem(KLUCZ_HASLA) || "",
          podglad_promptu: true, style: [id],
          orientacja: el("orientacja").value, uwagi: el("uwagi").value,
          zdjecie: "x", mime: "image/jpeg",
        }),
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.prompt) throw new Error(j.blad || "Nie udało się pobrać promptu.");
          return navigator.clipboard.writeText(j.prompt);
        })
        .then(function () { pokazKomunikat("Prompt skopiowany — wklej go do Gemini razem ze zdjęciem."); })
        .catch(function (e) { pokazKomunikat(e.message, "blad"); });
    });
    podepnijZrzut();
  }

  document.addEventListener("DOMContentLoaded", start);
})();
