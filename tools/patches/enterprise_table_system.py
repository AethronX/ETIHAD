#!/usr/bin/env python3
"""Bring the 23 generic-page tables up to the quotes list's table standard.

Measured gap: two table renderers exist. The quotes list (`isQuoteList`) is
the one fully-featured list -- search, stage tabs, filter chips, clickable
column sort, and numbered pagination. Every other data module (`po`, `cnwh`,
`containers`, `shipping`, `omwh`, `inv`, `acct`, `docs`, `reports`,
`customers`, `sales`, `invoices`, `suppliers`, `cnoffice`, `clearance`,
`analytics`, `notifications`, `audit`, `permissions`, `integrations`,
`health`, `team`, `settings`) renders through one shared block --
`page.hasTable` in renderVals() -- that only ever had search + filter chips:
no column sort, no pagination, all filtered rows dumped into one table.

Because that block is shared by all 23 modules, fixing it once fixes it
everywhere at once -- this is the "full sweep" applied through the
architecture's one shared code path, not 23 separate hand-edits.

What this adds, generically, to every one of those 23 tables:
  - clickable column headers that sort the (already-filtered) rows, with a
    numeric-aware compare (smartCompare) so currency/percentage/weight/date
    columns like "¥ 184,600" or "94%" sort correctly and not lexicographically
  - numbered pagination (8 rows/page), reusing the same `page` state field
    and pager markup pattern the quotes list already uses
  - sort/page state resets on navigation (go()), same as the quotes list's
    tableQuery/genFilter reset

What this deliberately does NOT add, and why:
  - bulk selection / bulk actions -- the quotes list's bulk bar calls real,
    specific actions ("send for approval", "assign to employee"); inventing
    equivalents for 23 unrelated modules would be fabricating operations
    with no defined backend semantics
  - per-column visibility toggles -- a real feature, but a separate UI
    surface (menu, hidden-column state) large enough to deserve its own
    patch and its own review, not bundled into a table-parity fix
  - list virtualization -- explicitly scoped to pagination instead; no
    virtualization library exists in this codebase and no windowing
    infrastructure the template language could drive safely

Run against the inner document, not the bundle:

    python3 tools/patches/enterprise_table_system.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("erp/index.html", "erp/Etihad_ERP.html")

STATE_OLD = "    genQuery: '', genFilter: 0, readNotifs: [],\n"
STATE_NEW = (
    "    genQuery: '', genFilter: 0, genSortCol: null, genSortDir: 'asc', readNotifs: [],\n"
)

GO_OLD = (
    "    this.setState(Object.assign({ mod, palette: false, notifs: false, profile: false, "
    "loading: true, selected: [], page: 1, tableQuery: '', genQuery: '', genFilter: 0, "
    "stageFilter: null, stagePop: false }, extra || {}));"
)
GO_NEW = (
    "    this.setState(Object.assign({ mod, palette: false, notifs: false, profile: false, "
    "loading: true, selected: [], page: 1, tableQuery: '', genQuery: '', genFilter: 0, "
    "genSortCol: null, genSortDir: 'asc', stageFilter: null, stagePop: false }, extra || {}));"
)

SMART_COMPARE_OLD = "  row(cells, go) { return { cells, go }; }\n"
SMART_COMPARE_NEW = (
    SMART_COMPARE_OLD
    + "\n"
    + "  /* رقمي إن أمكن (يشيل ¥ / ر.ع / % / فواصل الآلاف)، وإلا مقارنة نصية */\n"
    + "  smartCompare(a, b) {\n"
    + "    const da = String(a).replace(/[^0-9.-]/g, '');\n"
    + "    const db = String(b).replace(/[^0-9.-]/g, '');\n"
    + "    const na = parseFloat(da), nb = parseFloat(db);\n"
    + "    if (da.length && db.length && !isNaN(na) && !isNaN(nb)) return na - nb;\n"
    + "    return String(a).localeCompare(String(b), 'ar');\n"
    + "  }\n"
)

TABLE_LOGIC_OLD = """      if (page.table) {
        const all = page.table.rows;
        const gq = s.genQuery.trim();
        let rows = all;
        if (s.genFilter > 0) {
          const term = (page.filters[s.genFilter] || {}).t || '';
          rows = all.filter((r) => r.cells.some((cc) => String(cc.v).includes(term)));
        }
        if (gq) rows = rows.filter((r) => r.cells.some((cc) => String(cc.v).includes(gq)));
        page.tableTotal = all.length;
        page.tableCount = rows.length + ' من ' + all.length + ' سجل';
        page.tableEmpty = rows.length === 0;
        page.table = { head: page.table.head, rows };
      }"""

TABLE_LOGIC_NEW = """      if (page.table) {
        const all = page.table.rows;
        const gq = s.genQuery.trim();
        let rows = all;
        if (s.genFilter > 0) {
          const term = (page.filters[s.genFilter] || {}).t || '';
          rows = all.filter((r) => r.cells.some((cc) => String(cc.v).includes(term)));
        }
        if (gq) rows = rows.filter((r) => r.cells.some((cc) => String(cc.v).includes(gq)));
        page.tableTotal = all.length;
        page.tableEmpty = rows.length === 0;
        const sortCol = s.genSortCol;
        if (sortCol !== null && rows[0] && rows[0].cells[sortCol]) {
          const dir = s.genSortDir === 'asc' ? 1 : -1;
          rows = rows.slice().sort((a, b) => this.smartCompare(a.cells[sortCol].v, b.cells[sortCol].v) * dir);
        }
        page.tableCount = rows.length + ' من ' + all.length + ' سجل';
        const genPer = 8;
        const genPages = Math.max(1, Math.ceil(rows.length / genPer));
        const genCur = Math.min(s.page, genPages);
        const shown = rows.slice((genCur - 1) * genPer, genCur * genPer);
        page.pageLabel = 'صفحة ' + genCur + ' من ' + genPages + ' · ' + rows.length + ' سجل';
        page.pager = [{ t: '‹', p: Math.max(1, genCur - 1) }].concat(
          Array.from({ length: genPages }, (_, i) => ({ t: String(i + 1), p: i + 1 })),
          [{ t: '›', p: Math.min(genPages, genCur + 1) }]
        ).map((p) => ({ t: p.t, st: { minWidth: '34px', height: '34px', padding: '0 10px', borderRadius: '9px', cursor: 'pointer', fontFamily: 'Inter, sans-serif', fontSize: '13px', border: '1px solid ' + (p.t === String(genCur) ? 'var(--p)' : 'var(--bd)'), background: p.t === String(genCur) ? 'var(--p)' : 'var(--card)', color: p.t === String(genCur) ? '#fff' : 'var(--t1)', fontWeight: p.t === String(genCur) ? 600 : 400 }, go: () => this.setState({ page: p.p }) }));
        page.table = {
          head: page.table.head.map((h, i) => ({
            t: h, st: this.th,
            bst: { display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'transparent', border: 0, padding: '5px 0', cursor: 'pointer', fontFamily: 'inherit', fontSize: '11.5px', fontWeight: sortCol === i ? 600 : 500, color: sortCol === i ? 'var(--p-text)' : 'var(--t2)' },
            ist: sortCol === i ? I(s.genSortDir === 'asc' ? 'arrow-up' : 'arrow-down', 13) : I('chevrons-up-down', 13, 'var(--t3)'),
            go: () => this.setState({ genSortCol: i, genSortDir: sortCol === i && s.genSortDir === 'desc' ? 'asc' : 'desc', page: 1 }),
          })),
          rows: shown,
        };
      }"""

HEADER_MARKUP_OLD = """                      <sc-for list="{{ page.table.head }}" as="h" hint-placeholder-count="7">
                        <sc-raw-th scope="col" style="{{ thSt }}">{{ h }}</sc-raw-th>
                      </sc-for>"""
HEADER_MARKUP_NEW = """                      <sc-for list="{{ page.table.head }}" as="h" hint-placeholder-count="7">
                        <sc-raw-th scope="col" style="{{ h.st }}"><button sc-camel-on-click="{{ h.go }}" style="{{ h.bst }}">{{ h.t }}<span style="{{ h.ist }}"></span></button></sc-raw-th>
                      </sc-for>"""

EMPTY_AND_PAGER_OLD = """              <sc-if value="{{ page.tableEmpty }}" hint-placeholder-val="{{ true }}">
                <div style="padding: 56px 24px; text-align: center; animation: fade 160ms ease both;">
                  <div style="width: 52px; height: 52px; margin: 0 auto 16px; border-radius: 16px; background: var(--bg); display: grid; place-items: center; color: var(--t3);"><span style="{{ emptyIcon }}"></span></div>
                  <div style="font-size: 15.5px; font-weight: 600;">لا نتائج مطابقة</div>
                  <div style="font-size: 13px; color: var(--t2); margin-top: 7px;">جرّب كلمة أقصر أو أعد ضبط المرشّح.</div>
                  <button sc-camel-on-click="{{ clearGenQuery }}" style="{{ btnGhostCenter }}">مسح البحث والمرشّحات</button>
                </div>
              </sc-if>
            </div>
          </sc-if>"""
EMPTY_AND_PAGER_NEW = """              <sc-if value="{{ page.tableEmpty }}" hint-placeholder-val="{{ true }}">
                <div style="padding: 56px 24px; text-align: center; animation: fade 160ms ease both;">
                  <div style="width: 52px; height: 52px; margin: 0 auto 16px; border-radius: 16px; background: var(--bg); display: grid; place-items: center; color: var(--t3);"><span style="{{ emptyIcon }}"></span></div>
                  <div style="font-size: 15.5px; font-weight: 600;">لا نتائج مطابقة</div>
                  <div style="font-size: 13px; color: var(--t2); margin-top: 7px;">جرّب كلمة أقصر أو أعد ضبط المرشّح.</div>
                  <button sc-camel-on-click="{{ clearGenQuery }}" style="{{ btnGhostCenter }}">مسح البحث والمرشّحات</button>
                </div>
              </sc-if>
              <div style="display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 16px 22px; border-top: 1px solid var(--bd); flex-wrap: wrap;">
                <div style="font-size: 12.5px; color: var(--t2);">{{ page.pageLabel }}</div>
                <div style="display: flex; gap: 6px;">
                  <sc-for list="{{ page.pager }}" as="p" hint-placeholder-count="5">
                    <button sc-camel-on-click="{{ p.go }}" style="{{ p.st }}">{{ p.t }}</button>
                  </sc-for>
                </div>
              </div>
            </div>
          </sc-if>"""

EDITS = [
    ("add genSortCol/genSortDir to initial state", STATE_OLD, STATE_NEW, 1),
    ("reset sort state on navigation in go()", GO_OLD, GO_NEW, 1),
    ("add the smartCompare numeric-aware comparator", SMART_COMPARE_OLD, SMART_COMPARE_NEW, 1),
    ("sort + paginate the 23 generic-page tables", TABLE_LOGIC_OLD, TABLE_LOGIC_NEW, 1),
    ("make generic table headers clickable sort buttons", HEADER_MARKUP_OLD, HEADER_MARKUP_NEW, 1),
    ("add a pagination footer to the generic table", EMPTY_AND_PAGER_OLD, EMPTY_AND_PAGER_NEW, 1),
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
    src = bundle.read(os.path.join(ROOT, "erp", "index.html"))
    inner, applied = apply(bundle.get_template(src))
    out = bundle.set_template(src, inner)
    bundle.verify(out)
    for target in TARGETS:
        bundle.write(os.path.join(ROOT, target), out)
    print("Applied enterprise table system (sort + pagination, all 23 generic modules):")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
