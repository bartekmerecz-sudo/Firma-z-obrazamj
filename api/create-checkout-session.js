/**
 * PixelPędzel — automatyczne płatności (Stripe Checkout)
 *
 * Funkcja serverless kompatybilna z Vercel (folder /api) oraz Netlify
 * (przez netlify.toml, który przekierowuje /api/* na /.netlify/functions/*).
 *
 * Tworzy sesję Stripe Checkout w PLN z metodami: karta, BLIK, Przelewy24.
 * WAŻNE: cena jest liczona TUTAJ (po stronie serwera) na podstawie rozmiaru —
 * nigdy nie ufamy cenie przesłanej z przeglądarki.
 *
 * Wymagana zmienna środowiskowa: STRIPE_SECRET_KEY (patrz README).
 */

// Ceny w groszach (1 zł = 100 gr) — muszą odpowiadać cennikowi na stronie.
const PRICES = {
  "30×40 cm": 12900,
  "40×50 cm": 16900,
  "50×70 cm": 22900,
  "60×90 cm": 29900,
};
const SHIPPING = 1500;        // 15 zł
const FREE_SHIPPING_FROM = 25000; // darmowa dostawa od 250 zł

module.exports = async (req, res) => {
  // CORS (na wypadek innego hosta frontendu)
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST")
    return res.status(405).json({ error: "Metoda niedozwolona." });

  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) {
    return res.status(501).json({
      error:
        "Płatności online nie są jeszcze skonfigurowane (brak STRIPE_SECRET_KEY).",
    });
  }

  let stripe;
  try {
    stripe = require("stripe")(key);
  } catch (e) {
    return res
      .status(500)
      .json({ error: "Brak biblioteki 'stripe'. Uruchom `npm install`." });
  }

  try {
    const body =
      typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
    const { style, size, name, email } = body;

    const unit = PRICES[size];
    if (!unit) return res.status(400).json({ error: "Nieprawidłowy rozmiar." });

    const shipping = unit >= FREE_SHIPPING_FROM ? 0 : SHIPPING;
    const origin =
      req.headers.origin ||
      (req.headers.host ? "https://" + req.headers.host : "");

    const line_items = [
      {
        price_data: {
          currency: "pln",
          unit_amount: unit,
          product_data: {
            name: "Obraz na płótnie — " + (style || "wybrany styl"),
            description: "Rozmiar: " + size,
          },
        },
        quantity: 1,
      },
    ];
    if (shipping > 0) {
      line_items.push({
        price_data: {
          currency: "pln",
          unit_amount: shipping,
          product_data: { name: "Dostawa (kurier)" },
        },
        quantity: 1,
      });
    }

    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      payment_method_types: ["card", "blik", "p24"],
      line_items,
      customer_email: email || undefined,
      metadata: {
        styl: style || "",
        rozmiar: size || "",
        klient: name || "",
      },
      success_url: origin + "/podziekowanie.html?status=success",
      cancel_url: origin + "/index.html#konfigurator",
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    return res
      .status(500)
      .json({ error: err.message || "Błąd tworzenia płatności." });
  }
};
