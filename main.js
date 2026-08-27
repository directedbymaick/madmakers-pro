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

/* ============ PAIN TABS (section probleme) ============ */
(function painTabs(){
  const tablist = document.querySelector('.pain-tablist');
  if (!tablist) return;
  const tabs = Array.from(tablist.querySelectorAll('.pain-tab'));
  const panels = Array.from(document.querySelectorAll('.pain-panel'));

  function activate(targetTab){
    const idx = tabs.indexOf(targetTab);
    if (idx < 0) return;
    tabs.forEach((t, i) => {
      const active = i === idx;
      t.classList.toggle('is-active', active);
      t.setAttribute('aria-selected', active ? 'true' : 'false');
      t.setAttribute('tabindex', active ? '0' : '-1');
    });
    panels.forEach((p, i) => {
      const active = i === idx;
      p.classList.toggle('is-active', active);
      if (active){ p.removeAttribute('hidden'); }
      else { p.setAttribute('hidden', ''); }
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => activate(tab));
  });

  tablist.addEventListener('keydown', (e) => {
    const current = document.activeElement;
    const idx = tabs.indexOf(current);
    if (idx < 0) return;
    let next = -1;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = (idx + 1) % tabs.length;
    else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = (idx - 1 + tabs.length) % tabs.length;
    else if (e.key === 'Home') next = 0;
    else if (e.key === 'End') next = tabs.length - 1;
    if (next >= 0){
      e.preventDefault();
      tabs[next].focus();
      activate(tabs[next]);
    }
  });
})();
