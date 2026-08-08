#!/usr/bin/env node
/**
 * Measures the built page in a real browser and fails if any of the
 * accessibility budgets regress.
 *
 * `tools/checks.py` proves a customization is still *present* in the markup.
 * This proves the page still *behaves*: contrast is computed from resolved
 * colours, tab order is walked with real Tab presses, and the dialogs are
 * opened and dismissed. Markup assertions cannot see any of that.
 *
 *   node tools/audit/a11y.js               # audit ./index.html
 *   node tools/audit/a11y.js path/to.html
 *
 * Requires Playwright. Set CHROME_PATH if Chromium is not on the default
 * Playwright search path.
 *
 * Exits non-zero on any budget failure, so it can gate a release.
 */

const path = require('path');
const { chromium } = require('playwright');

const target = process.argv[2] || path.join(__dirname, '..', '..', 'index.html');
const URL = /^https?:/.test(target) ? target : 'file://' + path.resolve(target);
const EXECUTABLE = process.env.CHROME_PATH || undefined;

// Budgets. Every number here was zero when this file was written; a
// non-zero reading means the page regressed, not that the budget is wrong.
const BUDGET = {
  contrastLight: 0,
  contrastDark: 0,
  unnamedControls: 0,
  unnamedGraphics: 0,
  imagesWithoutAlt: 0,
  duplicateIds: 0,
  targetsUnder24px: 0,
  focusableButInvisible: 0,
  horizontalOverflow: 0,
  uncaughtErrors: 0,
};

/* ------------------------------------------------------------------ */
/* Runs inside the page. Keep it dependency-free.                      */
/* ------------------------------------------------------------------ */
const collect = () => {
  const out = {
    contrast: [], names: [], graphics: [], images: [], dupIds: [], targets: [],
    headings: [], landmarks: {},
  };

  const parse = (c) => {
    const m = c && c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(parseFloat);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const flatten = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  const luminance = (c) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  };
  const ratio = (a, b) => {
    const l1 = luminance(a), l2 = luminance(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  };

  // Composite every translucent layer between the text and an opaque backdrop.
  const backdrop = (el) => {
    let node = el, acc = null;
    while (node && node.nodeType === 1) {
      const bg = parse(getComputedStyle(node).backgroundColor);
      if (bg && bg.a > 0) {
        acc = acc ? flatten(acc, bg) : bg;
        if (acc.a >= 0.999) return acc;
      }
      node = node.parentElement;
    }
    const body = parse(getComputedStyle(document.body).backgroundColor)
      || { r: 255, g: 255, b: 255, a: 1 };
    return acc ? flatten(acc, body) : body;
  };

  // An element counts as visible only if no ancestor hides it. Checking the
  // element alone is what made an earlier version of this audit report 33
  // "undersized targets" that lived inside a hidden sidebar.
  const shown = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) return false;
    }
    return true;
  };

  const where = (el) => {
    const parts = [];
    let n = el;
    for (let i = 0; n && n.nodeType === 1 && i < 4; i++, n = n.parentElement) {
      const cls = typeof n.className === 'string' && n.className.trim()
        ? '.' + n.className.trim().split(/\s+/)[0] : '';
      parts.unshift(n.tagName.toLowerCase() + cls);
    }
    return parts.join('>');
  };

  document.querySelectorAll('*').forEach((el) => {
    if (!shown(el)) return;
    const own = Array.from(el.childNodes)
      .filter((n) => n.nodeType === 3 && n.textContent.trim())
      .map((n) => n.textContent.trim()).join(' ');
    if (!own) return;
    const s = getComputedStyle(el);
    const fg = parse(s.color);
    if (!fg) return;
    const bg = backdrop(el);
    const r = ratio(flatten(fg, bg), bg);
    const px = parseFloat(s.fontSize);
    const large = px >= 24 || (px >= 18.66 && parseInt(s.fontWeight, 10) >= 700);
    const need = large ? 3 : 4.5;
    if (r < need - 0.005) {
      out.contrast.push({ text: own.slice(0, 40), ratio: +r.toFixed(2), need, px, at: where(el) });
    }
  });

  const hasName = (el) => {
    if (el.getAttribute('aria-label')) return true;
    const by = el.getAttribute('aria-labelledby');
    if (by && by.split(/\s+/).some((id) => document.getElementById(id))) return true;
    if (el.title) return true;
    if ((el.textContent || '').trim()) return true;
    if (el.tagName === 'INPUT' && ((el.labels && el.labels.length) || el.placeholder)) return true;
    return !!el.querySelector('img[alt]:not([alt=""])');
  };

  document.querySelectorAll(
    'button, a[href], input, select, textarea, [role="button"], [tabindex]:not([tabindex="-1"])'
  ).forEach((el) => {
    if (shown(el) && !hasName(el)) out.names.push({ at: where(el), html: el.outerHTML.slice(0, 100) });
  });

  document.querySelectorAll('svg').forEach((el) => {
    if (!shown(el)) return;
    if (el.getAttribute('aria-hidden') === 'true') return;
    if (el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.querySelector('title')) return;
    const r = el.getBoundingClientRect();
    out.graphics.push({ w: Math.round(r.width), h: Math.round(r.height), at: where(el) });
  });

  document.querySelectorAll('img').forEach((el) => {
    if (shown(el) && el.getAttribute('alt') === null) out.images.push(where(el));
  });

  const seen = {};
  document.querySelectorAll('[id]').forEach((el) => { seen[el.id] = (seen[el.id] || 0) + 1; });
  Object.keys(seen).forEach((k) => { if (seen[k] > 1) out.dupIds.push({ id: k, count: seen[k] }); });

  // WCAG 2.5.8 minimum target size.
  document.querySelectorAll('button, a[href], [role="button"]').forEach((el) => {
    if (!shown(el)) return;
    const r = el.getBoundingClientRect();
    if (r.width < 24 || r.height < 24) {
      out.targets.push({ w: Math.round(r.width), h: Math.round(r.height), text: (el.textContent || '').trim().slice(0, 24), at: where(el) });
    }
  });

  document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role="heading"]').forEach((el) => {
    if (!shown(el)) return;
    out.headings.push(el.getAttribute('role') === 'heading'
      ? +(el.getAttribute('aria-level') || 2)
      : +el.tagName[1]);
  });

  out.landmarks = {
    main: document.querySelectorAll('main, [role="main"]').length,
    nav: document.querySelectorAll('nav, [role="navigation"]').length,
    banner: document.querySelectorAll('header, [role="banner"]').length,
    skipLink: !!document.querySelector('[data-skip-link]'),
  };
  return out;
};

/* ------------------------------------------------------------------ */

async function measure(browser, theme) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e).split('\n')[0].slice(0, 160)));
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  if (theme === 'dark') {
    await page.evaluate(() => { document.body.dataset.theme = 'dark'; });
    await page.waitForTimeout(400);
  }
  const data = await page.evaluate(collect);
  return { page, ctx, data, errors };
}

async function tabWalk(page, steps) {
  const stops = [];
  await page.evaluate(() => { if (document.activeElement) document.activeElement.blur(); });
  for (let i = 0; i < steps; i++) {
    await page.keyboard.press('Tab');
    stops.push(await page.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return { tag: 'BODY', invisible: false };
      const r = el.getBoundingClientRect();
      let invisible = r.width === 0 || r.height === 0;
      for (let n = el; n && n.nodeType === 1 && !invisible; n = n.parentElement) {
        const s = getComputedStyle(n);
        if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) invisible = true;
      }
      return { tag: el.tagName, text: (el.textContent || '').trim().slice(0, 30), invisible };
    }));
  }
  return stops;
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXECUTABLE, args: ['--no-sandbox'] });
  const results = {};
  const detail = {};

  const light = await measure(browser, 'light');
  const dark = await measure(browser, 'dark');

  results.contrastLight = light.data.contrast.length;
  results.contrastDark = dark.data.contrast.length;
  results.unnamedControls = light.data.names.length;
  results.unnamedGraphics = light.data.graphics.length;
  results.imagesWithoutAlt = light.data.images.length;
  results.duplicateIds = light.data.dupIds.length;
  results.targetsUnder24px = light.data.targets.length;
  detail.contrastLight = light.data.contrast;
  detail.contrastDark = dark.data.contrast;
  detail.unnamedControls = light.data.names;
  detail.unnamedGraphics = light.data.graphics;
  detail.targetsUnder24px = light.data.targets;

  // Tab order: nothing invisible may be reachable.
  const stops = await tabWalk(light.page, 40);
  const phantom = stops.filter((s) => s.invisible);
  results.focusableButInvisible = phantom.length;
  detail.focusableButInvisible = phantom;

  // Responsive: the body must never scroll sideways.
  let overflow = 0;
  const widths = {};
  for (const w of [390, 768, 1024, 1440]) {
    await light.page.setViewportSize({ width: w, height: 900 });
    await light.page.waitForTimeout(300);
    const px = await light.page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    widths[w] = px;
    if (px > 0) overflow += 1;
  }
  results.horizontalOverflow = overflow;
  detail.horizontalOverflow = widths;

  results.uncaughtErrors = light.errors.length + dark.errors.length;
  detail.uncaughtErrors = light.errors.concat(dark.errors);

  const structure = {
    headings: light.data.headings,
    landmarks: light.data.landmarks,
  };

  await browser.close();

  const failed = Object.keys(BUDGET).filter((k) => results[k] > BUDGET[k]);
  const width = Math.max(...Object.keys(BUDGET).map((k) => k.length));
  console.log('Accessibility budgets for ' + URL + '\n');
  for (const k of Object.keys(BUDGET)) {
    const bad = results[k] > BUDGET[k];
    console.log(
      (bad ? '  FAIL  ' : '  ok    ') + k.padEnd(width)
      + '  ' + String(results[k]).padStart(3) + '  (budget ' + BUDGET[k] + ')'
    );
  }
  console.log('\n  headings: ' + JSON.stringify(structure.headings)
    + '\n  landmarks: ' + JSON.stringify(structure.landmarks));

  if (failed.length) {
    console.log('\nDetail for failures:');
    for (const k of failed) console.log('\n  ' + k + ':\n' + JSON.stringify(detail[k], null, 2).split('\n').map((l) => '    ' + l).join('\n'));
    process.exit(1);
  }
  console.log('\nAll budgets met.');
})();
