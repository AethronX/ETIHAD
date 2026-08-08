// ============================================================
// Figma builder — script 2 of 3
// Stats strip + features grid + how-it-works
// Requires script 1 to have run. Pass the page frame id it returned.
// ============================================================
const PAGE_FRAME_ID = 'PASTE_pageFrameId_FROM_SCRIPT_1';

const F = 'Cairo', NUM = 'Inter';
await Promise.all([
  figma.loadFontAsync({ family: F, style: 'Regular' }),
  figma.loadFontAsync({ family: F, style: 'Medium' }),
  figma.loadFontAsync({ family: F, style: 'SemiBold' }),
  figma.loadFontAsync({ family: F, style: 'Bold' }),
  figma.loadFontAsync({ family: NUM, style: 'Bold' }),
]);

const hex = (h) => { h = h.replace('#', ''); return { r: parseInt(h.slice(0,2),16)/255, g: parseInt(h.slice(2,4),16)/255, b: parseInt(h.slice(4,6),16)/255 }; };
const solid = (h, o) => o === undefined ? [{ type:'SOLID', color: hex(h) }] : [{ type:'SOLID', color: hex(h), opacity:o }];
const P = { navy:'#051C4A', navy2:'#0A2A63', blue:'#0F4C81', cyan:'#00B8D9', orange:'#F7931E',
  green:'#16A34A', red:'#DC2626', ink:'#111827', body:'#374151', muted:'#6B7280',
  line:'#E7EBF0', bg:'#F6F8FB', card:'#FFFFFF' };

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
  inner.fills = [];
  band.appendChild(inner);
  inner.resize(1200, 10);
  inner.layoutSizingHorizontal = 'FIXED'; inner.layoutSizingVertical = 'HUG';
  created.push(band.id);
  return { band, inner };
};
const Head = (inner, eyebrow, title, sub) => {
  const h = Col({ name: 'عنوان القسم', itemSpacing: 16 });
  h.fills = []; inner.appendChild(h);
  h.resize(760, 10); h.layoutSizingHorizontal = 'FIXED'; h.layoutSizingVertical = 'HUG';
  h.appendChild(T(eyebrow, { size: 14, weight: 'SemiBold', color: P.blue, spacing: 14 }));
  h.appendChild(T(title, { size: 42, weight: 'Bold', width: 720, lh: 1.24 }));
  if (sub) h.appendChild(T(sub, { size: 18, color: P.body, width: 720, lh: 1.75 }));
  return h;
};
const Card = (parent, w) => {
  const c = Col({ name: 'بطاقة', itemSpacing: 11 });
  c.fills = solid(P.card);
  c.strokes = solid(P.line); c.strokeWeight = 1;
  c.cornerRadius = 28;
  c.paddingTop = 34; c.paddingBottom = 34; c.paddingLeft = 32; c.paddingRight = 32;
  c.effects = [{ type:'DROP_SHADOW', color:{r:0.02,g:0.11,b:0.29,a:0.06}, offset:{x:0,y:10}, radius:30, spread:0, visible:true, blendMode:'NORMAL' }];
  parent.appendChild(c);
  c.resize(w, 10); c.layoutSizingHorizontal = 'FIXED'; c.layoutSizingVertical = 'HUG';
  return c;
};

// ---------- STATS ----------
{
  const { band, inner } = Section('شريط الأرقام', { padY: 52 });
  band.strokes = solid(P.line); band.strokeBottomWeight = 1; band.strokeAlign = 'INSIDE';
  const row = Row({ name: 'الأرقام', itemSpacing: 0 });
  row.fills = []; inner.appendChild(row);
  row.layoutSizingHorizontal = 'FILL'; row.layoutSizingVertical = 'HUG';
  [['30','شاشة عمل','كلها بالعربية'], ['9','أدوار وظيفية','لكل دور شاشته'],
   ['7','مراحل للعرض','بمسؤول معروف'], ['2','مستودعان','قوانزو ونزوى']]
   .forEach(([v,l,s], i) => {
     const cell = Col({ itemSpacing: 8, counterAxisAlignItems: 'CENTER' });
     cell.fills = [];
     if (i > 0) { cell.strokes = solid(P.line); cell.strokeRightWeight = 1; cell.strokeAlign = 'INSIDE'; }
     row.appendChild(cell);
     cell.layoutSizingHorizontal = 'FILL'; cell.layoutSizingVertical = 'HUG';
     cell.appendChild(T(v, { size: 44, weight: 'Bold', color: P.blue, family: NUM, align: 'CENTER' }));
     cell.appendChild(T(l, { size: 15, weight: 'Medium', color: P.body, align: 'CENTER' }));
     cell.appendChild(T(s, { size: 12.5, color: P.muted, align: 'CENTER' }));
   });
}

// ---------- FEATURES ----------
{
  const { inner } = Section('الميزات');
  Head(inner, 'ما الذي يفعله النظام',
    'ستّة أشياء تُدار اليوم في جداول متفرّقة — هنا في مكان واحد',
    'كل قسم يكتب مرة واحدة، والبقية يقرؤون النتيجة في اللحظة نفسها.');
  const grid = Col({ name: 'الشبكة', itemSpacing: 24 });
  grid.fills = []; inner.appendChild(grid);
  grid.layoutSizingHorizontal = 'FILL'; grid.layoutSizingVertical = 'HUG';
  grid.paddingTop = 52;
  const items = [
    [P.red, 'برج التحكم', 'كل ما خرج عن الخطة في شاشة واحدة، مرتّباً بالخطورة ثم بالمهلة المتبقية. الهدف أن تفرغ الشاشة.'],
    [P.blue, 'التكلفة الواصلة', 'ثمن المورد والنولون والجمارك والتخليص والنقل — وحتى رسوم التخزين المتراكمة. الربح الفعلي، لا المقدَّر.'],
    [P.cyan, 'الحاويات والتخليص', 'من حجز مكان في الحاوية حتى بوابة نزوى: المراحل والمستندات والبيان الجمركي وتنبيه قبل بدء الأرضيات.'],
    [P.orange, 'المستودعان', 'استلام بالباركود في قوانزو، وفحص وتسليم في نزوى، وخريطة رفوف تُظهر الشاغر والمحجوز والممتلئ.'],
    [P.green, 'الأدوار والصلاحيات', 'موظف المبيعات لا يرى تكلفة المورد، وموظف الصين لا يرى سعر البيع. مطبَّق في النظام، لا مكتوب في سياسة.'],
    [P.navy2, 'بوابة العميل', 'رابط خاص يعرض للعميل شحناته وفواتيره ومستنداته. كل استعلام يجيب عنه النظام مكالمة لم تصل إليك.'],
  ];
  for (let r = 0; r < 2; r++) {
    const line = Row({ itemSpacing: 24 }); line.fills = [];
    grid.appendChild(line);
    line.layoutSizingHorizontal = 'FILL'; line.layoutSizingVertical = 'HUG';
    line.counterAxisAlignItems = 'MIN';
    for (let i = 0; i < 3; i++) {
      const [c, title, desc] = items[r * 3 + i];
      const card = Card(line, 384);
      card.layoutSizingHorizontal = 'FILL';
      const ic = figma.createFrame();
      ic.name = 'أيقونة'; ic.resize(50, 50); ic.cornerRadius = 15; ic.fills = solid(c);
      card.appendChild(ic);
      card.appendChild(T(title, { size: 21, weight: 'SemiBold', lh: 1.35 }));
      const d = T(desc, { size: 15.5, color: P.body, lh: 1.75 });
      card.appendChild(d); d.layoutSizingHorizontal = 'FILL';
    }
  }
}

// ---------- HOW IT WORKS ----------
{
  const { inner } = Section('كيف يعمل', { bg: P.bg });
  Head(inner, 'كيف يعمل',
    'دورة عرض السعر: سبع مراحل، ولكل مرحلة مسؤول واحد',
    'لا يتقدّم العرض خطوة إلا بيد صاحبها. النظام يبدأ عدّاد المهلة ويذكّر تلقائياً عند التأخر.');

  const steps = Row({ name: 'المراحل', itemSpacing: 12 });
  steps.fills = []; steps.counterAxisAlignItems = 'MIN';
  inner.appendChild(steps);
  steps.layoutSizingHorizontal = 'FILL'; steps.layoutSizingVertical = 'HUG';
  steps.paddingTop = 56;
  [['طلب تسعير','مبيعات',P.blue],['تسعير المورد','مكتب الصين',P.cyan],['مراجعة الربح','مبيعات',P.blue],
   ['اعتماد الإدارة','المدير العام',P.navy],['أُرسل للعميل','مبيعات',P.blue],
   ['موافقة العميل','العميل',P.orange],['محوَّل','النظام',P.green]]
  .forEach(([t, who, c], i) => {
    const st = Col({ itemSpacing: 8 }); st.fills = [];
    steps.appendChild(st);
    st.layoutSizingHorizontal = 'FILL'; st.layoutSizingVertical = 'HUG';
    const bar = figma.createFrame(); bar.name = 'شريط'; bar.resize(100, 5);
    bar.cornerRadius = 3; bar.fills = solid(c);
    st.appendChild(bar); bar.layoutSizingHorizontal = 'FILL';
    st.appendChild(T('0' + (i + 1), { size: 13, weight: 'Bold', color: c, family: NUM, align: 'LEFT' }));
    st.appendChild(T(t, { size: 16, weight: 'SemiBold', lh: 1.35 }));
    st.appendChild(T(who, { size: 13, color: P.muted }));
  });

  const rules = Row({ name: 'الضوابط', itemSpacing: 24 });
  rules.fills = []; rules.counterAxisAlignItems = 'MIN';
  inner.appendChild(rules);
  rules.layoutSizingHorizontal = 'FILL'; rules.layoutSizingVertical = 'HUG';
  rules.paddingTop = 52;
  [['٤٨ ساعة','مهلة ردّ مكتب الصين — العدّاد يبدأ لحظة الإرسال، والتذكير آليّ.'],
   ['٣٠٪','أي خصم يتجاوزها يستدعي اعتماد المدير العام قبل أن يخرج العرض.'],
   ['نسخة مجمّدة','الاعتماد يُصدر PDF بالعربية والإنجليزية، وأي تعديل يفتح نسخة جديدة.']]
  .forEach(([k, d]) => {
    const c = Col({ itemSpacing: 10 });
    c.fills = solid(P.card); c.strokes = solid(P.line); c.strokeWeight = 1;
    c.cornerRadius = 20; c.paddingTop = 28; c.paddingBottom = 28; c.paddingLeft = 30; c.paddingRight = 30;
    rules.appendChild(c);
    c.layoutSizingHorizontal = 'FILL'; c.layoutSizingVertical = 'HUG';
    c.appendChild(T(k, { size: 30, weight: 'Bold', color: P.blue }));
    const t = T(d, { size: 15, color: P.body, lh: 1.7 });
    c.appendChild(t); t.layoutSizingHorizontal = 'FILL';
  });
}

return { createdNodeIds: created, note: 'Sections built: stats, features, how-it-works. Run script 3 next.' };
