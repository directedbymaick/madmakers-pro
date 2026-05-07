/* =========================================================
   Mad Makers Pro - service card WebGL effect
   ---------------------------------------------------------
   Resting state  : dark grey-black + grain
   Pointer enter  : a green "splash" expands radially from the
                    entry point with an FBM-perturbed leading
                    edge and fills the card. Inside the splash,
                    a tri-lobed lens (3 metaballs, smooth-min
                    blended) reveals the dark base underneath
                    with a very long, soft feather.
   Pointer leave  : splash retreats back to the origin.

   Performance budget:
     - per-pixel: 2 FBM calls (3 octaves, cheap value noise)
     - lobe jitter computed CPU-side, passed as uniforms
     - DPR capped at 1.0 (effect is all soft gradients, no need)
     - trail loop short-circuited when there's no energy
     - render loop parks itself when nothing's animating
   ========================================================= */
(function () {
  "use strict";

  if (typeof window === "undefined") return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  // skip on small / coarse-pointer devices: 8 WebGL contexts + per-pixel
  // shader is too heavy on mid-range phones, and the green CSS fallback
  // gradient on .svc looks fine without the effect
  if (matchMedia("(max-width: 720px), (pointer: coarse)").matches) return;

  const TRAIL = 12;

  const VS = `
    attribute vec2 a_pos;
    void main(){ gl_Position = vec4(a_pos, 0.0, 1.0); }
  `;

  // Cheap value noise + 3-octave FBM. Two fbm calls per pixel total.
  const FS = `
    precision mediump float;
    uniform vec2  u_res;
    uniform vec2  u_lens;
    uniform vec2  u_lobe1;
    uniform vec2  u_lobe2;
    uniform vec2  u_lobe3;
    uniform vec2  u_vel;
    uniform vec2  u_trail[${TRAIL}];
    uniform float u_time;
    uniform float u_energy;
    uniform float u_splash;
    uniform vec2  u_splashOrigin;

    float hash21(vec2 p){
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }
    float vnoise(vec2 p){
      vec2 i = floor(p);
      vec2 f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      float a = hash21(i + vec2(0.0, 0.0));
      float b = hash21(i + vec2(1.0, 0.0));
      float c = hash21(i + vec2(0.0, 1.0));
      float d = hash21(i + vec2(1.0, 1.0));
      return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
    }
    // 3-octave FBM (output ~0..1, recentred to ~-0.5..0.5 by callers)
    float fbm(vec2 p){
      float v = 0.5    * vnoise(p);
      v += 0.25  * vnoise(p * 2.03);
      v += 0.125 * vnoise(p * 4.07);
      return v;  // ~ 0..0.875
    }

    float smin(float a, float b, float k){
      float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
      return mix(b, a, h) - k * h * (1.0 - h);
    }

    void main(){
      vec2 uv = gl_FragCoord.xy / u_res.xy;
      uv.y = 1.0 - uv.y;
      float ar = u_res.x / u_res.y;
      vec2 p  = vec2(uv.x * ar, uv.y);
      vec2 SO = vec2(u_splashOrigin.x * ar, u_splashOrigin.y);
      vec2 V  = vec2(u_vel.x * ar, u_vel.y);

      // ---- two reusable noise samples ----
      float bigN    = fbm(p * 3.5 + vec2(u_time * 0.15, -u_time * 0.10)) - 0.45;
      float detailN = fbm(p * 6.5 - vec2(u_time * 0.18,  u_time * 0.12)) - 0.45;

      // ---- light grain ----
      float g = hash21(gl_FragCoord.xy + u_time * 31.7);
      float grain = (g - 0.5) * 0.05;

      // ===== DARK BASE =====
      vec3 baseDark = mix(vec3(0.075, 0.085, 0.045),
                          vec3(0.025, 0.030, 0.015), uv.y);
      // Dot grid with magnifying-lens warp around u_lens.
      // The warp (and the brighter dot tint) are gated by u_splash so the
      // resting state is a clean grid - no lens residue when not hovered.
      vec2 toLens = uv - u_lens;
      float distToLens = length(toLens);
      float lensZone = smoothstep(0.30, 0.0, distToLens) * u_splash;
      vec2 dotUV = u_lens + toLens * (1.0 + lensZone * 0.55);
      float edge = lensZone * (1.0 - lensZone) * 4.0;
      vec2 refractDir = distToLens > 0.0005 ? toLens / distToLens : vec2(0.0);
      dotUV += refractDir * edge * 0.020;

      vec2 dotCell = dotUV * 8.0;
      vec2 dotOff  = fract(dotCell) - 0.5;
      float dotR   = length(dotOff);
      float dotShape = smoothstep(0.045, 0.022, dotR);
      float dotFade = smoothstep(0.78, 0.28, length((uv - vec2(0.5, 0.42)) * vec2(0.95, 1.10)) * 1.15);
      float dots = dotShape * dotFade * 0.26;
      vec3 dotColor = mix(vec3(0.945, 0.925, 0.879), vec3(1.000, 0.985, 0.940), lensZone);
      baseDark = mix(baseDark, dotColor, dots);

      // ===== GREEN OIL =====
      vec3 g0 = vec3(0.847, 1.000, 0.369);
      vec3 g1 = vec3(0.714, 0.902, 0.165);
      vec3 g2 = vec3(0.533, 0.714, 0.078);
      vec3 g3 = vec3(0.220, 0.310, 0.030);
      float yy = clamp(uv.y, 0.0, 1.0);
      vec3 oil =
        (yy < 0.35) ? mix(g0, g1, smoothstep(0.00, 0.35, yy)) :
        (yy < 0.70) ? mix(g1, g2, smoothstep(0.35, 0.70, yy)) :
                      mix(g2, g3, smoothstep(0.70, 1.00, yy));

      // ===== TRI-LOBED LENS =====
      vec2 m1 = vec2(u_lobe1.x * ar, u_lobe1.y);
      vec2 m2 = vec2(u_lobe2.x * ar, u_lobe2.y);
      vec2 m3 = vec2(u_lobe3.x * ar, u_lobe3.y);
      float dLens = smin(smin(distance(p, m1), distance(p, m2), 0.180),
                         distance(p, m3), 0.180);
      // organic surface variation (reuse base+detail noise)
      dLens += bigN * 0.090 + detailN * 0.045;

      float coreR  = 0.025;
      float feather = 0.55;
      float lensRaw = smoothstep(coreR, coreR + feather, dLens);
      // floor: never pure black inside the lens core
      float lensMask = mix(0.13, 1.0, lensRaw);
      lensMask += detailN * 0.08;
      lensMask = clamp(lensMask, 0.13, 1.0);

      // ===== HOVER WAKE (only when energy > 0) =====
      float wake = 0.0;
      if (u_energy > 0.001) {
        for (int i = 0; i < ${TRAIL}; i++) {
          float age = float(i) / float(${TRAIL} - 1);
          vec2 tp = vec2(u_trail[i].x * ar, u_trail[i].y);
          float td = distance(p, tp);
          float kk = mix(8.0, 5.0, age);
          wake += exp(-td * kk) * pow(age + 0.05, 1.7);
        }
        wake /= float(${TRAIL}) * 0.22;
        wake *= 0.55 + 0.55 * (bigN + 0.45);
        wake *= u_energy;
        wake = clamp(wake, 0.0, 0.45);
      }

      // ===== FILLED RENDER (what we'd see if splash = 1) =====
      vec3 filled = mix(baseDark, oil, lensMask);
      vec3 warm = vec3(1.000, 0.660, 0.180);
      filled = mix(filled, mix(filled, warm, 0.50), wake * lensMask);

      // ===== SPLASH FRONT =====
      float splashR = u_splash * 1.55;
      float dSplash = distance(p, SO);
      float edgeNoise = bigN * 0.20 + detailN * 0.10;
      float splashFill = smoothstep(splashR + 0.06,
                                    splashR - 0.18,
                                    dSplash + edgeNoise);
      // hard kill any residual fill when the splash has fully retreated -
      // the FBM edgeNoise can otherwise leave a small puddle at u_splash = 0
      splashFill *= smoothstep(0.0, 0.04, u_splash);
      // foam / leading-edge highlight - only during the transition
      float frontDist = abs(dSplash - splashR + edgeNoise * 0.5);
      float front = exp(-frontDist * 12.0)
                  * smoothstep(0.02, 0.18, u_splash)
                  * smoothstep(1.00, 0.78, u_splash);

      // ===== COMPOSE =====
      vec3 col = mix(baseDark, filled, splashFill);
      col = mix(col, vec3(0.93, 1.00, 0.55), front * 0.55);
      col += vec3(grain);
      float vig = 1.0 - smoothstep(0.55, 1.10, length(uv - 0.5) * 1.4);
      col *= 0.88 + 0.12 * vig;

      gl_FragColor = vec4(col, 1.0);
    }
  `;

  // ---- CPU-side noise for lobe jitter (matches the shader's vnoise/fbm) ----
  function jsHash(x, y) {
    return Math.abs(Math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1;
  }
  function jsVnoise(x, y) {
    const ix = Math.floor(x), iy = Math.floor(y);
    let fx = x - ix, fy = y - iy;
    fx = fx * fx * (3 - 2 * fx);
    fy = fy * fy * (3 - 2 * fy);
    const a = jsHash(ix,     iy);
    const b = jsHash(ix + 1, iy);
    const c = jsHash(ix,     iy + 1);
    const d = jsHash(ix + 1, iy + 1);
    return (a * (1 - fx) + b * fx) * (1 - fy)
         + (c * (1 - fx) + d * fx) * fy;
  }
  function jsFbm(x, y) {
    return 0.5 * jsVnoise(x, y) + 0.25 * jsVnoise(x * 2.03, y * 2.03)
         + 0.125 * jsVnoise(x * 4.07, y * 4.07);
  }

  function compileShader(gl, type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.warn("[cards-fx] compile error:", gl.getShaderInfoLog(s));
      gl.deleteShader(s);
      return null;
    }
    return s;
  }

  function buildProgram(gl) {
    const vs = compileShader(gl, gl.VERTEX_SHADER, VS);
    const fs = compileShader(gl, gl.FRAGMENT_SHADER, FS);
    if (!vs || !fs) return null;
    const p = gl.createProgram();
    gl.attachShader(p, vs);
    gl.attachShader(p, fs);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      console.warn("[cards-fx] link error:", gl.getProgramInfoLog(p));
      return null;
    }
    return p;
  }

  class CardFX {
    constructor(card) {
      this.card = card;
      this.canvas = document.createElement("canvas");
      this.canvas.className = "svc-fx";
      this.canvas.setAttribute("aria-hidden", "true");
      card.insertBefore(this.canvas, card.firstChild);

      const opts = {
        antialias: false, alpha: false, premultipliedAlpha: false,
        depth: false, stencil: false,
      };
      this.gl = this.canvas.getContext("webgl", opts) || this.canvas.getContext("experimental-webgl", opts);
      if (!this.gl) { this.canvas.remove(); return; }

      this.prog = buildProgram(this.gl);
      if (!this.prog) { this.canvas.remove(); return; }

      const gl = this.gl;
      this.aPos          = gl.getAttribLocation(this.prog, "a_pos");
      this.uRes          = gl.getUniformLocation(this.prog, "u_res");
      this.uLens         = gl.getUniformLocation(this.prog, "u_lens");
      this.uLobe1        = gl.getUniformLocation(this.prog, "u_lobe1");
      this.uLobe2        = gl.getUniformLocation(this.prog, "u_lobe2");
      this.uLobe3        = gl.getUniformLocation(this.prog, "u_lobe3");
      this.uVel          = gl.getUniformLocation(this.prog, "u_vel");
      this.uTime         = gl.getUniformLocation(this.prog, "u_time");
      this.uEnergy       = gl.getUniformLocation(this.prog, "u_energy");
      this.uSplash       = gl.getUniformLocation(this.prog, "u_splash");
      this.uSplashOrigin = gl.getUniformLocation(this.prog, "u_splashOrigin");
      this.uTrail        = [];
      for (let i = 0; i < TRAIL; i++) {
        this.uTrail.push(gl.getUniformLocation(this.prog, "u_trail[" + i + "]"));
      }

      this.buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, this.buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
        -1, -1,  1, -1, -1, 1,
        -1,  1,  1, -1,  1, 1,
      ]), gl.STATIC_DRAW);

      this.t0 = performance.now();
      this.lastFrame = this.t0;
      // CAP DPR AT 1 - the effect is all soft gradients, native res is plenty.
      // Also halve again on small cards to be safe.
      this.dpr = Math.min(window.devicePixelRatio || 1, 1);

      // lens / motion
      this.lensX = 0.5; this.lensY = 0.5;
      this.tgtX  = 0.5; this.tgtY  = 0.5;
      this.prevLensX = this.lensX; this.prevLensY = this.lensY;
      this.velX = 0; this.velY = 0;
      this.energy = 0;
      this.lastPX = 0.5; this.lastPY = 0.5; this.lastPT = 0;
      this.trail = new Float32Array(TRAIL * 2);
      for (let i = 0; i < TRAIL; i++) {
        this.trail[i * 2]     = 0.5;
        this.trail[i * 2 + 1] = 0.5;
      }

      // splash
      this.splash = 0;
      this.splashOX = 0.5;
      this.splashOY = 0.5;
      this.splashInRate  = 1 / 0.55;
      this.splashOutRate = 1 / 0.40;

      this.visible = false;
      this.hovered = false;
      this.running = false;

      card.addEventListener("pointerenter", (e) => {
        const r = this.card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top)  / r.height;
        this.hovered = true;
        this.splashOX = x;
        this.splashOY = y;
        this.lensX = x; this.lensY = y;
        this.tgtX = x; this.tgtY = y;
        for (let i = 0; i < TRAIL; i++) {
          this.trail[i * 2]     = x;
          this.trail[i * 2 + 1] = y;
        }
        this.start();
      });
      card.addEventListener("pointerleave", () => {
        this.hovered = false;
      });
      card.addEventListener("pointermove", (e) => this.onMove(e));

      this.io = new IntersectionObserver((entries) => {
        for (const en of entries) {
          this.visible = en.isIntersecting;
          if (this.visible) this.start();
        }
      }, { threshold: 0 });
      this.io.observe(card);

      window.addEventListener("resize", () => this.resize(), { passive: true });

      this.resize();
      this.start();
    }

    onMove(e) {
      const r = this.card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width;
      const y = (e.clientY - r.top)  / r.height;
      const now = performance.now();
      const dt = Math.max(1, now - this.lastPT);
      const dx = x - this.lastPX;
      const dy = y - this.lastPY;
      const v = Math.hypot(dx, dy) / dt;
      this.energy = Math.min(1, this.energy + v * 16);
      this.tgtX = x; this.tgtY = y;
      this.lastPX = x; this.lastPY = y; this.lastPT = now;
      this.start();
    }

    resize() {
      const r = this.card.getBoundingClientRect();
      const w = Math.max(1, Math.floor(r.width  * this.dpr));
      const h = Math.max(1, Math.floor(r.height * this.dpr));
      if (this.canvas.width !== w || this.canvas.height !== h) {
        this.canvas.width = w;
        this.canvas.height = h;
      }
    }

    start() {
      if (this.running) return;
      this.running = true;
      this.lastFrame = performance.now();
      requestAnimationFrame(this.frame);
    }

    // CPU-side computation of the 3 lobe positions for this frame
    computeLobes(t) {
      const baseAng = t * 0.08;
      const j1 = jsFbm(t * 0.40,       1.3) - 0.5;
      const j2 = jsFbm(t * 0.40 + 2.1, 4.7) - 0.5;
      const j3 = jsFbm(t * 0.40 + 4.3, 8.1) - 0.5;
      const spread = 0.110;
      const a1 = baseAng + 0.0      + j1 * 0.55;
      const a2 = baseAng + 2.0944   + j2 * 0.55;
      const a3 = baseAng + 4.1888   + j3 * 0.55;
      const r1 = spread * (0.85 + 0.30 * (j1 + 0.5));
      const r2 = spread * (0.85 + 0.30 * (j2 + 0.5));
      const r3 = spread * (0.85 + 0.30 * (j3 + 0.5));
      this.l1x = this.lensX + Math.cos(a1) * r1;
      this.l1y = this.lensY + Math.sin(a1) * r1;
      this.l2x = this.lensX + Math.cos(a2) * r2;
      this.l2y = this.lensY + Math.sin(a2) * r2;
      this.l3x = this.lensX + Math.cos(a3) * r3;
      this.l3y = this.lensY + Math.sin(a3) * r3;
    }

    frame = (now) => {
      if (!this.running) return;
      const gl = this.gl;
      if (!gl) { this.running = false; return; }

      const dt = Math.min(0.05, (now - this.lastFrame) / 1000);
      this.lastFrame = now;
      const t = (now - this.t0) / 1000;

      // splash
      if (this.hovered) {
        this.splash = Math.min(1, this.splash + dt * this.splashInRate);
      } else {
        this.splash = Math.max(0, this.splash - dt * this.splashOutRate);
      }

      // lens follow
      const k = 1 - Math.exp(-dt * 12);
      this.prevLensX = this.lensX;
      this.prevLensY = this.lensY;
      this.lensX += (this.tgtX - this.lensX) * k;
      this.lensY += (this.tgtY - this.lensY) * k;

      const vDt = Math.max(dt, 0.001);
      const instVx = (this.lensX - this.prevLensX) / vDt;
      const instVy = (this.lensY - this.prevLensY) / vDt;
      const vk = 1 - Math.exp(-dt * 18);
      this.velX += (instVx - this.velX) * vk;
      this.velY += (instVy - this.velY) * vk;

      for (let i = 0; i < TRAIL - 1; i++) {
        this.trail[i * 2]     = this.trail[(i + 1) * 2];
        this.trail[i * 2 + 1] = this.trail[(i + 1) * 2 + 1];
      }
      this.trail[(TRAIL - 1) * 2]     = this.lensX;
      this.trail[(TRAIL - 1) * 2 + 1] = this.lensY;

      this.energy *= Math.exp(-dt * 1.6);
      if (this.energy < 0.001) this.energy = 0;

      this.computeLobes(t);

      const moving = Math.abs(this.tgtX - this.lensX) > 0.0008
                  || Math.abs(this.tgtY - this.lensY) > 0.0008;
      const splashSettled = this.hovered ? this.splash >= 0.999 : this.splash <= 0.001;
      const idle = !this.hovered && !moving && this.energy === 0 && splashSettled;

      if (this.visible) {
        gl.viewport(0, 0, this.canvas.width, this.canvas.height);
        gl.useProgram(this.prog);
        gl.bindBuffer(gl.ARRAY_BUFFER, this.buf);
        gl.enableVertexAttribArray(this.aPos);
        gl.vertexAttribPointer(this.aPos, 2, gl.FLOAT, false, 0, 0);

        gl.uniform2f(this.uRes,           this.canvas.width, this.canvas.height);
        gl.uniform2f(this.uLens,          this.lensX, this.lensY);
        gl.uniform2f(this.uLobe1,         this.l1x, this.l1y);
        gl.uniform2f(this.uLobe2,         this.l2x, this.l2y);
        gl.uniform2f(this.uLobe3,         this.l3x, this.l3y);
        gl.uniform2f(this.uVel,           this.velX, this.velY);
        gl.uniform1f(this.uTime,          t);
        gl.uniform1f(this.uEnergy,        this.energy);
        gl.uniform1f(this.uSplash,        this.splash);
        gl.uniform2f(this.uSplashOrigin,  this.splashOX, this.splashOY);
        for (let i = 0; i < TRAIL; i++) {
          if (this.uTrail[i] !== null) {
            gl.uniform2f(this.uTrail[i], this.trail[i * 2], this.trail[i * 2 + 1]);
          }
        }
        gl.drawArrays(gl.TRIANGLES, 0, 6);
      }

      if (idle) {
        this.running = false;
        return;
      }
      requestAnimationFrame(this.frame);
    }
  }

  function init() {
    document.querySelectorAll(".svc").forEach((c) => new CardFX(c));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
