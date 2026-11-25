/* Top Speed — premium site · shared UI behavior */
(function () {
  var burger = document.querySelector('[data-burger]');
  var nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () { nav.classList.toggle('open'); });
  }
  /* "Ask Speedy" doors open the real Speedy widget (loaded from the
     flagship, same knowledge base + same booking queue). */
  function openSpeedy() {
    if (typeof window.TSOpenSpeedy === 'function') { window.TSOpenSpeedy(); return true; }
    return false;
  }
  document.querySelectorAll('[data-ask-speedy]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!openSpeedy()) {
        /* Widget still loading — retry briefly, then fall back to the
           flagship Speedy page rather than leaving a dead button. */
        e.preventDefault();
        var tries = 0;
        var t = setInterval(function () {
          tries++;
          if (openSpeedy() || tries > 12) {
            clearInterval(t);
            if (tries > 12 && !openSpeedy()) location.href = 'https://topspeedserviceos.com/speedy';
          }
        }, 250);
      }
    });
  });
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
