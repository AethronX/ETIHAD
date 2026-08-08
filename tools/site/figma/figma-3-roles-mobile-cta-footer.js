// ============================================================
// Figma builder — script 3 of 3
// Roles + mobile + CTA band + footer
// Requires script 1. Pass the page frame id it returned.
// ============================================================
const PAGE_FRAME_ID = 'PASTE_pageFrameId_FROM_SCRIPT_1';

const F = 'Cairo', NUM = 'Inter';
await Promise.all([
  figma.loadFontAsync({ family: F, style: 'Regular' }),
  figma.loadFontAsync({ family: F, style: 'Medium' }),
  figma.loadFontAsync({ family: F, style: 'SemiBold' }),
  figma.loadFontAsync({ family: F, style: 'Bold' }),
  figma.loadFontAsync({ family: NUM, style: 'Regular' }),
]);

const hex = (h) => { h = h.replace('#',''); return { r: parseInt(h.slice(0,2),16)/255, g: parseInt(h.slice(2,4),16)/255, b: parseInt(h.slice(4,6),16)/255 }; };
const solid = (h, o) => o === undefined ? [{ type:'SOLID', color: hex(h) }] : [{ type:'SOLID', color: hex(h), opacity:o }];
const P = { navy:'#051C4A', navy2:'#0A2A63', blue:'#0F4C81', cyan:'#00B8D9', orange:'#F7931E',
  green:'#16A34A', ink:'#111827', body:'#374151', muted:'#6B7280', line:'#E7EBF0',
  bg:'#F6F8FB', card:'#FFFFFF' };

const T = (chars, { size=16, weight='Regular', color=P.ink, width, lh=1.6, family=F, align='RIGHT', spacing } = {}) => {
  const t = figma.createText();
  t.fontName = { family, style: weight };
  t.characters = chars; t.fontSize = size; t.fills = solid(color);
  t.textAlignHorizontal = align;
  t.lineHeight = { unit:'PERCENT', value: Math.round(lh*100) };
  if (spacing !== undefined) t.letterSpacing = { unit:'PERCENT', value: spacing };
  if (width) { t.textAutoResize = 'HEIGHT'; t.resize(width, t.height); } else t.textAutoResize = 'WIDTH_AND_HEIGHT';
  return t;
};
const Row = (p={}) => figma.createAutoLayout('HORIZONTAL', Object.assign({ counterAxisAlignItems:'CENTER' }, p));
const Col = (p={}) => figma.createAutoLayout('VERTICAL', p);

const page = await figma.getNodeByIdAsync(PAGE_FRAME_ID);
if (!page) throw new Error('page frame not found — check PAGE_FRAME_ID');
const created = [];

const Section = (name, { bg = P.card, padY = 104 } = {}) => {
  const band = Col({ name, itemSpacing: 0, counterAxisAlignItems: 'CENTER' });
  band.fills = solid(bg);
  page.appendChild(band);
  band.layoutSizingHorizontal = 'FILL'; band.layoutSizingVertical = 'HUG';
  band.paddingTop = padY; band.paddingBottom = padY; band.paddingLeft = 120; band.paddingRight = 120;
  const inner = Col({ name: 'المحتوى', itemSpacing: 0 });
  inner.fills = []; band.appendChild(inner);
  inner.resize(1200, 10);
  inner.layoutSizingHorizontal = 'FIXED'; inner.layoutSizingVertical = 'HUG';
  created.push(band.id);
  return { band, inner };
};

// ---------- ROLES ----------
{
  const { inner } = Section('الأدوار');
  const h = Col({ itemSpacing: 16 }); h.fills = []; inner.appendChild(h);
  h.resize(760, 10); h.layoutSizingHorizontal = 'FIXED'; h.layoutSizingVertical = 'HUG';
  h.appendChild(T('تسجيل الدخول', { size: 14, weight: 'SemiBold', color: P.blue, spacing: 14 }));
  h.appendChild(T('كل موظف يدخل فيجد نظامه هو', { size: 42, weight: 'Bold', width: 720, lh: 1.24 }));
  h.appendChild(T('الدور لا يغيّر الصلاحيات فقط — يغيّر القائمة والشاشة الأولى والأرقام المعروضة. الموظف لا يرى ما لا يخصّه، فلا يضيع فيه ولا يطّلع عليه.',
    { size: 18, color: P.body, width: 720, lh: 1.75 }));

  const grid = Col({ itemSpacing: 18 }); grid.fills = []; inner.appendChild(grid);
  grid.layoutSizingHorizontal = 'FILL'; grid.layoutSizingVertical = 'HUG';
  grid.paddingTop = 52;
  const roles = [
    ['مدير النظام','وصول كامل غير مقيّد، بما في ذلك الإعدادات وسجل التدقيق',P.navy],
    ['المدير العام','قراءة كل شيء، واعتماد ما يتجاوز حدود الصلاحية المالية',P.navy2],
    ['موظف مبيعات','عملاؤه وعروضه فقط — لا يرى تكلفة المورد الأصلية',P.blue],
    ['محاسب','الفواتير والمدفوعات والمصروفات وكل التقارير المالية',P.blue],
    ['موظف مكتب الصين','الموردون والتسعير وأوامر الشراء — لا يرى سعر البيع',P.cyan],
    ['مدير مستودع الصين','الاستلام والباركود والتخزين وتحميل الحاويات',P.cyan],
    ['مدير مستودع عُمان','الاستلام والفحص والمخزون وطابور الاستلام في نزوى',P.green],
    ['مسؤول التخليص','البيان الجمركي والرسوم ومستندات الحاوية عند الميناء',P.orange],
    ['عامل مستودع','مسح الباركود وتحريك المخزون وتسليم العميل فقط',P.muted],
  ];
  for (let r = 0; r < 3; r++) {
    const line = Row({ itemSpacing: 18 }); line.fills = []; line.counterAxisAlignItems = 'MIN';
    grid.appendChild(line);
    line.layoutSizingHorizontal = 'FILL'; line.layoutSizingVertical = 'HUG';
    for (let i = 0; i < 3; i++) {
      const [t, d, c] = roles[r * 3 + i];
      const card = Row({ itemSpacing: 14 });
      card.counterAxisAlignItems = 'MIN';
      card.fills = solid(P.card); card.strokes = solid(P.line); card.strokeWeight = 1;
      card.cornerRadius = 20;
      card.paddingTop = 24; card.paddingBottom = 24; card.paddingLeft = 26; card.paddingRight = 26;
      line.appendChild(card);
      card.layoutSizingHorizontal = 'FILL'; card.layoutSizingVertical = 'HUG';
      const sw = figma.createFrame(); sw.name = 'لون'; sw.resize(34, 34); sw.cornerRadius = 10; sw.fills = solid(c);
      card.appendChild(sw);
      const col = Col({ itemSpacing: 6 }); col.fills = [];
      card.appendChild(col); col.layoutSizingHorizontal = 'FILL'; col.layoutSizingVertical = 'HUG';
      col.appendChild(T(t, { size: 17.5, weight: 'SemiBold' }));
      const dd = T(d, { size: 14, color: P.muted, lh: 1.65 });
      col.appendChild(dd); dd.layoutSizingHorizontal = 'FILL';
    }
  }
}

// ---------- MOBILE ----------
{
  const { inner } = Section('على الهاتف', { bg: P.navy });
  const row = Row({ itemSpacing: 64 }); row.fills = []; row.counterAxisAlignItems = 'CENTER';
  inner.appendChild(row);
  row.layoutSizingHorizontal = 'FILL'; row.layoutSizingVertical = 'HUG';

  const left = Col({ itemSpacing: 16 }); left.fills = [];
  row.appendChild(left); left.layoutSizingHorizontal = 'FILL'; left.layoutSizingVertical = 'HUG';
  left.appendChild(T('في الميدان', { size: 14, weight: 'SemiBold', color: '#7FE3F5', spacing: 14 }));
  const t2 = T('النظام نفسه في الجيب — لا نسخة مختصرة', { size: 42, weight: 'Bold', color: '#FFFFFF', lh: 1.24 });
  left.appendChild(t2); t2.layoutSizingHorizontal = 'FILL';
  const s2 = T('الثلاثون شاشة كلها تعمل على الهاتف. الجداول تتحوّل إلى بطاقات مقروءة، والقائمة إلى درج جانبي، وشريط سفلي يضع أكثر خمس شاشات استعمالاً تحت الإبهام.',
    { size: 18, color: '#C3D0E4', lh: 1.75 });
  left.appendChild(s2); s2.layoutSizingHorizontal = 'FILL';
  const chips = Row({ itemSpacing: 12 }); chips.fills = []; left.appendChild(chips);
  [['صفر تمرير أفقي', true], ['أهداف لمس ≥ ٢٤ بكسل', false], ['يعمل بالمتصفّح فقط', false]]
    .forEach(([label, cy]) => {
      const ch = Row(); ch.cornerRadius = 999;
      ch.paddingLeft = 18; ch.paddingRight = 18; ch.paddingTop = 9; ch.paddingBottom = 9;
      ch.fills = cy ? solid(P.cyan, 0.18) : solid('#FFFFFF', 0.10);
      ch.appendChild(T(label, { size: 14.5, weight: 'SemiBold', color: cy ? '#7FE3F5' : '#FFFFFF' }));
      chips.appendChild(ch);
    });

  const phones = Row({ itemSpacing: 26 }); phones.fills = []; row.appendChild(phones);
  ['لقطة الهاتف — لوحة التحكم (m-01-dash.png)', 'لقطة الهاتف — القائمة الجانبية (m-02-drawer.png)']
    .forEach((name) => {
      const shell = Col(); shell.name = name;
      shell.fills = solid('#0B1220'); shell.cornerRadius = 34;
      shell.paddingTop = 9; shell.paddingBottom = 9; shell.paddingLeft = 9; shell.paddingRight = 9;
      shell.effects = [{ type:'DROP_SHADOW', color:{r:0.02,g:0.11,b:0.29,a:0.30}, offset:{x:0,y:24}, radius:60, spread:0, visible:true, blendMode:'NORMAL' }];
      phones.appendChild(shell);
      const scr = figma.createFrame(); scr.name = 'ضع اللقطة هنا';
      scr.resize(220, 476); scr.cornerRadius = 26; scr.fills = solid('#152238');
      shell.appendChild(scr);
    });
}

// ---------- CTA BAND ----------
{
  const { band, inner } = Section('نداء الإجراء', { bg: P.blue, padY: 92 });
  inner.itemSpacing = 18; inner.counterAxisAlignItems = 'CENTER';
  const t = T('ابدأ بشحنة واحدة — عرض سعر حقيقي يمشي حتى التسليم',
    { size: 44, weight: 'Bold', color: '#FFFFFF', width: 840, lh: 1.24, align: 'CENTER' });
  inner.appendChild(t);
  const p = T('نهيّئ العملاء والموردين والأدوار، ثم نشغّل شحنة داخل النظام وخارجه معاً للمقارنة. القرار بعدها لكم.',
    { size: 19, color: '#C3D0E4', width: 640, lh: 1.7, align: 'CENTER' });
  inner.appendChild(p);
  const ctas = Row({ itemSpacing: 14 }); ctas.fills = []; inner.appendChild(ctas);
  ctas.paddingTop = 18;
  [['احجز عرضاً حيّاً', true], ['تحدّث إلينا', false]].forEach(([label, filled]) => {
    const b = Row(); b.cornerRadius = 12;
    b.paddingLeft = 32; b.paddingRight = 32; b.paddingTop = 17; b.paddingBottom = 17;
    if (filled) { b.fills = solid('#FFFFFF'); b.appendChild(T(label, { size: 17, weight: 'SemiBold', color: P.navy })); }
    else { b.fills = []; b.strokes = solid('#FFFFFF', 0.32); b.strokeWeight = 1; b.appendChild(T(label, { size: 17, weight: 'SemiBold', color: '#FFFFFF' })); }
    ctas.appendChild(b);
  });
}

// ---------- FOOTER ----------
{
  const { inner } = Section('التذييل', { bg: P.navy, padY: 64 });
  const row = Row({ itemSpacing: 80 }); row.fills = []; row.counterAxisAlignItems = 'MIN';
  inner.appendChild(row);
  row.layoutSizingHorizontal = 'FILL'; row.layoutSizingVertical = 'HUG';

  const brandCol = Col({ itemSpacing: 18 }); brandCol.fills = [];
  row.appendChild(brandCol); brandCol.layoutSizingHorizontal = 'FILL'; brandCol.layoutSizingVertical = 'HUG';
  const lock = Row({ itemSpacing: 13 }); lock.fills = [];
  const mk = figma.createFrame(); mk.name = 'شعار اتحاد (أبيض)'; mk.resize(28, 40);
  mk.fills = solid('#FFFFFF', 0.14); mk.cornerRadius = 6;
  lock.appendChild(mk);
  const lt = Col({ itemSpacing: 2 }); lt.fills = [];
  lt.appendChild(T('اتحاد', { size: 21, weight: 'Bold', color: '#FFFFFF', lh: 1.1 }));
  lt.appendChild(T('CHINA — OMAN ERP', { size: 9.5, color: '#6B80A3', family: NUM, align: 'LEFT', spacing: 15 }));
  lock.appendChild(lt);
  brandCol.appendChild(lock);
  const bp = T('منصّة تشغيل موحّدة لتجارة الاستيراد بين الصين وسلطنة عُمان.',
    { size: 14.5, color: '#8FA2C0', width: 300, lh: 1.8 });
  brandCol.appendChild(bp);

  [['النظام', ['لوحة التحكم','برج التحكم','التكلفة الواصلة','بوابة العميل']],
   ['الأقسام', ['المبيعات والعملاء','المشتريات','اللوجستيات','المستودعات']],
   ['الشركة', ['من نحن','الأسعار','الدعم','تواصل معنا']]]
  .forEach(([title, links]) => {
    const c = Col({ itemSpacing: 11 }); c.fills = []; row.appendChild(c);
    const h = T(title, { size: 14, weight: 'SemiBold', color: '#FFFFFF' });
    c.appendChild(h); c.itemSpacing = 11;
    links.forEach((l) => c.appendChild(T(l, { size: 14.5, color: '#8FA2C0' })));
  });

  const bot = Row({ itemSpacing: 0 }); bot.fills = [];
  bot.strokes = solid('#FFFFFF', 0.08); bot.strokeTopWeight = 1; bot.strokeAlign = 'INSIDE';
  bot.paddingTop = 26;
  inner.appendChild(bot);
  bot.layoutSizingHorizontal = 'FILL'; bot.layoutSizingVertical = 'HUG';
  const c1 = T('© ٢٠٢٦ شركة الاتحاد المحدودة — جميع الحقوق محفوظة', { size: 13.5, color: '#6B80A3' });
  bot.appendChild(c1); c1.layoutSizingHorizontal = 'FILL';
  bot.appendChild(T('الخوض · قوانزو · نزوى', { size: 13.5, color: '#6B80A3', align: 'LEFT' }));
}

return { createdNodeIds: created, note: 'Landing page complete. Replace the three image placeholders with the real PNGs.' };
