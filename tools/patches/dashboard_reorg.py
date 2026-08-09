#!/usr/bin/env python3
"""Regroup the dashboard's ten sections into five labeled zones.

Measured problem: the dashboard stacked ten sections in an order that mixed
themes rather than grouping them -- a financial chart sat next to a warehouse
donut (both under one "split" row), then two personal-planning widgets, then
a second financial chart paired with a container-status donut, then a
warehouse heatmap paired with a shipments list. Financial charts, warehouse
widgets and shipment widgets were each split across two or three unrelated
rows instead of sitting together.

This reorders and re-pairs the *same* widgets -- nothing here rewrites a
chart or table, every sc-for/sc-if binding is untouched -- into five zones,
each with its own heading, in decreasing order of urgency:

  1. (unlabeled, unchanged) greeting/actions, six KPIs, needs-your-decision
  2. Shipments & Containers: the pipeline strip, then container status +
     recent shipments
  3. Financial Performance: revenue & margin chart + revenue vs expenses
  4. Warehouse Operations: capacity donut + activity heatmap
  5. Your Work Today: tasks + week view, quick actions, pending quotes +
     activity log

Verified losslessly against the pre-patch content before writing this file:
every one of the ten original section headings appears the same number of
times in the new arrangement as the old one, and open/close <div> counts
balance (84/84 old, 88/88 new -- the difference is exactly the four new
zone-heading divs).

Run against the inner document, not the bundle:

    python3 tools/patches/dashboard_reorg.py   # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

ZONE_DICT_OLD = "    lang_label: { ar: 'اللغة', en: 'Language', zh: '语言' },\n  };"
ZONE_DICT_NEW = (
    ZONE_DICT_OLD[:-len("\n  };")]
    + "\n    zone_shipments: { ar: 'الشحنات والحاويات', en: 'Shipments & Containers', zh: '货运与集装箱' },"
    + "\n    zone_financial: { ar: 'الأداء المالي', en: 'Financial Performance', zh: '财务表现' },"
    + "\n    zone_warehouse: { ar: 'عمليات المستودعات', en: 'Warehouse Operations', zh: '仓库运营' },"
    + "\n    zone_your_work: { ar: 'مهامك اليوم', en: 'Your Work Today', zh: '今日待办' },"
    + "\n  };"
)

PROPS_OLD = "      exportLabel: this.t('btn_export'), newQuoteLabel: this.t('btn_new_quote'),"
PROPS_NEW = (
    PROPS_OLD
    + "\n      zoneShipments: this.t('zone_shipments'), zoneFinancial: this.t('zone_financial'),"
    + "\n      zoneWarehouse: this.t('zone_warehouse'), zoneYourWork: this.t('zone_your_work'),"
)

DASH_OLD = """

          <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; flex-wrap: wrap; margin-bottom: 28px;">
            <div>
              <h1 style="font-size: 27px; font-weight: 600; margin: 0; letter-spacing: -0.01em;">{{ greeting }}</h1>
              <p style="font-size: 14px; color: var(--t2); margin: 8px 0 0;">{{ todayLine }}</p>
            </div>
            <div style="display: flex; gap: 10px;">
              <button sc-camel-on-click="{{ exportPdf }}" style="{{ btnGhost }}"><span style="{{ downloadIcon }}"></span>{{ exportLabel }}</button>
              <button sc-camel-on-click="{{ newQuote }}" style="{{ btnPrimary }}"><span style="{{ plusIcon }}"></span>{{ newQuoteLabel }}</button>
            </div>
          </div>

          <div data-grid="4" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
            <sc-for list="{{ kpis }}" as="k" hint-placeholder-count="6">
              <button sc-camel-on-click="{{ k.go }}" style="text-align: right; font-family: inherit; color: var(--t1); cursor: pointer; background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 22px; transition: border-color 150ms ease, transform 150ms ease;" style-hover="border-color: var(--p-text); transform: translateY(-2px);">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">
                  <div style="font-size: 12.5px; color: var(--t2); line-height: 1.4; display: flex; align-items: center; gap: 6px;">
                    {{ k.label }}
                    <sc-if value="{{ k.editKey }}" hint-placeholder-val="{{ true }}">
                      <span sc-camel-on-click="{{ k.editGo }}" title="تعديل يدوي" style="{{ k.editSt }}" style-hover="background: var(--bg); color: var(--p-text);"><span style="{{ k.editIcon }}"></span></span>
                    </sc-if>
                  </div>
                  <div style="{{ k.iwrap }}"><span style="{{ k.ist }}"></span></div>
                </div>
                <div style="font-size: 32px; font-weight: 600; letter-spacing: -0.02em; margin-top: 14px; font-feature-settings: 'tnum'; direction: ltr; unicode-bidi: plaintext; text-align: right;">{{ k.value }}</div>
                <div style="display: flex; align-items: center; gap: 8px; margin-top: 12px;">
                  <span style="{{ k.dst }}">{{ k.delta }}</span>
                  <span style="font-size: 12px; color: var(--t2);">{{ k.sub }}</span>
                </div>
                <svg aria-hidden="true" focusable="false" sc-camel-view-box="0 0 200 34" sc-camel-preserve-aspect-ratio="none" style="width: 100%; height: 34px; margin-top: 14px; overflow: visible;">
                  <polyline points="{{ k.spark }}" fill="none" stroke="{{ k.sparkColor }}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></polyline>
                </svg>
              </button>
            </sc-for>
          </div>

          <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
              <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--sem-action);"></span>
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">{{ alertCount }}</div>
            </div>
            <div data-grid="2" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
              <sc-for list="{{ alerts }}" as="a" hint-placeholder-count="4">
                <button sc-camel-on-click="{{ a.go }}" style="{{ a.wrap }}" style-hover="box-shadow: var(--sh-md);">
                  <span style="{{ a.iwrap }}"><span style="{{ a.ist }}"></span></span>
                  <span style="flex: 1; min-width: 0;">
                    <span style="display: block; font-size: 13.5px; font-weight: 600; line-height: 1.55;">{{ a.t }}</span>
                    <span style="display: block; font-size: 12.5px; color: var(--t2); margin-top: 5px; line-height: 1.65;">{{ a.d }}</span>
                    <span style="{{ a.ctaSt }}">{{ a.cta }} ←</span>
                  </span>
                </button>
              </sc-for>
            </div>
          </div>

          <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 22px 24px; margin-bottom: 24px;">
            <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">خط سير الحاويات</div>
            <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 20px;">اللون يتدرّج من الخامل إلى الحركة إلى الجاهز للاستلام</div>
            <div data-grid="7" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(108px, 1fr)); gap: 14px;">
              <sc-for list="{{ pipeline }}" as="p" hint-placeholder-count="7">
                <button sc-camel-on-click="{{ p.go }}" style="{{ p.st }}" style-hover="opacity: 0.72;">
                  <div style="{{ p.nSt }}">{{ p.n }}</div>
                  <div style="font-size: 12px; color: var(--t2); margin-top: 8px; line-height: 1.45;">{{ p.t }}</div>
                </button>
              </sc-for>
            </div>
          </div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 20px; margin-bottom: 24px; align-items: stretch;">
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin-bottom: 22px;">
                <div>
                  <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">الإيراد وهامش الربح</div>
                  <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px;">آخر ١٢ شهراً · ريال عُماني</div>
                </div>
                <div style="display: flex; gap: 4px; background: var(--bg); padding: 4px; border-radius: 10px;">
                  <sc-for list="{{ rangeTabs }}" as="t" hint-placeholder-count="3">
                    <button sc-camel-on-click="{{ t.go }}" style="{{ t.st }}">{{ t.t }}</button>
                  </sc-for>
                </div>
              </div>
              <svg role="img" aria-label="رسم بياني: الإيراد وهامش الربح — آخر ١٢ شهراً بالريال العُماني" sc-camel-view-box="0 0 740 250" style="width: 100%; height: auto; overflow: visible;">
                <defs>
                  <linearGradient id="etihadArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="var(--p)" stop-opacity="0.22"></stop>
                    <stop offset="100%" stop-color="var(--p)" stop-opacity="0"></stop>
                  </linearGradient>
                </defs>
                <sc-for list="{{ gridLines }}" as="g" hint-placeholder-count="5">
                  <line x1="0" y1="{{ g.y }}" x2="740" y2="{{ g.y }}" stroke="var(--bd)" stroke-width="1"></line>
                </sc-for>
                <sc-for list="{{ gridLines }}" as="g" hint-placeholder-count="5">
                  <text x="746" y="{{ g.ty }}" font-size="10.5" fill="var(--t3)" font-family="Inter, sans-serif">{{ g.l }}</text>
                </sc-for>
                <polygon points="{{ areaPoly }}" fill="url(#etihadArea)"></polygon>
                <polyline points="{{ revLine }}" fill="none" stroke="var(--p)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></polyline>
                <polyline points="{{ marginLine }}" fill="none" stroke="var(--p2)" stroke-width="2" stroke-dasharray="5 5" stroke-linecap="round"></polyline>
                <sc-for list="{{ points }}" as="p" hint-placeholder-count="12">
                  <circle cx="{{ p.x }}" cy="{{ p.y }}" r="{{ p.r }}" fill="var(--card)" stroke="var(--p)" stroke-width="2.5"></circle>
                </sc-for>
                <sc-for list="{{ points }}" as="p" hint-placeholder-count="12">
                  <text x="{{ p.x }}" y="242" text-anchor="middle" font-size="11" fill="var(--t3)">{{ p.m }}</text>
                </sc-for>
              </svg>
              <div style="display: flex; gap: 20px; margin-top: 16px; font-size: 12.5px; color: var(--t2);">
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 14px; height: 3px; border-radius: 2px; background: var(--p);"></span>الإيراد</span>
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 14px; height: 3px; border-radius: 2px; background: var(--p2);"></span>هامش الربح ٪</span>
              </div>
            </div>

            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px; display: flex; flex-direction: column;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">سعة المستودعات</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px;">قوانزو ونزوى — الإشغال الحالي</div>
              <div style="display: flex; justify-content: center; padding: 18px 0 6px;">
                <svg role="img" aria-label="رسم بياني: سعة المستودعات — الإشغال الحالي في قوانزو ونزوى" sc-camel-view-box="0 0 180 180" style="width: 172px; height: 172px;">
                  <circle cx="90" cy="90" r="70" fill="none" stroke="var(--bd)" stroke-width="16"></circle>
                  <circle cx="90" cy="90" r="70" fill="none" stroke="var(--p)" stroke-width="16" stroke-linecap="round" stroke-dasharray="{{ donutA }}" transform="rotate(-90 90 90)"></circle>
                  <circle cx="90" cy="90" r="50" fill="none" stroke="var(--bd)" stroke-width="14"></circle>
                  <circle cx="90" cy="90" r="50" fill="none" stroke="var(--p2)" stroke-width="14" stroke-linecap="round" stroke-dasharray="{{ donutB }}" transform="rotate(-90 90 90)"></circle>
                  <text x="90" y="86" text-anchor="middle" font-size="28" font-weight="600" fill="var(--t1)" font-family="Inter, sans-serif">71%</text>
                  <text x="90" y="106" text-anchor="middle" font-size="11" fill="var(--t2)">إجمالي الإشغال</text>
                </svg>
              </div>
              <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 8px;">
                <sc-for list="{{ capacity }}" as="c" hint-placeholder-count="2">
                  <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 7px;">
                      <span style="display: flex; align-items: center; gap: 8px;"><span style="{{ c.dot }}"></span>{{ c.t }}</span>
                      <span style="font-weight: 600; font-feature-settings: 'tnum';">{{ c.v }}</span>
                    </div>
                    <div style="height: 7px; background: var(--bg); border-radius: 4px; overflow: hidden;">
                      <div style="{{ c.bar }}"></div>
                    </div>
                  </div>
                </sc-for>
              </div>
            </div>
          </div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 20px; margin-bottom: 24px; align-items: start;">
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">مهام اليوم</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 20px;">خمس مهام مفتوحة على اسمك أو على فريقك</div>
              <div style="display: flex; flex-direction: column; gap: 4px;">
                <sc-for list="{{ tasks }}" as="t" hint-placeholder-count="5">
                  <button sc-camel-on-click="{{ t.go }}" style="display: flex; align-items: flex-start; gap: 12px; width: 100%; padding: 11px 12px; background: transparent; border: 0; border-radius: var(--r-xs); cursor: pointer; text-align: right; color: var(--t1);" style-hover="background: var(--bg);">
                    <span style="{{ t.dot }}"></span>
                    <span style="flex: 1; min-width: 0;">
                      <span style="{{ t.tSt }}">{{ t.t }}</span>
                      <span style="display: block; font-size: 11.5px; color: var(--t2); margin-top: 3px;">{{ t.d }}</span>
                    </span>
                  </button>
                </sc-for>
              </div>
            </div>
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">أسبوع العمل</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 20px;">الشريط الملوّن = موعد مرتبط بشحنة أو دفعة</div>
              <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px;">
                <sc-for list="{{ week }}" as="w" hint-placeholder-count="7">
                  <div style="{{ w.st }}">
                    <span style="{{ w.dSt }}">{{ w.d }}</span>
                    <span style="{{ w.nSt }}">{{ w.n }}</span>
                    <span style="{{ w.pip }}"></span>
                  </div>
                </sc-for>
              </div>
              <div style="display: flex; align-items: center; gap: 10px; margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--bd);">
                <span style="width: 34px; height: 34px; flex: 0 0 34px; border-radius: 10px; background: rgba(247,147,30,0.16); color: var(--badge-action-fg); display: grid; place-items: center;"><span style="{{ calIcon }}"></span></span>
                <span style="flex: 1;">
                  <span style="display: block; font-size: 13px; font-weight: 600;">وصول CTR-2026-0074</span>
                  <span style="display: block; font-size: 11.5px; color: var(--t2); margin-top: 2px;">الأحد ٩ أغسطس · مستودع نزوى</span>
                </span>
              </div>
            </div>
          </div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 20px; margin-bottom: 24px; align-items: start;">
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">الإيراد مقابل المصروفات</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px; margin-bottom: 20px;">ستة أشهر · الخط الأزرق هو صافي الربح</div>
              <svg role="img" aria-label="رسم بياني: الإيراد مقابل المصروفات على ستة أشهر، والخط الأزرق هو صافي الربح" sc-camel-view-box="0 0 700 220" style="width: 100%; height: auto; overflow: visible;">
                <sc-for list="{{ gridLines }}" as="g" hint-placeholder-count="5">
                  <line x1="0" y1="{{ g.y }}" x2="700" y2="{{ g.y }}" stroke="var(--bd)" stroke-width="1"></line>
                </sc-for>
                <sc-for list="{{ expBars }}" as="b" hint-placeholder-count="12">
                  <rect x="{{ b.x }}" y="{{ b.y }}" width="{{ b.w }}" height="{{ b.h }}" rx="4" fill="{{ b.fill }}"></rect>
                </sc-for>
                <polyline points="{{ profitPts }}" fill="none" stroke="var(--sem-transit)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></polyline>
                <sc-for list="{{ expLabels }}" as="l" hint-placeholder-count="6">
                  <text x="{{ l.x }}" y="212" text-anchor="middle" font-size="11" fill="var(--t3)">{{ l.m }}</text>
                </sc-for>
              </svg>
              <div style="display: flex; gap: 20px; margin-top: 16px; font-size: 12.5px; color: var(--t2); flex-wrap: wrap;">
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: var(--sem-money);"></span>الإيراد</span>
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: var(--sem-late);"></span>المصروفات</span>
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 14px; height: 3px; border-radius: 2px; background: var(--sem-transit);"></span>صافي الربح</span>
              </div>
            </div>

            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">حالة الحاويات</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px;">توزيع الأسطول النشط الآن</div>
              <div style="display: flex; justify-content: center; padding: 16px 0 4px;">
                <svg role="img" aria-label="رسم بياني: حالة الحاويات — توزيع الأسطول النشط" sc-camel-view-box="0 0 160 160" style="width: 160px; height: 160px;">
                  <sc-for list="{{ csArcs }}" as="a" hint-placeholder-count="4">
                    <circle cx="80" cy="80" r="62" fill="none" stroke="{{ a.c }}" stroke-width="17" stroke-dasharray="{{ a.dash }}" stroke-dashoffset="{{ a.off }}" transform="rotate(-90 80 80)"></circle>
                  </sc-for>
                  <text x="80" y="76" text-anchor="middle" font-size="30" font-weight="600" fill="var(--t1)" font-family="Inter, sans-serif">{{ csTotal }}</text>
                  <text x="80" y="96" text-anchor="middle" font-size="11" fill="var(--t2)">حاوية نشطة</text>
                </svg>
              </div>
              <div style="display: flex; flex-direction: column; gap: 11px; margin-top: 10px;">
                <sc-for list="{{ csLegend }}" as="l" hint-placeholder-count="4">
                  <div style="display: flex; align-items: center; gap: 9px; font-size: 13px;">
                    <span style="{{ l.dot }}"></span>
                    <span style="flex: 1; color: var(--t2);">{{ l.t }}</span>
                    <span style="font-weight: 600; font-feature-settings: 'tnum';">{{ l.n }}</span>
                  </div>
                </sc-for>
              </div>
            </div>
          </div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1fr 1.3fr; gap: 20px; margin-bottom: 24px; align-items: start;">
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">كثافة حركة المستودع</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px; margin-bottom: 20px;">أغمق = حركة أكثر · اضغط أي خانة</div>
              <div data-heatgrid="1" style="display: grid; grid-template-columns: 46px repeat(5, 1fr); gap: 5px; align-items: center;">
                <span></span>
                <sc-for list="{{ heatHours }}" as="h" hint-placeholder-count="5">
                  <span style="font-size: 10.5px; color: var(--t3); text-align: center;">{{ h }}</span>
                </sc-for>
              </div>
              <div data-heatgrid="1" style="display: grid; grid-template-columns: 46px repeat(5, 1fr); gap: 5px; margin-top: 5px; align-items: center;">
                <sc-for list="{{ heatRows }}" as="r" hint-placeholder-count="5">
                  <span style="font-size: 11px; color: var(--t2); white-space: nowrap;">{{ r.d }}</span>
                  <sc-for list="{{ r.cells }}" as="c" hint-placeholder-count="5">
                    <button sc-camel-on-click="{{ c.go }}" title="{{ c.title }}" style="{{ c.st }}"></button>
                  </sc-for>
                </sc-for>
              </div>
            </div>

            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); overflow: hidden;">
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 22px 24px 14px;">
                <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">آخر الشحنات</div>
                <button sc-camel-on-click="{{ goShipping }}" style="background: transparent; border: 0; cursor: pointer; font-family: inherit; font-size: 13px; color: var(--p-text); font-weight: 500; padding: 5px 6px; margin: -5px -6px;">عرض الكل ←</button>
              </div>
              <div style="display: flex; flex-direction: column; padding: 0 10px 12px;">
                <sc-for list="{{ recent }}" as="r" hint-placeholder-count="4">
                  <button sc-camel-on-click="{{ r.go }}" style="display: flex; align-items: center; gap: 12px; padding: 12px 14px; background: transparent; border: 0; border-radius: var(--r-xs); cursor: pointer; text-align: right; color: var(--t1);" style-hover="background: var(--bg);">
                    <span style="flex: 1; min-width: 0;">
                      <span style="display: block; font-size: 13.5px; font-weight: 600; font-family: Inter, sans-serif;">{{ r.id }}</span>
                      <span style="display: block; font-size: 12px; color: var(--t2); margin-top: 3px;">{{ r.c }} · {{ r.t }}</span>
                    </span>
                    <span style="{{ r.badge }}">{{ r.s }}</span>
                  </button>
                </sc-for>
              </div>
            </div>
          </div>

          <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px; margin-bottom: 24px;">
            <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">إجراءات سريعة</div>
            <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 18px;">المهام الأكثر تكراراً لدورك الحالي</div>
            <div data-grid="4" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
              <sc-for list="{{ quickActions }}" as="q" hint-placeholder-count="4">
                <button sc-camel-on-click="{{ q.go }}" style="display: flex; align-items: center; gap: 13px; padding: 16px; background: var(--bg); border: 1px solid var(--bd); border-radius: var(--r-sm); cursor: pointer; text-align: right; color: var(--t1); transition: all 150ms ease;" style-hover="border-color: var(--p-text); box-shadow: var(--sh);">
                  <span style="{{ q.iwrap }}"><span style="{{ q.ist }}"></span></span>
                  <span style="flex: 1; min-width: 0;">
                    <span style="display: block; font-size: 13.5px; font-weight: 600;">{{ q.t }}</span>
                    <span style="display: block; font-size: 11.5px; color: var(--t2); margin-top: 3px;">{{ q.d }}</span>
                  </span>
                </button>
              </sc-for>
            </div>
          </div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 20px;">
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); overflow: hidden;">
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 20px 24px 16px;">
                <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">عروض أسعار تنتظرك</div>
                <button sc-camel-on-click="{{ goQuotes }}" style="background: transparent; border: 0; cursor: pointer; font-size: 13px; color: var(--p-text); font-weight: 500; padding: 5px 6px; margin: -5px -6px;">عرض الكل ←</button>
              </div>
              <sc-raw-table data-stack="1" style="width: 100%; border-collapse: collapse;">
                <sc-raw-thead>
                  <sc-raw-tr>
                    <sc-for list="{{ quoteMini.head }}" as="h" hint-placeholder-count="4">
                      <sc-raw-th scope="col" style="{{ thSt }}">{{ h }}</sc-raw-th>
                    </sc-for>
                  </sc-raw-tr>
                </sc-raw-thead>
                <sc-raw-tbody>
                  <sc-for list="{{ quoteMini.rows }}" as="r" hint-placeholder-count="5">
                    <sc-raw-tr sc-camel-on-click="{{ r.go }}" style="cursor: pointer;" style-hover="background: var(--bg);">
                      <sc-for list="{{ r.cells }}" as="c" hint-placeholder-count="4">
                        <sc-raw-td data-label="{{ c.lbl }}" style="{{ c.st }}"><span style="{{ c.bst }}">{{ c.v }}</span></sc-raw-td>
                      </sc-for>
                    </sc-raw-tr>
                  </sc-for>
                </sc-raw-tbody>
              </sc-raw-table>
            </div>

            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 22px 24px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 20px;">سجل النشاط</div>
              <div style="display: flex; flex-direction: column;">
                <sc-for list="{{ activity }}" as="a" hint-placeholder-count="6">
                  <div style="display: flex; gap: 14px;">
                    <div style="display: flex; flex-direction: column; align-items: center; flex: 0 0 auto;">
                      <span style="{{ a.dot }}"></span>
                      <span style="{{ a.line }}"></span>
                    </div>
                    <div style="padding-bottom: 18px; min-width: 0;">
                      <div style="font-size: 13.5px; line-height: 1.6;">{{ a.t }}</div>
                      <div style="font-size: 11.5px; color: var(--t2); margin-top: 4px;">{{ a.who }} · {{ a.time }}</div>
                    </div>
                  </div>
                </sc-for>
              </div>
            </div>
          </div>
"""

DASH_NEW = """

          <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; flex-wrap: wrap; margin-bottom: 28px;">
            <div>
              <h1 style="font-size: 27px; font-weight: 600; margin: 0; letter-spacing: -0.01em;">{{ greeting }}</h1>
              <p style="font-size: 14px; color: var(--t2); margin: 8px 0 0;">{{ todayLine }}</p>
            </div>
            <div style="display: flex; gap: 10px;">
              <button sc-camel-on-click="{{ exportPdf }}" style="{{ btnGhost }}"><span style="{{ downloadIcon }}"></span>{{ exportLabel }}</button>
              <button sc-camel-on-click="{{ newQuote }}" style="{{ btnPrimary }}"><span style="{{ plusIcon }}"></span>{{ newQuoteLabel }}</button>
            </div>
          </div>

          <div data-grid="4" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
            <sc-for list="{{ kpis }}" as="k" hint-placeholder-count="6">
              <button sc-camel-on-click="{{ k.go }}" style="text-align: right; font-family: inherit; color: var(--t1); cursor: pointer; background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 22px; transition: border-color 150ms ease, transform 150ms ease;" style-hover="border-color: var(--p-text); transform: translateY(-2px);">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">
                  <div style="font-size: 12.5px; color: var(--t2); line-height: 1.4; display: flex; align-items: center; gap: 6px;">
                    {{ k.label }}
                    <sc-if value="{{ k.editKey }}" hint-placeholder-val="{{ true }}">
                      <span sc-camel-on-click="{{ k.editGo }}" title="تعديل يدوي" style="{{ k.editSt }}" style-hover="background: var(--bg); color: var(--p-text);"><span style="{{ k.editIcon }}"></span></span>
                    </sc-if>
                  </div>
                  <div style="{{ k.iwrap }}"><span style="{{ k.ist }}"></span></div>
                </div>
                <div style="font-size: 32px; font-weight: 600; letter-spacing: -0.02em; margin-top: 14px; font-feature-settings: 'tnum'; direction: ltr; unicode-bidi: plaintext; text-align: right;">{{ k.value }}</div>
                <div style="display: flex; align-items: center; gap: 8px; margin-top: 12px;">
                  <span style="{{ k.dst }}">{{ k.delta }}</span>
                  <span style="font-size: 12px; color: var(--t2);">{{ k.sub }}</span>
                </div>
                <svg aria-hidden="true" focusable="false" sc-camel-view-box="0 0 200 34" sc-camel-preserve-aspect-ratio="none" style="width: 100%; height: 34px; margin-top: 14px; overflow: visible;">
                  <polyline points="{{ k.spark }}" fill="none" stroke="{{ k.sparkColor }}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></polyline>
                </svg>
              </button>
            </sc-for>
          </div>

          <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
              <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--sem-action);"></span>
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">{{ alertCount }}</div>
            </div>
            <div data-grid="2" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
              <sc-for list="{{ alerts }}" as="a" hint-placeholder-count="4">
                <button sc-camel-on-click="{{ a.go }}" style="{{ a.wrap }}" style-hover="box-shadow: var(--sh-md);">
                  <span style="{{ a.iwrap }}"><span style="{{ a.ist }}"></span></span>
                  <span style="flex: 1; min-width: 0;">
                    <span style="display: block; font-size: 13.5px; font-weight: 600; line-height: 1.55;">{{ a.t }}</span>
                    <span style="display: block; font-size: 12.5px; color: var(--t2); margin-top: 5px; line-height: 1.65;">{{ a.d }}</span>
                    <span style="{{ a.ctaSt }}">{{ a.cta }} ←</span>
                  </span>
                </button>
              </sc-for>
            </div>
          </div>

          <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 22px 24px; margin-bottom: 24px;">
            <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">خط سير الحاويات</div>
            <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 20px;">اللون يتدرّج من الخامل إلى الحركة إلى الجاهز للاستلام</div>
            <div data-grid="7" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(108px, 1fr)); gap: 14px;">
              <sc-for list="{{ pipeline }}" as="p" hint-placeholder-count="7">
                <button sc-camel-on-click="{{ p.go }}" style="{{ p.st }}" style-hover="opacity: 0.72;">
                  <div style="{{ p.nSt }}">{{ p.n }}</div>
                  <div style="font-size: 12px; color: var(--t2); margin-top: 8px; line-height: 1.45;">{{ p.t }}</div>
                </button>
              </sc-for>
            </div>
          </div>

          <div role="heading" aria-level="2" style="margin: 8px 0 18px; padding-top: 30px; border-top: 1px solid var(--bd); font-size: 12.5px; font-weight: 700; letter-spacing: 0.06em; color: var(--t3);">{{ zoneShipments }}</div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; align-items: start;">
                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">حالة الحاويات</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px;">توزيع الأسطول النشط الآن</div>
              <div style="display: flex; justify-content: center; padding: 16px 0 4px;">
                <svg role="img" aria-label="رسم بياني: حالة الحاويات — توزيع الأسطول النشط" sc-camel-view-box="0 0 160 160" style="width: 160px; height: 160px;">
                  <sc-for list="{{ csArcs }}" as="a" hint-placeholder-count="4">
                    <circle cx="80" cy="80" r="62" fill="none" stroke="{{ a.c }}" stroke-width="17" stroke-dasharray="{{ a.dash }}" stroke-dashoffset="{{ a.off }}" transform="rotate(-90 80 80)"></circle>
                  </sc-for>
                  <text x="80" y="76" text-anchor="middle" font-size="30" font-weight="600" fill="var(--t1)" font-family="Inter, sans-serif">{{ csTotal }}</text>
                  <text x="80" y="96" text-anchor="middle" font-size="11" fill="var(--t2)">حاوية نشطة</text>
                </svg>
              </div>
              <div style="display: flex; flex-direction: column; gap: 11px; margin-top: 10px;">
                <sc-for list="{{ csLegend }}" as="l" hint-placeholder-count="4">
                  <div style="display: flex; align-items: center; gap: 9px; font-size: 13px;">
                    <span style="{{ l.dot }}"></span>
                    <span style="flex: 1; color: var(--t2);">{{ l.t }}</span>
                    <span style="font-weight: 600; font-feature-settings: 'tnum';">{{ l.n }}</span>
                  </div>
                </sc-for>
              </div>
            </div>

                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); overflow: hidden;">
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 22px 24px 14px;">
                <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">آخر الشحنات</div>
                <button sc-camel-on-click="{{ goShipping }}" style="background: transparent; border: 0; cursor: pointer; font-family: inherit; font-size: 13px; color: var(--p-text); font-weight: 500; padding: 5px 6px; margin: -5px -6px;">عرض الكل ←</button>
              </div>
              <div style="display: flex; flex-direction: column; padding: 0 10px 12px;">
                <sc-for list="{{ recent }}" as="r" hint-placeholder-count="4">
                  <button sc-camel-on-click="{{ r.go }}" style="display: flex; align-items: center; gap: 12px; padding: 12px 14px; background: transparent; border: 0; border-radius: var(--r-xs); cursor: pointer; text-align: right; color: var(--t1);" style-hover="background: var(--bg);">
                    <span style="flex: 1; min-width: 0;">
                      <span style="display: block; font-size: 13.5px; font-weight: 600; font-family: Inter, sans-serif;">{{ r.id }}</span>
                      <span style="display: block; font-size: 12px; color: var(--t2); margin-top: 3px;">{{ r.c }} · {{ r.t }}</span>
                    </span>
                    <span style="{{ r.badge }}">{{ r.s }}</span>
                  </button>
                </sc-for>
              </div>
            </div>
          </div>

          <div role="heading" aria-level="2" style="margin: 8px 0 18px; padding-top: 30px; border-top: 1px solid var(--bd); font-size: 12.5px; font-weight: 700; letter-spacing: 0.06em; color: var(--t3);">{{ zoneFinancial }}</div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; align-items: start;">
                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin-bottom: 22px;">
                <div>
                  <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">الإيراد وهامش الربح</div>
                  <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px;">آخر ١٢ شهراً · ريال عُماني</div>
                </div>
                <div style="display: flex; gap: 4px; background: var(--bg); padding: 4px; border-radius: 10px;">
                  <sc-for list="{{ rangeTabs }}" as="t" hint-placeholder-count="3">
                    <button sc-camel-on-click="{{ t.go }}" style="{{ t.st }}">{{ t.t }}</button>
                  </sc-for>
                </div>
              </div>
              <svg role="img" aria-label="رسم بياني: الإيراد وهامش الربح — آخر ١٢ شهراً بالريال العُماني" sc-camel-view-box="0 0 740 250" style="width: 100%; height: auto; overflow: visible;">
                <defs>
                  <linearGradient id="etihadArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="var(--p)" stop-opacity="0.22"></stop>
                    <stop offset="100%" stop-color="var(--p)" stop-opacity="0"></stop>
                  </linearGradient>
                </defs>
                <sc-for list="{{ gridLines }}" as="g" hint-placeholder-count="5">
                  <line x1="0" y1="{{ g.y }}" x2="740" y2="{{ g.y }}" stroke="var(--bd)" stroke-width="1"></line>
                </sc-for>
                <sc-for list="{{ gridLines }}" as="g" hint-placeholder-count="5">
                  <text x="746" y="{{ g.ty }}" font-size="10.5" fill="var(--t3)" font-family="Inter, sans-serif">{{ g.l }}</text>
                </sc-for>
                <polygon points="{{ areaPoly }}" fill="url(#etihadArea)"></polygon>
                <polyline points="{{ revLine }}" fill="none" stroke="var(--p)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></polyline>
                <polyline points="{{ marginLine }}" fill="none" stroke="var(--p2)" stroke-width="2" stroke-dasharray="5 5" stroke-linecap="round"></polyline>
                <sc-for list="{{ points }}" as="p" hint-placeholder-count="12">
                  <circle cx="{{ p.x }}" cy="{{ p.y }}" r="{{ p.r }}" fill="var(--card)" stroke="var(--p)" stroke-width="2.5"></circle>
                </sc-for>
                <sc-for list="{{ points }}" as="p" hint-placeholder-count="12">
                  <text x="{{ p.x }}" y="242" text-anchor="middle" font-size="11" fill="var(--t3)">{{ p.m }}</text>
                </sc-for>
              </svg>
              <div style="display: flex; gap: 20px; margin-top: 16px; font-size: 12.5px; color: var(--t2);">
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 14px; height: 3px; border-radius: 2px; background: var(--p);"></span>الإيراد</span>
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 14px; height: 3px; border-radius: 2px; background: var(--p2);"></span>هامش الربح ٪</span>
              </div>
            </div>

                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">الإيراد مقابل المصروفات</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px; margin-bottom: 20px;">ستة أشهر · الخط الأزرق هو صافي الربح</div>
              <svg role="img" aria-label="رسم بياني: الإيراد مقابل المصروفات على ستة أشهر، والخط الأزرق هو صافي الربح" sc-camel-view-box="0 0 700 220" style="width: 100%; height: auto; overflow: visible;">
                <sc-for list="{{ gridLines }}" as="g" hint-placeholder-count="5">
                  <line x1="0" y1="{{ g.y }}" x2="700" y2="{{ g.y }}" stroke="var(--bd)" stroke-width="1"></line>
                </sc-for>
                <sc-for list="{{ expBars }}" as="b" hint-placeholder-count="12">
                  <rect x="{{ b.x }}" y="{{ b.y }}" width="{{ b.w }}" height="{{ b.h }}" rx="4" fill="{{ b.fill }}"></rect>
                </sc-for>
                <polyline points="{{ profitPts }}" fill="none" stroke="var(--sem-transit)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></polyline>
                <sc-for list="{{ expLabels }}" as="l" hint-placeholder-count="6">
                  <text x="{{ l.x }}" y="212" text-anchor="middle" font-size="11" fill="var(--t3)">{{ l.m }}</text>
                </sc-for>
              </svg>
              <div style="display: flex; gap: 20px; margin-top: 16px; font-size: 12.5px; color: var(--t2); flex-wrap: wrap;">
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: var(--sem-money);"></span>الإيراد</span>
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: var(--sem-late);"></span>المصروفات</span>
                <span style="display: flex; align-items: center; gap: 7px;"><span style="width: 14px; height: 3px; border-radius: 2px; background: var(--sem-transit);"></span>صافي الربح</span>
              </div>
            </div>
          </div>

          <div role="heading" aria-level="2" style="margin: 8px 0 18px; padding-top: 30px; border-top: 1px solid var(--bd); font-size: 12.5px; font-weight: 700; letter-spacing: 0.06em; color: var(--t3);">{{ zoneWarehouse }}</div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; align-items: start;">
                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px; display: flex; flex-direction: column;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">سعة المستودعات</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px;">قوانزو ونزوى — الإشغال الحالي</div>
              <div style="display: flex; justify-content: center; padding: 18px 0 6px;">
                <svg role="img" aria-label="رسم بياني: سعة المستودعات — الإشغال الحالي في قوانزو ونزوى" sc-camel-view-box="0 0 180 180" style="width: 172px; height: 172px;">
                  <circle cx="90" cy="90" r="70" fill="none" stroke="var(--bd)" stroke-width="16"></circle>
                  <circle cx="90" cy="90" r="70" fill="none" stroke="var(--p)" stroke-width="16" stroke-linecap="round" stroke-dasharray="{{ donutA }}" transform="rotate(-90 90 90)"></circle>
                  <circle cx="90" cy="90" r="50" fill="none" stroke="var(--bd)" stroke-width="14"></circle>
                  <circle cx="90" cy="90" r="50" fill="none" stroke="var(--p2)" stroke-width="14" stroke-linecap="round" stroke-dasharray="{{ donutB }}" transform="rotate(-90 90 90)"></circle>
                  <text x="90" y="86" text-anchor="middle" font-size="28" font-weight="600" fill="var(--t1)" font-family="Inter, sans-serif">71%</text>
                  <text x="90" y="106" text-anchor="middle" font-size="11" fill="var(--t2)">إجمالي الإشغال</text>
                </svg>
              </div>
              <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 8px;">
                <sc-for list="{{ capacity }}" as="c" hint-placeholder-count="2">
                  <div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 7px;">
                      <span style="display: flex; align-items: center; gap: 8px;"><span style="{{ c.dot }}"></span>{{ c.t }}</span>
                      <span style="font-weight: 600; font-feature-settings: 'tnum';">{{ c.v }}</span>
                    </div>
                    <div style="height: 7px; background: var(--bg); border-radius: 4px; overflow: hidden;">
                      <div style="{{ c.bar }}"></div>
                    </div>
                  </div>
                </sc-for>
              </div>
            </div>

                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">كثافة حركة المستودع</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-top: 4px; margin-bottom: 20px;">أغمق = حركة أكثر · اضغط أي خانة</div>
              <div data-heatgrid="1" style="display: grid; grid-template-columns: 46px repeat(5, 1fr); gap: 5px; align-items: center;">
                <span></span>
                <sc-for list="{{ heatHours }}" as="h" hint-placeholder-count="5">
                  <span style="font-size: 10.5px; color: var(--t3); text-align: center;">{{ h }}</span>
                </sc-for>
              </div>
              <div data-heatgrid="1" style="display: grid; grid-template-columns: 46px repeat(5, 1fr); gap: 5px; margin-top: 5px; align-items: center;">
                <sc-for list="{{ heatRows }}" as="r" hint-placeholder-count="5">
                  <span style="font-size: 11px; color: var(--t2); white-space: nowrap;">{{ r.d }}</span>
                  <sc-for list="{{ r.cells }}" as="c" hint-placeholder-count="5">
                    <button sc-camel-on-click="{{ c.go }}" title="{{ c.title }}" style="{{ c.st }}"></button>
                  </sc-for>
                </sc-for>
              </div>
            </div>
          </div>

          <div role="heading" aria-level="2" style="margin: 8px 0 18px; padding-top: 30px; border-top: 1px solid var(--bd); font-size: 12.5px; font-weight: 700; letter-spacing: 0.06em; color: var(--t3);">{{ zoneYourWork }}</div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 20px; margin-bottom: 24px; align-items: start;">
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">مهام اليوم</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 20px;">خمس مهام مفتوحة على اسمك أو على فريقك</div>
              <div style="display: flex; flex-direction: column; gap: 4px;">
                <sc-for list="{{ tasks }}" as="t" hint-placeholder-count="5">
                  <button sc-camel-on-click="{{ t.go }}" style="display: flex; align-items: flex-start; gap: 12px; width: 100%; padding: 11px 12px; background: transparent; border: 0; border-radius: var(--r-xs); cursor: pointer; text-align: right; color: var(--t1);" style-hover="background: var(--bg);">
                    <span style="{{ t.dot }}"></span>
                    <span style="flex: 1; min-width: 0;">
                      <span style="{{ t.tSt }}">{{ t.t }}</span>
                      <span style="display: block; font-size: 11.5px; color: var(--t2); margin-top: 3px;">{{ t.d }}</span>
                    </span>
                  </button>
                </sc-for>
              </div>
            </div>
            <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">أسبوع العمل</div>
              <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 20px;">الشريط الملوّن = موعد مرتبط بشحنة أو دفعة</div>
              <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px;">
                <sc-for list="{{ week }}" as="w" hint-placeholder-count="7">
                  <div style="{{ w.st }}">
                    <span style="{{ w.dSt }}">{{ w.d }}</span>
                    <span style="{{ w.nSt }}">{{ w.n }}</span>
                    <span style="{{ w.pip }}"></span>
                  </div>
                </sc-for>
              </div>
              <div style="display: flex; align-items: center; gap: 10px; margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--bd);">
                <span style="width: 34px; height: 34px; flex: 0 0 34px; border-radius: 10px; background: rgba(247,147,30,0.16); color: var(--badge-action-fg); display: grid; place-items: center;"><span style="{{ calIcon }}"></span></span>
                <span style="flex: 1;">
                  <span style="display: block; font-size: 13px; font-weight: 600;">وصول CTR-2026-0074</span>
                  <span style="display: block; font-size: 11.5px; color: var(--t2); margin-top: 2px;">الأحد ٩ أغسطس · مستودع نزوى</span>
                </span>
              </div>
            </div>
          </div>

          <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 24px; margin-bottom: 24px;">
            <div style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">إجراءات سريعة</div>
            <div style="font-size: 12.5px; color: var(--t2); margin-bottom: 18px;">المهام الأكثر تكراراً لدورك الحالي</div>
            <div data-grid="4" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
              <sc-for list="{{ quickActions }}" as="q" hint-placeholder-count="4">
                <button sc-camel-on-click="{{ q.go }}" style="display: flex; align-items: center; gap: 13px; padding: 16px; background: var(--bg); border: 1px solid var(--bd); border-radius: var(--r-sm); cursor: pointer; text-align: right; color: var(--t1); transition: all 150ms ease;" style-hover="border-color: var(--p-text); box-shadow: var(--sh);">
                  <span style="{{ q.iwrap }}"><span style="{{ q.ist }}"></span></span>
                  <span style="flex: 1; min-width: 0;">
                    <span style="display: block; font-size: 13.5px; font-weight: 600;">{{ q.t }}</span>
                    <span style="display: block; font-size: 11.5px; color: var(--t2); margin-top: 3px;">{{ q.d }}</span>
                  </span>
                </button>
              </sc-for>
            </div>
          </div>

          <div data-grid="split" style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 20px; margin-top: 24px;">
                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); overflow: hidden;">
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 20px 24px 16px;">
                <div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">عروض أسعار تنتظرك</div>
                <button sc-camel-on-click="{{ goQuotes }}" style="background: transparent; border: 0; cursor: pointer; font-size: 13px; color: var(--p-text); font-weight: 500; padding: 5px 6px; margin: -5px -6px;">عرض الكل ←</button>
              </div>
              <sc-raw-table data-stack="1" style="width: 100%; border-collapse: collapse;">
                <sc-raw-thead>
                  <sc-raw-tr>
                    <sc-for list="{{ quoteMini.head }}" as="h" hint-placeholder-count="4">
                      <sc-raw-th scope="col" style="{{ thSt }}">{{ h }}</sc-raw-th>
                    </sc-for>
                  </sc-raw-tr>
                </sc-raw-thead>
                <sc-raw-tbody>
                  <sc-for list="{{ quoteMini.rows }}" as="r" hint-placeholder-count="5">
                    <sc-raw-tr sc-camel-on-click="{{ r.go }}" style="cursor: pointer;" style-hover="background: var(--bg);">
                      <sc-for list="{{ r.cells }}" as="c" hint-placeholder-count="4">
                        <sc-raw-td data-label="{{ c.lbl }}" style="{{ c.st }}"><span style="{{ c.bst }}">{{ c.v }}</span></sc-raw-td>
                      </sc-for>
                    </sc-raw-tr>
                  </sc-for>
                </sc-raw-tbody>
              </sc-raw-table>
            </div>

                        <div style="background: var(--card); border: 1px solid var(--bd); border-radius: var(--r); box-shadow: var(--sh); padding: 22px 24px;">
              <div style="font-size: 16px; font-weight: 600; margin-bottom: 20px;">سجل النشاط</div>
              <div style="display: flex; flex-direction: column;">
                <sc-for list="{{ activity }}" as="a" hint-placeholder-count="6">
                  <div style="display: flex; gap: 14px;">
                    <div style="display: flex; flex-direction: column; align-items: center; flex: 0 0 auto;">
                      <span style="{{ a.dot }}"></span>
                      <span style="{{ a.line }}"></span>
                    </div>
                    <div style="padding-bottom: 18px; min-width: 0;">
                      <div style="font-size: 13.5px; line-height: 1.6;">{{ a.t }}</div>
                      <div style="font-size: 11.5px; color: var(--t2); margin-top: 4px;">{{ a.who }} · {{ a.time }}</div>
                    </div>
                  </div>
                </sc-for>
              </div>
            </div>
          </div>"""

EDITS = [
    ("extend the T dictionary with four zone labels", ZONE_DICT_OLD, ZONE_DICT_NEW, 1),
    ("compute the four zone-heading props", PROPS_OLD, PROPS_NEW, 1),
    ("regroup the dashboard into five zones", DASH_OLD, DASH_NEW, 1),
]


def apply(inner):
    applied = []
    for desc, old, new, expected in EDITS:
        found = inner.count(old)
        if found != expected:
            raise SystemExit(
                "patch target moved: expected %d of %r, found %d\n  (%s)"
                % (expected, old[:70], found, desc)
            )
        inner = inner.replace(old, new)
        applied.append("%-4d %s" % (found, desc))
    return inner, applied


def main():
    src = bundle.read(os.path.join(ROOT, "index.html"))
    inner, applied = apply(bundle.get_template(src))
    out = bundle.set_template(src, inner)
    bundle.verify(out)
    for target in TARGETS:
        bundle.write(os.path.join(ROOT, target), out)
    print("Applied dashboard reorg:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
