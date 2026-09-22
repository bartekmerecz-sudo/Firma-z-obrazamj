/**
 * Wariant dla Netlify — cienka przejsciowka do /api/generate.js.
 *
 * Funkcja platnosci jest w tym repo zduplikowana miedzy Vercel a Netlify i to
 * sie juz mscilo przy innych plikach: poprawka trafiala do jednej kopii.
 * Tutaj logika jest jedna, a to tylko tlumaczenie formatu zdarzenia Netlify
 * na (req, res), ktorego uzywa Vercel.
 */
const handler = require("../../api/generate.js");

exports.handler = async (event) => {
  let kod = 200;
  const naglowki = {};
  let tresc = "";

  const res = {
    setHeader: (k, v) => { naglowki[k] = v; },
    status(c) { kod = c; return this; },
    json(o) { naglowki["Content-Type"] = "application/json"; tresc = JSON.stringify(o); return this; },
    end() { return this; },
  };

  const req = {
    method: event.httpMethod,
    headers: event.headers || {},
    body: event.isBase64Encoded && event.body
      ? Buffer.from(event.body, "base64").toString("utf8")
      : event.body,
  };

  await handler(req, res);
  return { statusCode: kod, headers: naglowki, body: tresc };
};
