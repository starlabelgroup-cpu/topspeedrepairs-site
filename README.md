# topspeedrepairs.com — Top Speed Appliance (Premium Redesign, Option A)

Standalone site for **topspeedrepairs.com only**, built to the approved Figma
design "Top Speed — Premium Redesign 2026" (*precision motorsport, elevated*).
The flagship (top-speed-service-os) is untouched by this repo.

## Structure

- `build.py` — the generator. Run `python3 build.py` to regenerate every page
  from the templates + `cities_data.py` (the live 65-city directory).
- Static output is committed alongside the generator (Vercel serves the repo
  root; `cleanUrls` on).
- `assets/css/site.css` — the design system (tokens + components from the
  Figma kit: Deep Navy ramp, Signal Red, Orbitron / Rajdhani / Inter).
- `assets/js/book.js` — the booking form. It posts **directly** to the Service
  OS intake (`POST https://top-speed-service-os.vercel.app/api/v1/speedy/book`,
  the flagship's exact payload shape). The API's CORS allowlists
  `https://topspeedrepairs.com` (verified 2026-11-24), so no proxy and no
  flagship change were needed.
- Speedy chat is the flagship's real widget
  (`https://topspeedserviceos.com/speedy-widget.js`) — same knowledge base,
  same queue. "Ask Speedy" buttons call `window.TSOpenSpeedy`.
- `api/img.js` + `api/_imgdata.js` — the two art-directed photos are served
  from base64 chunks because the GitHub write path is text-only (see
  `gen_imgdata.py`). URLs: `/api/img?n=hero-kitchen`, `/api/img?n=city-van`.

## Pages

Home · `/book` · `/services` + 9 service pages · `/cities` + 65 city pages ·
`/pricing` · `/privacy` · `/terms` · 404 · `sitemap.xml` · `robots.txt` ·
`llms.txt` — 81 sitemap URLs.

## Locked facts (do not edit casually)

(844) 460-7038 · 65 cities · 9 services · Mon–Fri 8am–7pm · $99 residential
diagnostic credited toward repair (due if declined) · $210 flat repair labor ·
$150 flat installation labor · parts at written quote · "The Faster, The
Better." · service-area business — **no street address anywhere** · no ratings
or review counts · form leads, Speedy below.
