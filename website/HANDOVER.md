# ملف التسليم الكامل — شركة الاتحاد المحدودة (Etihad Limited)
CHINA — OMAN LOGISTICS · موقع تسويقي عام + نظام ERP داخلي خلف تسجيل الدخول

آخر تحديث: 2026-08-09

---

## 1. نظرة عامة

| البند | القيمة |
|---|---|
| النشاط | الشحن والتخليص الجمركي بين الصين وعُمان |
| الموقع المنشور | https://etihad-limited.lovable.app |
| المعاينة | https://id-preview--396349ed-b715-438b-aa02-35743b9cc5d8.lovable.app |
| البريد الرسمي | Shween90@hotmail.com |
| إنستقرام | https://www.instagram.com/etihad_limited (@etihad_limited) |
| اللغات | العربية (RTL, افتراضية) · English · 中文 |

الموقع العام موجّه للعملاء فقط: لا يُعرض فيه أي تفصيل تشغيلي داخلي (هوامش الربح، الخصومات، سياسات الاعتماد الداخلية، الهياكل الإدارية، سجلات التدقيق). هذا قرار ثابت يجب احترامه في أي تطوير لاحق.

---

## 2. التقنيات

- **TanStack Start v1** (React 19 + SSR) على **Vite 7**
- **Tailwind CSS v4** عبر `src/styles.css` (بدون tailwind.config.js)
- **shadcn/ui + Radix + lucide-react**
- **Supabase** (Lovable Cloud): Auth + Postgres + RLS
- **TypeScript** صارم، ESLint + Prettier
- بيئة التشغيل: Cloudflare Workers (edge) — لا تستخدم حزم Node-only في السيرفر

أوامر: `npm run dev` · `npm run build` · `npm run lint` · `npm run format`

---

## 3. نظام التصميم

الألوان (رموز دلالية في `src/styles.css`، ممنوع كتابة ألوان مباشرة في المكوّنات):

| الاسم | القيمة | الاستخدام |
|---|---|---|
| Navy | `#051C4A` | الأقسام الداكنة، الهيدر |
| Blue | `#0F4C81` | الروابط والأيقونات |
| Cyan | `#00B8D9` | خط المسار البحري، التمييز |
| Orange | `#F7931E` | تنبيه/تمييز ثانوي |
| Green | `#16A34A` | حالات النجاح |

- الخطوط: **IBM Plex Sans Arabic** للنص، **Inter** للأرقام واللاتيني (`.latin`, `.num`, `unicode-bidi: plaintext`).
- **قاعدة حرجة:** `letter-spacing` ممنوع على النص العربي (يكسر اتصال الحروف). القاعدة العامة `:lang(ar) { letter-spacing: normal }` مطبّقة؛ استخدم `.latin` فقط للكلمات اللاتينية.
- خصائص CSS منطقية دائمًا (`start/end`, `ms-/me-/ps-/pe-`) لدعم RTL/LTR.
- مسافات رأسية 96–120px بين الأقسام، زوايا 20px/24px، ظلال خفيفة (Linear/Stripe style).

---

## 4. بنية الملفات

```
src/
  routes/
    __root.tsx                 الجذر: الخطوط، JSON-LD، LanguageProvider، معالج الأخطاء
    index.tsx                  الصفحة الرئيسية العامة
    auth.tsx                   تسجيل الدخول (noindex)
    _authenticated/
      route.tsx                بوابة الحماية (تحويل لغير المسجلين)
      erp.tsx / erp.index.tsx / erp.$module.tsx
  components/
    home/       Hero, TrackingWidget, Services, Process, Network, WhyUs,
                Business, Capabilities, QuoteForm, CtaBand, SiteHeader, SiteFooter
    erp/        ErpShell, ModuleScreen, PortalScreen, Screens
    ui-kit/     Cta, Eyebrow, Logo, Reveal, SectionHeading, LanguageSwitcher (+DirArrow)
    RouteMap.tsx + route-map-data.json   خريطة المسار البحري (SVG، سواحل حقيقية + Catmull–Rom)
  i18n/         index.tsx (LanguageProvider/useI18n) + dict.ar.ts / dict.en.ts / dict.zh.ts
  erp/          modules.ts (سجل الوحدات + RBAC), pages.ts/json, quotes.json
  lib/          auth.ts, logistics.functions.ts, utils.ts
  content/site.ts   بيانات ثابتة (أيقونات، بريد، روابط)
  integrations/supabase/   ملفات مولّدة تلقائيًا — لا تُعدّل
```

### الصفحة الرئيسية بالترتيب
Header (زجاجي + مبدّل لغة، وفي الهاتف زر كرة أرضية مستقل + شريط لغة أعلى القائمة) → Hero (Navy، عنوان: «من الصين إلى عُمان- كل خطوة بإدارة واحدة») → شريط التتبع → الخدمات (6) → كيف نعمل (مراحل) → الشبكة (خريطة الصين–عُمان) → لماذا نحن → القطاعات (Pills) → بوابة العميل → CTA → Footer.

---

## 5. i18n

- `LanguageProvider` يخزّن اللغة في `localStorage` بمفتاح `etihad.lang` (تُقرأ بعد الترطيب لتفادي عدم تطابق SSR).
- يحدّث `html.lang` و`html.dir` و`document.title` و`meta[name=description]` و`og:locale`.
- كل النصوص تأتي من القواميس الثلاثة — **ممنوع** كتابة نص ثابت داخل المكوّنات.
- عند إضافة نص جديد: أضِفه في `dict.ar.ts` (المصدر للنوع `Dict`) ثم في `en` و`zh`.

---

## 6. المصادقة والصلاحيات

- الأدوار: `app_role` enum = `admin | staff | customer`، مخزّنة في جدول منفصل `public.user_roles` (ممنوع تخزين الدور على جدول المستخدمين/الملف الشخصي).
- `public.has_role(_user_id, _role)` دالة SECURITY DEFINER تُستخدم داخل سياسات RLS؛ محصورة بحيث تُبلّغ فقط عن أدوار المستخدم الحالي.
- Trigger `handle_new_user_role()` يمنح الدور `customer` تلقائيًا لأي حساب جديد (منفّذ لـ service_role فقط).
- بعد تسجيل الدخول يوجّه `src/lib/auth.ts` المستخدم حسب دوره إلى الوحدة الافتراضية داخل `/erp`.
- حساب مدير النظام: **محجوب من هذا المستودع العام** — بيانات الحساب لدى المالك.
  (نُشر هذا المستودع علناً، وذكر بريد حساب المدير فيه يسلّم نصف بيانات الاعتماد
  لأي قارئ. يُنصح بتغيير كلمة المرور بعد الإطلاق وتفعيل التحقق بخطوتين.)
- مسارات `/auth` و`/erp` عليها `noindex`.

### الجداول
| الجدول | الوصف | RLS |
|---|---|---|
| `user_roles` | ربط المستخدم بالدور | قراءة الذات + إدارة كاملة للـ admin |
| `shipments` | الشحنات وحالاتها | العميل يقرأ شحناته فقط؛ الكتابة من السيرفر |
| `shipment_events` | أحداث تتبّع الشحنة | قراءة أحداث الشحنات المرئية |
| `quote_requests` | طلبات عروض الأسعار | قراءة/تحديث للموظفين؛ الإدخال من السيرفر |

كل جدول جديد يجب أن يتبعه في نفس الـ migration: `GRANT` ثم `ENABLE ROW LEVEL SECURITY` ثم السياسات.

---

## 7. نظام ERP الداخلي

`src/erp/modules.ts` هو المرجع الوحيد للوحدات والصلاحيات — 26 وحدة موزّعة على مجموعات:
البداية · المبيعات · التوريد في الصين · الشحن والتخليص · المستودعات · المالية · المعرفة · النظام.

الأدوار: `OPS = admin+staff` لأغلب الوحدات التشغيلية، `ADMIN` فقط للمالية والتحليلات والنظام، `ALL` لبوابة العميل.
التوجيه ديناميكي عبر `/erp/$module`، والواجهة عبر `ErpShell` (سايدبار + مجموعات) و`ModuleScreen`.

---

## 8. حالة الجاهزية

منجز: تصميم كامل ثلاثي اللغات · تتبع الشحنات مع حالة «غير موجود» · نموذج عرض السعر مع تحقق · خريطة المسار · SEO (عناوين ووصف لكل مسار + Organization JSON-LD + robots) · إصلاح اتصال الحروف العربية · مبدّل اللغة في الهاتف · معالجة نتائج الفحص الأمني.

مقترح لاحقًا:
1. تعبئة وحدات ERP ببيانات حقيقية بدل الشاشات النموذجية.
2. إضافة رقم هاتف رسمي (حاليًا البريد فقط).
3. ربط المشروع بـ GitHub (Project Settings → GitHub) لفتحه في أي أداة خارجية.
4. تغيير كلمة مرور حساب المدير وإضافة حسابات الموظفين.
5. ربط نطاق مخصّص.

---

## 9. قواعد يجب عدم كسرها

1. لا معلومات داخلية على الموقع العام (هوامش، خصومات، SLA داخلية، هياكل إدارية، سجلات تدقيق).
2. لا ألوان مباشرة في المكوّنات — رموز دلالية فقط.
3. لا `letter-spacing` على العربية.
4. لا تعديل ملفات `src/integrations/supabase/*` أو `.env` (مولّدة تلقائيًا).
5. لا نصوص ثابتة خارج ملفات i18n.
6. لا خصائص CSS اتجاهية (left/right) — منطقية فقط.
7. الأدوار في جدول منفصل دائمًا.
