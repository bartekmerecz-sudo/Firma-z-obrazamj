/* ============================================================
   PixelPędzel — logika strony
   ============================================================ */
(function () {
  "use strict";

  const SHIPPING = 15;          // koszt dostawy (zł)
  const FREE_SHIPPING_FROM = 250; // darmowa dostawa od (zł)

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ---------- Rok w stopce ---------- */
  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Menu mobilne ---------- */
  const toggle = $(".nav__toggle");
  const links = $(".nav__links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    $$(".nav__links a").forEach((a) =>
      a.addEventListener("click", () => {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      })
    );
  }

  /* ---------- Suwak „przed → po" ---------- */
  $$("[data-compare]").forEach((box) => {
    const after = $(".compare__after", box);
    const handle = $(".compare__handle", box);
    if (!after || !handle) return;

    const setPos = (clientX) => {
      const rect = box.getBoundingClientRect();
      let pct = ((clientX - rect.left) / rect.width) * 100;
      pct = Math.max(0, Math.min(100, pct));
      after.style.clipPath = "inset(0 0 0 " + pct + "%)";
      handle.style.left = pct + "%";
    };

    let dragging = false;
    const start = (e) => { dragging = true; move(e); };
    const stop = () => { dragging = false; };
    const move = (e) => {
      if (!dragging) return;
      const x = e.touches ? e.touches[0].clientX : e.clientX;
      setPos(x);
      if (e.cancelable) e.preventDefault();
    };

    box.addEventListener("mousedown", start);
    box.addEventListener("touchstart", start, { passive: true });
    window.addEventListener("mousemove", move);
    window.addEventListener("touchmove", move, { passive: false });
    window.addEventListener("mouseup", stop);
    window.addEventListener("touchend", stop);
    // klik = ustaw pozycję
    box.addEventListener("click", (e) => setPos(e.clientX));
  });

  /* ---------- Konfigurator ---------- */
  const form = $("#orderForm");
  if (!form) return;

  const sumStyle = $("#sumStyle");
  const sumSize = $("#sumSize");
  const sumOrient = $("#sumOrient");
  const sumAddons = $("#sumAddons");
  const sumAddonsRow = $("#sumAddonsRow");
  const sumShip = $("#sumShip");
  const sumTotal = $("#sumTotal");
  const fStyle = $("#fStyle");
  const fSize = $("#fSize");
  const fOrient = $("#fOrient");
  const fAddons = $("#fAddons");
  const fTotal = $("#fTotal");

  function selectedStyle() {
    const el = $('input[name="style_radio"]:checked');
    return el ? el.value : "";
  }
  function selectedSize() {
    const el = $('input[name="size_radio"]:checked');
    return el
      ? { label: el.value, price: parseInt(el.dataset.price, 10) || 0 }
      : { label: "", price: 0 };
  }
  function selectedOrient() {
    const el = $('input[name="orient_radio"]:checked');
    return el ? el.value : "Pionowa";
  }
  function selectedAddons() {
    return $$('input[name="addon"]:checked').map((el) => ({
      code: el.value,
      label: el.dataset.label || el.value,
      price: parseInt(el.dataset.price, 10) || 0,
    }));
  }

  function recalc() {
    const style = selectedStyle();
    const size = selectedSize();
    const orient = selectedOrient();
    const addons = selectedAddons();
    const addonsTotal = addons.reduce((s, a) => s + a.price, 0);
    const subtotal = size.price + addonsTotal;
    const shipping = subtotal >= FREE_SHIPPING_FROM ? 0 : SHIPPING;
    const total = subtotal + shipping;

    if (sumStyle) sumStyle.textContent = style || "—";
    if (sumSize) sumSize.textContent = size.label || "—";
    if (sumOrient) sumOrient.textContent = orient;
    if (sumAddonsRow) sumAddonsRow.hidden = addons.length === 0;
    if (sumAddons)
      sumAddons.textContent = addons.length
        ? addons.map((a) => a.label + " (+" + a.price + " zł)").join(", ")
        : "—";
    if (sumShip) sumShip.textContent = shipping === 0 ? "Gratis" : shipping + " zł";
    if (sumTotal) sumTotal.textContent = total + " zł";

    if (fStyle) fStyle.value = style;
    if (fSize) fSize.value = size.label;
    if (fOrient) fOrient.value = orient;
    if (fAddons) fAddons.value = addons.length ? addons.map((a) => a.label).join(", ") : "brak";
    if (fTotal)
      fTotal.value =
        total + " zł (w tym dostawa: " + (shipping === 0 ? "gratis" : shipping + " zł") + ")";
  }

  $$(
    'input[name="style_radio"], input[name="size_radio"], input[name="orient_radio"], input[name="addon"]'
  ).forEach((el) => el.addEventListener("change", recalc));
  recalc();

  /* ---------- Klik w kartę galerii → wybierz styl + przewiń ---------- */
  $$(".card[data-style]").forEach((card) => {
    card.style.cursor = "pointer";
    card.addEventListener("click", () => {
      const name = card.getAttribute("data-style");
      const radio = $(`input[name="style_radio"][value="${name}"]`);
      if (radio) {
        radio.checked = true;
        recalc();
      }
      const cfg = $("#konfigurator");
      if (cfg) cfg.scrollIntoView({ behavior: "smooth" });
    });
  });

  /* ---------- Podgląd zdjęcia ---------- */
  const photoInput = $("#photoInput");
  const uploadBox = $("#uploadBox");
  const uploadText = $("#uploadText");
  const uploadPreview = $("#uploadPreview");
  if (photoInput) {
    photoInput.addEventListener("change", () => {
      const file = photoInput.files && photoInput.files[0];
      if (!file) return;
      if (file.size > 12 * 1024 * 1024) {
        alert("Plik jest zbyt duży (max ~10 MB). Wybierz mniejsze zdjęcie.");
        photoInput.value = "";
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        uploadPreview.src = e.target.result;
        uploadPreview.hidden = false;
        uploadText.innerHTML =
          "<strong>" + file.name + "</strong><br /><small>Kliknij, aby zmienić zdjęcie</small>";
        uploadBox.classList.add("has-file");
      };
      reader.readAsDataURL(file);
    });
  }

  /* ---------- Wysyłka zamówienia ----------
     Przepływ:
     1) Zapis zamówienia (+ zdjęcie) przez Formspree.
     2) Potwierdzenie: "przygotuję projekt i odezwę się w 24 h".

     Zamówienie obrazu NIE przechodzi tu przez płatność. Link do zapłaty
     wysyłamy ręcznie, dopiero po akceptacji projektu — tak brzmi obietnica
     powtórzona na stronie pięć razy i we wszystkich materiałach.

     PAYMENT_ENDPOINT zostaje, bo korzysta z niego bon podarunkowy (orderBon):
     tam przedpłata jest naturalna, bo nie ma projektu do zaakceptowania.
  */
  const PAYMENT_ENDPOINT = "/api/create-checkout-session";
  const statusEl = $("#formStatus");

  function resetFormUI() {
    form.reset();
    if (uploadPreview) uploadPreview.hidden = true;
    if (uploadBox) uploadBox.classList.remove("has-file");
    if (uploadText)
      uploadText.innerHTML =
        "Kliknij, aby wybrać zdjęcie<br /><small>JPG lub PNG, max ~10 MB, jedno zdjęcie</small>";
    recalc();
  }

  // --- BON PODARUNKOWY: zakup przez Stripe Checkout ---
  async function orderBon(amount) {
    const st = document.querySelector("#bonStatus");
    const zl = parseInt(amount, 10);
    const say = (m, cls) => {
      if (st) st.className = "hint" + (cls ? " " + cls : "");
      if (st) st.textContent = m;
    };
    if (!zl || zl < 50 || zl > 2000) {
      say("Podaj kwotę od 50 do 2000 zł.", "err");
      return;
    }
    say("Przenoszę do bezpiecznej płatności…");
    try {
      const r = await fetch(PAYMENT_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bon: true, amount: zl }),
      });
      if (r.ok) {
        const d = await r.json().catch(() => ({}));
        if (d && d.url) {
          window.location.href = d.url;
          return;
        }
      }
      const d = await r.json().catch(() => ({}));
      say(
        d.error ||
          "Płatności chwilowo niedostępne. Napisz: pixelpedzelkontakt@gmail.com",
        "err"
      );
    } catch (_) {
      say("Błąd połączenia. Spróbuj ponownie.", "err");
    }
  }
  document.querySelectorAll(".bon-amt").forEach((b) =>
    b.addEventListener("click", () => orderBon(b.getAttribute("data-amount")))
  );
  const bonCustomBtn = document.querySelector("#bonCustomBtn");
  if (bonCustomBtn)
    bonCustomBtn.addEventListener("click", () =>
      orderBon((document.querySelector("#bonCustom") || {}).value)
    );

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    recalc();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const btn = $('button[type="submit"]', form);
    const order = {
      style: selectedStyle(),
      size: selectedSize().label,
      orient: selectedOrient(),
      addons: selectedAddons().map((a) => a.code),
      name: (($("#name") || {}).value || "").trim(),
      email: (($("#email") || {}).value || "").trim(),
    };

    if (btn) btn.disabled = true;
    setStatus("Przetwarzanie zamówienia…", "");

    // 1) Zapis zamówienia (+ zdjęcie) w Formspree
    let orderRecorded = false;
    const formspreeConfigured = !form.action.includes("FORM_ID");
    if (formspreeConfigured) {
      try {
        const r = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" },
        });
        orderRecorded = r.ok;
      } catch (_) {
        orderRecorded = false;
      }
    }

    // 2) Potwierdzenie. Platnosci NIE pobieramy tutaj.
    //
    // Strona obiecuje w pieciu miejscach "placisz, gdy Ci sie spodoba" i to samo
    // mowia wszystkie posty, TikToki oraz ogloszenie na OLX. Przekierowanie
    // prosto do Stripe zaraz po formularzu przeczylo tej obietnicy dokladnie
    // w momencie, w ktorym miala zadzialac. Link do platnosci wysylamy recznie,
    // dopiero gdy klient zaakceptuje projekt.
    //
    // Bon podarunkowy zostaje na Stripe (orderBon) — tam przedplata jest
    // naturalna, bo nie ma projektu do zaakceptowania.
    if (orderRecorded) {
      resetFormUI();
      setStatus(
        "Dziękujemy! Zamówienie przyjęte. Przygotuję projekt i odezwę się " +
          "na podany e-mail w ciągu 24 godzin. Płacisz dopiero, gdy projekt " +
          "Ci się spodoba.",
        "ok"
      );
    } else {
      setStatus(
        "Nie udało się wysłać zamówienia. Spróbuj ponownie lub napisz na " +
          "pixelpedzelkontakt@gmail.com",
        "err"
      );
    }
    if (btn) btn.disabled = false;
  });

  /* Krawedz pod paskiem nawigacji pojawia sie dopiero, gdy tresc pod niego
     wchodzi. Nasluch jest pasywny i odczytuje scrollY raz na klatke —
     handler scrolla wykonywany synchronicznie potrafi zaciac przewijanie. */
  (function navScrollEdge() {
    const nav = document.querySelector(".nav");
    if (!nav) return;
    let ticking = false;
    const apply = () => {
      nav.classList.toggle("is-scrolled", window.scrollY > 8);
      ticking = false;
    };
    addEventListener("scroll", () => {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
  })();

  function setStatus(msg, kind) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.className = "form-status" + (kind ? " " + kind : "");
  }
})();
