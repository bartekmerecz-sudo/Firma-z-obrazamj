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

  /* ---------- Konfigurator ---------- */
  const form = $("#orderForm");
  if (!form) return;

  const sumStyle = $("#sumStyle");
  const sumSize = $("#sumSize");
  const sumShip = $("#sumShip");
  const sumTotal = $("#sumTotal");
  const fStyle = $("#fStyle");
  const fSize = $("#fSize");
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

  function recalc() {
    const style = selectedStyle();
    const size = selectedSize();
    const shipping = size.price >= FREE_SHIPPING_FROM ? 0 : SHIPPING;
    const total = size.price + shipping;

    if (sumStyle) sumStyle.textContent = style || "—";
    if (sumSize) sumSize.textContent = size.label || "—";
    if (sumShip) sumShip.textContent = shipping === 0 ? "Gratis" : shipping + " zł";
    if (sumTotal) sumTotal.textContent = total + " zł";

    if (fStyle) fStyle.value = style;
    if (fSize) fSize.value = size.label;
    if (fTotal) fTotal.value = total + " zł (w tym dostawa: " + (shipping === 0 ? "gratis" : shipping + " zł") + ")";
  }

  $$('input[name="style_radio"], input[name="size_radio"]').forEach((el) =>
    el.addEventListener("change", recalc)
  );
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

  /* ---------- Wysyłka formularza (Formspree AJAX) ---------- */
  const statusEl = $("#formStatus");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    recalc();

    // Jeśli formularz nie został jeszcze skonfigurowany (placeholder FORM_ID)
    if (form.action.includes("FORM_ID")) {
      setStatus(
        "Formularz nie jest jeszcze podłączony. Skonfiguruj Formspree (patrz README) " +
          "lub napisz na kontakt@pixelpedzel.pl.",
        "err"
      );
      return;
    }

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    setStatus("Wysyłanie…", "");
    const btn = $('button[type="submit"]', form);
    if (btn) btn.disabled = true;

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });
      if (res.ok) {
        form.reset();
        if (uploadPreview) uploadPreview.hidden = true;
        if (uploadBox) uploadBox.classList.remove("has-file");
        if (uploadText)
          uploadText.innerHTML =
            "Kliknij, aby wybrać zdjęcie<br /><small>JPG lub PNG, max ~10 MB, jedno zdjęcie</small>";
        recalc();
        setStatus(
          "Dziękujemy! Zamówienie przyjęte. Wkrótce wyślemy e-mail z potwierdzeniem i danymi do płatności.",
          "ok"
        );
      } else {
        const data = await res.json().catch(() => ({}));
        const msg =
          data.errors && data.errors.length
            ? data.errors.map((x) => x.message).join(", ")
            : "Coś poszło nie tak. Spróbuj ponownie lub napisz na kontakt@pixelpedzel.pl.";
        setStatus(msg, "err");
      }
    } catch (err) {
      setStatus(
        "Błąd połączenia. Sprawdź internet i spróbuj ponownie, lub napisz na kontakt@pixelpedzel.pl.",
        "err"
      );
    } finally {
      if (btn) btn.disabled = false;
    }
  });

  function setStatus(msg, kind) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.className = "form-status" + (kind ? " " + kind : "");
  }
})();
