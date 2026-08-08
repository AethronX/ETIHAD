#!/usr/bin/env node
/**
 * Walks every page in both themes at a phone and a desktop width, and fails
 * if any of them reports a defect.
 *
 * a11y.js measures the dashboard in its default state. That is one page out of
 * thirty, in one of two themes, with nothing selected -- and defects hide in
 * all three of those gaps:
 *
 *   - `--p` as text failed only once a tab, column, view, role or workspace
 *     was *selected*; the default view has nothing selected, so it read clean.
 *   - The bottom-nav label only exists below 1081px, so a desktop-width audit
 *     never saw it.
 *   - The SLA countdown, the permissions matrix, the rack map and both range
 *     sliders live on pages the dashboard never links to directly.
 *
 * Each of those measured zero on the dashboard and non-zero here.
 *
 *   node tools/audit/pages.js               # audit ./index.html
 *   node tools/audit/pages.js path/to.html
 *
 * Requires Playwright. Set CHROME_PATH if Chromium is not on the default
 * Playwright search path. Exits non-zero if anything is found.
 */

const path = require('path');
const { chromium } = require('playwright');
const collect = require('./collect');

const target = process.argv[2] || path.join(__dirname, '..', '..', 'index.html');
const URL = /^https?:/.test(target) ? target : 'file://' + path.resolve(target);
const EXECUTABLE = process.env.CHROME_PATH || undefined;

const VIEWPORTS = [
  { label: '390px', width: 390, height: 844, mobile: true },
  { label: '1440px', width: 1440, height: 900, mobile: false },
];

async function sweep(browser, theme, vp) {
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    isMobile: vp.mobile,
    hasTouch: vp.mobile,
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e).split('\n')[0].slice(0, 160)));
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(1400);
  if (theme === 'dark') {
    await page.evaluate(() => { document.body.dataset.theme = 'dark'; });
    await page.waitForTimeout(350);
  }

  const findings = [];
  let visited = 0;
  for (;;) {
    // On a phone the nav lives behind the drawer, so it has to be opened
    // before each hop.
    if (vp.mobile) {
      await page.evaluate(() => {
        const h = document.querySelector('[data-hamburger]');
        if (h) h.click();
      });
      await page.waitForTimeout(320);
    }
    const moved = await page.evaluate((i) => {
      const items = Array.from(document.querySelectorAll('aside[data-nav-panel] nav button'));
      if (i >= items.length) return false;
      items[i].click();
      return true;
    }, visited);
    if (!moved) break;
    await page.waitForTimeout(700);

    const title = await page.evaluate(() => {
      const h = document.querySelector('main h1');
      return h ? h.textContent.trim().slice(0, 40) : '(untitled)';
    });
    const data = await page.evaluate(collect);
    const add = (kind, list) => list.forEach((item) => findings.push({ theme, vp: vp.label, page: title, kind, item }));
    add('contrast', data.contrast);
    add('unnamed control', data.names);
    add('unnamed graphic', data.graphics);
    add('image without alt', data.images.map((at) => ({ at })));
    add('target under 24px', data.targets);
    visited += 1;
  }

  errors.forEach((e) => findings.push({ theme, vp: vp.label, page: '-', kind: 'page error', item: { message: e } }));
  await ctx.close();
  return { visited, findings };
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXECUTABLE, args: ['--no-sandbox'] });
  console.log('Full-site sweep of ' + URL + '\n');

  const all = [];
  for (const theme of ['light', 'dark']) {
    for (const vp of VIEWPORTS) {
      const { visited, findings } = await sweep(browser, theme, vp);
      all.push(...findings);
      const mark = findings.length ? 'FAIL' : ' ok ';
      console.log(`  ${mark}  ${theme.padEnd(5)} ${vp.label.padEnd(7)} ${String(visited).padStart(2)} pages   ${findings.length} finding(s)`);
    }
  }
  await browser.close();

  if (!all.length) {
    console.log('\nNo findings across every page, both themes, both widths.');
    return;
  }

  // Collapse the repeats: one shape recurring on twenty list pages is one bug.
  const seen = new Map();
  for (const f of all) {
    const key = f.kind + '|' + JSON.stringify(f.item);
    if (!seen.has(key)) seen.set(key, { ...f, count: 0, pages: new Set() });
    const entry = seen.get(key);
    entry.count += 1;
    entry.pages.add(f.page);
  }
  console.log('\n' + all.length + ' finding(s), ' + seen.size + ' distinct:\n');
  for (const e of seen.values()) {
    console.log(`  [${e.kind}] x${e.count}  ${e.theme}/${e.vp}  on: ${[...e.pages].slice(0, 3).join(', ')}`);
    console.log('      ' + JSON.stringify(e.item));
  }
  process.exit(1);
})();
