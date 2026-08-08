const { chromium } = require('playwright');
const path = require('path');
const URL = 'file://' + path.resolve('/home/user/ETIHAD/index.html');
const OUT = '/tmp/claude-0/-home-user-ETIHAD/ce6372e9-d81d-5e65-af91-3b53bb676f1f/scratchpad/deck/shots';

// nav index -> label (order of sidebar buttons)
const NAV = ['dash','tower','analytics','customers','sales','quotes','invoices','po','suppliers',
 'cnoffice','shipping','containers','clearance','loadplan','cnwh','omwh','pickup','inv',
 'acct','docs','landed','reports','notifications','permissions','team','integrations','health','audit','settings','portal'];

async function go(page, id, mobile) {
  const i = NAV.indexOf(id);
  if (mobile) { await page.evaluate(()=>{const h=document.querySelector('[data-hamburger]'); if(h) h.click();}); await page.waitForTimeout(320); }
  await page.evaluate((n)=>{const b=Array.from(document.querySelectorAll('aside[data-nav-panel] nav button')); b[n].click();}, i);
  await page.waitForTimeout(950);
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox','--force-color-profile=srgb'] });

  // ---------- LAPTOP 1600x1000 @2x ----------
  const dctx = await browser.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2 });
  const p = await dctx.newPage();
  await p.goto(URL, { waitUntil: 'load' }); await p.waitForTimeout(1600);
  // open the sidebar so the deck shows the full navigation
  await p.keyboard.press('Control+b'); await p.waitForTimeout(700);

  const desk = [['dash','01-dash'],['tower','02-tower'],['quotes','03-quotes'],['containers','04-containers'],
                ['landed','05-landed'],['cnwh','06-cnwh'],['permissions','07-permissions'],['analytics','08-analytics'],
                ['acct','09-acct'],['portal','10-portal']];
  for (const [id,name] of desk) { await go(p, id, false); await p.screenshot({ path: `${OUT}/d-${name}.png` }); }

  // command palette
  await go(p,'dash',false);
  await p.keyboard.press('Control+k'); await p.waitForTimeout(500);
  await p.keyboard.type('حاوية'); await p.waitForTimeout(600);
  await p.screenshot({ path: `${OUT}/d-11-palette.png` });
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);

  // dark dashboard
  await p.evaluate(()=>{document.body.dataset.theme='dark';}); await p.waitForTimeout(600);
  await p.screenshot({ path: `${OUT}/d-12-dark.png` });
  await dctx.close();

  // ---------- PHONE 390x844 @3x ----------
  const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  const m = await mctx.newPage();
  await m.goto(URL, { waitUntil: 'load' }); await m.waitForTimeout(1600);
  await m.screenshot({ path: `${OUT}/m-01-dash.png` });
  // drawer open
  const ham = await m.evaluate(()=>{const h=document.querySelector('[data-hamburger]');const r=h.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2};});
  await m.touchscreen.tap(ham.x, ham.y); await m.waitForTimeout(800);
  await m.screenshot({ path: `${OUT}/m-02-drawer.png` });
  await m.keyboard.press('Escape'); await m.waitForTimeout(400);
  for (const [id,name] of [['omwh','03-omwh'],['containers','04-containers'],['quotes','05-quotes'],['portal','06-portal']]) {
    await go(m, id, true); await m.screenshot({ path: `${OUT}/m-${name}.png` });
  }
  await m.evaluate(()=>{document.body.dataset.theme='dark';}); await m.waitForTimeout(500);
  await go(m,'cnwh',true); await m.screenshot({ path: `${OUT}/m-07-dark.png` });
  await mctx.close();

  await browser.close();
  console.log('shots done');
})();
