/* =========================================================
   Mad Makers Pro - main behaviours
   No framework, no build step. Vanilla JS, ES modules-free.
   ========================================================= */
(function () {
  "use strict";

  // ---------- Eyebrow loop: cycle through several lines in sync with the animation ----------
  (function () {
    const eyebrow = document.querySelector(".eyebrow-loop .eyebrow-text");
    if (!eyebrow) return;
    const lines = [
      "AGENCE WEB CRÉATIVE - PARIS",
      "IMAGINÉ PAR MAÏCK & GOUDET",
      "MAKE IT MAD!",
    ];
    let i = 0;
    eyebrow.textContent = lines[0];
    // animationiteration fires each loop, when the keyframe is back at 0%
    // (text scaleX = 0, i.e. invisible) - perfect moment to swap content
    eyebrow.addEventListener("animationiteration", () => {
      i = (i + 1) % lines.length;
      eyebrow.textContent = lines[i];
    });
  })();

  // ---------- Founder cards -> details modal ----------
  (function () {
    const modal = document.getElementById("founderModal");
    if (!modal) return;
    const cards = document.querySelectorAll(".duo-card[data-founder]");
    if (!cards.length) return;

    const founders = {
      maick: {
        name: "Maïck",
        role: "Cofondateur · Direction artistique & production",
        meta: "Rayan Mpondo · Paris",
        photo: "assets/maick%20pfp.jpeg",
        bio:
          "<p>Profil hybride formé au marketing digital chez <b>Orange</b> et <b>Vinci Construction</b>, sur des audiences exigeantes - dirigeants PME, directions marketing grands groupes.</p>" +
          "<p>Chez Mad Makers, prend les briefs, conçoit les directions créatives et pilote la production jusqu'à la mise en ligne. <b>Votre interlocuteur unique</b> du premier appel à la livraison.</p>",
        linkedin: "https://www.linkedin.com/in/rayan-m-3a8ba6145/",
      },
      goudet: {
        name: "Goudet Abalé",
        role: "Cofondateur · Stratégie & développement",
        meta: "Sciences Po Lille · Johns Hopkins SAIS",
        photo: "assets/goudet%20pfp.jpeg",
        bio:
          "<p>Diplômé de <b>Sciences Po Lille</b> et titulaire d'un master à <b>Johns Hopkins (SAIS)</b>. Deux fois lauréat du Harvard MUN.</p>" +
          "<p>10+ ans en conseil stratégique international - Assemblée nationale, ministère de la Justice, dirigeants d'entreprise, missions Europe et Afrique francophone.</p>" +
          "<p>Chez Mad Makers, co-dirige le <b>développement commercial et la stratégie</b>.</p>",
        linkedin: "https://www.linkedin.com/in/goudet-abal%C3%A9-329909104/",
      },
    };

    const photo = modal.querySelector("#fmPhoto");
    const nameEl = modal.querySelector("#fmName");
    const roleEl = modal.querySelector("#fmRole");
    const metaEl = modal.querySelector("#fmMeta");
    const bioEl = modal.querySelector("#fmBio");
    const linkEl = modal.querySelector("#fmLink");
    let lastFocus = null;

    // Preload both founder photos so the modal never shows a stale image
    // when the user switches from one card to the other.
    const preloads = {};
    Object.keys(founders).forEach((k) => {
      const i = new Image();
      i.src = founders[k].photo;
      preloads[k] = i;
    });

    function paint(key) {
      const f = founders[key];
      if (!f) return;
      // hide the photo first, only swap src once we know the new one is ready
      photo.style.opacity = "0";
      const showPhoto = () => {
        photo.alt = "Portrait de " + f.name;
        photo.src = f.photo;
        // next frame so opacity transition plays after src swap
        requestAnimationFrame(() => { photo.style.opacity = "1"; });
      };
      if (preloads[key].complete && preloads[key].naturalWidth > 0) {
        showPhoto();
      } else {
        preloads[key].addEventListener("load", showPhoto, { once: true });
      }
      nameEl.textContent = f.name;
      roleEl.textContent = f.role;
      metaEl.textContent = f.meta || "";
      bioEl.innerHTML = f.bio;
      linkEl.href = f.linkedin;
    }

    function open(key, sourceEl) {
      if (!founders[key]) return;
      lastFocus = sourceEl || document.activeElement;
      paint(key);
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      setTimeout(() => {
        const btn = modal.querySelector(".founder-modal-close");
        if (btn) btn.focus();
      }, 60);
    }

    function close() {
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    cards.forEach((card) => {
      card.addEventListener("click", () => open(card.dataset.founder, card));
    });
    modal.querySelectorAll("[data-close-modal]").forEach((el) => {
      el.addEventListener("click", close);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("is-open")) close();
    });
  })();

  // ---------- Hero h1: per-character "lens" detachment on cursor proximity ----------
  // Each character of the heading gets wrapped in a span with a random push
  // direction. On pointermove we compute a proximity factor 0..1 for each
  // char (1 at the cursor, 0 outside a ~95 px radius) and lerp it into a
  // CSS variable. The CSS uses that --t to translate / rotate the char
  // proportionally - so chars near the cursor "lift off" subtly while the
  // rest of the title stays still.
  (function () {
    const h1 = document.querySelector(".hero h1");
    if (!h1) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    // hover-only effect; skip on touch / small screens
    if (matchMedia("(pointer: coarse), (max-width: 720px)").matches) return;

    // walk text nodes and split each printable character into a span;
    // preserve <br> and any inline elements (like <em>) by recursing.
    function splitNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent;
        if (!text || !text.trim()) return;
        const frag = document.createDocumentFragment();
        for (const ch of text) {
          if (ch === " ") {
            frag.appendChild(document.createTextNode(" "));
          } else {
            const sp = document.createElement("span");
            sp.className = "frag-char";
            sp.textContent = ch;
            sp.setAttribute("data-ch", ch);  // for the gradient ::before pseudo
            // stable random push direction + small rotation per char
            const a = Math.random() * Math.PI * 2;
            sp.style.setProperty("--rx", Math.cos(a).toFixed(3));
            sp.style.setProperty("--ry", Math.sin(a).toFixed(3));
            sp.style.setProperty("--rot", ((Math.random() - 0.5) * 7).toFixed(1) + "deg");
            frag.appendChild(sp);
          }
        }
        node.parentNode.replaceChild(frag, node);
      } else if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== "BR") {
        Array.from(node.childNodes).forEach(splitNode);
      }
    }
    Array.from(h1.childNodes).forEach(splitNode);

    const chars = Array.from(h1.querySelectorAll(".frag-char"));
    if (!chars.length) return;

    // Each char inside <em> gets a SOLID colour sampled from the gradient
    // at its position. Solid colour paints the whole glyph (including italic
    // overhang) so nothing gets clipped, no matter where the char sits in em.
    // Gradient: lime (#c8ff3d) 0..55%, fade toward rgba(241,236,224,0.35) at 100%.
    function sampleLimeGradient(t) {
      const lime = [200, 255, 61];
      // Visual approximation of rgba(241,236,224,0.35) over the dark hero bg
      const fade = [200, 195, 165];
      if (t <= 0.55) return "rgb(" + lime[0] + "," + lime[1] + "," + lime[2] + ")";
      let k = (t - 0.55) / 0.45;
      k = k * k * (3 - 2 * k); // smoothstep
      const r = Math.round(lime[0] + (fade[0] - lime[0]) * k);
      const g = Math.round(lime[1] + (fade[1] - lime[1]) * k);
      const b = Math.round(lime[2] + (fade[2] - lime[2]) * k);
      return "rgb(" + r + "," + g + "," + b + ")";
    }
    function syncEmGradients() {
      h1.querySelectorAll("em").forEach((em) => {
        const er = em.getBoundingClientRect();
        em.querySelectorAll(".frag-char").forEach((c) => {
          c.classList.add("frag-char-em");
          const cr = c.getBoundingClientRect();
          const center = cr.left + cr.width / 2 - er.left;
          const t = Math.max(0, Math.min(1, center / er.width));
          c.style.color = sampleLimeGradient(t);
        });
      });
    }
    requestAnimationFrame(syncEmGradients);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncEmGradients);
    }

    const RADIUS = 95;     // px - influence zone around the cursor
    const LERP = 0.20;     // smoothing factor toward target each frame

    let mx = -1e6, my = -1e6;
    let active = false;
    let raf = 0;
    let rects = null;

    const cacheRects = () => {
      rects = chars.map((s) => {
        const r = s.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      });
    };

    const states = chars.map(() => ({ cur: 0 }));

    const tick = () => {
      if (!rects) cacheRects();
      let any = false;
      for (let i = 0; i < chars.length; i++) {
        const c = rects[i];
        const dx = c.x - mx, dy = c.y - my;
        const dist = Math.hypot(dx, dy);
        const raw = Math.max(0, 1 - dist / RADIUS);
        const target = raw * raw * (3 - 2 * raw); // smoothstep
        const s = states[i];
        s.cur += (target - s.cur) * LERP;
        if (s.cur < 0.001) s.cur = 0;
        chars[i].style.setProperty("--t", s.cur.toFixed(3));
        if (s.cur > 0.005 || target > 0.005) any = true;
      }
      if (active || any) {
        raf = requestAnimationFrame(tick);
      } else {
        raf = 0;
      }
    };

    h1.addEventListener("pointerenter", (e) => {
      cacheRects();
      mx = e.clientX; my = e.clientY;
      active = true;
      if (!raf) raf = requestAnimationFrame(tick);
    });
    h1.addEventListener("pointermove", (e) => {
      mx = e.clientX; my = e.clientY;
    });
    h1.addEventListener("pointerleave", () => {
      active = false;
      mx = -1e6; my = -1e6;
      // tick keeps running until all states relax to 0
      if (!raf) raf = requestAnimationFrame(tick);
    });

    // invalidate rect cache + re-sync em gradients when layout changes
    let resizeRaf = 0;
    window.addEventListener("resize", () => {
      rects = null;
      if (resizeRaf) cancelAnimationFrame(resizeRaf);
      resizeRaf = requestAnimationFrame(syncEmGradients);
    }, { passive: true });
    window.addEventListener("scroll", () => { rects = null; }, { passive: true });
  })();

  // ---------- Sticky nav + back-to-top toggle (single scroll handler) ----------
  const nav = document.getElementById("nav");
  const backTop = document.getElementById("backTop");
  if (nav || backTop) {
    let lastY = window.scrollY;
    let ticking = false;
    const onScroll = () => {
      const y = window.scrollY;
      if (nav) {
        if (y > 80 && y > lastY) nav.classList.add("is-hidden");
        else nav.classList.remove("is-hidden");
      }
      if (backTop) {
        if (y > 700) backTop.classList.add("is-visible");
        else backTop.classList.remove("is-visible");
      }
      lastY = y;
      ticking = false;
    };
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(onScroll);
    }, { passive: true });
    onScroll(); // initial state
  }
  if (backTop) {
    backTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // ---------- Scroll reveal ----------
  const revealEls = document.querySelectorAll(
    "section, .feature-card, .article, .duo-card, .svc-row, .stat, .logos .l, .proj-card"
  );
  revealEls.forEach((el) => el.classList.add("reveal"));
  const revealIO = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        revealIO.unobserve(e.target);
      }
    }
  }, { threshold: 0.12 });
  revealEls.forEach((el) => revealIO.observe(el));

  // ---------- Footer-CTA: WebGL dot grid with magnifying lens at the cursor ----------
  (function () {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    // skip on touch / small devices - hover-only effect, no point on phones
    if (matchMedia("(pointer: coarse), (max-width: 720px)").matches) return;
    const cta = document.querySelector(".footer-cta");
    if (!cta) return;

    const canvas = document.createElement("canvas");
    canvas.className = "footer-cta-fx";
    canvas.setAttribute("aria-hidden", "true");
    // insert as the first child so it's behind text but in front of the video/tint
    cta.insertBefore(canvas, cta.firstChild);

    const gl = canvas.getContext("webgl", {
      alpha: true, premultipliedAlpha: false,
      antialias: false, depth: false, stencil: false,
    });
    if (!gl) { canvas.remove(); return; }

    const TRAIL = 20;
    const VS = "attribute vec2 a_pos;void main(){gl_Position=vec4(a_pos,0.0,1.0);}";
    const FS = [
      "precision mediump float;",
      "uniform vec2 u_res;",
      "uniform vec2 u_mouse;",
      "uniform float u_active;",
      "uniform float u_cell;",
      "uniform float u_time;",
      "uniform vec2 u_trail[" + TRAIL + "];",       // past mouse positions (device px)
      "uniform float u_trailI[" + TRAIL + "];",     // intensity 0..1 per trail point (decays)
      "float hash21(vec2 p){return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);}",
      "float vnoise(vec2 p){",
      "  vec2 i = floor(p); vec2 f = fract(p); f = f*f*(3.0 - 2.0*f);",
      "  return mix(mix(hash21(i), hash21(i+vec2(1.0,0.0)), f.x),",
      "             mix(hash21(i+vec2(0.0,1.0)), hash21(i+vec2(1.0,1.0)), f.x), f.y);",
      "}",
      "void main(){",
      "  vec2 frag = vec2(gl_FragCoord.x, u_res.y - gl_FragCoord.y);",
      "  vec2 toMouse = frag - u_mouse;",
      "  float dist = length(toMouse);",
      "  float ang = atan(toMouse.y, toMouse.x);",
      // boundary wobble scales with the larger radius so the silhouette stays
      // proportionally distorted, not just a smooth larger circle
      "  float wob = (vnoise(vec2(ang * 1.6, u_time * 0.5)) - 0.5) * 180.0",
      "             + (vnoise(vec2(ang * 4.2 + 1.7, u_time * 0.8)) - 0.5) * 84.0;",
      "  float lensRadius = 330.0;",
      "  float lensZone = smoothstep(lensRadius, 0.0, dist + wob) * u_active;",
      // gentler distortion (was 0.30 -> 0.15) and very light edge refraction
      "  vec2 warped = u_mouse + toMouse * (1.0 + lensZone * 0.15);",
      "  float edge = lensZone * (1.0 - lensZone) * 4.0;",
      "  vec2 refractDir = dist > 0.5 ? toMouse / dist : vec2(0.0);",
      "  warped += refractDir * edge * 1.8;",
      "  vec2 cell = warped / u_cell;",
      "  vec2 off = fract(cell) - 0.5;",
      "  float r = length(off);",
      // smaller dots than before (was 0.085/0.045)
      "  float dot = smoothstep(0.060, 0.030, r);",
      // === TRAIL: past positions glow dots more, wobbly distorted boundary ===
      "  float trailBoost = 0.0;",
      "  for (int i = 0; i < " + TRAIL + "; i++) {",
      "    float ti = u_trailI[i];",
      "    if (ti > 0.005) {",
      "      vec2 to = frag - u_trail[i];",
      "      float td = length(to);",
      "      float ta = atan(to.y, to.x);",
      "      float tw = (vnoise(vec2(ta * 1.5 + float(i) * 0.7, u_time * 0.7 + float(i) * 1.3)) - 0.5) * 126.0;",
      // 3x larger trail blob (was 100, now 300)
      "      float t = smoothstep(300.0, 0.0, td + tw) * ti;",
      "      trailBoost = max(trailBoost, t);",
      "    }",
      "  }",
      // Dots are invisible by default; they only appear where the lens or
      // the trail reveals them. The reveal factor combines the current lens
      // zone and the trail glow, so the user "uncovers" the grid as they
      // move the cursor.
      "  float reveal = max(lensZone, trailBoost);",
      "  float a = dot * reveal;",
      "  gl_FragColor = vec4(0.945, 0.925, 0.879, a);",
      "}",
    ].join("\n");

    function compile(t, s) {
      const sh = gl.createShader(t);
      gl.shaderSource(sh, s);
      gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
        console.warn("[footer-fx]", gl.getShaderInfoLog(sh));
        return null;
      }
      return sh;
    }
    const vs = compile(gl.VERTEX_SHADER, VS);
    const fs = compile(gl.FRAGMENT_SHADER, FS);
    if (!vs || !fs) { canvas.remove(); return; }
    const prog = gl.createProgram();
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { canvas.remove(); return; }

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER,
      new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]),
      gl.STATIC_DRAW);
    const aPos = gl.getAttribLocation(prog, "a_pos");
    const uRes = gl.getUniformLocation(prog, "u_res");
    const uMouse = gl.getUniformLocation(prog, "u_mouse");
    const uActive = gl.getUniformLocation(prog, "u_active");
    const uCell = gl.getUniformLocation(prog, "u_cell");
    const uTime = gl.getUniformLocation(prog, "u_time");
    const uTrail  = gl.getUniformLocation(prog, "u_trail[0]");
    const uTrailI = gl.getUniformLocation(prog, "u_trailI[0]");

    gl.enable(gl.BLEND);
    gl.blendFuncSeparate(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA, gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

    // cap DPR at 1 - the dot grid is a soft gradient pattern, doesn't need
     // retina pixels, and 20-iteration trail loop is heavy at 2x DPR
    const dpr = Math.min(window.devicePixelRatio || 1, 1);
    function resize() {
      const r = cta.getBoundingClientRect();
      const w = Math.max(1, Math.floor(r.width * dpr));
      const h = Math.max(1, Math.floor(r.height * dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w; canvas.height = h;
      }
    }
    resize();
    window.addEventListener("resize", resize, { passive: true });
    new ResizeObserver(resize).observe(cta);

    let tx = -1e6, ty = -1e6;
    let cx = tx, cy = ty;
    let active = 0;            // 0..1
    let activeTarget = 0;
    let raf = 0;
    const t0 = performance.now();

    // Trail of recent mouse positions. Each entry has its own timestamp; the
    // frame computes a 1..0 intensity based on how recent it is. Captured
    // every TRAIL_INTERVAL ms while the lens is active. Fades over TRAIL_LIFE.
    // 20 slots * 50ms = 1000ms - the buffer's oldest slot is just expiring
    // when it gets overwritten, so there's no visible "pop" of an old position
    // suddenly becoming a fresh trail point.
    const TRAIL_INTERVAL = 50;
    const TRAIL_LIFE = 1000;
    const trailX = new Float32Array(TRAIL);
    const trailY = new Float32Array(TRAIL);
    const trailT = new Float32Array(TRAIL);
    for (let i = 0; i < TRAIL; i++) { trailX[i] = -1e6; trailY[i] = -1e6; trailT[i] = -1e9; }
    let trailHead = 0;
    let lastTrailCapture = 0;
    // packed buffers reused each frame
    const trailPosBuf = new Float32Array(TRAIL * 2);
    const trailIntBuf = new Float32Array(TRAIL);

    function frame() {
      const now = performance.now();
      // tighter lerp - low factor was making the lens lag visibly behind the
      // cursor between RAF frames, which read as "jerky". 0.32 keeps it snug.
      cx += (tx - cx) * 0.32;
      cy += (ty - cy) * 0.32;
      active += (activeTarget - active) * 0.18;

      // capture a trail point every TRAIL_INTERVAL ms while lens is on
      if (activeTarget > 0 && (now - lastTrailCapture) > TRAIL_INTERVAL) {
        trailX[trailHead] = cx;
        trailY[trailHead] = cy;
        trailT[trailHead] = now;
        trailHead = (trailHead + 1) % TRAIL;
        lastTrailCapture = now;
      }

      // pack uniform arrays + check if trail still alive
      let trailAlive = false;
      for (let i = 0; i < TRAIL; i++) {
        const age = (now - trailT[i]) / TRAIL_LIFE;
        const intensity = Math.max(0, 1 - age);
        trailIntBuf[i] = intensity;
        trailPosBuf[i * 2]     = trailX[i] * dpr;
        trailPosBuf[i * 2 + 1] = trailY[i] * dpr;
        if (intensity > 0.005) trailAlive = true;
      }

      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.useProgram(prog);
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.enableVertexAttribArray(aPos);
      gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform2f(uMouse, cx * dpr, cy * dpr);
      gl.uniform1f(uActive, Math.max(0, Math.min(1, active)));
      gl.uniform1f(uCell, 28 * dpr);
      gl.uniform1f(uTime, (now - t0) / 1000);
      if (uTrail)  gl.uniform2fv(uTrail, trailPosBuf);
      if (uTrailI) gl.uniform1fv(uTrailI, trailIntBuf);
      gl.drawArrays(gl.TRIANGLES, 0, 6);

      const moving = Math.abs(tx - cx) > 0.4 || Math.abs(ty - cy) > 0.4;
      const fading = Math.abs(activeTarget - active) > 0.005;
      // keep animating while lens is on, fading, or trail still has glow
      if (moving || fading || activeTarget > 0 || trailAlive) {
        raf = requestAnimationFrame(frame);
      } else {
        raf = 0;
      }
    }
    function kick() { if (!raf) raf = requestAnimationFrame(frame); }

    // initial paint so the resting grid shows immediately (active = 0)
    requestAnimationFrame(frame);

    cta.addEventListener("pointerenter", (e) => {
      const r = cta.getBoundingClientRect();
      tx = e.clientX - r.left;
      ty = e.clientY - r.top;
      cx = tx; cy = ty;            // snap on entry
      activeTarget = 1;
      kick();
    });
    cta.addEventListener("pointermove", (e) => {
      const r = cta.getBoundingClientRect();
      tx = e.clientX - r.left;
      ty = e.clientY - r.top;
      kick();
    });
    cta.addEventListener("pointerleave", () => {
      activeTarget = 0;
      kick();
    });
  })();

  // ---------- Background videos: force play, but skip on mobile ----------
  // The hero video is ~43 MB and the footer ~5 MB. On phones we just don't
  // load them at all - the CSS gradients on .hero-bg / .footer-cta act as a
  // graceful fallback (see styles.css mobile media query).
  const skipVideos = matchMedia("(max-width: 720px)").matches;
  document.querySelectorAll(".hero-video, .footer-video").forEach((v) => {
    if (skipVideos) {
      v.removeAttribute("autoplay");
      v.removeAttribute("src");
      try { v.load(); } catch(_){}
      return;
    }
    v.muted = true;
    v.playsInline = true;
    const tryPlay = () => {
      const p = v.play();
      if (p && p.catch) p.catch(() => {});
    };
    if (v.readyState >= 2) tryPlay();
    v.addEventListener("loadeddata", tryPlay, { once: true });
    v.addEventListener("canplay", tryPlay, { once: true });
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) tryPlay();
    });
  });

  // ---------- Services scroller ----------
  // - wheel on the cards (or anywhere in the bleed area of the scroller)
  //   converts vertical wheel into smooth horizontal scroll via RAF lerp
  // - drag-to-scroll fallback for touch / mouse-press
  // - releases to the page at edges so the user is never trapped
  const grid = document.querySelector(".services-grid");
  if (grid) {
    let target = grid.scrollLeft;
    let raf = 0;
    const lerp = () => {
      const cur = grid.scrollLeft;
      const diff = target - cur;
      if (Math.abs(diff) < 0.5) {
        grid.scrollLeft = target;
        raf = 0;
        return;
      }
      grid.scrollLeft = cur + diff * 0.22;
      raf = requestAnimationFrame(lerp);
    };
    const ensureLoop = () => { if (!raf) raf = requestAnimationFrame(lerp); };

    grid.addEventListener("wheel", (e) => {
      const dy = e.deltaY;
      const dx = e.deltaX;
      if (Math.abs(dx) > Math.abs(dy)) return; // trackpad horizontal: native
      let amount = dy;
      if (e.deltaMode === 1)      amount = dy * 16;
      else if (e.deltaMode === 2) amount = dy * grid.clientHeight;
      const max = grid.scrollWidth - grid.clientWidth;
      if (max <= 0) return;
      // edge release to page scroll
      if ((target <= 0 && amount < 0) || (target >= max && amount > 0)) return;
      e.preventDefault();
      target = Math.max(0, Math.min(max, target + amount));
      ensureLoop();
    }, { passive: false });

    // drag-to-scroll
    let isDown = false, startX = 0, startScroll = 0, moved = false;
    grid.addEventListener("pointerdown", (e) => {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      // cancel any in-flight wheel inertia
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      target = grid.scrollLeft;
      isDown = true; moved = false;
      startX = e.clientX;
      startScroll = grid.scrollLeft;
      grid.classList.add("is-grabbing");
    });
    grid.addEventListener("pointermove", (e) => {
      if (!isDown) return;
      const d = e.clientX - startX;
      if (Math.abs(d) > 4) moved = true;
      if (moved) {
        const max = grid.scrollWidth - grid.clientWidth;
        grid.scrollLeft = Math.max(0, Math.min(max, startScroll - d));
        target = grid.scrollLeft;
      }
    });
    const release = () => {
      isDown = false;
      grid.classList.remove("is-grabbing");
    };
    grid.addEventListener("pointerup", release);
    grid.addEventListener("pointercancel", release);
    grid.addEventListener("pointerleave", release);
    grid.addEventListener("click", (e) => { if (moved) e.preventDefault(); }, true);
  }
})();
