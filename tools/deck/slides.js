const { C } = require('./theme');

const LOGO_W = 'assets/etihad-logo-white.png';
const LOGO_N = 'assets/etihad-logo-navy.png';

const lockDark = `<div class="lock"><img src="${LOGO_W}"><div><div class="nm">اتحاد</div><div class="sb">CHINA — OMAN ERP</div></div></div>`;
const mark = () => `<div class="mark"><span>نظام اتحاد</span></div>`;

// icon bubble
const bub = (bg, txt) => `<div class="dot" style="background:${bg}">${txt}</div>`;

/* ============================ 1. TITLE ============================ */
const s01 = () => `
<div class="slide dark">
  <div data-bleed="1" style="position:absolute;left:-180px;top:-120px;width:900px;height:900px;border-radius:50%;
              background:radial-gradient(circle at 40% 40%, rgba(0,184,217,.18), rgba(0,184,217,0) 62%);"></div>
  <div data-bleed="1" style="position:absolute;right:-160px;bottom:-260px;width:820px;height:820px;border-radius:50%;
              background:radial-gradient(circle at 50% 50%, rgba(247,147,30,.13), rgba(247,147,30,0) 62%);"></div>
  <img data-bleed="1" src="${LOGO_W}" style="position:absolute; left:118px; top:50%; transform:translateY(-50%);
       height:660px; opacity:.07;">
  <div class="pad" style="display:flex;flex-direction:column;justify-content:space-between;padding-top:70px;padding-bottom:70px;">
    <div>${lockDark}</div>
    <div style="max-width:1180px;margin-top:-40px;">
      <div class="kicker">منصّة التشغيل الموحّدة</div>
      <h1 style="margin-top:26px;">نظام اتحاد<br>لإدارة تجارة الصين — عُمان</h1>
      <p class="lead" style="margin-top:34px;max-width:1000px;">
        من طلب التسعير في الخوض، إلى مورّد في قوانزو، إلى حاوية في ميناء صحار،
        إلى تسليم العميل في نزوى — <b style="color:#fff;font-weight:600;">مسار واحد متصل</b>،
        لا رسائل متفرّقة ولا جداول متوازية.
      </p>
      <div style="display:flex;gap:14px;margin-top:44px;">
        <div class="chip" style="background:rgba(255,255,255,.10);color:#fff;">
          <span class="num">٣٠</span> شاشة عمل</div>
        <div class="chip" style="background:rgba(255,255,255,.10);color:#fff;">
          <span class="num">٩</span> أدوار وظيفية</div>
        <div class="chip" style="background:rgba(0,184,217,.18);color:#7FE3F5;">
          عربي بالكامل · يعمل على الهاتف</div>
      </div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div class="cap">عرض تقديمي — شركة الاتحاد المحدودة</div>
      <div class="cap">أغسطس ٢٠٢٦</div>
    </div>
  </div>
</div>`;

/* ============================ 2. PROBLEM ============================ */
const rowsProblem = [
  [C.red, '١', 'السعر يُبنى على تخمين', 'تكلفة المورد وأجرة الشحن والجمارك والأرضيات تصل متفرّقة وبعد أسابيع. الهامش يُعرف بعد أن تُغلق الصفقة، لا قبلها.'],
  [C.orange, '٢', 'الشحنة تعيش في رسائل واتساب', 'حالة الحاوية يعرفها شخص واحد. إن كان في إجازة، تتوقّف الإجابة. ولا سجلّ يُراجَع لاحقاً.'],
  [C.blue, '٣', 'كل قسم يملك جدوله الخاص', 'المبيعات في ملف، المستودع في دفتر، المحاسبة في نظام ثالث. الأرقام لا تتطابق، والتسوية عمل شهري كامل.'],
  [C.navy2, '٤', 'لا أحد يرى الاستثناءات', 'الشحنة المتأخرة والفاتورة غير المحصّلة والمهلة المجانية المنتهية تظهر حين تتحوّل إلى خسارة.'],
];
const s02 = () => `
<div class="slide">
  <div class="pad ctr">
    <div class="kicker dk">أين يتسرّب المال اليوم</div>
    <h2 style="margin-top:20px;">أربع فجوات تكلّف الشركة في كل شحنة</h2>
    <div class="grid2" style="margin-top:52px;">
      ${rowsProblem.map(([col, n, t, d]) => `
        <div class="card" style="padding:38px 40px;display:flex;gap:24px;align-items:flex-start;">
          ${bub(col, `<span class="num">${n}</span>`)}
          <div><h3>${t}</h3><p class="body" style="margin-top:12px;">${d}</p></div>
        </div>`).join('')}
    </div>
  </div>
  <div class="pg"><span class="num">02</span></div>${mark()}
</div>`;

/* ============================ 3. THE IDEA ============================ */
const s03 = () => `
<div class="slide dark">
  <img data-bleed="1" src="${LOGO_W}" style="position:absolute;right:-90px;top:-80px;height:760px;opacity:.06;">
  <div class="pad" style="display:flex;flex-direction:column;justify-content:center;">
    <div class="kicker">الفكرة</div>
    <h2 style="margin-top:24px;max-width:1500px;font-size:64px;">
      الشحنة كائن واحد في النظام — يحمل عرضه وأمر شرائه وحاويته
      وبيانه الجمركي وتكلفته الفعلية وفاتورته.
    </h2>
    <p class="lead" style="margin-top:40px;max-width:1240px;">
      لا يُعاد إدخال أي رقم مرتين. كل مرحلة تُسلّم التالية تلقائياً، وكل حركة تُسجَّل
      باسم منفّذها ووقتها. ما تراه الإدارة هو ما يراه المستودع — في اللحظة نفسها.
    </p>
    <div class="grid4" style="margin-top:64px;">
      ${[['عرض السعر', 'يبدأ المسار'], ['أمر الشراء', 'يُنشأ تلقائياً'], ['الحاوية', 'تُحجز وتُتتبَّع'], ['الفاتورة', 'تُصدر وتُحصَّل']]
    .map(([t, d], i) => `
        <div style="border-top:1px solid rgba(255,255,255,.16);padding-top:22px;">
          <div class="num" style="font-size:17px;font-weight:700;color:${C.cyan};">0${i + 1}</div>
          <div style="font-size:27px;font-weight:600;margin-top:12px;">${t}</div>
          <div class="cap" style="margin-top:6px;">${d}</div>
        </div>`).join('')}
    </div>
  </div>
  <div class="pg"><span class="num">03</span></div>${mark()}
</div>`;

/* ============================ 4. DASHBOARD HERO ============================ */
const s04 = () => `
<div class="slide">
  <div class="pad" style="padding-bottom:0;">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div style="max-width:940px;">
        <div class="kicker dk">الشاشة الأولى لكل موظف</div>
        <h2 style="margin-top:18px;">لوحة التحكم تفتح على ما يخصّك أنت</h2>
        <p class="body" style="margin-top:18px;max-width:880px;">
          ستة مؤشرات حيّة، ثم قائمة «يحتاج قرارك» — الشحنات والفواتير والعروض
          المتوقّفة على إجراء منك، مرتّبة بالخطورة. لا تبحث عن العمل، العمل يظهر لك.
        </p>
      </div>
      <div style="display:flex;gap:12px;">
        <div class="chip" style="background:#E8F0F7;color:${C.blue};">مؤشرات قابلة للتحرير</div>
        <div class="chip" style="background:#FFF4E6;color:#96450A;">تنبيهات بالخطورة</div>
      </div>
    </div>
    <div class="laptop" style="margin-top:40px;width:1420px;margin-inline:auto;">
      <div class="screen"><img class="crop" style="height:512px;" src="shots/d-01-dash.png"></div>
      <div class="base" style="width:1560px;"></div>
      <div class="foot" style="width:1200px;"></div>
    </div>
  </div>
  <div class="pg"><span class="num">04</span></div>${mark()}
</div>`;

/* ============================ 5. SEVEN GROUPS ============================ */
const groups = [
  [C.blue, 'نظرة عامة', ['لوحة التحكم', 'برج التحكم', 'التحليلات']],
  [C.cyan, 'المبيعات والعملاء', ['العملاء', 'المبيعات', 'عروض الأسعار', 'الفواتير']],
  [C.orange, 'المشتريات', ['أوامر الشراء', 'الموردون', 'مكتب الصين']],
  [C.navy2, 'اللوجستيات', ['الشحن والتتبع', 'الحاويات', 'التخليص الجمركي', 'تخطيط التحميل']],
  [C.green, 'المستودعات', ['مستودع الصين', 'مستودع عُمان', 'مواعيد الاستلام', 'المخزون']],
  [C.blue, 'المالية والأرشيف', ['المحاسبة', 'المستندات', 'التكلفة الواصلة', 'التقارير']],
  [C.navy, 'النظام', ['الإشعارات', 'الصلاحيات', 'الفرق', 'التكاملات', 'حالة النظام', 'سجل التدقيق', 'الإعدادات', 'بوابة العميل']],
];
const s05 = () => `
<div class="slide">
  <div class="pad ctr">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div>
        <div class="kicker dk">خريطة النظام</div>
        <h2 style="margin-top:18px;">سبع مجموعات تغطّي دورة العمل كاملة</h2>
      </div>
      <p class="cap" style="max-width:520px;text-align:left;">
        كل موظف يرى المجموعات التي يعمل بها فقط — القائمة نفسها تتغيّر بتغيّر الدور.
      </p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:46px;">
      ${groups.map(([col, g, items]) => `
        <div class="card" style="padding:30px 28px;">
          <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:12px;height:12px;border-radius:50%;background:${col};"></div>
            <div style="font-size:25px;font-weight:600;">${g}</div>
          </div>
          <div style="margin-top:18px;display:flex;flex-direction:column;gap:9px;">
            ${items.map((i) => `<div class="cap" style="font-size:19px;color:${C.body};">${i}</div>`).join('')}
          </div>
        </div>`).join('')}
      <div class="card" style="padding:30px 28px;background:${C.navy};border-color:${C.navy};color:#fff;
           display:flex;flex-direction:column;justify-content:center;">
        <div class="stat" style="color:#fff;">30</div>
        <div style="font-size:23px;font-weight:600;margin-top:10px;">شاشة عمل</div>
        <div class="cap" style="color:#8A9CBB;margin-top:8px;font-size:18px;">
          كلها بالعربية، وكلها تعمل على الهاتف.
        </div>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">05</span></div>${mark()}
</div>`;

/* ============================ 6. CONTROL TOWER ============================ */
const s06 = () => `
<div class="slide">
  <div class="pad" style="display:flex;gap:56px;align-items:center;">
    <div style="flex:0 0 620px;">
      <div class="kicker dk">برج التحكم</div>
      <h2 style="margin-top:18px;font-size:50px;">كل ما خرج عن الخطة<br>في شاشة واحدة</h2>
      <p class="body" style="margin-top:22px;">
        الشحنة المتأخرة، البيان الجمركي المعلّق، المهلة المجانية التي انتهت،
        الفاتورة التي تجاوزت أجلها — مرتّبة بالخطورة ثم بالوقت المتبقّي.
      </p>
      <div style="margin-top:34px;display:flex;flex-direction:column;gap:18px;">
        ${[[C.red, 'حرِج', 'يكلّف مالاً الآن — أرضيات أو غرامة تأخير'],
    [C.orange, 'يحتاج إجراء', 'مهلة تقترب، والقرار ما زال ممكناً'],
    [C.blue, 'للمتابعة', 'تحت السيطرة، يُراقَب فقط']]
    .map(([col, t, d]) => `
          <div style="display:flex;gap:16px;align-items:flex-start;">
            <div style="width:14px;height:14px;border-radius:50%;background:${col};margin-top:8px;flex:0 0 14px;"></div>
            <div><div style="font-size:24px;font-weight:600;">${t}</div>
                 <div class="cap" style="margin-top:4px;">${d}</div></div>
          </div>`).join('')}
      </div>
      <div class="card" style="margin-top:36px;padding:26px 30px;background:#F0F7FF;border-color:#CFE3F7;">
        <p class="body" style="color:${C.navy};font-size:21px;">
          <b style="font-weight:600;">الهدف أن تفرغ الشاشة.</b>
          حين لا يبقى فيها شيء، فكل شحنة تسير كما خُطّط لها.
        </p>
      </div>
    </div>
    <div class="laptop" style="flex:1;">
      <div class="screen"><img src="shots/d-02-tower.png"></div>
      <div class="base" style="width:104%;margin-inline-start:-2%;"></div>
    </div>
  </div>
  <div class="pg"><span class="num">06</span></div>${mark()}
</div>`;

/* ============================ 7. WORKFLOW ============================ */
const stages = [
  ['طلب تسعير', 'مبيعات', C.blue],
  ['تسعير المورد', 'مكتب الصين', C.cyan],
  ['مراجعة الربح', 'مبيعات', C.blue],
  ['اعتماد الإدارة', 'المدير العام', '#7FB6E4'],
  ['أُرسل للعميل', 'مبيعات', C.blue],
  ['موافقة العميل', 'العميل', C.orange],
  ['محوَّل', 'النظام', C.green],
];
const s07 = () => `
<div class="slide dark">
  <div class="pad">
    <div class="kicker">دورة عرض السعر</div>
    <h2 style="margin-top:18px;">سبع مراحل، ولكل مرحلة مسؤول واحد معروف</h2>
    <p class="lead" style="margin-top:20px;max-width:1320px;">
      لا يتقدّم العرض خطوة إلا بيد صاحبها. النظام يعرف من عليه الدور الآن،
      ويبدأ عدّاد المهلة، ويذكّر تلقائياً عند التأخر.
    </p>
    <div style="display:flex;gap:14px;margin-top:60px;align-items:stretch;">
      ${stages.map(([t, who, col], i) => `
        <div style="flex:1;display:flex;flex-direction:column;">
          <div style="height:6px;border-radius:3px;background:${col};"></div>
          <div class="num" style="font-size:16px;font-weight:700;color:${col};margin-top:20px;">0${i + 1}</div>
          <div style="font-size:24px;font-weight:600;margin-top:10px;line-height:1.3;">${t}</div>
          <div class="cap" style="margin-top:8px;">${who}</div>
        </div>`).join('')}
    </div>
    <div class="grid3" style="margin-top:68px;">
      ${[['٤٨ ساعة', 'مهلة ردّ مكتب الصين — العدّاد يبدأ لحظة الإرسال'],
    ['٣٠٪', 'أي خصم يتجاوزها يستدعي اعتماد المدير العام'],
    ['نسخة مجمّدة', 'الاعتماد يُصدر PDF بالعربية والإنجليزية، وأي تعديل يفتح نسخة جديدة']]
    .map(([n, d]) => `
        <div style="background:rgba(255,255,255,.06);border-radius:22px;padding:32px 34px;">
          <div style="font-size:40px;font-weight:700;color:${C.cyan};">${n}</div>
          <div class="cap" style="margin-top:12px;font-size:19px;">${d}</div>
        </div>`).join('')}
    </div>
  </div>
  <div class="pg"><span class="num">07</span></div>${mark()}
</div>`;

/* ============================ 8. LANDED COST ============================ */
const s08 = () => `
<div class="slide">
  <div class="pad" style="display:flex;gap:56px;align-items:center;">
    <div class="laptop" style="flex:1;">
      <div class="screen"><img src="shots/d-05-landed.png"></div>
      <div class="base" style="width:104%;margin-inline-start:-2%;"></div>
    </div>
    <div style="flex:0 0 600px;">
      <div class="kicker dk">التكلفة الواصلة</div>
      <h2 style="margin-top:18px;font-size:50px;">الربح المقدَّر ليس الربح الفعلي</h2>
      <p class="body" style="margin-top:22px;">
        النظام يجمع كل ريال أُنفق على الشحنة حتى لحظة تسليمها: ثمن المورد،
        الشحن الداخلي في الصين، النولون البحري، التأمين، الجمارك، التخليص،
        النقل إلى نزوى — <b style="font-weight:600;color:${C.ink}">ورسوم التخزين التي تتراكم كلما تأخّر الاستلام.</b>
      </p>
      <div style="margin-top:32px;display:flex;flex-direction:column;gap:14px;">
        ${['التكلفة تُوزَّع على البنود بالحجم أو بالقيمة',
    'الهامش الفعلي يظهر لكل صنف، لا للشحنة فقط',
    'المقارنة بالمقدَّر تكشف أين ضاع الفرق']
    .map((t) => `
          <div style="display:flex;gap:14px;align-items:flex-start;">
            <div style="width:26px;height:26px;border-radius:50%;background:${C.green};color:#fff;
                        display:grid;place-items:center;font-size:15px;flex:0 0 26px;margin-top:3px;">✓</div>
            <div class="body" style="font-size:21px;">${t}</div>
          </div>`).join('')}
      </div>
      <div class="card" style="margin-top:34px;padding:26px 30px;background:#FFF7ED;border-color:#FBD9A5;">
        <p class="body" style="color:#7C3A06;font-size:21px;">
          هذه الشاشة وحدها تكفي لتغيير قرار التسعير في الصفقة القادمة.
        </p>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">08</span></div>${mark()}
</div>`;

/* ============================ 9. LOGISTICS ============================ */
const s09 = () => `
<div class="slide">
  <div class="pad ctr">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div>
        <div class="kicker dk">اللوجستيات</div>
        <h2 style="margin-top:18px;">الحاوية من الحجز حتى بوابة نزوى</h2>
      </div>
      <p class="cap" style="max-width:560px;text-align:left;">
        كل حاوية تحمل شحناتها ومستنداتها وبيانها الجمركي ومواعيدها — ملف واحد يتحرّك معها.
      </p>
    </div>
    <div style="display:flex;gap:34px;margin-top:42px;align-items:flex-start;">
      <div class="laptop" style="flex:1.35;">
        <div class="screen"><img src="shots/d-04-containers.png"></div>
        <div class="base" style="width:104%;margin-inline-start:-2%;"></div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:20px;padding-top:10px;">
        ${[[C.cyan, 'تتبّع بالمراحل', 'جاهزة في الصين ← في البحر ← تخليص ← في نزوى ← الاستلام'],
    [C.orange, 'تخطيط التحميل', 'حاوية 40HQ بسعة ٦٧٫٧ م³ — النظام يمنع تجاوز السعة ويطالب بإشغال ٩٠٪ قبل الإقفال'],
    [C.navy2, 'التخليص الجمركي', 'البيان والرسوم والمستندات في مكان واحد، مع تنبيه قبل بدء الأرضيات'],
    [C.green, 'مواعيد الاستلام', 'رصيف نزوى عنق الزجاجة — الحجز المسبق يمنع ازدحام صباح الأحد']]
    .map(([col, t, d]) => `
          <div class="card" style="padding:26px 30px;display:flex;gap:18px;align-items:flex-start;">
            <div style="width:10px;height:10px;border-radius:50%;background:${col};margin-top:11px;flex:0 0 10px;"></div>
            <div><div style="font-size:24px;font-weight:600;">${t}</div>
                 <div class="cap" style="margin-top:7px;font-size:18px;">${d}</div></div>
          </div>`).join('')}
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">09</span></div>${mark()}
</div>`;

/* ============================ 10. WAREHOUSES ============================ */
const s10 = () => `
<div class="slide">
  <div class="pad">
    <div class="kicker dk">المستودعات</div>
    <h2 style="margin-top:18px;">مستودعان، ولغة واحدة: الباركود</h2>
    <div style="display:flex;gap:40px;margin-top:36px;align-items:flex-start;">
      <div style="flex:1.25;">
        <div class="laptop">
          <div class="screen"><img class="crop" style="height:452px;" src="shots/d-06-cnwh.png"></div>
          <div class="base" style="width:104%;margin-inline-start:-2%;"></div>
        </div>
        <div class="card" style="margin-top:26px;padding:26px 30px;">
          <h3>مستودع قوانزو</h3>
          <p class="cap" style="margin-top:10px;font-size:19px;">
            استلام من المورد، توليد الباركود، التخزين في الرفوف، ثم التخصيص لحاوية.
            خريطة الرفوف تُظهر الشاغر والمحجوز والممتلئ في لمحة.
          </p>
        </div>
      </div>
      <div style="flex:.75;">
        <div class="phone" style="width:262px;margin-inline:auto;">
          <div class="shell"><img src="shots/m-03-omwh.png"></div>
        </div>
        <div class="card" style="margin-top:26px;padding:26px 30px;">
          <h3>مستودع نزوى — في يد العامل</h3>
          <p class="cap" style="margin-top:10px;font-size:19px;">
            الفحص والاستلام والتسليم تُنفَّذ من الهاتف داخل المستودع.
            عامل المستودع يرى أربع شاشات فقط — ما يحتاجه، لا أكثر.
          </p>
        </div>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">10</span></div>${mark()}
</div>`;

/* ============================ 11. ROLES ============================ */
const roles = [
  ['مدير النظام', 'وصول كامل غير مقيّد، بما في ذلك الإعدادات وسجل التدقيق', C.navy],
  ['المدير العام', 'قراءة كل شيء، واعتماد ما يتجاوز حدود الصلاحية المالية', C.navy2],
  ['موظف مبيعات', 'عملاؤه وعروضه فقط — لا يرى تكلفة المورد الأصلية', C.blue],
  ['محاسب', 'الفواتير والمدفوعات والمصروفات وكل التقارير المالية', C.blue],
  ['موظف مكتب الصين', 'الموردون والتسعير وأوامر الشراء — لا يرى سعر البيع للعميل', C.cyan],
  ['مدير مستودع الصين', 'الاستلام والباركود والتخزين وتحميل الحاويات', C.cyan],
  ['مدير مستودع عُمان', 'الاستلام والفحص والمخزون وطابور الاستلام في نزوى', C.green],
  ['مسؤول التخليص', 'البيان الجمركي والرسوم ومستندات الحاوية عند الميناء', C.orange],
  ['عامل مستودع', 'مسح الباركود وتحريك المخزون وتسليم العميل فقط', C.muted],
];
const s11 = () => `
<div class="slide">
  <div class="pad ctr">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div>
        <div class="kicker dk">تسجيل الدخول</div>
        <h2 style="margin-top:18px;">كل موظف يدخل فيجد نظامه هو</h2>
      </div>
      <p class="cap" style="max-width:600px;text-align:left;">
        الدور لا يغيّر الصلاحيات فقط — يغيّر القائمة والشاشة الأولى والأرقام المعروضة.
        الموظف لا يرى ما لا يخصّه، فلا يضيع فيه ولا يطّلع عليه.
      </p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:44px;">
      ${roles.map(([t, d, col]) => `
        <div class="card" style="padding:28px 30px;">
          <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:38px;height:38px;border-radius:11px;background:${col};flex:0 0 38px;"></div>
            <div style="font-size:24px;font-weight:600;">${t}</div>
          </div>
          <div class="cap" style="margin-top:14px;font-size:18px;line-height:1.6;">${d}</div>
        </div>`).join('')}
    </div>
    <div class="card" style="margin-top:26px;padding:26px 34px;background:${C.navy};border-color:${C.navy};
         display:flex;align-items:center;gap:20px;">
      <div style="font-size:23px;color:#fff;font-weight:600;">وبوابة عاشرة للعميل نفسه</div>
      <div class="cap" style="color:#9DB0CC;font-size:19px;">
        يرى شحناته وفواتيره ومستنداته فقط — ولا يرى شيئاً من عمليات الشركة الداخلية.
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">11</span></div>${mark()}
</div>`;

/* ============================ 12. PERMISSIONS ============================ */
const s12 = () => `
<div class="slide">
  <div class="pad" style="display:flex;gap:56px;align-items:center;">
    <div style="flex:0 0 580px;">
      <div class="kicker dk">الصلاحيات</div>
      <h2 style="margin-top:18px;font-size:50px;">مطبَّقة في النظام،<br>لا مكتوبة في سياسة</h2>
      <p class="body" style="margin-top:22px;">
        مصفوفة واضحة تُظهر لكل دور ما له في كل وحدة: وصول كامل، محدود ضمن نطاقه،
        قراءة فقط، أو لا وصول إطلاقاً.
      </p>
      <div style="margin-top:32px;display:flex;flex-direction:column;gap:16px;">
        ${[['●', 'كامل', C.blue], ['◐', 'محدود ضمن النطاق', C.cyan], ['○', 'قراءة فقط', C.muted], ['—', 'لا وصول', '#B6BFCB']]
    .map(([g, t, col]) => `
          <div style="display:flex;gap:16px;align-items:center;">
            <div style="font-size:26px;color:${col};width:30px;text-align:center;">${g}</div>
            <div class="body" style="font-size:21px;">${t}</div>
          </div>`).join('')}
      </div>
      <div class="card" style="margin-top:34px;padding:26px 30px;background:#F0F7FF;border-color:#CFE3F7;">
        <p class="body" style="color:${C.navy};font-size:21px;">
          وأي تعديل على الصلاحيات يُسجَّل في <b style="font-weight:600;">سجل التدقيق</b>
          باسم من نفّذه ووقته.
        </p>
      </div>
    </div>
    <div class="laptop" style="flex:1;">
      <div class="screen"><img src="shots/d-07-permissions.png"></div>
      <div class="base" style="width:104%;margin-inline-start:-2%;"></div>
    </div>
  </div>
  <div class="pg"><span class="num">12</span></div>${mark()}
</div>`;

/* ============================ 13. CLIENT PORTAL ============================ */
const s13 = () => `
<div class="slide">
  <div class="pad">
    <div style="max-width:1160px;">
      <div class="kicker dk">بوابة العميل</div>
      <h2 style="margin-top:18px;">العميل يتابع شحنته بنفسه</h2>
      <p class="body" style="margin-top:16px;max-width:1080px;">
        رابط خاص لكل عميل يعرض شحناته ومراحلها وفواتيره ورصيده المستحق ومستنداته.
        كل استعلام يجيب عنه النظام هو مكالمة لم تصل إلى موظفيك.
      </p>
    </div>
    <div style="display:flex;gap:44px;margin-top:34px;align-items:flex-start;">
      <div class="laptop" style="flex:1;">
        <div class="screen"><img class="crop" style="height:496px;" src="shots/d-10-portal.png"></div>
        <div class="base" style="width:104%;margin-inline-start:-2%;"></div>
      </div>
      <div class="phone" style="width:268px;flex:0 0 268px;">
        <div class="shell"><img src="shots/m-06-portal.png"></div>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">13</span></div>${mark()}
</div>`;

/* ============================ 14. MOBILE ============================ */
const s14 = () => `
<div class="slide dark">
  <div class="pad">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div style="max-width:960px;">
        <div class="kicker">في الميدان</div>
        <h2 style="margin-top:18px;">النظام نفسه في الجيب — لا نسخة مختصرة</h2>
        <p class="lead" style="margin-top:18px;">
          الثلاثون شاشة كلها تعمل على الهاتف. الجداول تتحوّل إلى بطاقات مقروءة،
          والقائمة إلى درج جانبي، وشريط سفلي يضع أكثر خمس شاشات استعمالاً تحت الإبهام.
        </p>
      </div>
      <div style="display:flex;gap:12px;">
        <div class="chip" style="background:rgba(0,184,217,.18);color:#7FE3F5;">صفر تمرير أفقي</div>
        <div class="chip" style="background:rgba(255,255,255,.10);color:#fff;">أهداف لمس ≥ ٢٤ بكسل</div>
      </div>
    </div>
    <div style="display:flex;gap:46px;justify-content:center;margin-top:52px;">
      ${[['m-01-dash.png', 'لوحة التحكم'], ['m-02-drawer.png', 'القائمة الجانبية'], ['m-05-quotes.png', 'عروض الأسعار'], ['m-07-dark.png', 'الوضع الليلي']]
    .map(([f, t]) => `
        <div style="text-align:center;">
          <div class="phone" style="width:296px;">
            <div class="shell"><img src="shots/${f}"></div>
          </div>
          <div class="cap" style="margin-top:20px;font-size:20px;color:#C3D0E4;">${t}</div>
        </div>`).join('')}
    </div>
  </div>
  <div class="pg"><span class="num">14</span></div>${mark()}
</div>`;

/* ============================ 15. SEARCH + THEME ============================ */
const s15 = () => `
<div class="slide">
  <div class="pad">
    <div class="kicker dk">تفاصيل الاستعمال اليومي</div>
    <h2 style="margin-top:18px;">أشياء صغيرة تُختصر بها ساعات</h2>
    <div class="grid2" style="margin-top:40px;">
      <div>
        <div class="laptop"><div class="screen"><img src="shots/d-11-palette.png"></div>
          <div class="base" style="width:104%;margin-inline-start:-2%;"></div></div>
        <div class="card" style="margin-top:26px;padding:28px 32px;">
          <h3>بحث شامل بضغطة واحدة</h3>
          <p class="cap" style="margin-top:10px;font-size:19px;">
            <span class="num">Ctrl</span> + <span class="num">K</span> من أي شاشة — اكتب رقم حاوية أو اسم عميل
            أو رقم فاتورة، فتنتقل إليه مباشرة دون المرور بالقوائم.
          </p>
        </div>
      </div>
      <div>
        <div class="laptop"><div class="screen"><img src="shots/d-12-dark.png"></div>
          <div class="base" style="width:104%;margin-inline-start:-2%;"></div></div>
        <div class="card" style="margin-top:26px;padding:28px 32px;">
          <h3>وضع ليلي كامل</h3>
          <p class="cap" style="margin-top:10px;font-size:19px;">
            مستودع بإضاءة خافتة أو نوبة ليلية — الوضع الليلي مقيس على كل شاشة،
            لا مجرد قلب للألوان.
          </p>
        </div>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">15</span></div>${mark()}
</div>`;

/* ============================ 16. DIFFERENTIATION ============================ */
const s16 = () => `
<div class="slide">
  <div class="pad ctr">
    <div class="kicker dk">لماذا هذا النظام</div>
    <h2 style="margin-top:18px;">مبني لهذا الخط تحديداً، لا نظام عام مُكيَّف</h2>
    <div style="display:flex;gap:26px;margin-top:44px;">
      <div class="card" style="flex:1;padding:38px 40px;">
        <div class="chip" style="background:#F1F3F6;color:${C.muted};">أنظمة ERP العامة</div>
        <div style="margin-top:26px;display:flex;flex-direction:column;gap:20px;">
          ${['مصمَّمة لكل الصناعات، فتحتاج تكييفاً طويلاً لتناسب الاستيراد',
    'التكلفة الواصلة إضافة تُشترى أو تُبرمج، لا جزء أصيل',
    'الواجهة إنجليزية والعربية ترجمة لاحقة تُقلب من اليمين',
    'مكتب الصين والمستودع خارج النظام غالباً',
    'الترخيص سنوي لكل مستخدم، ويكبر مع الفريق']
    .map((t) => `<div style="display:flex;gap:14px;align-items:flex-start;">
              <div style="color:#B6BFCB;font-size:22px;margin-top:-2px;">—</div>
              <div class="body" style="font-size:20px;color:${C.muted};">${t}</div></div>`).join('')}
        </div>
      </div>
      <div class="card" style="flex:1;padding:38px 40px;background:${C.navy};border-color:${C.navy};">
        <div class="chip" style="background:rgba(0,184,217,.20);color:#7FE3F5;">نظام اتحاد</div>
        <div style="margin-top:26px;display:flex;flex-direction:column;gap:20px;">
          ${['مبني على دورة الخوض ← قوانزو ← صحار ← نزوى كما هي فعلاً',
    'التكلفة الواصلة شاشة أساسية، والأرضيات محسوبة يوماً بيوم',
    'عربي أصلاً ومن اليمين لليسار — والأرقام تُعرض بلا تكسّر',
    'مكتب الصين والمستودعان داخل المسار نفسه، بأدوار وصلاحيات',
    'يعمل على أي هاتف بمتصفّح — لا تطبيق يُثبَّت ولا جهاز خاص']
    .map((t) => `<div style="display:flex;gap:14px;align-items:flex-start;">
              <div style="width:24px;height:24px;border-radius:50%;background:${C.cyan};color:${C.navy};
                          display:grid;place-items:center;font-size:14px;font-weight:700;flex:0 0 24px;margin-top:2px;">✓</div>
              <div class="body" style="font-size:20px;color:#DCE6F5;">${t}</div></div>`).join('')}
        </div>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">16</span></div>${mark()}
</div>`;

/* ============================ 17. QUALITY ============================ */
const s17 = () => `
<div class="slide">
  <div class="pad ctr">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div style="max-width:1000px;">
        <div class="kicker dk">الجودة</div>
        <h2 style="margin-top:18px;">جودة مقيسة بالأرقام، لا موصوفة بالكلام</h2>
        <p class="body" style="margin-top:18px;">
          النظام يُفحص آلياً على كل صفحاته الثلاثين، في الوضعين الفاتح والداكن،
          على مقاس الهاتف ومقاس الحاسب — في متصفّح حقيقي، قبل كل إصدار.
        </p>
      </div>
    </div>
    <div class="grid4" style="margin-top:48px;">
      ${[['0', 'إخفاق تباين ألوان', 'على ١٢٠ قياس صفحة'],
    ['0', 'عنصر بلا اسم مقروء', 'لقارئات الشاشة'],
    ['0', 'تمرير أفقي', 'على ٣٩٠ و٧٦٨ و١٠٢٤ و١٤٤٠'],
    ['28', 'فحص آلي', 'يمنع فقدان أي تخصيص']]
    .map(([n, t, d]) => `
        <div class="card" style="padding:34px 32px;">
          <div class="stat" style="color:${C.blue};">${n}</div>
          <div style="font-size:23px;font-weight:600;margin-top:14px;">${t}</div>
          <div class="cap" style="margin-top:6px;font-size:17px;">${d}</div>
        </div>`).join('')}
    </div>
    <div style="display:flex;gap:26px;margin-top:36px;">
      <div class="card" style="flex:1;padding:32px 36px;">
        <h3>يعمل بلوحة المفاتيح وحدها</h3>
        <p class="cap" style="margin-top:10px;font-size:19px;">
          رابط تخطٍّ إلى المحتوى، وتركيز محبوس داخل النوافذ، ويعود إلى زرّه عند الإغلاق.
          موظف الإدخال السريع لا يحتاج الفأرة.
        </p>
      </div>
      <div class="card" style="flex:1;padding:32px 36px;">
        <h3>يصمد أمام انقطاع الشبكة</h3>
        <p class="cap" style="margin-top:10px;font-size:19px;">
          إن تعذّر الاتصال بمصدر البيانات الحيّة، يواصل النظام العمل بالأرقام المخزَّنة
          بدل أن يتوقّف.
        </p>
      </div>
      <div class="card" style="flex:1;padding:32px 36px;">
        <h3>كل حركة لها سجل</h3>
        <p class="cap" style="margin-top:10px;font-size:19px;">
          سجل التدقيق يحفظ من فعل ماذا ومتى — مرجع عند الخلاف، ودليل عند المراجعة.
        </p>
      </div>
    </div>
  </div>
  <div class="pg"><span class="num">17</span></div>${mark()}
</div>`;

/* ============================ 18. CLOSE ============================ */
const s18 = () => `
<div class="slide dark">
  <div data-bleed="1" style="position:absolute;right:-200px;top:-160px;width:900px;height:900px;border-radius:50%;
              background:radial-gradient(circle at 50% 50%, rgba(0,184,217,.16), rgba(0,184,217,0) 62%);"></div>
  <img data-bleed="1" src="${LOGO_W}" style="position:absolute;left:130px;bottom:-70px;height:560px;opacity:.07;">
  <div class="pad" style="display:flex;flex-direction:column;justify-content:space-between;">
    <div>${lockDark}</div>
    <div>
      <div class="kicker">الخطوة التالية</div>
      <h2 style="margin-top:22px;font-size:62px;max-width:1400px;">
        نبدأ بخط واحد كامل: عرض سعر حقيقي يمشي حتى التسليم.
      </h2>
      <div style="display:flex;gap:24px;margin-top:56px;">
        ${[['١', 'تهيئة', 'العملاء والموردون وقائمة الأصناف والأدوار'],
    ['٢', 'تشغيل موازٍ', 'شحنة واحدة داخل النظام وخارجه معاً للمقارنة'],
    ['٣', 'اعتماد', 'إيقاف الجداول الموازية وتحويل الفريق كاملاً']]
    .map(([n, t, d]) => `
          <div style="flex:1;background:rgba(255,255,255,.06);border-radius:22px;padding:34px 36px;">
            <div class="num" style="font-size:17px;font-weight:700;color:${C.cyan};">المرحلة ${n}</div>
            <div style="font-size:29px;font-weight:600;margin-top:14px;">${t}</div>
            <div class="cap" style="margin-top:10px;font-size:19px;">${d}</div>
          </div>`).join('')}
      </div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div class="lead" style="font-size:25px;">شكراً لوقتكم — والنظام جاهز للعرض الحيّ الآن.</div>
      <div class="cap">شركة الاتحاد المحدودة</div>
    </div>
  </div>
</div>`;

module.exports = [
  { id: 1, html: s01, notes: 'افتتاح. الرسالة: النظام يربط الخوض بقوانزو بصحار بنزوى في مسار واحد. اذكر أن كل ما سيُعرض لقطات حقيقية من النظام العامل، لا تصاميم.' },
  { id: 2, html: s02, notes: 'ابدأ بالألم قبل الحل. اسأل الحضور: كم مرة عرفتم الهامش الحقيقي بعد إغلاق الصفقة؟ الفجوات الأربع هي ما سيعالجه باقي العرض.' },
  { id: 3, html: s03, notes: 'المفتاح الفكري للعرض: الشحنة كائن واحد. كل ما بعده تفصيل لهذه الجملة. لا تستعجل هذه الشريحة.' },
  { id: 4, html: s04, notes: 'أول لقطة حقيقية. أشر إلى قسم «يحتاج قرارك» — هذه هي الفكرة: العمل يأتي إليك. المؤشرات الثلاثة العلوية قابلة للتحرير يدوياً وتُحسب نسبة التغير تلقائياً.' },
  { id: 5, html: s05, notes: 'خريطة سريعة. لا تقرأ كل الأسماء — قل إن القائمة تتغير بتغير الدور، وسنرى ذلك بعد قليل في شريحة الأدوار.' },
  { id: 6, html: s06, notes: 'برج التحكم هو الشاشة التي يفتحها المدير صباحاً. الجملة المفتاحية: الهدف أن تفرغ الشاشة.' },
  { id: 7, html: s07, notes: 'أقوى شريحة في العرض. الدورة السبع مراحل بمسؤول معروف لكل مرحلة. اذكر مهلة ٤٨ ساعة وحد الخصم ٣٠٪ — هذه ضوابط مبنية في النظام لا تعليمات على ورق.' },
  { id: 8, html: s08, notes: 'شريحة المال. الفرق بين الربح المقدر والفعلي هو ما يقنع المالك. ركز على رسوم التخزين المتراكمة — غالباً هي المفاجأة.' },
  { id: 9, html: s09, notes: 'مرّ سريعاً على الأربع بطاقات. إن كان الحضور تشغيلياً، توسّع في تخطيط التحميل ومواعيد الاستلام.' },
  { id: 10, html: s10, notes: 'أظهر التقابل: الحاسب في مكتب قوانزو، والهاتف في يد عامل نزوى. النظام نفسه.' },
  { id: 11, html: s11, notes: 'هذه الشريحة تجيب سؤال «هل سيضيع موظفي في نظام كبير؟». الجواب: لا يرى إلا ما يخصه. اذكر أن موظف المبيعات لا يرى تكلفة المورد، وموظف الصين لا يرى سعر البيع.' },
  { id: 12, html: s12, notes: 'الصلاحيات مطبقة تقنياً لا موصوفة في سياسة. مفيدة جداً مع الإدارة المالية والمراجعين.' },
  { id: 13, html: s13, notes: 'البوابة تقلل المكالمات. اذكر أن كل استعلام يجيب عنه النظام هو مكالمة لم تصل للموظف.' },
  { id: 14, html: s14, notes: 'أربع لقطات هاتف حقيقية. الرسالة: ليست نسخة مختصرة — الثلاثون شاشة كلها تعمل. أشر إلى الشريط السفلي.' },
  { id: 15, html: s15, notes: 'تفاصيل صغيرة تبيع النظام للمستخدم اليومي. جرّب Ctrl+K حياً إن كان العرض على الجهاز.' },
  { id: 16, html: s16, notes: 'المقارنة. كن منصفاً: الأنظمة العامة قوية لكنها أفقية وتحتاج تكييفاً. ميزتنا التخصص في هذا الخط تحديداً.' },
  { id: 17, html: s17, notes: 'الجودة بالأرقام تميّزنا عن أي عرض منافس. هذه أرقام مقيسة آلياً في متصفح حقيقي على كل الصفحات، لا ادعاءات.' },
  { id: 18, html: s18, notes: 'اختم بخطة الثلاث مراحل واطلب قراراً: شحنة واحدة تجريبية. اعرض الانتقال إلى عرض حيّ على الجهاز.' },
];
