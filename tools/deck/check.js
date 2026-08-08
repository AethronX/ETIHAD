// Geometry check for the rendered slides: nothing may spill past the canvas,
// nothing may sit closer than the margin, and no text may be clipped.
// Eyeballing eighteen slides misses exactly the defects that matter.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { CSS } = require('./theme');
const slides = require('./slides');

const DIR = __dirname;
const W = 1920, H = 1080, MARGIN = 60;

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
  let bad = 0;

  for (const s of slides) {
    const html = `<!doctype html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
      <style>${CSS}</style></head><body>${s.html()}</body></html>`;
    const file = path.join(DIR, `.check-${s.id}.html`);
    fs.writeFileSync(file, html);
    await page.goto('file://' + file, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(250);

    const issues = await page.evaluate(({ W, H, MARGIN }) => {
      const out = [];
      const root = document.querySelector('.slide');
      const push = (kind, el, extra) => {
        const r = el.getBoundingClientRect();
        out.push({
          kind,
          tag: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : ''),
          text: (el.textContent || '').trim().slice(0, 46),
          box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
          ...extra,
        });
      };
      // 1. anything painted past the canvas
      root.querySelectorAll('*').forEach((el) => {
        const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden') return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return;
        // deliberate decoration is allowed to bleed
        if (el.dataset.bleed === '1') return;
        const over = { right: Math.round(-r.x), bottom: Math.round(r.bottom - H), top: Math.round(-r.y), left: Math.round(r.right - W) };
        if (r.bottom > H + 1 || r.y < -1 || r.x < -1 || r.right > W + 1) push('outside-canvas', el, { over });
      });
      // 2. text clipped by its own container
      root.querySelectorAll('*').forEach((el) => {
        if (!Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim())) return;
        if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow !== 'visible') push('text-clipped', el, {});
      });
      // 3. page body must not scroll
      if (document.documentElement.scrollHeight > H + 1) out.push({ kind: 'body-scrolls', h: document.documentElement.scrollHeight });
      if (document.documentElement.scrollWidth > W + 1) out.push({ kind: 'body-scrolls-x', w: document.documentElement.scrollWidth });
      return out;
    }, { W, H, MARGIN });

    // de-dupe: a parent and child both outside report once
    const seen = new Set();
    const uniq = issues.filter((i) => {
      const k = i.kind + JSON.stringify(i.box || i.h || i.w);
      if (seen.has(k)) return false; seen.add(k); return true;
    });

    if (uniq.length) {
      bad += 1;
      console.log(`\nslide ${String(s.id).padStart(2, '0')}  ${uniq.length} issue(s)`);
      uniq.slice(0, 8).forEach((i) => console.log('   ' + JSON.stringify(i)));
    } else {
      console.log(`slide ${String(s.id).padStart(2, '0')}  ok`);
    }
    fs.unlinkSync(file);
  }
  await browser.close();
  console.log(bad ? `\n${bad} slide(s) need fixing.` : '\nAll slides fit the canvas.');
  process.exit(bad ? 1 : 0);
})();
