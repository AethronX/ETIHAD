// Renders each slide's HTML in Chromium at 1920x1080 @2x and writes a PNG.
// Chromium is used rather than a PPTX text layout because the deck is Arabic:
// shaping, RTL bidi and the product's own webfont all have to be exact, and
// rasterising here means the deck looks the same on any machine that opens it.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { CSS } = require('./theme');
const slides = require('./slides');

const DIR = __dirname;
const OUT = path.join(DIR, 'render');
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    args: ['--no-sandbox', '--force-color-profile=srgb', '--font-render-hinting=none'],
  });
  const ctx = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();

  const only = process.argv[2] ? process.argv.slice(2).map(Number) : null;
  for (const s of slides) {
    if (only && !only.includes(s.id)) continue;
    const html = `<!doctype html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
      <style>${CSS}</style></head><body>${s.html()}</body></html>`;
    // Written beside assets/ and shots/ so the relative src paths resolve.
    const file = path.join(DIR, `.page-${String(s.id).padStart(2, '0')}.html`);
    fs.writeFileSync(file, html);
    await page.goto('file://' + file, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(450);
    const png = path.join(OUT, `slide-${String(s.id).padStart(2, '0')}.png`);
    await page.screenshot({ path: png, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    process.stdout.write(`rendered ${path.basename(png)}\n`);
  }
  await browser.close();
})();
