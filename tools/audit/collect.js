/**
 * The in-page measurement pass, shared by a11y.js (one page, budgets) and
 * pages.js (every page, every theme, two viewports).
 *
 * Runs inside the browser via page.evaluate, so it must stay dependency-free
 * and must not close over anything from Node.
 */

module.exports = function collect() {
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

  // Every colour stop in a gradient, so text over one can be scored against
  // the stop that suits it least. Without this the audit walks straight past
  // a gradient hero to the page background and reports readable white text as
  // a 1.05:1 failure.
  const gradientStops = (image) => {
    if (!image || image === 'none') return [];
    return (image.match(/rgba?\([^)]+\)/g) || [])
      .map(parse).filter((c) => c && c.a > 0);
  };

  // Composite every translucent layer between the text and an opaque backdrop.
  // Returns the list of candidate backdrops -- more than one when a gradient
  // is involved.
  const backdrops = (el) => {
    let node = el, acc = null;
    while (node && node.nodeType === 1) {
      const style = getComputedStyle(node);
      const stops = gradientStops(style.backgroundImage);
      if (stops.length) {
        return stops.map((s) => (acc ? flatten(acc, s) : s));
      }
      const bg = parse(style.backgroundColor);
      if (bg && bg.a > 0) {
        acc = acc ? flatten(acc, bg) : bg;
        if (acc.a >= 0.999) return [acc];
      }
      node = node.parentElement;
    }
    const body = parse(getComputedStyle(document.body).backgroundColor)
      || { r: 255, g: 255, b: 255, a: 1 };
    return [acc ? flatten(acc, body) : body];
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
    // Worst stop wins: text over a gradient has to stay legible along all of it.
    const r = Math.min(...backdrops(el).map((bg) => ratio(flatten(fg, bg), bg)));
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
}
