#!/usr/bin/env node
/**
 * Drives the page with a real keyboard and pointer and asserts the
 * interactions that a static budget cannot see.
 *
 *   node tools/audit/behaviour.js               # test ./index.html
 *   node tools/audit/behaviour.js path/to.html
 *
 * Requires Playwright. Set CHROME_PATH if Chromium is not on the default
 * Playwright search path. Exits non-zero if any assertion fails.
 */

const path = require('path');
const { chromium } = require('playwright');

const target = process.argv[2] || path.join(__dirname, '..', '..', 'index.html');
const URL = /^https?:/.test(target) ? target : 'file://' + path.resolve(target);
const EXECUTABLE = process.env.CHROME_PATH || undefined;

let failures = 0;
const assert = (name, pass, note) => {
  if (!pass) failures += 1;
  console.log((pass ? '  ok    ' : '  FAIL  ') + name + (note ? '   ' + note : ''));
};

const dialogOpen = (page, label) => page.evaluate((l) => {
  const sel = l ? `[role="dialog"][aria-label="${l}"]` : '[role="dialog"]';
  return !!Array.from(document.querySelectorAll(sel)).find((d) => d.getBoundingClientRect().width > 0);
}, label);

(async () => {
  const browser = await chromium.launch({ executablePath: EXECUTABLE, args: ['--no-sandbox'] });
  console.log('Behaviour checks for ' + URL + '\n');

  /* ---------------- desktop ---------------- */
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e).split('\n')[0].slice(0, 160)));
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(1500);

  // The skip link must be the first thing a keyboard reaches, and must land
  // focus on the content rather than merely scrolling to it.
  await page.keyboard.press('Tab');
  await page.waitForTimeout(300);
  const first = await page.evaluate(() => {
    const el = document.activeElement;
    const r = el.getBoundingClientRect();
    return { skip: el.hasAttribute('data-skip-link'), onScreen: r.top >= 0 && r.left >= 0 };
  });
  assert('skip link is the first tab stop', first.skip);
  assert('skip link is visible once focused', first.onScreen);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(300);
  const landed = await page.evaluate(() => document.activeElement.id || document.activeElement.tagName);
  assert('skip link moves focus into <main>', landed === 'etihad-main', 'focus=' + landed);

  // Opening an overlay from a control and dismissing it must return focus to
  // that control, not to <body>.
  await page.evaluate(() => {
    const b = document.querySelector('button[aria-label^="الإشعارات"]');
    b.dataset.probe = '1';
    b.focus();
    b.click();
  });
  await page.waitForTimeout(500);
  assert('bell opens the notification dialog', await dialogOpen(page, 'مركز الإشعارات'));
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  assert('Escape returns focus to the bell',
    await page.evaluate(() => document.activeElement && document.activeElement.dataset.probe === '1'));

  // The AI panel used to be pointer-only.
  await page.evaluate(() => document.querySelector('button[aria-label="المساعد الذكي"]').click());
  await page.waitForTimeout(400);
  const aiOpened = await dialogOpen(page, 'المساعد الذكي');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  assert('Escape closes the AI panel', aiOpened && !(await dialogOpen(page, 'المساعد الذكي')));

  // An open modal must contain Tab; aria-modal alone does not.
  await page.keyboard.press('Control+k');
  await page.waitForTimeout(400);
  assert('Ctrl+K opens the command palette', await dialogOpen(page));
  let contained = true;
  for (let i = 0; i < 15; i++) {
    await page.keyboard.press('Tab');
    const inside = await page.evaluate(() => {
      const d = Array.from(document.querySelectorAll('[role="dialog"]')).find((e) => e.getBoundingClientRect().width > 0);
      return d ? d.contains(document.activeElement) : null;
    });
    if (inside === false) contained = false;
  }
  assert('Tab stays inside the open palette', contained);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  assert('Escape closes the palette', !(await dialogOpen(page)));

  // Collapsing the sidebar must hide it from the keyboard; expanding it must
  // hand it back.
  const reachable = () => page.evaluate(() => Array.from(
    document.querySelectorAll('aside[data-nav-panel] button')
  ).filter((b) => getComputedStyle(b).visibility !== 'hidden').length);
  const collapsed = await reachable();
  await page.keyboard.press('Control+b');
  await page.waitForTimeout(600);
  const expanded = await reachable();
  assert('collapsed sidebar is out of the tab order', collapsed === 0, 'reachable=' + collapsed);
  assert('expanded sidebar is back in the tab order', expanded > 20, 'reachable=' + expanded);

  assert('no uncaught page errors', errors.length === 0, errors.join(' | '));

  /* ---------------- mobile drawer ---------------- */
  const mob = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const m = await mob.newPage();
  await m.goto(URL, { waitUntil: 'load' });
  await m.waitForTimeout(1500);
  const mobReach = () => m.evaluate(() => Array.from(
    document.querySelectorAll('aside[data-nav-panel] button')
  ).filter((b) => getComputedStyle(b).visibility !== 'hidden').length);
  const shut = await mobReach();
  await m.evaluate(() => document.querySelector('[data-hamburger]').click());
  await m.waitForTimeout(700);
  const open = await mobReach();
  assert('mobile drawer is out of the tab order when closed', shut === 0, 'reachable=' + shut);
  assert('mobile drawer is reachable when open', open > 20, 'reachable=' + open);

  await browser.close();
  console.log('\n' + (failures ? failures + ' assertion(s) failed.' : 'All behaviour checks passed.'));
  process.exit(failures ? 1 : 0);
})();
