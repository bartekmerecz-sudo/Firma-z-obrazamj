/**
 * PixelPędzel — automatyczne płatności (Stripe Checkout) — wariant dla Netlify.
 *
 * Ta sama logika co w /api/create-checkout-session.js, ale w formacie
 * funkcji Netlify (exports.handler). Dzięki netlify.toml frontend może
 * wołać ten sam adres /api/create-checkout-session na obu platformach.
 *
 * Wymagana zmienna środowiskowa: STRIPE_SECRET_KEY.
 */

const PRICES = {
  "30×40 cm": 12900,
  "40×50 cm": 16900,
  "50×70 cm": 22900,
  "60×90 cm": 29900,
};
const ADDONS = {
  ekspres: { label: "Ekspres 48h", price: 4900 },
  cyfrowa: { label: "Wersja cyfrowa", price: 2900 },
  rama: { label: "Rama drewniana", price: 7900 },
};
const SHIPPING = 1500;
const FREE_SHIPPING_FROM = 25000;

const json = (statusCode, obj) => ({
  statusCode,
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  },
  body: JSON.stringify(obj),
});

exports.handler = async (event) => {
  if (event.httpMethod !== "POST")
    return json(405, { error: "Metoda niedozwolona." });

  const key = process.env.STRIPE_SECRET_KEY;
  if (!key)
    return json(501, {
      error:
        "Płatności online nie są jeszcze skonfigurowane (brak STRIPE_SECRET_KEY).",
    });

  let stripe;
  try {
    stripe = require("stripe")(key);
  } catch (e) {
    return json(500, { error: "Brak biblioteki 'stripe'. Uruchom `npm install`." });
  }

  try {
    const body = JSON.parse(event.body || "{}");

    const proto = event.headers["x-forwarded-proto"] || "https";
    const host = event.headers.host || "";
    const origin = event.headers.origin || (host ? proto + "://" + host : "");

    // --- BON PODARUNKOWY ---
    if (body.bon) {
      const zl = parseInt(body.amount, 10);
      if (!zl || zl < 50 || zl > 2000)
        return json(400, { error: "Nieprawidłowa kwota bonu (50–2000 zł)." });
      const bonSession = await stripe.checkout.sessions.create({
        mode: "payment",
        payment_method_types: ["card", "blik", "p24"],
        line_items: [
          {
            price_data: {
              currency: "pln",
              unit_amount: zl * 100,
              product_data: {
                name: "Bon podarunkowy PixelPędzel — " + zl + " zł",
                description:
                  "Ważny 6 miesięcy, do wykorzystania na dowolny obraz.",
              },
            },
            quantity: 1,
          },
        ],
        customer_email: body.email || undefined,
        metadata: { typ: "bon", kwota: zl + " zł" },
        success_url: origin + "/podziekowanie.html?status=bon",
        cancel_url: origin + "/index.html#bon",
      });
      return json(200, { url: bonSession.url });
    }

    const { style, size, orient, addons, name, email } = body;

    const unit = PRICES[size];
    if (!unit) return json(400, { error: "Nieprawidłowy rozmiar." });

    const chosen = (Array.isArray(addons) ? addons : [])
      .map((c) => ADDONS[c])
      .filter(Boolean);
    const addonsTotal = chosen.reduce((s, a) => s + a.price, 0);
    const subtotal = unit + addonsTotal;
    const shipping = subtotal >= FREE_SHIPPING_FROM ? 0 : SHIPPING;

    const line_items = [
      {
        price_data: {
          currency: "pln",
          unit_amount: unit,
          product_data: {
            name: "Obraz na płótnie — " + (style || "wybrany styl"),
            description: "Rozmiar: " + size + (orient ? " · " + orient : ""),
          },
        },
        quantity: 1,
      },
    ];
    chosen.forEach((a) => {
      line_items.push({
        price_data: {
          currency: "pln",
          unit_amount: a.price,
          product_data: { name: "Dodatek: " + a.label },
        },
        quantity: 1,
      });
    });
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
        orientacja: orient || "",
        dodatki: chosen.map((a) => a.label).join(", ") || "brak",
        klient: name || "",
      },
      success_url: origin + "/podziekowanie.html?status=success",
      cancel_url: origin + "/index.html#konfigurator",
    });

    return json(200, { url: session.url });
  } catch (err) {
    return json(500, { error: err.message || "Błąd tworzenia płatności." });
  }
};
