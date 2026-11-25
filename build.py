#!/usr/bin/env python3
"""Top Speed — topspeedrepairs.com · premium redesign (Option A standalone).
Generates the full static site from the approved Figma design system.
Run:  python3 build.py   (writes the site into this repo's root)
Pages: home, /book, /services + 9 service pages, /cities + 65 city pages,
/pricing, /privacy, /terms, 404, sitemap.xml, robots.txt, llms.txt.
Locked facts only — see DESIGN-BRIEF.md in the redesign package."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cities_data import CITIES

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://topspeedrepairs.com"
PHONE = "(844) 460-7038"
TEL = "tel:+18444607038"
FLAG = "https://topspeedserviceos.com"
IMG_HERO = "/api/img?n=hero-tech"
IMG_VAN = "/api/img?n=city-van"

# ---------------------------------------------------------------- services
SERVICES = [
 dict(slug="refrigerator-repair", name="Refrigerator Repair", short="Refrigerator",
      img="/api/img?n=svc-refrigerator", alt="Samsung French-door refrigerator with ice and water dispenser",
      h1a="Your fridge,", h1b="back to cold.", price=210,
      blurb="Not cooling, leaking, ice maker down — diagnosed on the first visit and quoted in writing before any work starts.",
      symptoms=[("Running warm","Food spoiling before its date — airflow, fans or sealed-system faults, confirmed on site."),
                ("Leaking water","Puddles inside or underneath — drain lines, valves and seals traced to the source."),
                ("Ice maker quit","No ice, slow ice, bad taste — maker, valve and filter checked in one pass."),
                ("Noisy or cycling","Loud fans, clicking, constant running — motors and controls tested before a quote.")]),
 dict(slug="washer-repair", name="Washer Repair", short="Washer",
      img="/api/img?n=svc-washer", alt="Whirlpool Cabrio top-load washer",
      h1a="Your washer,", h1b="back in the wash.", price=210,
      blurb="Won't drain, spin or fill — pumps, belts and seals checked on site and quoted in writing before any work starts.",
      symptoms=[("Won't drain","Standing water after the cycle — pump, hose and filter traced on site."),
                ("Won't spin or agitate","Belts, couplers and motors tested before a quote is written."),
                ("Leaking","Puddles at the base — hoses, seals and valves checked in one pass."),
                ("Loud or shaking","Banging on spin — suspension, bearings and level confirmed on site.")]),
 dict(slug="dryer-repair", name="Dryer Repair", short="Dryer",
      img="/api/img?n=svc-dryer", alt="GE dryer",
      h1a="Your dryer,", h1b="back to hot.", price=210,
      blurb="Runs but no heat, or drums that won't turn — elements, fuses and airflow tested end to end.",
      symptoms=[("No heat","Runs cold — elements, fuses and thermostats tested end to end."),
                ("Won't tumble","Drum still, motor humming — belts and rollers checked on site."),
                ("Takes forever","Three cycles to dry — airflow and venting tested first."),
                ("Squealing or thumping","Noise that grows — rollers, glides and bearings inspected before a quote.")]),
 dict(slug="oven-range-repair", name="Oven & Range Repair", short="Oven",
      img="/api/img?n=svc-oven", alt="Whirlpool glass-top slide-in range",
      h1a="Your oven,", h1b="back to baking.", price=210,
      blurb="Won't heat, uneven baking, dead burners — igniters, elements and controls checked safely.",
      symptoms=[("Won't heat","Dead oven, cold range — igniters and elements tested safely."),
                ("Uneven baking","Hot spots and raw centers — sensors and elements calibrated on site."),
                ("Dead burner","One ring out — switches and elements traced before a quote."),
                ("Temperature off","Burning or underdone — thermostat and control checked in one pass.")]),
 dict(slug="dishwasher-repair", name="Dishwasher Repair", short="Dishwasher",
      img="/api/img?n=svc-dishwasher", alt="Stainless KitchenAid dishwasher installed under a granite counter",
      h1a="Your dishwasher,", h1b="back to clean.", price=210,
      blurb="Won't run, drain or clean — door, drain and control faults traced before a quote is written.",
      symptoms=[("Won't drain","Water standing in the tub — pump, hose and filter traced on site."),
                ("Won't start","Dead panel or silent start — door latch, power and controls checked safely."),
                ("Leaking","Puddles at the door — seals, valves and hoses inspected first."),
                ("Dishes still dirty","Grit and film — spray arms, filters and water heat tested end to end.")]),
 dict(slug="freezer-ice-maker-repair", name="Freezer & Ice Maker Repair", short="Freezer",
      img="/api/img?n=svc-freezer", alt="In-door ice maker unit",
      h1a="Your freezer,", h1b="back to frozen.", price=210,
      blurb="Thawing food or an ice maker that's quit — airflow, fans and controls inspected first.",
      symptoms=[("Thawing food","Soft ice cream, warm spots — airflow, fans and sealed system checked."),
                ("Ice maker quit","No ice or slow ice — maker, valve and filter checked in one pass."),
                ("Frost buildup","Ice on the walls — defrost system and door seals tested on site."),
                ("Running constantly","Never cycles off — coils, fans and controls tested before a quote.")]),
 dict(slug="microwave-repair", name="Microwave Repair", short="Microwave",
      img="/api/img?n=svc-microwave", alt="Sharp microwave drawer installed under a marble counter",
      h1a="Your microwave,", h1b="back to heating.", price=210,
      blurb="Dead panel, no heat, sparking — door switches and power checked the safe way, on site.",
      symptoms=[("No heat","Runs but food stays cold — power parts tested the safe way, on site."),
                ("Dead panel","No lights, no response — power and controls traced before a quote."),
                ("Sparking","Arcing inside — waveguide and interior inspected first, safely."),
                ("Turntable stopped","Plate still, food uneven — motor and rollers checked in one pass.")]),
 dict(slug="garbage-disposal-repair", name="Garbage Disposal Repair", short="Disposal",
      img="/api/img?n=svc-disposal", alt="Garbage disposal installed under a kitchen sink",
      h1a="Your disposal,", h1b="back to clear.", price=210,
      blurb="Jammed, humming or leaking — cleared and tested safely under the sink.",
      symptoms=[("Jammed","Stuck solid — cleared safely and tested under load."),
                ("Humming, not grinding","Motor hums, plate still — jam and motor faults traced on site."),
                ("Leaking","Drips under the sink — seals, flange and housing checked in one pass."),
                ("Won't turn on","Silent at the switch — power, reset and switch tested before a quote.")]),
 dict(slug="appliance-installation", name="Appliance Installation", short="Installation",
      img="/api/img?n=svc-installation", alt="Built-in side-by-side refrigerator installed in a white kitchen",
      h1a="Your new appliance,", h1b="in and working.", price=150, install=True,
      blurb="New unit going in — leveled, connected and tested, with the old haul-away arranged.",
      symptoms=[("Refrigerators & freezers","Set, leveled and cooling-checked — ice makers connected and tested."),
                ("Washers & dryers","Hooked up, balanced and run-tested — venting checked on dryers."),
                ("Ovens, ranges & cooktops","Connected and burner-tested — fit and level confirmed."),
                ("Dishwashers & disposals","Plumbed, powered and leak-tested before we leave.")]),
]
SVC = {s["short"]: s for s in SERVICES}

# ---------------------------------------------------------------- shared ui
def icon(name, size=22):
    p = {
      "gauge": '<circle cx="12" cy="13" r="8"/><path d="M12 13l3.5-3.5"/><path d="M5 19h14"/>',
      "flag": '<path d="M5 21V4"/><path d="M5 4h13l-2.5 4L18 12H5"/>',
      "bolt": '<path d="M13 2L4.5 13.5H11L9.5 22 19 10h-6.5L13 2z"/>',
      "wrench": '<path d="M14.5 6.5a4.2 4.2 0 0 1 5.6-4L17.5 5l2.5 2.5 2.6-2.5a4.2 4.2 0 0 1-5.5 5.6L8 19.7a2.1 2.1 0 0 1-3-3l9.5-10.2z"/>',
      "pin": '<path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/>',
      "cal": '<rect x="3.5" y="5" width="17" height="16" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
      "phone": '<path d="M5 4h4l2 5-2.5 1.5a12 12 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
      "check": '<path d="M20 6L9 17l-5-5"/>',
      "stoplight": '<rect x="8" y="2.5" width="8" height="19" rx="3.5"/><circle cx="12" cy="7" r="1.4" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="12" cy="17" r="1.4" fill="currentColor" stroke="none"/>',
      "shield": '<path d="M12 3l7 2.4V11c0 4.6-2.9 7.9-7 9.7C7.9 18.9 5 15.6 5 11V5.4z"/><path d="M12.6 7.2L9.4 12h2.2l-.9 3.6L14 11h-2.1z" fill="currentColor" stroke="none"/>',
      "road": '<path d="M4.5 21L9.5 3M19.5 21L14.5 3"/><path d="M12 18.2v-2.4M12 13.4V11M12 8.2V6" stroke-width="1.8"/>',
      "sign": '<path d="M12 21.5V11"/><path d="M4 3.5h12.5L20 7l-3.5 3.5H4z"/><path d="M7.5 7h6" stroke-width="1.6"/>',
      "stripes": '<path d="M3 7h11M3 12h14M3 17h11"/><path d="M17.5 7.5L21 12l-3.5 4.5" stroke-width="1.8"/>',
      "laurels": '<path d="M7.2 20.2C4.8 16.9 4.2 12.6 5.6 8.6M16.8 20.2c2.4-3.3 3-7.6 1.6-11.6"/><path d="M5.8 15.5l-2.6-.9M6 11.5L3.6 10M7 7.8L5 5.6M18.2 15.5l2.6-.9M18 11.5l2.4-1.5M17 7.8l2-2.2" stroke-width="1.6"/><path d="M8.5 20.5h7" stroke-width="1.6"/>',
      "tools": '<path d="M13.8 5.2a3.6 3.6 0 0 1 4.9-3.4L16.4 4l2.1 2.1 2.3-2.2a3.6 3.6 0 0 1-4.8 4.8L8.6 16a1.8 1.8 0 0 1-2.5-2.5z"/>',
      "checker-flag": '<path d="M5 21.5v-19"/><path d="M5 3h13v9H5z"/><path d="M9.3 3v9M13.7 3v9M5 7.5h13" stroke-width="1.1"/><path d="M5 3h4.3v4.5H5zM13.7 7.5H18V12h-4.3z" fill="currentColor" stroke="none"/>',
    }[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

LOGO_MARK = ('<span class="logo-mark"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" '
             'stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M12 3.2l6.2 2.1v5c0 4.1-2.6 7-6.2 8.6C8.4 17.3 5.8 14.4 5.8 10.3v-5z"/><path d="M12.5 7.4L9.7 11.9h2l-.8 3.3 3-4.4h-2z" fill="#fff" stroke="none"/></svg></span>')

def head(title, desc, path, ld=None):
    ld_html = ""
    if ld:
        ld_html = '\n<script type="application/ld+json">' + json.dumps(ld) + "</script>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Top Speed Appliance">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}{IMG_HERO}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800&family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">{ld_html}
</head>
<body>
"""

def nav():
    return f"""
<header class="nav">
  <div class="wrap nav-in">
    <a class="logo" href="/" aria-label="Top Speed Appliance — home">{LOGO_MARK}
      <span><span class="logo-name">TOP SPEED</span><div class="logo-sub">APPLIANCE</div></span></a>
    <nav class="nav-links" aria-label="Main">
      <a href="/services">Services</a>
      <a href="/cities">Cities</a>
      <a href="/pricing">Pricing</a>
      <a href="{FLAG}/track">Track My Tech</a>
      <a href="{FLAG}/top-speed-os">Top Speed OS</a>
    </nav>
    <div class="nav-right">
      <a class="nav-phone" href="{TEL}">{PHONE}</a>
      <a class="btn btn-primary" href="/book">Book a repair</a>
      <button class="burger" data-burger aria-label="Menu"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
  <div class="mobile-menu">
    <a href="/services">Services</a>
    <a href="/cities">Cities</a>
    <a href="/pricing">Pricing</a>
    <a href="{FLAG}/track">Track My Tech</a>
    <a href="{FLAG}/top-speed-os">Top Speed OS</a>
    <a href="{TEL}">Call {PHONE}</a>
    <a href="/book">Book a repair</a>
  </div>
</header>
<div class="checker" aria-hidden="true"></div>
"""

def footer():
    svc_links = []
    groups = [SERVICES[0:3], SERVICES[3:6], SERVICES[6:9]]
    for g in groups:
        svc_links.append(" · ".join(f'<a href="/services/{s["slug"]}" style="display:inline;padding:0">{s["short"]}</a>' for s in g))
    svc_html = "<br>".join(svc_links)
    return f"""
<div class="checker" aria-hidden="true"></div>
<footer class="footer">
  <div class="wrap footer-in">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/">{LOGO_MARK}
          <span><span class="logo-name">TOP SPEED</span><div class="logo-sub">THE FASTER, THE BETTER.</div></span></a>
        <a class="footer-phone" href="{TEL}">{PHONE}</a>
        <div class="crest-row"><img class="crest" src="/assets/brand/shield-badge.svg" alt="" aria-hidden="true" width="40" height="40"><span>The Top Speed standard — precision motorsport, applied to appliance repair.</span></div>
        <p>Mon–Fri, 8am–7pm · Service-area business — repairs at your home or business<br>
        across 65 cities in Broward, Palm Beach &amp; Miami-Dade.</p>
      </div>
      <div class="footer-cols">
        <div><h4>Services</h4>{svc_html}</div>
        <div><h4>Platform</h4>
          <a href="/book">Book a repair</a>
          <a href="{FLAG}/track">Track My Tech</a>
          <a href="{FLAG}/top-speed-os">Top Speed OS</a>
        </div>
        <div><h4>Company</h4>
          <a href="{FLAG}/top-speed-os">About the network</a>
          <a href="https://topspeedappliances.com">Sales OS — shop</a>
          <a href="{FLAG}/advertise">Advertise with us</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Top Speed Appliance LLC — <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · 131 local pages, one platform.</span>
      <span><a href="/book">Book online</a> · <a href="#" data-ask-speedy>Ask Speedy</a> · <a href="{TEL}">Call {PHONE}</a></span>
    </div>
  </div>
</footer>
<script src="{FLAG}/speedy-widget.js" defer></script>
<script src="/assets/js/site.js" defer></script>
<script src="/ads-stream.js" defer></script>
</body>
</html>
"""

ORG_LD = {
  "@context": "https://schema.org", "@type": "Organization",
  "name": "Top Speed Appliance LLC", "alternateName": "Top Speed Appliance",
  "url": BASE + "/", "slogan": "The Faster, The Better.",
  "telephone": "+1-844-460-7038", "openingHours": "Mo-Fr 08:00-19:00",
  "areaServed": ["Broward County, FL", "Palm Beach County, FL", "Miami-Dade County, FL"],
  "sameAs": [
    "https://www.facebook.com/profile.php?id=61596590488055",
    "https://www.instagram.com/rome64220/",
    "https://www.instagram.com/topspeedappliance/",
    "https://www.instagram.com/rom64220/"]
}

def svc_card(s, city=None):
    q = f"?service={s['short']}" + (f"&city={city}" if city else "")
    cta = "Book installation" if s.get("install") else "Book this service"
    tag = "Photo — a Top Speed install" if s.get("install") else f"Photo — {s['short']} service"
    img = s["img"]
    return f"""
      <article class="card svc-card">
        <div class="svc-photo"><img src="{img}" alt="{s['alt']}" loading="lazy"><span class="photo-tag">{tag}</span></div>
        <div class="svc-body">
          <h3 class="h3">{s['name']}</h3>
          <p>{s['blurb']}</p>
          <div class="svc-foot"><span class="price-line">${s['price']} flat labor</span>
          <a class="book-link" href="/book{q}">{cta} →</a></div>
        </div>
      </article>"""

def rate_cards():
    return """
    <div class="rate-grid">
      <div class="card rate-card"><div class="rate-price">$99</div><div class="rate-name">Diagnostic</div>
        <p>Residential. Collected at booking to reserve your window — credited in full toward your approved repair. Still due if you decline the repair.</p>
        <div class="rate-tag">Credited toward repair</div></div>
      <div class="card rate-card"><div class="rate-price">$210</div><div class="rate-name">Repair labor — flat</div>
        <p>One flat labor rate for the repair, quoted in writing on site before any work starts. Parts are always in the written quote first.</p>
        <div class="rate-tag">Flat — no hourly meter</div></div>
      <div class="card rate-card"><div class="rate-price">$150</div><div class="rate-name">Installation labor — flat</div>
        <p>Leveled, connected and tested. Parts and materials are always in a written quote first.</p>
        <div class="rate-tag">Flat — every install</div></div>
    </div>"""

def steps_band(steps, eyebrow="How it works", title="Red light to green light."):
    cols = "".join(f"""
      <div class="step"><div class="step-num">0{i+1}</div><h3>{t}</h3><p>{d}</p></div>""" for i, (t, d) in enumerate(steps))
    cls = "steps steps-4" if len(steps) == 4 else "steps"
    return f"""
<section class="band"><div class="wrap section">
  <div class="band-head"><div><p class="eyebrow">{eyebrow}</p><h2 class="h2">{title}</h2></div>
  <img class="band-light" src="/assets/brand/stoplight.svg" alt="" aria-hidden="true" width="34" height="82"></div>
  <div class="{cls}">{cols}</div>
</div></section>"""

FLEET = [("fleet-f1", "Formula 1"), ("fleet-stallion", "Race Stallion"), ("fleet-cheetah", "Cheetah"),
         ("fleet-jet", "Fighter Jet"), ("fleet-speedboat", "Speedboat"), ("fleet-spaceship", "Spaceship")]

def fleet_band():
    tiles = "".join(f'''<figure class="fleet-tile"><img src="/assets/brand/{f}.svg" alt="" aria-hidden="true" width="96" height="64"><figcaption>{n}</figcaption></figure>''' for f, n in FLEET)
    return f"""
<section class="fleet-band on-dark"><div class="wrap section">
  <p class="eyebrow">The Top Speed fleet</p>
  <h2 class="h2">Six machines. One standard: fast.</h2>
  <p class="lede" style="margin-top:14px;max-width:62ch">The racers, runners and rockets that set our pace — the standard behind every visit: prepared, precise, and built for speed.</p>
  <div class="fleet-grid">{tiles}</div>
</div></section>"""

HOME_STEPS = [
  ("Book in about a minute", "The classic form or Speedy — same queue, same confirmation. Tell us the appliance and the symptom."),
  ("A Service Setter confirms", "A real person confirms your window by phone. No bots dispatching your visit — people do."),
  ("Track your tech live", "From request to repair, follow every stage in Track My Tech — and see your tech on the way."),
]

# ── Ads Library stream (2026-11-24) ─────────────────────────────
# This site's service slugs → the Ads Library's service tags.
AD_TAGS = {
    "refrigerator-repair": "refrigerator",
    "washer-repair": "washer",
    "dryer-repair": "dryer",
    "oven-range-repair": "oven-range",
    "dishwasher-repair": "dishwasher",
    "freezer-ice-maker-repair": "freezer-ice-maker",
    "microwave-repair": "microwave",
    "garbage-disposal-repair": "garbage-disposal",
    "appliance-installation": "installation",
}

def ad_slot(slot, service=None, city=None):
    """One streaming slot for the managed Flywheel Ads Library.
    The embed (/ads-stream.js, loaded in the footer) fills it with
    the next house creative — matched, rotated and counted by the
    Service OS. An empty library renders nothing at all."""
    attrs = 'data-slot="' + slot + '" data-platform="topspeedrepairs"'
    if service:
        attrs += ' data-service="' + service + '"'
    if city:
        attrs += ' data-city="' + city + '"'
    return ('\n<section class="section" style="padding-top:0;padding-bottom:8px">'
            '<div class="wrap" style="max-width:880px">\n'
            '  <div data-ts-ad ' + attrs + '></div>\n'
            '</div></section>\n')

def speedy_section():
    return f"""
<section class="section"><div class="wrap speedy-grid">
  <div>
    <p class="eyebrow">Meet Speedy — not sure what's wrong?</p>
    <h2 class="h2">Snap it. Send it. Diagnosed.</h2>
    <p class="lede" style="margin-top:16px">Speedy is Top Speed's AI service assistant. Send a photo of the appliance
    and what it's doing — Speedy reads it, gives you a head start on the likely issue, and books the visit when
    you're ready. Speedy summarizes your request and asks for your confirmation before anything is sent to the
    Service Setters office. A technician always confirms in person.</p>
    <div class="hero-cta"><button class="btn btn-primary" data-ask-speedy>Ask Speedy</button>
    <a class="btn btn-navy" href="{TEL}" style="box-shadow:none">Call {PHONE}</a></div>
  </div>
  <div class="chat-panel" aria-hidden="true">
    <div class="chat-head"><span class="chat-avatar">S</span>
      <div><b>Speedy — AI Service Assistant</b><span>Online — answers in seconds</span></div></div>
    <div class="msg msg-user">My fridge is running warm and the ice maker quit. What should I check first?</div>
    <div class="msg msg-bot">Send me a photo of the back panel and the temperature setting — I'll read it now and
    line up a visit if it needs one. Your $99 diagnostic is credited toward the repair.</div>
    <p class="chat-note">A look at the conversation — tap “Ask Speedy” to start the real one.</p>
  </div>
</div></section>"""

# ---------------------------------------------------------------- homepage
def home():
    cards = "\n".join(svc_card(s) for s in SERVICES)
    featured = ["Fort Lauderdale","Hollywood","Coral Springs","Pompano Beach","Plantation","Davie",
                "Boca Raton","Deerfield Beach","Sunrise","Weston","Coconut Creek","Miami Gardens"]
    by_name = {c["name"]: c for c in CITIES}
    chips = "\n".join(f'<a class="chip chip-light" href="/cities/{by_name[n]["slug"]}">{n}</a>' for n in featured)
    ld = [ORG_LD, {"@context":"https://schema.org","@type":"WebSite","name":"Top Speed Appliance",
                   "url": BASE + "/"}]
    body = f"""{nav()}
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Appliance repair — Tri-County, South Florida</p>
      <h1 class="h1">Appliance<br>repair.<br><span class="red">At full speed.</span></h1>
      <p class="lede" style="margin-top:22px">Professional repair and installation, run on one platform — book in
      about a minute, a Service Setter confirms your visit, and you track your tech live to your door.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="/book">Book a repair</a>
        <a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a>
      </div>
      <div class="chips">
        <span class="chip chip-dark">$99 diagnostic — credited toward your repair</span>
        <span class="chip chip-dark">Mon–Fri · 8am–7pm</span>
        <span class="chip chip-dark">65 cities served</span>
      </div>
    </div>
    <div class="hero-photo"><img src="{IMG_HERO}" alt="Top Speed technician repairing a refrigerator in a customer's kitchen" fetchpriority="high">
      <span class="photo-tag">Photo — technician at work</span></div>
  </div>
</div></section>
<div class="wrap"><div class="stats" role="list" aria-label="Top Speed at a glance">
  <div class="stat"><b>65</b><span>Cities served</span></div>
  <div class="stat"><b>9</b><span>Appliance services</span></div>
  <div class="stat"><b>131</b><span>Local pages</span></div>
  <div class="stat"><b>90-day</b><span>Parts &amp; labor warranty</span></div>
</div></div>

<section class="section"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">What we fix</p><h2 class="h2">Nine services. One fast call.</h2></div>
  <a class="more" href="/services">See all services →</a></div>
  <div class="grid-3">{cards}
  </div>
</div></section>
{steps_band(HOME_STEPS)}
{speedy_section()}
{fleet_band()}
{ad_slot("home")}
<section class="section" id="pricing" style="padding-top:24px"><div class="wrap">
  <p class="eyebrow">Flat, published pricing</p>
  <h2 class="h2" style="margin-bottom:40px">The rate card. No ranges, no guessing.</h2>
  {rate_cards()}
</div></section>
<section class="section" style="padding-top:24px"><div class="wrap">
  <p class="eyebrow">Coverage</p>
  <h2 class="h2" style="margin-bottom:34px">Find service in your city.</h2>
  <div class="chips">{chips}</div>
  <p style="margin-top:22px"><a class="book-link" href="/cities" style="color:var(--red-600)">All 65 cities →</a></p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap invite">
  <div>
    <p class="eyebrow">After the visit</p>
    <h2 class="h2"><span class="laurel-ic">{icon("laurels", 30)}</span>Fixed? Tell the next neighbor.</h2>
    <p class="lede" style="margin-top:14px">Word of mouth is our fastest lane. If your tech earned it, leave a review
    on our Google profile — and send a friend our way with Refer &amp; Earn: they get $25 off their first repair,
    you earn a $25 credit when their job is done.</p>
  </div>
  <div class="invite-actions">
    <a class="btn btn-primary" href="/book">Book a repair</a>
    <a class="btn btn-navy" href="https://appliancereferral.com">Refer &amp; Earn →</a>
  </div>
</div></section>
{footer()}"""
    return head("Appliance Repair in Broward, Palm Beach & Miami-Dade | Top Speed Appliance",
                "Top Speed Appliance — flat-rate appliance repair & installation across 65 cities in Broward, Palm Beach & Miami-Dade. $99 diagnostic credited, $210 flat repair labor. Book in about a minute.",
                "/", ld) + body

# ---------------------------------------------------------------- /book
def book():
    appl = "".join(f'<button type="button" class="pill-btn" data-appliance="{s["short"]}">{s["short"]}</button>' for s in SERVICES)
    steps = "".join(f'<div class="p-step"><span class="p-dot">{i+1}</span><span>{n}</span></div>'
                    for i, n in enumerate(["Contact","Location","Appliance","Schedule","Review"]))
    body = f"""{nav()}
<section class="page-hero"><div class="wrap">
  <div style="display:flex;justify-content:space-between;gap:32px;align-items:flex-start;flex-wrap:wrap">
    <div>
      <p class="eyebrow">Book a repair</p>
      <h1 class="h1" style="font-size:clamp(36px,4.6vw,54px)">Book your visit.</h1>
      <p class="lede" style="margin-top:14px">The classic form — about a minute, no account needed. A Service Setter confirms every request by phone.</p>
    </div>
    <div class="progress" aria-hidden="true">{steps}</div>
  </div>
</div></section>
<div class="wrap"><div class="book-grid">
  <form class="form-card" id="book-form" novalidate>
    <div id="form-card-inner">
    <div class="f-head"><h2>Your details</h2><span class="step-note">The classic form leads — Speedy is below, if you prefer.</span></div>
    <div class="f-row">
      <div><label class="f-label" for="f-first">First name</label><input class="input" id="f-first" autocomplete="given-name" placeholder="Jordan"></div>
      <div><label class="f-label" for="f-last">Last name</label><input class="input" id="f-last" autocomplete="family-name" placeholder="Rivera"></div>
    </div>
    <div class="f-row" style="margin-top:18px">
      <div><label class="f-label" for="f-phone">Mobile phone</label><input class="input" id="f-phone" type="tel" autocomplete="tel" placeholder="(555) 555-0142"></div>
      <div><label class="f-label" for="f-email">Email <span style="text-transform:none;letter-spacing:0">(optional)</span></label><input class="input" id="f-email" type="email" autocomplete="email" placeholder="jordan@email.com"></div>
    </div>

    <div class="f-sec"><div class="zip-panel">
      <label class="f-label" for="f-zip">Where's the appliance?</label>
      <div class="zip-row">
        <input class="input" id="f-zip" inputmode="numeric" autocomplete="postal-code" placeholder="ZIP — e.g. 33301" maxlength="5">
        <span class="zip-msg" id="zip-msg" role="status"></span>
        <button type="button" class="linklike" id="use-location">Use my location</button>
      </div>
      <div id="city-wrap" style="display:none;margin-top:16px">
        <label class="f-label" for="f-city">Your city</label>
        <select class="input" id="f-city"><option value="">Choose your city…</option></select>
      </div>
      <div style="margin-top:16px">
        <label class="f-label" for="f-address">Street address</label>
        <input class="input" id="f-address" autocomplete="street-address" placeholder="Street, unit, city">
      </div>
    </div></div>

    <div class="f-sec">
      <span class="f-label">Appliance</span>
      <div class="pill-group">{appl}</div>
    </div>

    <div class="f-sec">
      <label class="f-label" for="f-issue">What's it doing?</label>
      <textarea class="input" id="f-issue" placeholder="Running warm — food spoiling, ice maker quit"></textarea>
    </div>

    <div class="f-sec">
      <div class="f-row">
        <div><label class="f-label" for="f-date">Preferred day</label><input class="input" id="f-date" type="date"></div>
        <div><span class="f-label">Arrival window</span><div class="pill-group" id="win-group"></div></div>
      </div>
      <p class="step-note" id="avail-note" style="margin-top:10px">Pick a day and window — your Service Setter confirms the exact appointment by text.</p>
    </div>

    <input class="hp" id="f-website" name="companyWebsite" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="form-err" id="form-err" role="alert"></div>
    <div class="form-foot">
      <button class="btn btn-primary" id="submit-btn" type="submit">Send booking request</button>
      <span class="note">$99 diagnostic collected at booking — credited toward your repair.</span>
    </div>
    </div>
  </form>

  <div class="rail">
    <aside class="visit-card" aria-label="Your visit summary">
      <p class="eyebrow">Your visit</p>
      <div class="visit-title" id="visit-title">Your repair visit</div>
      <div class="visit-sub" id="visit-sub">Your city · your ZIP</div>
      <div class="visit-rows">
        <div><span>Diagnostic</span><b>$99 — credited</b></div>
        <div><span>Repair labor</span><b>$210 flat</b></div>
        <div><span>Parts</span><b>Written quote first</b></div>
        <div><span>Window</span><b id="visit-window">Confirmed by phone</b></div>
      </div>
      <p class="visit-fine">90-day parts &amp; labor warranty on the repair.</p>
    </aside>
    <aside class="speedy-card">
      <span class="chat-avatar">S</span>
      <h3 class="h3" style="margin-top:14px">Prefer the high-tech way?</h3>
      <p>Tell Speedy what's wrong — type it, say it, or snap a photo. Speedy books it in the chat. Same queue, same confirmation.</p>
      <div class="msg msg-user" style="margin:0 0 18px;max-width:100%">My washer won't drain — can you come Thursday?</div>
      <button class="btn btn-navy" data-ask-speedy>Ask Speedy</button>
      <p style="margin-top:16px">Or call <a href="{TEL}" style="font-weight:600;color:var(--ink-900)">{PHONE}</a> — Mon–Fri, 8am–7pm.</p>
    </aside>
  </div>
</div></div>
<div style="height:96px"></div>
{footer()}
<script src="/assets/js/book.js" defer></script>"""
    # book.js expects the success swap target to be the form card itself
    body = body.replace('<form class="form-card" id="book-form"', '<form class="form-card" id="book-form"')
    return head("Book a Repair — Book Your Visit | Top Speed Appliance",
                "Book appliance repair online in about a minute. $99 diagnostic credited toward your repair, $210 flat repair labor, confirmed by a real Service Setter. Mon–Fri 8am–7pm.",
                "/book") + body

# ---------------------------------------------------------------- services
def service_page(s):
    sym_title = "What we install" if s.get("install") else "Sound familiar?"
    sym = "\n".join(f'<div class="card sym-card"><h3>{t}</h3><p>{d}</p></div>' for t, d in s["symptoms"])
    if s.get("install"):
        steps = [("Book the install","Tell us what's arriving and where it goes — about a minute, online or by phone."),
                 ("Flat $150 labor","One flat installation labor rate. Any parts or materials are in a written quote first."),
                 ("Tested before we leave","Leveled, connected and run-tested in front of you — the old haul-away arranged.")]
        chips = '<span class="chip chip-dark">$150 flat installation labor</span><span class="chip chip-dark">Leveled · connected · tested</span>'
    else:
        steps = [("Diagnose","The tech tests the unit and names the cause — no guessing, no parts-swapping."),
                 ("Written quote","Exact price in writing: $210 flat labor plus the parts your appliance actually needs."),
                 ("Repair on approval","Work starts only after your OK — and the $99 diagnostic comes off the total.")]
        chips = '<span class="chip chip-dark">$99 diagnostic — credited</span><span class="chip chip-dark">$210 flat repair labor · parts in a written quote</span>'
    others = "".join(f'<a class="chip chip-light" href="/services/{o["slug"]}">{o["short"]}</a>' for o in SERVICES if o is not s)
    ld = {"@context":"https://schema.org","@type":"Service","name": s["name"],
          "provider": {"@type":"Organization","name":"Top Speed Appliance LLC","telephone":"+1-844-460-7038","url": BASE + "/"},
          "areaServed": ["Broward County, FL","Palm Beach County, FL","Miami-Dade County, FL"],
          "serviceType": s["name"], "url": f"{BASE}/services/{s['slug']}"}
    body = f"""{nav()}
<section class="hero"><div class="wrap"><div class="hero-grid" style="min-height:480px">
  <div class="hero-copy" style="padding:64px 48px 72px 0">
    <p class="eyebrow">{s['name']}</p>
    <h1 class="h1" style="font-size:clamp(36px,4.6vw,56px)">{s['h1a']}<br><span class="red">{s['h1b']}</span></h1>
    <p class="lede" style="margin-top:20px">{s['blurb']}</p>
    <div class="hero-cta"><a class="btn btn-primary" href="/book?service={s['short']}">Book a repair</a>
    <a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a></div>
    <div class="chips">{chips}</div>
  </div>
  <div class="hero-photo"><img src="{s['img']}" alt="{s['alt']}">
    <span class="photo-tag">{"Photo — a Top Speed install" if s.get("install") else "Photo — " + s['short'] + " service"}</span></div>
</div></div></section>

<section class="section"><div class="wrap">
  <p class="eyebrow">{'Installations' if s.get('install') else 'Common symptoms'}</p>
  <h2 class="h2" style="margin-bottom:40px">{sym_title}</h2>
  <div class="grid-2">{sym}</div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="grid-2" style="grid-template-columns:1.35fr .85fr;align-items:stretch">
    <div class="card" style="padding:38px 34px">
      <p class="eyebrow">How the visit works</p>
      {''.join(f'<div style="display:flex;gap:20px;padding:16px 0;border-bottom:1px solid var(--line)"><span class="step-num" style="font-size:30px">{i+1}</span><div><h3 class="h3" style="font-size:21px">{t}</h3><p style="color:var(--ink-600);font-size:15px;margin-top:4px">{d}</p></div></div>' for i,(t,d) in enumerate(steps))}
    </div>
    <div class="rate-panel">
      <p class="eyebrow">The rate card</p>
      <div class="rp-row"><span class="rp-price">$99</span><p>diagnostic — credited toward your repair</p></div>
      <div class="rp-row"><span class="rp-price">$210</span><p>flat repair labor</p></div>
      <div class="rp-row"><span class="rp-price">$150</span><p>flat installation labor</p></div>
      <a class="btn btn-primary" href="/book?service={s['short']}" style="margin-top:24px;width:100%;justify-content:center">Book a repair</a>
    </div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <p class="eyebrow">Who we serve</p>
  <h2 class="h2" style="margin-bottom:40px">Homes first. Businesses covered.</h2>
  <div class="grid-2">
    <div class="card lane"><p class="eyebrow">Residential</p><h3 class="h3">For homeowners</h3>
      <p>Same flat rate card, the credited diagnostic, and live tracking on every visit.</p>
      <a class="book-link" href="/book?service={s['short']}">Book a home visit →</a></div>
    <div class="card lane"><p class="eyebrow">Commercial</p><h3 class="h3">For businesses &amp; property managers</h3>
      <p>Restaurants, laundromats, landlords — priority windows, multi-unit scheduling, one invoice. Priced by custom quote.</p>
      <a class="book-link" href="https://www.appliancepro.net/">Talk to Appliance Pro →</a></div>
  </div>
  <p class="eyebrow" style="color:var(--ink-400);margin-top:56px">Also fixed by Top Speed</p>
  <div class="chips">{others}</div>
</div></section>
{ad_slot("service", service=AD_TAGS[s['slug']])}
{footer()}"""
    return head(f"{s['name']} — ${s['price']} Flat Labor | Top Speed Appliance",
                f"{s['name']} across 65 cities in Broward, Palm Beach & Miami-Dade. $99 diagnostic credited toward your repair, ${s['price']} flat labor, written quote before any work.",
                f"/services/{s['slug']}", ld) + body

def services_hub():
    cards = "\n".join(svc_card(s) for s in SERVICES)
    body = f"""{nav()}
<section class="page-hero" style="padding-bottom:72px"><div class="wrap">
  <p class="eyebrow">{icon("tools", 16)}Services</p>
  <h1 class="h1" style="font-size:clamp(36px,4.6vw,54px)">Nine services.<br><span class="red">One fast call.</span></h1>
  <p class="lede" style="margin-top:14px">Every service runs on the same flat rate card — $99 diagnostic credited toward your repair, $210 flat repair labor, $150 flat installation labor. Parts always in a written quote first.</p>
</div></section>
<section class="section"><div class="wrap"><div class="grid-3">{cards}</div></div></section>
{steps_band(HOME_STEPS)}
{footer()}"""
    return head("Appliance Services — 9 Flat-Rate Services | Top Speed Appliance",
                "Refrigerator, washer, dryer, oven, dishwasher, freezer & ice maker, microwave, garbage disposal repair and appliance installation — one flat rate card across 65 cities.",
                "/services") + body

# ---------------------------------------------------------------- cities
def nearby(city):
    same = [c for c in CITIES if c["county"] == city["county"] and c["name"] != city["name"]]
    i = [c["name"] for c in CITIES].index(city["name"])
    ordered = sorted(same, key=lambda c: abs([x["name"] for x in CITIES].index(c["name"]) - i))
    return ordered[:8]

def city_page(c):
    cards = "\n".join(svc_card(s, city=c["name"]) for s in SERVICES)
    near = "".join(f'<a class="chip chip-light" href="/cities/{n["slug"]}">{n["name"]}</a>' for n in nearby(c))
    steps4 = [("Book in about a minute","The classic form or Speedy — tell us the appliance and the symptom."),
              ("A Service Setter confirms","A real person confirms your window by phone — no bots dispatching."),
              ("Track your tech live","Follow every stage in Track My Tech and see your tech on the way."),
              ("Repaired on approval","Written quote first — work starts only after your OK.")]
    ld = {"@context":"https://schema.org","@type":"Service","name": f"Appliance Repair in {c['name']}",
          "provider": {"@type":"Organization","name":"Top Speed Appliance LLC","telephone":"+1-844-460-7038","url": BASE + "/"},
          "areaServed": {"@type":"City","name": f"{c['name']}, FL"},
          "serviceType": "Appliance repair and installation", "url": f"{BASE}/cities/{c['slug']}"}
    body = f"""{nav()}
<section class="city-hero">
  <img class="bg" src="{IMG_VAN}" alt="Top Speed service van on a palm-lined street in South Florida">
  <div class="wrap city-hero-in">
    <p class="eyebrow">{icon("road", 16)}Appliance repair — {c['county']} County</p>
    <h1 class="display">{c['name']}</h1>
    <p class="lede" style="margin-top:16px;max-width:56ch">Appliance repair and installation at your home or business in
    {c['name']} — book in about a minute, a Service Setter confirms your window by phone, and you track your tech live to your door.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="/book?city={c['name']}">Book a repair in {c['name']}</a>
      <a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a>
    </div>
    <div class="chips">
      <span class="chip chip-dark">$99 diagnostic — credited toward your repair</span>
      <span class="chip chip-dark">Mon–Fri · 8am–7pm</span>
      <span class="chip chip-dark">$210 flat repair labor</span>
    </div>
  </div>
</section>
<section class="section"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Services in {c['name']}</p><h2 class="h2">Nine services. One fast call.</h2></div>
  <a class="more" href="/services">See all services →</a></div>
  <div class="grid-3">{cards}</div>
</div></section>
{steps_band(steps4, eyebrow=f"A local visit in {c['name']}", title="From red light to green light.")}
<section class="section"><div class="wrap">
  <p class="eyebrow">Flat, published pricing</p>
  <h2 class="h2" style="margin-bottom:40px">The same rate card in {c['name']}.</h2>
  {rate_cards()}
  <p class="eyebrow" style="color:var(--ink-400);margin-top:64px">Nearby cities we serve</p>
  <div class="chips">{near}</div>
  <p style="margin-top:22px"><a class="book-link" href="/cities" style="color:var(--red-600)">All 65 cities →</a></p>
</div></section>
{ad_slot("city", city=c['slug'])}
{footer()}"""
    return head(f"Appliance Repair in {c['name']}, FL | Top Speed Appliance",
                f"Flat-rate appliance repair & installation in {c['name']} ({c['county']} County). $99 diagnostic credited, $210 flat repair labor. Book online in about a minute.",
                f"/cities/{c['slug']}", ld) + body

def cities_hub():
    groups = ""
    for county in ["Broward", "Palm Beach", "Miami-Dade"]:
        cs = [c for c in CITIES if c["county"] == county]
        chips = "".join(f'<a class="chip chip-light" href="/cities/{c["slug"]}">{c["name"]}</a>' for c in cs)
        groups += f'<p class="eyebrow" style="margin-top:44px">{county} County — {len(cs)} cities</p><div class="chips">{chips}</div>'
    body = f"""{nav()}
<section class="page-hero" style="padding-bottom:72px"><div class="wrap">
  <p class="eyebrow">{icon("road", 16)}Coverage</p>
  <h1 class="h1" style="font-size:clamp(36px,4.6vw,54px)">65 cities.<br><span class="red">One platform.</span></h1>
  <p class="lede" style="margin-top:14px">Top Speed is a service-area business — repairs happen at your home or business.
  Enter your ZIP when you book and we match your city automatically; every city below is served Mon–Fri, 8am–7pm.</p>
</div></section>
<section class="section" style="padding-top:16px"><div class="wrap">{groups}
  <div style="margin-top:56px;display:flex;gap:14px;align-items:center;color:var(--red-600)">{icon("sign", 26)}<a class="btn btn-primary" href="/book">Book a repair</a></div>
</div></section>
{footer()}"""
    return head("Service Areas — 65 Cities in Broward, Palm Beach & Miami-Dade | Top Speed Appliance",
                "Top Speed Appliance serves 65 cities across Broward (31), Palm Beach (16) and Miami-Dade (18) counties — appliance repair & installation at your door.",
                "/cities") + body

# ---------------------------------------------------------------- simple pages
def simple_hero(eyebrow, title_html, lede):
    return f"""{nav()}
<section class="page-hero" style="padding-bottom:72px"><div class="wrap">
  <p class="eyebrow">{eyebrow}</p>
  <h1 class="h1" style="font-size:clamp(34px,4.4vw,50px)">{title_html}</h1>
  <p class="lede" style="margin-top:14px">{lede}</p>
</div></section>"""

def pricing():
    body = f"""{simple_hero("Pricing", 'The rate card.<br><span class="red">No ranges, no guessing.</span>',
      "Flat, published pricing on every visit — the same numbers on every page, every quote, every invoice.")}
<section class="section"><div class="wrap">
  {rate_cards()}
  <div class="grid-2" style="margin-top:56px">
    <div class="card lane"><p class="eyebrow">How it works</p><h3 class="h3">Diagnose, quote, then decide</h3>
      <p>The $99 residential diagnostic is collected at booking to reserve your window and credited in full toward an
      approved repair — it is still due if you decline the repair. Your tech quotes the job in writing on site:
      flat labor plus the exact parts your appliance needs. No work is ever done without your approved written quote,
      and there is no hourly meter.</p></div>
    <div class="card lane"><p class="eyebrow">Commercial</p><h3 class="h3">Businesses are quoted, not rate-carded</h3>
      <p>Restaurants, laundromats, landlords and property managers run through Appliance Pro — priority windows,
      multi-unit scheduling, one invoice, priced by custom quote.</p>
      <a class="book-link" href="https://www.appliancepro.net/">Talk to Appliance Pro →</a></div>
  </div>
  <div style="margin-top:48px;display:flex;gap:14px;flex-wrap:wrap">
    <a class="btn btn-primary" href="/book">Book a repair</a>
    <a class="btn btn-navy" href="{TEL}">Call {PHONE}</a>
  </div>
</div></section>
{footer()}"""
    return head("Pricing — $99 Diagnostic · $210 Flat Repair Labor | Top Speed Appliance",
                "Flat, published appliance pricing: $99 residential diagnostic credited toward your repair, $210 flat repair labor, $150 flat installation labor. Parts in a written quote first.",
                "/pricing") + body

def privacy():
    body = f"""{simple_hero("Privacy", "Your details stay<br><span class='red'>on the job.</span>",
      "How Top Speed Appliance LLC handles the information you share when you book or ask a question.")}
<section class="section"><div class="wrap"><div class="prose">
  <h2>Who we are</h2>
  <p>Top Speed Appliance LLC is an appliance repair and installation company serving 65 cities across Broward,
  Palm Beach and Miami-Dade counties, Florida. We are a service-area business — repairs happen at your home or
  business. This site is topspeedrepairs.com; bookings run on the Top Speed Service OS platform.</p>
  <h2>What we collect</h2>
  <p>When you book or contact us we collect the details the job needs: your name, mobile phone, email (optional),
  the service address, your city and ZIP, the appliance and what it is doing, and your preferred day and window.
  If you chat with Speedy, the conversation is kept with your request so a Service Setter can confirm your visit.</p>
  <h2>How we use it</h2>
  <ul>
    <li>To schedule, confirm and run your visit — including confirmation calls and texts, and the live
    Track My Tech link when your technician is on the way.</li>
    <li>To quote, invoice and support the work, and to run the Refer &amp; Earn program if you take part.</li>
    <li>To keep the platform secure and understand which pages and cities need attention, in aggregate.</li>
  </ul>
  <h2>Sharing</h2>
  <p>Your details go to the Service Setters dispatch team and the technician assigned to your job, and to the
  messaging and payment providers that carry our confirmations and invoices. We do not sell your personal
  information. We share information only when the law requires it.</p>
  <h2>Your choices</h2>
  <p>Reply STOP to any text to stop messages, and call us at {PHONE} to update or delete your details.
  Deleting booking details can limit our ability to service warranty work on a past job.</p>
  <h2>Contact</h2>
  <p>Questions about privacy: call {PHONE}, Mon–Fri 8am–7pm.</p>
</div></div></section>
{footer()}"""
    return head("Privacy Policy | Top Speed Appliance", "How Top Speed Appliance LLC collects and uses booking details on topspeedrepairs.com.", "/privacy") + body

def terms():
    body = f"""{simple_hero("Terms", "Straight terms,<br><span class='red'>in writing.</span>",
      "The terms every Top Speed visit runs on — the same ones printed on your quote.")}
<section class="section"><div class="wrap"><div class="prose">
  <h2>Service</h2>
  <p>Top Speed Appliance LLC provides appliance repair and installation at your home or business across 65 cities
  in Broward, Palm Beach and Miami-Dade counties. Business hours are Monday–Friday, 8am–7pm. Every booking is
  confirmed by a human Service Setter — an online request is not a confirmed appointment until we confirm it.</p>
  <h2>Diagnostic</h2>
  <p>Residential service starts with a $99 diagnostic, collected at booking to reserve your window. The diagnostic
  is credited in full toward an approved repair performed by Top Speed. If you decline the repair, the diagnostic
  remains due for the visit and the findings.</p>
  <h2>Flat labor and written quotes</h2>
  <p>Repair labor is $210 flat and installation labor is $150 flat. Parts and materials are priced in a written
  quote on site. No work is done without your approved written quote, and there is no hourly billing.</p>
  <h2>Commercial work</h2>
  <p>Commercial service is priced by custom quote only, through Appliance Pro.</p>
  <h2>Warranty</h2>
  <p>Repairs carry a 90-day parts and labor warranty on the work performed. The warranty covers the repaired fault;
  unrelated faults and pre-existing conditions are quoted as new work.</p>
  <h2>Cancellations</h2>
  <p>Call {PHONE} to move or cancel a visit. Windows are held on a first-confirmed basis; weather and flooding can
  move windows for safety, and we will always call you first.</p>
</div></div></section>
{footer()}"""
    return head("Terms of Service | Top Speed Appliance", "Top Speed Appliance service terms: $99 diagnostic credited, flat labor, written quotes, 90-day parts & labor warranty.", "/terms") + body

def not_found():
    body = f"""{nav()}
<section class="page-hero" style="padding:96px 0"><div class="wrap">
  <p class="eyebrow">404 — off the road</p>
  <h1 class="h1">This page took<br><span class="red">a wrong turn.</span></h1>
  <p class="lede" style="margin-top:16px">The page you asked for isn't here — but a repair is one tap away.</p>
  <div class="hero-cta">
    <a class="btn btn-primary" href="/book">Book a repair</a>
    <a class="btn btn-ghost" href="/">Back to home</a>
    <a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a>
  </div>
</div></section>
{footer()}"""
    return head("Page Not Found | Top Speed Appliance", "That page isn't here. Book appliance repair with Top Speed instead.", "/404") + body

# ---------------------------------------------------------------- files
LLMS = """# Top Speed Appliance — Top Speed Service OS

> Top Speed Appliance LLC is an appliance repair, installation, sales and delivery company serving Florida's tri-county area (Broward, Palm Beach and Miami-Dade counties). Bookings, dispatch and live job tracking run on the Top Speed Service OS platform. Slogan: "The Faster, The Better."
> This site — topspeedrepairs.com — is the premium repair storefront of the same company and the same Service Setters dispatch queue.

## Contact

- Phone: (844) 460-7038
- Service area: 65 cities across Broward, Palm Beach & Miami-Dade — a service-area business; repairs happen at your home or business (no public street address)
- Hours: Monday–Friday, 8:00 AM – 7:00 PM
- Website: https://topspeedrepairs.com/

## Services

- Refrigerator repair: https://topspeedrepairs.com/services/refrigerator-repair
- Washer repair: https://topspeedrepairs.com/services/washer-repair
- Dryer repair: https://topspeedrepairs.com/services/dryer-repair
- Oven and range repair: https://topspeedrepairs.com/services/oven-range-repair
- Dishwasher repair: https://topspeedrepairs.com/services/dishwasher-repair
- Freezer and ice maker repair: https://topspeedrepairs.com/services/freezer-ice-maker-repair
- Microwave repair: https://topspeedrepairs.com/services/microwave-repair
- Garbage disposal repair: https://topspeedrepairs.com/services/garbage-disposal-repair
- Appliance installation: https://topspeedrepairs.com/services/appliance-installation

All services: https://topspeedrepairs.com/services

## Pricing (residential)

- Diagnostic: $99, collected at booking and credited toward an approved repair. The diagnostic is still due if the repair is declined.
- Repair labor: $210 flat.
- Installation labor: $150 flat.
- Parts and materials are priced in a written quote. No work is done without an approved written quote.
- Commercial service is priced by custom quote only — see Appliance Pro (https://www.appliancepro.net/).

## Booking

- Book online with the classic web form: https://topspeedrepairs.com/book
- Or ask Speedy, the AI service assistant on the site — Speedy summarizes your request and asks for your confirmation before anything is sent to the Service Setters office.
- Every job is confirmed by a human Service Setter and tracked live from request to completion (Track My Tech: https://topspeedserviceos.com/track).

## Coverage

- 65 cities across Broward (31), Palm Beach (16) and Miami-Dade (18) counties are matched automatically when booking; the platform publishes 131 local pages (65 city pages and 66 service pages).
- City directory on this site: https://topspeedrepairs.com/cities

## Programs

- Refer & Earn: customers earn a $25 credit for each completed referral (higher tiers for repeat referrers); the referred friend receives $25 off their first repair. https://appliancereferral.com
- Track My Tech: customers receive their technician's photo and a live tracking link when the tech is on the way.

## One platform — Top Speed Service OS

Top Speed Appliance LLC runs on one platform: Top Speed Service OS (https://topspeedserviceos.com). Every door below is the same company and the same Service Setters dispatch queue.

- Customer site & booking: https://topspeedserviceos.com
- This storefront: https://topspeedrepairs.com
- Residential repair site: https://www.topspeedappliance.net/
- Provider network (join, network businesses, dispatch): https://topspeedapplianceservice.com/
- Commercial portal — Appliance Pro: https://www.appliancepro.net/
- Marketplace — Pepper Lists (buy, sell, book): https://pepperlists.com
- Refer & Earn: https://topspeedserviceos.com/refer (program home: https://appliancereferral.com)
- Media OS — social and video: https://topspeedserviceos.com/media
- Ads OS — advertising: https://topspeedserviceos.com/ads
- Every door in one place: https://topspeedserviceos.com/links

## The enterprise — Top Speed OS

Top Speed OS is the main division of Top Speed Appliance LLC — the parent structure for the whole enterprise and every platform in it. Enterprise hub: https://topspeedserviceos.com/top-speed-os

- Top Speed Service OS (service division): appliance repair and installation, booking, Service Setters dispatch, live job tracking and the provider network, across 65 cities in Broward, Palm Beach and Miami-Dade. https://topspeedserviceos.com
- Top Speed Sales OS (retail division): the Sales OS console and the Top Speed Appliances shop for used appliances. Console: https://topspeedserviceos.com/sales-os · Shop: https://topspeedappliances.com
- Speedy AI: the AI service assistant on Top Speed surfaces — questions, photo diagnosis and booking help. https://topspeedserviceos.com/speedy

## Network partner

- Cleanout Vents is the Top Speed network's registered partner for dryer vent cleaning, vent repair and vent rerouting, reachable through Top Speed: https://topspeedserviceos.com/cleanout-vents-site or by calling (844) 460-7038. Vent services are quoted by Cleanout Vents; Top Speed does not publish vent prices.

## Official social profiles

- Facebook — Top Speed Appliance Repair and Installation (official Page): https://www.facebook.com/profile.php?id=61596590488055
- Instagram — Ramone Williams, owner ("Speed King"): https://www.instagram.com/rome64220/
- Instagram — Top Speed Appliance (business): https://www.instagram.com/topspeedappliance/
- Instagram — Top Speed Appliance (business, verified): https://www.instagram.com/rom64220/
"""

ROBOTS = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://topspeedrepairs.com/sitemap.xml
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
<rect width="48" height="48" rx="10" fill="#0C1B31"/>
<path fill="#fff" d="M24 5l12.5 4.3v9.6c0 8.1-5.2 14.1-12.5 17.5C16.7 33 11.5 27 11.5 18.9V9.3z"/>
<path fill="none" stroke="#E94E5C" stroke-width="1.8" d="M24 8.4l9.4 3.2v7.3c0 6.4-4 11.2-9.4 13.9-5.4-2.7-9.4-7.5-9.4-13.9v-7.3z"/>
<path fill="#0C1B31" d="M25.8 13.5L18.8 24h4.6l-1.4 8 8.4-11.4h-4.7z"/>
</svg>
"""

def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return rel

def main():
    urls = ["/", "/book", "/services", "/cities", "/pricing", "/privacy", "/terms"]
    write("index.html", home())
    write("book/index.html", book())
    write("services/index.html", services_hub())
    for s in SERVICES:
        write(f"services/{s['slug']}/index.html", service_page(s))
        urls.append(f"/services/{s['slug']}")
    write("cities/index.html", cities_hub())
    for c in CITIES:
        write(f"cities/{c['slug']}/index.html", city_page(c))
        urls.append(f"/cities/{c['slug']}")
    write("pricing/index.html", pricing())
    write("privacy/index.html", privacy())
    write("terms/index.html", terms())
    write("404.html", not_found())
    write("llms.txt", LLMS)
    write("robots.txt", ROBOTS)
    write("favicon.svg", FAVICON)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = "1.0" if u == "/" else ("0.9" if u in ("/book", "/services", "/cities") else "0.7")
        sm.append(f"  <url><loc>{BASE}{u}</loc><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    print(f"built {len(urls)} sitemap URLs · {9 + len(CITIES) + 7} pages total")

if __name__ == "__main__":
    main()
