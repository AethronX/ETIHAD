const { chromium } = require('playwright');
const path = require('path');
const dir = '/tmp/claude-0/-home-user-ETIHAD/ce6372e9-d81d-5e65-af91-3b53bb676f1f/scratchpad/site';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 })).newPage();
  await p.goto('file://' + dir + '/index.html', { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(600);
  const secs = await p.$$('section, .stats, footer');
  for (let i = 0; i < secs.length; i++) {
    await secs[i].screenshot({ path: `${dir}/qa-${String(i).padStart(2,'0')}.png` });
  }
  // geometry check: nothing may overflow horizontally, no text clipped
  const issues = await p.evaluate(() => {
    const out = [];
    if (document.documentElement.scrollWidth > window.innerWidth + 1) out.push({ kind: 'h-overflow', w: document.documentElement.scrollWidth });
    document.querySelectorAll('*').forEach(el => {
      if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden')
        out.push({ kind: 'clipped', tag: el.tagName + '.' + el.className, text: (el.textContent||'').trim().slice(0,40) });
      const r = el.getBoundingClientRect();
      if (r.width > 0 && (r.left < -1 || r.right > window.innerWidth + 1))
        out.push({ kind: 'outside', tag: el.tagName + '.' + el.className, l: Math.round(r.left), r: Math.round(r.right) });
    });
    return out;
  });
  console.log('sections:', secs.length);
  console.log('issues:', JSON.stringify(issues.slice(0,10)));
  await b.close();
})();
