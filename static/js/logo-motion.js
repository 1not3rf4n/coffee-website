/* ================================================================
   LOGO MOTION — GSAP coffee-fill intro

   The real brand mark is used as an alpha mask (see logo-motion.css).
   This file only sequences opacity / clip-path / transform on those
   masked layers — no procedural drawing — so it stays razor-sharp and
   reads as a polished, agency-grade logo reveal.

   Sequence:
     1. ghost logo fades in, warm glow blooms
     2. espresso rises from the base and fills the mark (clip-path)
     3. crema band tracks the rising surface
     4. a light sweep crosses the filled logo
     5. wordmark + rule reveal
     6. whole lockup lifts, curtain fades, site rises in
   ================================================================ */
(function () {
    'use strict';

    var overlay = document.getElementById('lmOverlay');
    if (!overlay) return;

    var root = document.documentElement;
    var reduce = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Grab the layers the timeline drives.
    var $ = function (sel) { return overlay.querySelector(sel); };
    var els = {
        stage:   $('.lm-stage'),
        glow:    $('.lm-glow'),
        wrap:    $('.lm-logo-wrap'),
        ghost:   $('.lm-ghost'),
        coffee:  $('.lm-coffee'),
        crema:   $('.lm-crema'),
        shine:   $('.lm-shine'),
        word:    $('.lm-word'),
        rule:    $('.lm-word-rule'),
        skip:    $('.lm-skip'),
        prog:    $('.lm-progress')
    };

    var finished = false;

    /* ---- Finale: open the curtain and let the page rise in. ---- */
    function reveal() {
        root.classList.add('lm-reveal');
    }
    function teardown() {
        if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
        root.classList.remove('lm-playing');
    }
    function finish(fast) {
        if (finished) return;
        finished = true;
        reveal();
        // fade the curtain, then remove it
        var gs = window.gsap;
        if (gs) {
            gs.to(overlay, {
                opacity: 0,
                duration: fast ? 0.35 : 0.7,
                ease: 'power2.inOut',
                onComplete: teardown
            });
        } else {
            overlay.style.transition = 'opacity 0.5s';
            overlay.style.opacity = '0';
            setTimeout(teardown, 520);
        }
    }

    /* ---- No-JS-animation fallbacks ---- */
    // Reduced motion: CSS already shows the filled logo; just hold + reveal.
    if (reduce) {
        if (els.skip) els.skip.style.opacity = '1';
        setTimeout(function () { finish(true); }, 900);
        wireSkip();
        return;
    }
    // GSAP failed to load (e.g. offline CDN): show a graceful CSS fill,
    // then reveal — never trap the visitor on a blank overlay.
    if (!window.gsap) {
        cssFallback();
        wireSkip();
        return;
    }

    var gsap = window.gsap;

    // Expose the timeline for debugging / manual control (harmless).
    var params = new URLSearchParams(location.search);

    /* ================= MAIN TIMELINE ================= */
    var tl = gsap.timeline({
        defaults: { ease: 'power2.out' },
        onUpdate: function () {
            if (els.prog) els.prog.style.width = (tl.progress() * 100) + '%';
        },
        onComplete: function () { finish(false); }
    });
    window.__lmTL = tl;   // debug handle

    // Optional pause point for QA: ?intro=freeze:1.8 holds the timeline.
    var freeze = params.get('intro');
    if (freeze && freeze.indexOf('freeze:') === 0) {
        var at = parseFloat(freeze.split(':')[1]) || 0;
        requestAnimationFrame(function () { tl.pause().time(at); });
    }

    // Start states
    gsap.set(els.stage, { scale: 0.92, y: 18, opacity: 0 });
    gsap.set(els.ghost, { opacity: 0 });
    gsap.set(els.coffee, { clipPath: 'inset(100% 0 0 0)' });
    gsap.set(els.crema, { opacity: 0, clipPath: 'inset(100% 0 0 0)' });
    gsap.set(els.glow, { opacity: 0, scale: 0.6 });

    // 1 — stage + ghost logo settle in, glow blooms
    tl.to(els.stage, { scale: 1, y: 0, opacity: 1, duration: 0.9, ease: 'power3.out' }, 0)
      .to(els.ghost, { opacity: 0.32, duration: 0.7 }, 0.15)
      .to(els.glow, { opacity: 0.5, scale: 1, duration: 1.1, ease: 'sine.out' }, 0.2);

    // 2 — espresso rises to fill the mark. A slight overshoot at the top
    //     mimics liquid settling. The crema band tracks the surface.
    var fillProxy = { v: 100 };   // remaining top inset, %
    tl.to(fillProxy, {
        v: 0,
        duration: 2.0,
        ease: 'power1.inOut',
        onUpdate: function () {
            var top = fillProxy.v;
            els.coffee.style.clipPath = 'inset(' + top + '% 0 0 0)';
            // crema is a ~10% band riding just under the surface
            var cremaTop = Math.max(0, top - 2);
            var cremaBot = Math.min(100, top + 8);
            els.crema.style.clipPath =
                'inset(' + cremaTop + '% 0 ' + (100 - cremaBot) + '% 0)';
        }
    }, 0.75)
      .to(els.crema, { opacity: 1, duration: 0.5 }, 0.9)
      // glow pulses warmer as the cup fills
      .to(els.glow, { opacity: 0.72, duration: 1.0, ease: 'sine.inOut' }, 1.1);

    // crema fades once settled, leaving a clean filled logo
    tl.to(els.crema, { opacity: 0, duration: 0.6 }, 2.95);

    // 4 — light sweep across the finished logo
    tl.set(els.shine, { opacity: 1, backgroundPosition: '140% 0' }, 3.0)
      .to(els.shine, { backgroundPosition: '-40% 0', duration: 0.9, ease: 'power2.inOut' }, 3.0)
      .to(els.shine, { opacity: 0, duration: 0.3 }, 3.75);

    // 5 — wordmark + rule reveal
    tl.fromTo(els.word,
        { opacity: 0, y: 16 },
        { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, 3.35)
      .fromTo(els.rule,
        { scaleX: 0 },
        { scaleX: 1, duration: 0.8, ease: 'power2.out' }, 3.5);

    // skip button eases in early and stays available
    if (els.skip) tl.to(els.skip, { opacity: 1, duration: 0.5 }, 1.1);

    // 6 — lift the whole lockup, dim the glow, hand off to the site
    tl.addLabel('lift', 4.5)
      .to(els.glow, { opacity: 0, duration: 0.8, ease: 'sine.in' }, 'lift')
      .to(els.stage, {
          y: -window.innerHeight * 0.32,
          scale: 0.86,
          opacity: 0,
          duration: 1.0,
          ease: 'power2.in'
      }, 'lift')
      // begin the page reveal slightly before the lockup clears frame,
      // so the two motions overlap into one continuous rise
      .add(reveal, 'lift+=0.35');

    /* ================= CONTROLS ================= */
    function wireSkip() {
        if (els.skip) {
            els.skip.addEventListener('click', function () { finish(true); });
        }
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') finish(true);
        });
    }
    wireSkip();

    // If the page loads in a background tab, rAF is suspended and the
    // timeline can't advance. Pause it and the safety timer until the tab
    // is actually visible, so a backgrounded intro never desyncs.
    var safetyTimer = null;
    function armSafety() {
        clearTimeout(safetyTimer);
        safetyTimer = setTimeout(function () { if (!finished) finish(true); }, 12000);
    }
    if (document.hidden) {
        tl.pause();
    } else {
        armSafety();
    }
    document.addEventListener('visibilitychange', function () {
        if (finished) return;
        if (document.hidden) {
            tl.pause();
            clearTimeout(safetyTimer);
        } else {
            tl.resume();
            armSafety();
        }
    });

    /* ================= FALLBACK (no GSAP) ================= */
    function cssFallback() {
        els.ghost.style.transition = 'opacity 0.6s ease';
        els.coffee.style.transition = 'clip-path 2s ease-in-out';
        els.word.style.transition = 'opacity 0.8s ease';
        els.rule.style.transition = 'transform 0.8s ease';
        if (els.skip) els.skip.style.opacity = '1';

        requestAnimationFrame(function () {
            els.ghost.style.opacity = '0.32';
            els.coffee.style.clipPath = 'inset(0 0 0 0)';
            setTimeout(function () {
                els.word.style.opacity = '1';
                els.rule.style.transform = 'scaleX(1)';
            }, 1400);
            setTimeout(function () { finish(false); }, 3400);
        });
    }
})();
