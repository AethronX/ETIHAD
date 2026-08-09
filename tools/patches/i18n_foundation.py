#!/usr/bin/env python3
"""Trilingual foundation for the ERP: Arabic / English / Chinese.

The public homepage now has a working ar/en/zh switcher (website/homepage*.html)
that links "تسجيل الدخول" to /erp -- but the ERP itself had zero i18n
infrastructure: no language state, no string dictionary, every screen
hardcoded Arabic. Translating all ~30 modules in one pass is a much larger,
higher-risk effort than can be verified with the same rigor as the rest of
this file's patches, so this covers the chrome every screen shares:

  - the sidebar (7 groups, 30 modules)
  - the dashboard's greeting, six KPI labels, and its two primary buttons

Deliberately NOT done here, and worth stating plainly rather than silently
shipping partial coverage:

  - the other ~26 modules' own content (tables, filters, stats) stays Arabic
  - direction stays RTL in every language. The root shell hardcodes
    dir="rtl" and flex-direction: row-reverse as literal markup, not a
    state-driven toggle -- this whole 30-module app was authored RTL-only.
    Flipping it for en/zh would need auditing every inline style for
    physical left/right assumptions across all 30 modules, which is a
    separate, much larger effort. English and Chinese text still renders
    correctly inside an RTL container (Unicode bidi handles each script's
    own run direction) -- the layout just stays right-anchored regardless
    of language.

Run against the inner document, not the bundle:

    python3 tools/patches/i18n_foundation.py   # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

# (js_key, ar, en, zh)
DICT = [
    ("grp_overview", "نظرة عامة", "Overview", "概览"),
    ("grp_sales", "المبيعات والعملاء", "Sales & Customers", "销售与客户"),
    ("grp_purchasing", "المشتريات", "Purchasing", "采购"),
    ("grp_logistics", "اللوجستيات", "Logistics", "物流"),
    ("grp_warehouses", "المستودعات", "Warehouses", "仓库"),
    ("grp_finance", "المالية والأرشيف", "Finance & Archive", "财务与档案"),
    ("grp_system", "النظام", "System", "系统"),
    ("nav_dash", "لوحة التحكم", "Dashboard", "仪表盘"),
    ("nav_tower", "برج التحكم", "Control Tower", "控制塔"),
    ("nav_analytics", "التحليلات", "Analytics", "分析"),
    ("nav_customers", "العملاء", "Customers", "客户"),
    ("nav_sales", "المبيعات", "Sales", "销售"),
    ("nav_quotes", "عروض الأسعار", "Quotes", "报价单"),
    ("nav_invoices", "الفواتير", "Invoices", "发票"),
    ("nav_po", "أوامر الشراء", "Purchase Orders", "采购订单"),
    ("nav_suppliers", "الموردون", "Suppliers", "供应商"),
    ("nav_cnoffice", "مكتب الصين", "China Office", "中国办事处"),
    ("nav_shipping", "الشحن والتتبع", "Shipping & Tracking", "运输与跟踪"),
    ("nav_containers", "الحاويات", "Containers", "集装箱"),
    ("nav_clearance", "التخليص الجمركي", "Customs Clearance", "清关"),
    ("nav_loadplan", "تخطيط التحميل", "Load Planning", "装载计划"),
    ("nav_cnwh", "مستودع الصين", "China Warehouse", "中国仓库"),
    ("nav_omwh", "مستودع عُمان", "Oman Warehouse", "阿曼仓库"),
    ("nav_pickup", "مواعيد الاستلام", "Pickup Schedule", "提货计划"),
    ("nav_inv", "المخزون", "Inventory", "库存"),
    ("nav_acct", "المحاسبة", "Accounting", "会计"),
    ("nav_docs", "المستندات", "Documents", "单证"),
    ("nav_landed", "التكلفة الواصلة", "Landed Cost", "到岸成本"),
    ("nav_reports", "التقارير", "Reports", "报表"),
    ("nav_notifications", "مركز الإشعارات", "Notification Center", "通知中心"),
    ("nav_permissions", "الأدوار والصلاحيات", "Roles & Permissions", "角色与权限"),
    ("nav_team", "الفرق والاعتمادات", "Teams & Approvals", "团队与审批"),
    ("nav_integrations", "التكاملات", "Integrations", "集成"),
    ("nav_health", "حالة النظام", "System Health", "系统状态"),
    ("nav_audit", "سجل التدقيق", "Audit Log", "审计日志"),
    ("nav_settings", "الإعدادات", "Settings", "设置"),
    ("nav_portal", "بوابة العميل", "Customer Portal", "客户门户"),
    ("greeting_prefix", "صباح الخير، ", "Good morning, ", "早上好，"),
    ("kpi_today_revenue", "إيراد اليوم", "Today's Revenue", "今日收入"),
    ("kpi_month_revenue", "إيراد الشهر", "This Month's Revenue", "本月收入"),
    ("kpi_containers_transit", "حاويات في الطريق", "Containers in Transit", "在途集装箱"),
    ("kpi_ready_pickup", "جاهزة للاستلام", "Ready for Pickup", "待提货"),
    ("kpi_inventory_value", "قيمة المخزون", "Inventory Value", "库存价值"),
    ("kpi_overdue_receivables", "مستحقات متأخرة", "Overdue Receivables", "逾期应收账款"),
    ("btn_export", "تصدير", "Export", "导出"),
    ("btn_new_quote", "طلب تسعير جديد", "New Quote Request", "新建报价请求"),
    ("needs_decision_prefix", "يحتاج قرارك — ", "Needs Your Decision — ", "需要您决策 — "),
    ("lang_label", "اللغة", "Language", "语言"),
]


def js_dict_literal():
    lines = ["  T = {"]
    for key, ar, en, zh in DICT:
        lines.append(
            "    %s: { ar: %s, en: %s, zh: %s },"
            % (key, _js_str(ar), _js_str(en), _js_str(zh))
        )
    lines.append("  };")
    return "\n".join(lines)


def _js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


T_DICT_LITERAL = js_dict_literal()

T_METHOD = """  t(key) {
    const e = this.T[key];
    if (!e) return key;
    return e[this.state.lang] || e.ar;
  }

  toggleLang() {
    const order = ['ar', 'en', 'zh'];
    const next = order[(order.indexOf(this.state.lang) + 1) % order.length];
    try { localStorage.setItem('etihad_lang', next); } catch (err) {}
    document.documentElement.lang = next;
    this.setState({ lang: next });
    this.say(next === 'ar' ? 'العربية' : next === 'en' ? 'English' : '中文');
  }
"""

STATE_OLD = "    dark: this.props.theme === 'dark', mini: true,"
STATE_NEW = (
    STATE_OLD
    + "\n    lang: (typeof localStorage !== 'undefined' && localStorage.getItem('etihad_lang')) || 'ar',"
)

MOUNT_OLD = "    document.body.dataset.theme = this.state.dark ? 'dark' : 'light';"
MOUNT_NEW = MOUNT_OLD + "\n    document.documentElement.lang = this.state.lang;"

ICONS_OLD = (
    "    'log-out': '<path d=\"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4\"/>"
    '<polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>\',\n'
    "  };"
)
ICONS_NEW = (
    "    'log-out': '<path d=\"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4\"/>"
    '<polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>\',\n'
    "    'globe': '<circle cx=\"12\" cy=\"12\" r=\"10\"/>"
    '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>\',\n'
    "  };"
)

NAVRAW_OLD = """    const navRaw = [
      { g: 'نظرة عامة', items: [
        { id: 'dash', t: 'لوحة التحكم', i: 'layout-dashboard' },
        { id: 'tower', t: 'برج التحكم', i: 'shield', badge: String(exOpenCount) },
        { id: 'analytics', t: 'التحليلات', i: 'trending-up' },
      ] },
      { g: 'المبيعات والعملاء', items: [
        { id: 'customers', t: 'العملاء', i: 'building-2' },
        { id: 'sales', t: 'المبيعات', i: 'hand-coins' },
        { id: 'quotes', t: 'عروض الأسعار', i: 'file-text', badge: '6' },
        { id: 'invoices', t: 'الفواتير', i: 'receipt', badge: '4' },
      ] },
      { g: 'المشتريات', items: [
        { id: 'po', t: 'أوامر الشراء', i: 'shopping-cart' },
        { id: 'suppliers', t: 'الموردون', i: 'factory' },
        { id: 'cnoffice', t: 'مكتب الصين', i: 'briefcase' },
      ] },
      { g: 'اللوجستيات', items: [
        { id: 'shipping', t: 'الشحن والتتبع', i: 'route' },
        { id: 'containers', t: 'الحاويات', i: 'container', badge: '14' },
        { id: 'clearance', t: 'التخليص الجمركي', i: 'stamp', badge: '3' },
        { id: 'loadplan', t: 'تخطيط التحميل', i: 'container' },
      ] },
      { g: 'المستودعات', items: [
        { id: 'cnwh', t: 'مستودع الصين', i: 'warehouse' },
        { id: 'omwh', t: 'مستودع عُمان', i: 'package', badge: '37' },
        { id: 'pickup', t: 'مواعيد الاستلام', i: 'calendar-days' },
        { id: 'inv', t: 'المخزون', i: 'layers' },
      ] },
      { g: 'المالية والأرشيف', items: [
        { id: 'acct', t: 'المحاسبة', i: 'wallet' },
        { id: 'docs', t: 'المستندات', i: 'folder' },
        { id: 'landed', t: 'التكلفة الواصلة', i: 'banknote' },
        { id: 'reports', t: 'التقارير', i: 'chart-column' },
      ] },
      { g: 'النظام', items: [
        { id: 'notifications', t: 'مركز الإشعارات', i: 'bell' },
        { id: 'permissions', t: 'الأدوار والصلاحيات', i: 'shield' },
        { id: 'team', t: 'الفرق والاعتمادات', i: 'users' },
        { id: 'integrations', t: 'التكاملات', i: 'briefcase' },
        { id: 'health', t: 'حالة النظام', i: 'clock' },
        { id: 'audit', t: 'سجل التدقيق', i: 'history' },
        { id: 'settings', t: 'الإعدادات', i: 'settings' },
        { id: 'portal', t: 'بوابة العميل', i: 'circle-user' },
      ] },
    ];"""

NAVRAW_NEW = """    const navRaw = [
      { g: this.t('grp_overview'), items: [
        { id: 'dash', t: this.t('nav_dash'), i: 'layout-dashboard' },
        { id: 'tower', t: this.t('nav_tower'), i: 'shield', badge: String(exOpenCount) },
        { id: 'analytics', t: this.t('nav_analytics'), i: 'trending-up' },
      ] },
      { g: this.t('grp_sales'), items: [
        { id: 'customers', t: this.t('nav_customers'), i: 'building-2' },
        { id: 'sales', t: this.t('nav_sales'), i: 'hand-coins' },
        { id: 'quotes', t: this.t('nav_quotes'), i: 'file-text', badge: '6' },
        { id: 'invoices', t: this.t('nav_invoices'), i: 'receipt', badge: '4' },
      ] },
      { g: this.t('grp_purchasing'), items: [
        { id: 'po', t: this.t('nav_po'), i: 'shopping-cart' },
        { id: 'suppliers', t: this.t('nav_suppliers'), i: 'factory' },
        { id: 'cnoffice', t: this.t('nav_cnoffice'), i: 'briefcase' },
      ] },
      { g: this.t('grp_logistics'), items: [
        { id: 'shipping', t: this.t('nav_shipping'), i: 'route' },
        { id: 'containers', t: this.t('nav_containers'), i: 'container', badge: '14' },
        { id: 'clearance', t: this.t('nav_clearance'), i: 'stamp', badge: '3' },
        { id: 'loadplan', t: this.t('nav_loadplan'), i: 'container' },
      ] },
      { g: this.t('grp_warehouses'), items: [
        { id: 'cnwh', t: this.t('nav_cnwh'), i: 'warehouse' },
        { id: 'omwh', t: this.t('nav_omwh'), i: 'package', badge: '37' },
        { id: 'pickup', t: this.t('nav_pickup'), i: 'calendar-days' },
        { id: 'inv', t: this.t('nav_inv'), i: 'layers' },
      ] },
      { g: this.t('grp_finance'), items: [
        { id: 'acct', t: this.t('nav_acct'), i: 'wallet' },
        { id: 'docs', t: this.t('nav_docs'), i: 'folder' },
        { id: 'landed', t: this.t('nav_landed'), i: 'banknote' },
        { id: 'reports', t: this.t('nav_reports'), i: 'chart-column' },
      ] },
      { g: this.t('grp_system'), items: [
        { id: 'notifications', t: this.t('nav_notifications'), i: 'bell' },
        { id: 'permissions', t: this.t('nav_permissions'), i: 'shield' },
        { id: 'team', t: this.t('nav_team'), i: 'users' },
        { id: 'integrations', t: this.t('nav_integrations'), i: 'briefcase' },
        { id: 'health', t: this.t('nav_health'), i: 'clock' },
        { id: 'audit', t: this.t('nav_audit'), i: 'history' },
        { id: 'settings', t: this.t('nav_settings'), i: 'settings' },
        { id: 'portal', t: this.t('nav_portal'), i: 'circle-user' },
      ] },
    ];"""

KPIRAW_OLD = """    const kpiRaw = [
      { label: 'إيراد اليوم', value: drStat.value, sub: drStat.sub + ' أمس', delta: drStat.delta, up: drStat.up, i: 'banknote', tone: 'p', editKey: 'daily_revenue', editType: 'daily' },
      { label: 'إيراد الشهر', value: 'ر.ع 62K', sub: 'الهدف ٥٨ ألف', delta: '+18.4%', up: true, i: 'trending-up', tone: 'p' },
      { label: 'حاويات في الطريق', value: '14', sub: 'منها ٣ تحت التخليص', delta: '+2', up: true, i: 'container', tone: 'cy' },
      { label: 'جاهزة للاستلام', value: '37', sub: 'شحنة في نزوى', delta: '9 متأخرة', up: false, i: 'package-check', tone: 'warn' },
      { label: 'قيمة المخزون', value: ivStat.value, sub: ivStat.sub + ' أمس', delta: ivStat.delta, up: ivStat.up, i: 'layers', tone: 'cy', editKey: 'inventory_value', editType: 'daily' },
      { label: 'مستحقات متأخرة', value: arStat.value, sub: arStat.sub + ' الأسبوع الماضي', delta: arStat.delta, up: !arStat.up, i: 'wallet', tone: 'bad', editKey: 'overdue_receivables', editType: 'weekly' },
    ];"""

KPIRAW_NEW = """    const kpiRaw = [
      { label: this.t('kpi_today_revenue'), value: drStat.value, sub: drStat.sub + ' أمس', delta: drStat.delta, up: drStat.up, i: 'banknote', tone: 'p', editKey: 'daily_revenue', editType: 'daily' },
      { label: this.t('kpi_month_revenue'), value: 'ر.ع 62K', sub: 'الهدف ٥٨ ألف', delta: '+18.4%', up: true, i: 'trending-up', tone: 'p' },
      { label: this.t('kpi_containers_transit'), value: '14', sub: 'منها ٣ تحت التخليص', delta: '+2', up: true, i: 'container', tone: 'cy' },
      { label: this.t('kpi_ready_pickup'), value: '37', sub: 'شحنة في نزوى', delta: '9 متأخرة', up: false, i: 'package-check', tone: 'warn' },
      { label: this.t('kpi_inventory_value'), value: ivStat.value, sub: ivStat.sub + ' أمس', delta: ivStat.delta, up: ivStat.up, i: 'layers', tone: 'cy', editKey: 'inventory_value', editType: 'daily' },
      { label: this.t('kpi_overdue_receivables'), value: arStat.value, sub: arStat.sub + ' الأسبوع الماضي', delta: arStat.delta, up: !arStat.up, i: 'wallet', tone: 'bad', editKey: 'overdue_receivables', editType: 'weekly' },
    ];"""

GREETING_OLD = "      greeting: 'صباح الخير، ' + roleObj.name.split(' ')[0],"
GREETING_NEW = "      greeting: this.t('greeting_prefix') + roleObj.name.split(' ')[0],"

ALERTCOUNT_OLD = "      alertCount: 'يحتاج قرارك — ' + alerts.length,"
ALERTCOUNT_NEW = "      alertCount: this.t('needs_decision_prefix') + alerts.length,"

BUTTONS_OLD = (
    '<button sc-camel-on-click="{{ exportPdf }}" style="{{ btnGhost }}">'
    "<span style=\"{{ downloadIcon }}\"></span>تصدير</button>\n"
    '              <button sc-camel-on-click="{{ newQuote }}" style="{{ btnPrimary }}">'
    "<span style=\"{{ plusIcon }}\"></span>طلب تسعير جديد</button>"
)
BUTTONS_NEW = (
    '<button sc-camel-on-click="{{ exportPdf }}" style="{{ btnGhost }}">'
    "<span style=\"{{ downloadIcon }}\"></span>{{ exportLabel }}</button>\n"
    '              <button sc-camel-on-click="{{ newQuote }}" style="{{ btnPrimary }}">'
    "<span style=\"{{ plusIcon }}\"></span>{{ newQuoteLabel }}</button>"
)

# computed-props wiring: expose exportLabel/newQuoteLabel, and the header button
PROPS_ANCHOR_OLD = "      bellIcon: I('bell', 18), themeIcon: I(s.dark ? 'sun' : 'moon', 18),"
PROPS_ANCHOR_NEW = (
    PROPS_ANCHOR_OLD
    + "\n      langIcon: I('globe', 18), langLabel: this.t('lang_label'),"
    " toggleLang: () => this.toggleLang(),"
    "\n      exportLabel: this.t('btn_export'), newQuoteLabel: this.t('btn_new_quote'),"
)

HEADER_BTN_OLD = (
    '<button sc-camel-on-click="{{ toggleTheme }}" title="{{ themeLabel }}"'
    ' aria-label="{{ themeLabel }}" style="width: 40px; height: 40px; display: grid;'
    ' place-items: center; background: transparent; border: 1px solid var(--bd);'
    ' border-radius: 12px; cursor: pointer; color: var(--t2);" style-hover="background:'
    ' var(--bg); color: var(--t1);">\n          <span style="{{ themeIcon }}"></span>\n'
    "        </button>"
)
HEADER_BTN_NEW = (
    HEADER_BTN_OLD
    + '\n        <button sc-camel-on-click="{{ toggleLang }}" title="{{ langLabel }}"'
    ' aria-label="{{ langLabel }}" style="width: 40px; height: 40px; display: grid;'
    ' place-items: center; background: transparent; border: 1px solid var(--bd);'
    ' border-radius: 12px; cursor: pointer; color: var(--t2);" style-hover="background:'
    ' var(--bg); color: var(--t1);">\n          <span style="{{ langIcon }}"></span>\n'
    "        </button>"
)

STRUCTURAL_EDITS = [
    ("add lang to initial state, persisted from localStorage", STATE_OLD, STATE_NEW, 1),
    ("sync document.lang on mount", MOUNT_OLD, MOUNT_NEW, 1),
    ("register the globe icon", ICONS_OLD, ICONS_NEW, 1),
    ("route sidebar groups + module names through t()", NAVRAW_OLD, NAVRAW_NEW, 1),
    ("route the six dashboard KPI labels through t()", KPIRAW_OLD, KPIRAW_NEW, 1),
    ("route the dashboard greeting prefix through t()", GREETING_OLD, GREETING_NEW, 1),
    ("route the needs-decision prefix through t()", ALERTCOUNT_OLD, ALERTCOUNT_NEW, 1),
    ("bind the export/new-quote buttons to computed labels", BUTTONS_OLD, BUTTONS_NEW, 1),
    ("compute langIcon/langLabel/toggleLang/exportLabel/newQuoteLabel", PROPS_ANCHOR_OLD, PROPS_ANCHOR_NEW, 1),
    ("add the language button to the header", HEADER_BTN_OLD, HEADER_BTN_NEW, 1),
]


def apply(inner):
    applied = []

    class_anchor = "  ICONS = {"
    assert inner.count(class_anchor) == 1, "ICONS class-property anchor not found"
    inner = inner.replace(
        class_anchor, T_DICT_LITERAL + "\n\n" + T_METHOD + "\n" + class_anchor, 1
    )
    applied.append("1    add the T dictionary and t()/toggleLang() methods")

    for desc, old, new, expected in STRUCTURAL_EDITS:
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
    print("Applied i18n foundation:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
