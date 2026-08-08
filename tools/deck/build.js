// Assembles the rendered slides into a 16:9 deck with speaker notes.
//
// Each slide ships as a full-bleed image rather than PowerPoint text boxes.
// That is a deliberate trade: the deck is Arabic, and rasterising in Chromium
// keeps the shaping, the RTL bidi and the product's own webfont identical on
// every machine that opens it — PowerPoint would otherwise substitute fonts
// and reflow the lines. Speaker notes stay real text.
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const slides = require('./slides');

const DIR = __dirname;
const REN = path.join(DIR, 'render');
const OUT = path.join(DIR, 'نظام-اتحاد-عرض-تقديمي.pptx');

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.333in x 7.5in — must precede addSlide
pres.author = 'نظام اتحاد';
pres.company = 'شركة الاتحاد المحدودة';
pres.subject = 'عرض النظام';
pres.title = 'نظام اتحاد — منصة تشغيل تجارة الصين — عُمان';

for (const s of slides) {
  const img = path.join(REN, `slide-${String(s.id).padStart(2, '0')}.png`);
  if (!fs.existsSync(img)) throw new Error('missing render: ' + img);
  const slide = pres.addSlide();
  slide.background = { color: '051C4A' };
  slide.addImage({ path: img, x: 0, y: 0, w: 13.333, h: 7.5 });
  slide.addNotes(s.notes);
}

pres.writeFile({ fileName: OUT }).then(() => {
  const mb = (fs.statSync(OUT).size / 1048576).toFixed(1);
  console.log(`wrote ${path.basename(OUT)}  (${slides.length} slides, ${mb} MB)`);
});
