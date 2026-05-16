/* =========================================================
   L'Accélérateur Carnet Plein® by Mad Makers
   Landing artisans - interactions vanilla, no build step
   ========================================================= */

(function () {
  'use strict';

  /* ---------- Nav scroll state + hide-on-scroll-down ---------- */
  const nav = document.getElementById('nav');
  const body = document.body;
  if (nav) {
    let ticking = false;
    let lastScrollY = window.scrollY;
    const HIDE_THRESHOLD = 80;  // ne déclenche le hide qu'après 80px de scroll
    const onScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const y = window.scrollY;
          nav.classList.toggle('is-scrolled', y > 24);

          // Direction du scroll
          const delta = y - lastScrollY;
          if (y < HIDE_THRESHOLD) {
            // Toujours visible en haut de page
            body.classList.remove('nav-hidden');
          } else if (delta > 4) {
            // Scroll down significatif → hide
            body.classList.add('nav-hidden');
          } else if (delta < -4) {
            // Scroll up significatif → show
            body.classList.remove('nav-hidden');
          }
          lastScrollY = y;
          ticking = false;
        });
        ticking = true;
      }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Banner height dynamique pour positionner la nav ---------- */
  const banner = document.querySelector('.pilote-banner');
  if (banner && nav) {
    const adjustNavTop = () => {
      nav.style.setProperty('top', banner.offsetHeight + 'px');
    };
    adjustNavTop();
    window.addEventListener('resize', adjustNavTop, { passive: true });
  }

  /* ---------- Nav burger (mobile) ---------- */
  const burger = document.getElementById('navBurger');
  const navLinks = document.getElementById('navLinks');
  if (burger && navLinks && nav) {
    burger.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(isOpen));
    });
    // Close on link click
    navLinks.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => {
        nav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Reveal animations (IntersectionObserver) ---------- */
  const revealTargets = document.querySelectorAll('[data-reveal], [data-reveal-stagger]');
  if (revealTargets.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealTargets.forEach((el) => io.observe(el));
  } else {
    // Fallback: reveal everything immediately
    revealTargets.forEach((el) => el.classList.add('is-revealed'));
  }

  /* ---------- Roadmap rail animated fill ---------- */
  const rail = document.querySelector('.roadmap-rail');
  if (rail && 'IntersectionObserver' in window) {
    const railIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            rail.style.setProperty('--rail-progress', '90%');
            railIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    railIO.observe(rail);
  }

  /* ---------- Back to top ---------- */
  const backTop = document.getElementById('backTop');
  if (backTop) {
    const onScrollBack = () => {
      backTop.classList.toggle('is-visible', window.scrollY > 800);
    };
    onScrollBack();
    window.addEventListener('scroll', onScrollBack, { passive: true });
    backTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- FAQ : ensure only one open at a time (optional, comment out if not wanted) ---------- */
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach((item) => {
    item.addEventListener('toggle', () => {
      if (item.open) {
        faqItems.forEach((other) => {
          if (other !== item && other.open) other.open = false;
        });
      }
    });
  });

  /* ---------- Lazy hero video (pause when out of viewport) ---------- */
  const heroVideo = document.querySelector('.hero-video');
  const footerVideo = document.querySelector('.footer-cta-video');
  [heroVideo, footerVideo].forEach((video) => {
    if (!video || !('IntersectionObserver' in window)) return;
    const vio = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            video.play().catch(() => {});
          } else {
            video.pause();
          }
        });
      },
      { threshold: 0.05 }
    );
    vio.observe(video);
  });

  /* ---------- Smooth scroll for anchor links (in case browser smooth-behavior is off) ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const offset = 90; // nav height
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ---------- Métiers grid filter - sliding thumb (Apple-style) + tile filtering ---------- */
  const metierFilters = document.getElementById('metierFilters');
  const metierGrid = document.getElementById('metierGrid');
  if (metierFilters && metierGrid) {
    // 1. Inject the sliding thumb
    const thumb = document.createElement('span');
    thumb.className = 'metier-chip-thumb is-init';
    thumb.setAttribute('aria-hidden', 'true');
    metierFilters.insertBefore(thumb, metierFilters.firstChild);

    // 2. Place the thumb on the active chip (no animation on init or resize)
    function moveThumb(animate) {
      const active = metierFilters.querySelector('.metier-chip.is-active');
      if (!active) return;
      const chipRect = active.getBoundingClientRect();
      const containerRect = metierFilters.getBoundingClientRect();
      const x = chipRect.left - containerRect.left + metierFilters.scrollLeft;
      if (!animate) {
        thumb.style.transition = 'none';
      } else {
        thumb.style.transition = '';
      }
      thumb.style.transform = 'translate3d(' + x + 'px, 0, 0)';
      thumb.style.width = chipRect.width + 'px';
      if (!animate) {
        // Force reflow so the transition is restored cleanly next time
        void thumb.offsetWidth;
        thumb.style.transition = '';
      }
    }

    // 3. Init with retries for font/layout settle
    const initThumb = () => {
      moveThumb(false);
      thumb.classList.remove('is-init');
    };
    requestAnimationFrame(initThumb);
    window.addEventListener('load', () => moveThumb(false));
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => moveThumb(false)).catch(function(){});
    }

    // 4. Resize handling - no animation
    if (typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(() => moveThumb(false)).observe(metierFilters);
    } else {
      window.addEventListener('resize', () => moveThumb(false));
    }

    // 5. Filter tiles - FLIP technique : vrais déplacements, opacité minime
    let filterBusy = false;
    function filterTiles(filter) {
      const allTiles = [...metierGrid.querySelectorAll('.metier-tile')];

      // Classify
      const targets = new Map();
      allTiles.forEach((tile) => {
        const isStat = tile.classList.contains('metier-stat');
        const match = isStat ? filter === 'all' : (filter === 'all' || tile.dataset.metier === filter);
        targets.set(tile, match);
      });
      const visibleNow = (t) => !t.classList.contains('is-hidden') && !t.classList.contains('is-leaving');
      const leavers  = allTiles.filter((t) => visibleNow(t) && !targets.get(t));
      const incomers = allTiles.filter((t) => !visibleNow(t) && targets.get(t));
      const stayers  = allTiles.filter((t) => visibleNow(t) && targets.get(t));

      if (leavers.length === 0 && incomers.length === 0) {
        filterBusy = false;
        return;
      }

      const FADE_OUT_MS = 240;
      const MOVE_MS = 580;

      // PHASE 1 : fade-out leavers (slight scale, full opacity drop is fast)
      leavers.forEach((tile) => tile.classList.add('is-leaving'));

      setTimeout(() => {
        // PHASE 2 : measure FIRST positions of stayers (BEFORE layout change)
        const firstRects = new Map();
        stayers.forEach((t) => firstRects.set(t, t.getBoundingClientRect()));

        // Hide leavers (display:none → grid reflows)
        leavers.forEach((tile) => {
          tile.classList.remove('is-leaving');
          tile.classList.add('is-hidden');
        });

        // Prep incomers : visible mais scale(0.86) opacity 0
        incomers.forEach((tile) => {
          tile.classList.remove('is-hidden');
          tile.classList.add('is-arriving');
        });

        // Force layout commit
        void metierGrid.offsetWidth;

        // FLIP : pour chaque stayer, invert via inline transform
        const flippers = [];
        stayers.forEach((tile) => {
          const last = tile.getBoundingClientRect();
          const first = firstRects.get(tile);
          const dx = first.left - last.left;
          const dy = first.top - last.top;
          if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) {
            tile.style.transition = 'none';
            tile.style.transform = 'translate3d(' + dx + 'px, ' + dy + 'px, 0)';
            flippers.push(tile);
          }
        });

        // Commit inverted transforms
        void metierGrid.offsetWidth;

        // PHASE 3 : animate everything to identity (double rAF garantit le rendu)
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            flippers.forEach((tile) => {
              tile.style.transition = 'transform ' + MOVE_MS + 'ms cubic-bezier(.32, .72, 0, 1)';
              tile.style.transform = '';
            });
            incomers.forEach((tile) => {
              tile.classList.remove('is-arriving');
            });
          });
        });

        // Cleanup inline styles after animation
        setTimeout(() => {
          flippers.forEach((tile) => {
            tile.style.transition = '';
            tile.style.transform = '';
          });
          filterBusy = false;
        }, MOVE_MS + 40);
      }, FADE_OUT_MS);
    }

    // 6. Click handler - slide thumb + filter tiles
    metierFilters.addEventListener('click', (e) => {
      const chip = e.target.closest('.metier-chip');
      if (!chip || !metierFilters.contains(chip)) return;
      if (chip.classList.contains('is-active') || filterBusy) return;

      filterBusy = true;
      metierFilters.querySelectorAll('.metier-chip').forEach((c) => c.classList.remove('is-active'));
      chip.classList.add('is-active');
      moveThumb(true);
      filterTiles(chip.dataset.filter);
    });
  }

  /* =====================================================================
     APPLE-STYLE POLISH
     - Section reveal (scale + fade) au scroll
     - Hero video parallax
     - Magnetic CTAs sur hover
     - Smooth scroll cubic ease pour les ancres
  ===================================================================== */

  /* ---------- 1. Section reveal au scroll (sauf hero qui a son propre flow) ---------- */
  const polishSections = document.querySelectorAll('section:not(.hero)');
  if (polishSections.length && 'IntersectionObserver' in window) {
    polishSections.forEach((s) => s.setAttribute('data-section-reveal', ''));
    const sectionObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in-view');
            sectionObs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.05, rootMargin: '0px 0px -8% 0px' }
    );
    polishSections.forEach((s) => sectionObs.observe(s));
  }

  /* ---------- 2. Hero video parallax ---------- */
  const heroVideoEl = document.querySelector('.hero-video');
  if (heroVideoEl) {
    let parallaxRaf = 0;
    const updateParallax = () => {
      const scrollY = window.scrollY;
      const max = window.innerHeight * 1.2;
      if (scrollY > max) return; // arret apres le hero
      const y = scrollY * 0.32;
      heroVideoEl.style.transform = `translate3d(0, ${y}px, 0)`;
    };
    window.addEventListener(
      'scroll',
      () => {
        cancelAnimationFrame(parallaxRaf);
        parallaxRaf = requestAnimationFrame(updateParallax);
      },
      { passive: true }
    );
    updateParallax();
  }

  /* ---------- 3. Magnetic CTAs - les btn-primary se laissent attirer par le curseur ---------- */
  document.querySelectorAll('.btn-primary, .nav-cta').forEach((btn) => {
    let magnetRaf = 0;
    btn.addEventListener('mousemove', (e) => {
      cancelAnimationFrame(magnetRaf);
      magnetRaf = requestAnimationFrame(() => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate3d(${x * 0.18}px, ${y * 0.22}px, 0)`;
      });
    });
    btn.addEventListener('mouseleave', () => {
      cancelAnimationFrame(magnetRaf);
      btn.style.transform = '';
    });
  });

  /* ---------- 4. Smooth scroll custom (cubic ease iOS) pour anchors ---------- */
  // Override le comportement par defaut declare plus haut pour duration + ease premium
  const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
  const smoothScrollTo = (targetY, duration = 900) => {
    const startY = window.scrollY;
    const distance = targetY - startY;
    const startTime = performance.now();
    const step = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutCubic(progress);
      window.scrollTo(0, startY + distance * eased);
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  // Re-bind les anchors deja interceptes plus haut, mais avec le custom easing
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      e.stopImmediatePropagation(); // empeche le handler precedent de tourner aussi
      const offset = 90;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      smoothScrollTo(top, 950);
    }, true); // capture phase pour passer avant l'ancien listener
  });
})();
