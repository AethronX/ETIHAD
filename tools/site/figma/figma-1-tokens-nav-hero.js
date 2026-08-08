// ============================================================
// Figma builder — script 1 of 3
// Variables + page frame + nav + hero
// Run with: use_figma  fileKey=covsf7EBCH4DGpcCjbZiMS
// ============================================================
// Font note: the product uses IBM Plex Sans Arabic, which Figma does not
// carry. Cairo is the closest available Arabic family with the weight range
// this design needs (Regular / Medium / SemiBold / Bold).

const F = 'Cairo';
const NUM = 'Inter';
await Promise.all([
  figma.loadFontAsync({ family: F, style: 'Regular' }),
  figma.loadFontAsync({ family: F, style: 'Medium' }),
  figma.loadFontAsync({ family: F, style: 'SemiBold' }),
  figma.loadFontAsync({ family: F, style: 'Bold' }),
  figma.loadFontAsync({ family: NUM, style: 'Regular' }),
  figma.loadFontAsync({ family: NUM, style: 'Bold' }),
]);

const hex = (h) => {
  h = h.replace('#', '');
  return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 };
};
const solid = (h, opacity) => opacity === undefined
  ? [{ type: 'SOLID', color: hex(h) }]
  : [{ type: 'SOLID', color: hex(h), opacity }];

const P = {
  navy: '#051C4A', navy2: '#0A2A63', blue: '#0F4C81', cyan: '#00B8D9',
  orange: '#F7931E', green: '#16A34A', red: '#DC2626',
  ink: '#111827', body: '#374151', muted: '#6B7280', line: '#E7EBF0',
  bg: '#F6F8FB', card: '#FFFFFF',
};

// ---------- design tokens as variables ----------
const col = figma.variables.createVariableCollection('اتحاد — الرموز');
const mode = col.modes[0].modeId;
const mkColor = (name, h, scopes) => {
  const v = figma.variables.createVariable(name, col, 'COLOR');
  v.scopes = scopes;
  v.setValueForMode(mode, hex(h));
  return v;
};
const fillScopes = ['FRAME_FILL', 'SHAPE_FILL'];
const textScopes = ['TEXT_FILL'];
const vars = {
  navy: mkColor('لون/كحلي-العلامة', P.navy, fillScopes),
  blue: mkColor('لون/أزرق-أساسي', P.blue, fillScopes),
  cyan: mkColor('لون/سماوي', P.cyan, fillScopes),
  orange: mkColor('لون/برتقالي', P.orange, fillScopes),
  bg: mkColor('لون/خلفية', P.bg, fillScopes),
  card: mkColor('لون/بطاقة', P.card, fillScopes),
  line: mkColor('لون/حد', P.line, fillScopes),
  ink: mkColor('نص/أساسي', P.ink, textScopes),
  body: mkColor('نص/متن', P.body, textScopes),
  muted: mkColor('نص/خافت', P.muted, textScopes),
};

// ---------- helpers ----------
const T = (chars, { size = 16, weight = 'Regular', color = P.ink, width, lh = 1.6, family = F, align = 'RIGHT', spacing } = {}) => {
  const t = figma.createText();
  t.fontName = { family, style: weight };
  t.characters = chars;
  t.fontSize = size;
  t.fills = solid(color);
  t.textAlignHorizontal = align;
  t.lineHeight = { unit: 'PERCENT', value: Math.round(lh * 100) };
  if (spacing !== undefined) t.letterSpacing = { unit: 'PERCENT', value: spacing };
  if (width) { t.textAutoResize = 'HEIGHT'; t.resize(width, t.height); }
  else t.textAutoResize = 'WIDTH_AND_HEIGHT';
  return t;
};
const Row = (props = {}) => figma.createAutoLayout('HORIZONTAL', Object.assign({ counterAxisAlignItems: 'CENTER' }, props));
const Col = (props = {}) => figma.createAutoLayout('VERTICAL', props);

const created = [];

// ---------- page frame ----------
const page = Col({ name: 'الصفحة الرئيسية — سطح المكتب', itemSpacing: 0 });
page.x = 200; page.y = 200;
page.fills = solid(P.card);
page.resize(1440, 100);
page.layoutSizingHorizontal = 'FIXED';
page.layoutSizingVertical = 'HUG';
figma.currentPage.appendChild(page);
created.push(page.id);

// A section shell: full-bleed band with a 1200px centred content column.
const Section = (name, { bg = P.card, padY = 104 } = {}) => {
  const band = Col({ name, itemSpacing: 0, counterAxisAlignItems: 'CENTER' });
  band.fills = solid(bg);
  page.appendChild(band);
  band.layoutSizingHorizontal = 'FILL';
  band.layoutSizingVertical = 'HUG';
  band.paddingTop = padY; band.paddingBottom = padY;
  band.paddingLeft = 120; band.paddingRight = 120;
  const inner = Col({ name: 'المحتوى', itemSpacing: 0 });
  inner.fills = [];
  band.appendChild(inner);
  inner.resize(1200, 10);
  inner.layoutSizingHorizontal = 'FIXED';
  inner.layoutSizingVertical = 'HUG';
  return { band, inner };
};

// ---------- NAV ----------
{
  const { band, inner } = Section('شريط التنقّل', { padY: 0 });
  band.paddingTop = 19; band.paddingBottom = 19;
  band.strokes = solid(P.line); band.strokeBottomWeight = 1; band.strokeAlign = 'INSIDE';
  const bar = Row({ name: 'المحتوى', itemSpacing: 44 });
  bar.fills = [];
  inner.appendChild(bar);
  bar.layoutSizingHorizontal = 'FILL';
  bar.layoutSizingVertical = 'HUG';

  const brand = Row({ name: 'العلامة', itemSpacing: 13 });
  brand.fills = [];
  const mark = figma.createFrame();
  mark.name = 'شعار اتحاد — ضع صورة الشعار هنا';
  mark.resize(28, 40);
  mark.fills = solid(P.navy, 0.12);
  mark.cornerRadius = 6;
  brand.appendChild(mark);
  const bt = Col({ itemSpacing: 2 }); bt.fills = [];
  bt.appendChild(T('اتحاد', { size: 21, weight: 'Bold', lh: 1.1 }));
  bt.appendChild(T('CHINA — OMAN ERP', { size: 9.5, color: P.muted, family: NUM, align: 'LEFT', spacing: 15 }));
  brand.appendChild(bt);
  bar.appendChild(brand);

  const links = Row({ name: 'الروابط', itemSpacing: 34 }); links.fills = [];
  ['الميزات', 'كيف يعمل', 'الأقسام', 'الأدوار', 'الأسعار']
    .forEach((l) => links.appendChild(T(l, { size: 15.5, weight: 'Medium', color: P.body })));
  bar.appendChild(links);

  const spacer = figma.createFrame(); spacer.fills = []; spacer.name = 'فراغ';
  bar.appendChild(spacer); spacer.layoutSizingHorizontal = 'FILL'; spacer.resize(10, 1);

  const Btn = (label, kind) => {
    const b = Row({ name: 'زر/' + label, itemSpacing: 8 });
    b.paddingLeft = 22; b.paddingRight = 22; b.paddingTop = 13; b.paddingBottom = 13;
    b.cornerRadius = 12; b.primaryAxisAlignItems = 'CENTER';
    if (kind === 'p') { b.fills = solid(P.blue); b.appendChild(T(label, { size: 15.5, weight: 'SemiBold', color: '#FFFFFF' })); }
    else { b.fills = []; b.strokes = solid(P.line); b.strokeWeight = 1; b.appendChild(T(label, { size: 15.5, weight: 'SemiBold', color: P.ink })); }
    return b;
  };
  const actions = Row({ itemSpacing: 12 }); actions.fills = [];
  actions.appendChild(Btn('تسجيل الدخول', 'g'));
  actions.appendChild(Btn('اطلب عرضاً حيّاً', 'p'));
  bar.appendChild(actions);
}

// ---------- HERO ----------
{
  const { band, inner } = Section('البطل', { bg: P.navy, padY: 0 });
  band.paddingTop = 96; band.paddingBottom = 0;
  inner.itemSpacing = 0;

  const kick = Row({ name: 'شارة', itemSpacing: 10 });
  kick.paddingLeft = 18; kick.paddingRight = 18; kick.paddingTop = 8; kick.paddingBottom = 8;
  kick.cornerRadius = 999;
  kick.fills = solid(P.cyan, 0.14);
  kick.strokes = solid(P.cyan, 0.26); kick.strokeWeight = 1;
  kick.appendChild(T('منصّة التشغيل الموحّدة لتجارة الصين — عُمان', { size: 14, weight: 'SemiBold', color: '#7FE3F5', spacing: 5 }));
  inner.appendChild(kick);
  kick.layoutSizingHorizontal = 'HUG';

  const h1 = T('كل شحنة من قوانزو إلى نزوى،\nفي نظام واحد', { size: 62, weight: 'Bold', color: '#FFFFFF', width: 820, lh: 1.16 });
  inner.appendChild(h1);
  h1.y = 0;
  const lead = T('من طلب التسعير حتى تسليم العميل — مسار واحد متصل يعرف من عليه الدور الآن، ويحسب التكلفة الواصلة فعلياً، ويعمل بالعربية على الحاسب والهاتف.',
    { size: 21, color: '#C3D0E4', width: 680, lh: 1.75 });
  inner.appendChild(lead);

  const HBtn = (label, filled) => {
    const b = Row({ name: 'زر/' + label });
    b.paddingLeft = 30; b.paddingRight = 30; b.paddingTop = 16; b.paddingBottom = 16;
    b.cornerRadius = 12; b.primaryAxisAlignItems = 'CENTER';
    if (filled) { b.fills = solid('#FFFFFF'); b.appendChild(T(label, { size: 16.5, weight: 'SemiBold', color: P.navy })); }
    else { b.fills = []; b.strokes = solid('#FFFFFF', 0.32); b.strokeWeight = 1; b.appendChild(T(label, { size: 16.5, weight: 'SemiBold', color: '#FFFFFF' })); }
    return b;
  };
  const ctas = Row({ name: 'أزرار', itemSpacing: 14 }); ctas.fills = [];
  ctas.appendChild(HBtn('اطلب عرضاً حيّاً', true));
  ctas.appendChild(HBtn('شاهد جولة الدقيقتين', false));
  inner.appendChild(ctas);

  const trust = Row({ name: 'أرقام الثقة', itemSpacing: 30 }); trust.fills = [];
  [['٣٠', 'شاشة عمل'], ['٩', 'أدوار وظيفية'], ['بوابة', 'خاصة للعميل'], ['بلا', 'تطبيق يُثبَّت']]
    .forEach(([b, l]) => {
      const r = Row({ itemSpacing: 6 }); r.fills = [];
      r.appendChild(T(b, { size: 14.5, weight: 'SemiBold', color: '#FFFFFF' }));
      r.appendChild(T(l, { size: 14.5, color: '#93A6C4' }));
      trust.appendChild(r);
    });
  inner.appendChild(trust);

  // product screenshot placeholder — replace the fill with the dashboard PNG
  const shotWrap = Col({ name: 'لقطة المنتج' });
  shotWrap.fills = solid('#0B1220');
  shotWrap.paddingLeft = 12; shotWrap.paddingRight = 12; shotWrap.paddingTop = 12; shotWrap.paddingBottom = 0;
  shotWrap.topLeftRadius = 18; shotWrap.topRightRadius = 18;
  shotWrap.effects = [{ type: 'DROP_SHADOW', color: { r: 0.02, g: 0.11, b: 0.29, a: 0.35 }, offset: { x: 0, y: 30 }, radius: 70, spread: 0, visible: true, blendMode: 'NORMAL' }];
  inner.appendChild(shotWrap);
  shotWrap.layoutSizingHorizontal = 'FILL';
  const shot = figma.createFrame();
  shot.name = 'ضع هنا لقطة لوحة التحكم (d-01-dash.png)';
  shot.fills = solid('#152238');
  shot.topLeftRadius = 10; shot.topRightRadius = 10;
  shotWrap.appendChild(shot);
  shot.layoutSizingHorizontal = 'FILL';
  shot.resize(shot.width, 700);
  const hint = T('لقطة لوحة التحكم', { size: 18, color: '#5A7196', align: 'CENTER' });
  shot.appendChild(hint);
  hint.x = 40; hint.y = 40;

  // spacing between hero children
  inner.itemSpacing = 0;
  h1.parent.children.forEach(() => {});
  inner.itemSpacing = 26;
}

return {
  createdNodeIds: created,
  pageFrameId: page.id,
  variableCollectionId: col.id,
  note: 'Sections built: nav, hero. Run script 2 next.',
};
