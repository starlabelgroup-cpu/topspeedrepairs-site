/* ============================================================
   Top Speed — /book · classic form, wired to the Service OS intake.
   Same endpoint + payload shape as the flagship ZIP wizard:
     POST https://top-speed-service-os.vercel.app/api/v1/speedy/book
   CORS from https://topspeedrepairs.com is allowlisted on the API
   (verified 2026-11-24) — no proxy, no flagship change.
   Helpers: /geo/zip (area match), /geo/cities, /speedy/availability.
   ============================================================ */
(function () {
  var API = 'https://top-speed-service-os.vercel.app/api/v1';
  var form = document.getElementById('book-form');
  if (!form) return;

  var state = { appliance: '', city: '', zipTier: '', areas: [], win: '', winLabel: '' };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- prefill from links (?service=, ?city=, ?zip=) ---------- */
  var qs = new URLSearchParams(location.search);
  function selectAppliance(name) {
    $$('[data-appliance]').forEach(function (b) {
      var on = b.getAttribute('data-appliance') === name;
      b.classList.toggle('sel', on);
      if (on) state.appliance = name;
    });
    rail();
  }
  $$('[data-appliance]').forEach(function (b) {
    b.addEventListener('click', function () { selectAppliance(b.getAttribute('data-appliance')); });
  });
  if (qs.get('service')) selectAppliance(qs.get('service'));
  if (qs.get('city')) { state.city = qs.get('city'); }

  /* ---------- live "Your visit" rail ---------- */
  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }
  function rail() {
    var t = $('#visit-title'), s = $('#visit-sub');
    if (!t) return;
    var issue = val('f-issue');
    t.textContent = state.appliance
      ? state.appliance + (issue ? ' — ' + issue.split('—')[0].trim().slice(0, 42) : '')
      : 'Your repair visit';
    var bits = [];
    if (state.city) bits.push(state.city);
    if (val('f-zip')) bits.push(val('f-zip'));
    s.textContent = bits.length ? bits.join(' · ') : 'Your city · your ZIP';
    var w = $('#visit-window');
    if (w) w.textContent = (val('f-date') && state.winLabel)
      ? val('f-date') + ' · ' + state.winLabel : 'Confirmed by phone';
  }
  ['f-issue', 'f-zip', 'f-date'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', rail);
  });

  /* ---------- ZIP area check ---------- */
  var zipTimer = null;
  var zipEl = document.getElementById('f-zip');
  var zipMsg = document.getElementById('zip-msg');
  var cityWrap = document.getElementById('city-wrap');
  var citySel = document.getElementById('f-city');
  function setZipMsg(text, cls) {
    if (!zipMsg) return;
    zipMsg.textContent = text || '';
    zipMsg.className = 'zip-msg' + (cls ? ' ' + cls : '');
  }
  function checkZip() {
    var zip = val('f-zip');
    state.zipTier = ''; state.areas = [];
    if (!/^\d{5}$/.test(zip)) { setZipMsg(''); rail(); return; }
    fetch(API + '/geo/zip?zip=' + encodeURIComponent(zip))
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var d = (j && j.data) || {};
        state.zipTier = d.tier || ''; state.areas = d.areas || [];
        if (d.tier === 'IN_AREA' && state.areas.length === 1) {
          state.city = state.areas[0];
          setZipMsg(state.city + ' — we serve your area', 'ok');
          if (cityWrap) cityWrap.style.display = 'none';
        } else if (state.areas.length > 1) {
          state.city = '';
          setZipMsg('We serve your ZIP — pick your city:', 'ok');
          if (citySel) {
            citySel.innerHTML = '<option value="">Choose your city…</option>' +
              state.areas.map(function (c) { return '<option>' + c + '</option>'; }).join('');
          }
          if (cityWrap) cityWrap.style.display = '';
        } else if (d.tier === 'OUT_OF_AREA') {
          setZipMsg('That ZIP is outside our auto-matched area — send the request anyway and a Service Setter will confirm coverage by phone.', 'warn');
          if (cityWrap) cityWrap.style.display = '';
        } else {
          setZipMsg('', '');
          if (cityWrap) cityWrap.style.display = '';
        }
        rail();
      })
      .catch(function () { if (cityWrap) cityWrap.style.display = ''; });
  }
  if (zipEl) {
    zipEl.addEventListener('input', function () {
      clearTimeout(zipTimer); zipTimer = setTimeout(checkZip, 450);
    });
    zipEl.addEventListener('blur', checkZip);
  }
  if (citySel) citySel.addEventListener('change', function () { state.city = citySel.value; rail(); });
  var locBtn = document.getElementById('use-location');
  if (locBtn) locBtn.addEventListener('click', function () {
    /* Deliberately simple: focus the ZIP field — the ZIP match is the
       coverage source of truth on this site. */
    if (zipEl) { zipEl.focus(); zipEl.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
  });

  /* ---------- availability windows ---------- */
  var dateEl = document.getElementById('f-date');
  var winWrap = document.getElementById('win-group');
  var WINDOWS = [
    { v: '08-10', label: '8–10 AM' }, { v: '10-12', label: '10 AM–12 PM' },
    { v: '12-14', label: '12–2 PM' }, { v: '14-16', label: '2–4 PM' },
    { v: '16-18', label: '4–6 PM' }
  ];
  function renderWindows(closed) {
    if (!winWrap) return;
    winWrap.innerHTML = '';
    WINDOWS.forEach(function (w) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'pill-btn'; b.textContent = w.label;
      b.setAttribute('data-win', w.v);
      if (closed && closed[w.v]) { b.disabled = true; b.title = 'Closed'; }
      b.addEventListener('click', function () {
        state.win = w.v; state.winLabel = w.label;
        $$('#win-group .pill-btn').forEach(function (x) { x.classList.toggle('sel', x === b); });
        rail();
      });
      winWrap.appendChild(b);
    });
  }
  renderWindows(null);
  function loadAvailability() {
    var d = val('f-date');
    if (!d) return;
    fetch(API + '/speedy/availability?date=' + encodeURIComponent(d))
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var closed = {};
        ((j && j.data && j.data.windows) || []).forEach(function (w) {
          if (w.status && w.status !== 'OPEN') closed[w.id] = true;
        });
        renderWindows(closed);
        if (state.win && closed[state.win]) { state.win = ''; state.winLabel = ''; }
        if (state.win) {
          $$('#win-group .pill-btn').forEach(function (x) {
            x.classList.toggle('sel', x.getAttribute('data-win') === state.win);
          });
        }
        var note = document.getElementById('avail-note');
        if (note) note.textContent = (j && j.data && j.data.capacityConfigured)
          ? 'Live availability for the day you picked — full and passed windows are closed.'
          : 'Pick a day and window — your Service Setter confirms the exact appointment by text.';
      })
      .catch(function () { /* every window stays pickable */ });
  }
  if (dateEl) {
    var today = new Date(); var iso = today.toISOString().slice(0, 10);
    dateEl.min = iso;
    dateEl.addEventListener('change', function () { loadAvailability(); rail(); });
  }

  /* ---------- progress track ---------- */
  function progress() {
    var steps = [
      !!(val('f-first') && val('f-phone')),
      !!val('f-zip'),
      !!state.appliance,
      !!(val('f-date') && state.win),
      false
    ];
    $$('.p-step').forEach(function (el, i) {
      el.classList.toggle('done', !!steps[i]);
      el.classList.toggle('now', !!steps[i] && !steps[i + 1]);
    });
  }
  form.addEventListener('input', progress);
  form.addEventListener('click', function () { setTimeout(progress, 30); });

  /* ---------- submit ---------- */
  var errBox = document.getElementById('form-err');
  function setErr(msg) {
    if (!errBox) return;
    errBox.textContent = msg || '';
    errBox.classList.toggle('show', !!msg);
    if (msg) errBox.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }
  var busy = false;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    var name = (val('f-first') + ' ' + val('f-last')).trim();
    var phone = val('f-phone');
    var address = val('f-address');
    var zip = val('f-zip');
    var issue = val('f-issue');
    if (val('f-first').length < 2) return setErr('Please add your name so the Service Setter knows who to ask for.');
    if (phone.replace(/\D/g, '').length < 10) return setErr('Please add a mobile phone number — your confirmation and tech tracking arrive by text.');
    if (!/^\d{5}$/.test(zip)) return setErr('Please add your 5-digit ZIP so we can match your city.');
    if (address.length < 6) return setErr('Please add the street address where the appliance is.');
    if (!state.appliance) return setErr('Pick the appliance that needs attention.');
    if (issue.length < 3) return setErr('Tell us briefly what the appliance is doing.');
    if (!val('f-date')) return setErr('Pick the day that suits you.');
    if (!state.win) return setErr('Pick an arrival window.');
    if (!state.city && citySel && citySel.value) state.city = citySel.value;
    setErr('');
    busy = true;
    var btn = document.getElementById('submit-btn');
    btn.disabled = true; btn.textContent = 'Sending…';

    var payload = {
      customer: { name: name, phone: phone, address: address },
      city: state.city || (state.areas && state.areas[0]) || '',
      zip: zip,
      appliance: state.appliance,
      issue: issue,
      preferredWindow: state.win,
      preferredDate: val('f-date'),
      source: 'WEB_FORM',
      companyWebsite: val('f-website'),
      via: 'topspeedrepairs.com'
    };
    if (val('f-email')) payload.customer.email = val('f-email');
    if (qs.get('src')) payload.source = qs.get('src');
    ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) {
      if (qs.get(k)) payload[k] = qs.get(k);
    });
    try {
      var rc = sessionStorage.getItem('tsos_ref_code');
      if (rc) payload.referralCode = rc;
    } catch (err) { /* private mode */ }

    fetch(API + '/speedy/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().then(function (j) { return { ok: r.ok, j: j }; });
    }).then(function (x) {
      if (!x.ok || !x.j || !x.j.data || !x.j.data.referenceCode) {
        throw new Error((x.j && x.j.error) || 'Something went wrong sending that.');
      }
      showDone(x.j.data);
    }).catch(function (err) {
      setErr(err.message + ' You can also book by chat — tap Ask Speedy below — or call (844) 460-7038.');
    }).finally(function () {
      busy = false;
      btn.disabled = false; btn.textContent = 'Send booking request';
    });
  });

  function showDone(data) {
    var card = document.getElementById('book-form');
    if (!card) return;
    var msg = data.areaMessage
      ? '<p class="lede" style="margin-top:10px">' + data.areaMessage + '</p>' : '';
    card.innerHTML =
      '<div class="done-card">' +
      '<div class="done-badge"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1F9D63" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg></div>' +
      '<h2>Request received.</h2>' +
      '<p style="color:var(--ink-600);margin-top:10px">Your booking reference is</p>' +
      '<div class="done-ref">' + data.referenceCode + '</div>' + msg +
      '<p style="color:var(--ink-600);margin-top:14px">A Service Setter confirms every request by phone — expect a call from <b>(844) 460-7038</b> during business hours, Mon–Fri 8am–7pm. When your tech is on the way you will get a live tracking link by text.</p>' +
      '<div class="form-foot"><a class="btn btn-navy" href="https://topspeedserviceos.com/track">Track My Tech</a>' +
      '<a class="btn btn-ghost" style="border-color:var(--line-2);color:var(--ink-900)" href="/">Back to home</a></div>' +
      '</div>';
    $$('.p-step').forEach(function (el) { el.classList.add('done'); el.classList.remove('now'); });
    card.scrollIntoView({ behavior: 'smooth' });
  }

  if (qs.get('zip')) { zipEl.value = qs.get('zip'); checkZip(); }
  rail(); progress();
})();
