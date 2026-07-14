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
    const { style, size, name, email } = body;

    const unit = PRICES[size];
    if (!unit) return json(400, { error: "Nieprawidłowy rozmiar." });

    const shipping = unit >= FREE_SHIPPING_FROM ? 0 : SHIPPING;
    const proto = event.headers["x-forwarded-proto"] || "https";
    const host = event.headers.host || "";
    const origin = event.headers.origin || (host ? proto + "://" + host : "");

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
      metadata: { styl: style || "", rozmiar: size || "", klient: name || "" },
      success_url: origin + "/podziekowanie.html?status=success",
      cancel_url: origin + "/index.html#konfigurator",
    });

    return json(200, { url: session.url });
  } catch (err) {
    return json(500, { error: err.message || "Błąd tworzenia płatności." });
  }
};
