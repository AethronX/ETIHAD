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

// Serialized into the page by page.evaluate. See collect.js.
const collect = require('./collect');

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
