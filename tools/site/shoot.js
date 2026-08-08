const { chromium } = require('playwright');
const path = require('path');
const URL = 'file://' + path.resolve('/tmp/claude-0/-home-user-ETIHAD/ce6372e9-d81d-5e65-af91-3b53bb676f1f/scratchpad/site/index.html');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox','--force-color-profile=srgb'] });
  const p = await (await b.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 })).newPage();
  await p.goto(URL, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(700);
  const h = await p.evaluate(() => document.body.scrollHeight);
  console.log('page height', h);
  await p.screenshot({ path: path.join(path.dirname(URL.replace('file://','')), 'home-desktop.png'), fullPage: true });
  await p.screenshot({ path: path.join(path.dirname(URL.replace('file://','')), 'home-fold.png') });
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log('horizontal overflow', overflow);
  await b.close();
})();
