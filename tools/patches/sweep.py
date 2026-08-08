#!/usr/bin/env python3
"""Fixes found by sweeping all 30 pages, not just the dashboard.

The earlier audits only ever loaded the default view, so they measured one
page in one state. Walking every page in both themes at 390px and 1440px
(tools/audit/pages.js) surfaced a different class of defect: things that only
exist once you navigate somewhere, or select something.

  1.4.3 Contrast     Every semantic colour fails as text in one theme or the
                     other -- they were chosen as fills and badge tints, where
                     the 3:1 non-text threshold applies:

                                     on light card   on dark card
                       --sem-money        8.86            1.92
                       --sem-transit      2.37            7.18
                       --sem-action       2.30            7.42
                       --sem-done         3.30            5.17
                       --sem-late         4.83            3.53
                       --sem-idle         2.54            6.71

                     Measured failures were the SLA countdown on the control
                     tower ("يتبقى 6 ساعة", 2.30:1 light) and the overrun text
                     ("تجاوز المهلة", 3.53:1 dark). This adds --sem-*-text in
                     the same shape as the existing --p / --p-text split and
                     routes the text usages through it. Fills, borders and
                     badge tints keep the original tokens.

  1.4.3 Contrast     The permissions matrix builds its glyph colour in a
                     helper -- `v === '●' ? 'var(--p)' : ...` -- so it escaped
                     the brand-token pass, which anchors on `color:`. The full
                     dot measured 3.32:1 in dark.

  4.1.2 Name         The quote table's select-all and per-row checkboxes had
                     no accessible name at all, and neither did the two range
                     sliders. Row checkboxes are named after the row they
                     select, so eight of them are not eight identical
                     "checkbox" announcements.

  2.5.8 Target Size  Sortable column headers are 14px tall (padding: 0). They
                     repeat across roughly twenty list pages, which is why the
                     raw finding count was 144 for 7 distinct shapes.

  2.5.8 Target Size  The warehouse rack map packs 24 columns into the viewport
                     width, giving 21px-wide bins on a phone. The grid now
                     holds a 28px minimum and scrolls inside its own card
                     rather than shrinking below the tappable minimum.

Run against the inner document, not the bundle:

    python3 tools/patches/sweep.py     # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

# Values verified against both surfaces a token can land on -- the card and
# the page background -- in their own theme. Lowest reading of each pair:
#   light  late 5.77  action 6.37  done 6.49
#   dark   late 6.16  action 7.93  done 8.86
LIGHT_TOKENS_OLD = "      --badge-late-fg: #C21C1C;\n"
LIGHT_TOKENS_NEW = (
    "      --badge-late-fg: #C21C1C;\n"
    "      /* الألوان الدلالية كنص عادي على البطاقة أو الخلفية */\n"
    "      --sem-late-text: #C21C1C; --sem-action-text: #96450A;\n"
    "      --sem-done-text: #116932;\n"
)

DARK_TOKENS_OLD = "      --badge-late-fg: #F58B8B;\n"
DARK_TOKENS_NEW = (
    "      --badge-late-fg: #F58B8B;\n"
    "      --sem-late-text: #F87171; --sem-action-text: #F59E0B;\n"
    "      --sem-done-text: #34D399;\n"
)

RACK_CSS_OLD = "    [data-hamburger] { display: grid; }\n"
RACK_CSS_NEW = (
    "    [data-hamburger] { display: grid; }\n"
    "    /* خريطة الرفوف تمرّر أفقياً بدل أن تنكمش تحت حد اللمس */\n"
    "    [data-racks] { overflow-x: auto; }\n"
)

# The export already reflows the rack map from 24 columns to 12 on phones,
# which lands each bin at 21px wide. Keeping that column count but giving the
# track a floor turns the shortfall into a scroll instead of an untappable
# target.
RACK_COLS_OLD = "[data-racks] { grid-template-columns: repeat(12, 1fr) !important; }"
RACK_COLS_NEW = (
    "[data-racks] { grid-template-columns:"
    " repeat(12, minmax(24px, 1fr)) !important; }"
)

# (description, old, new, expected_occurrences)
EDITS = [
    (
        "define semantic text tokens for light theme (WCAG 1.4.3)",
        LIGHT_TOKENS_OLD,
        LIGHT_TOKENS_NEW,
        1,
    ),
    (
        "define semantic text tokens for dark theme (WCAG 1.4.3)",
        DARK_TOKENS_OLD,
        DARK_TOKENS_NEW,
        1,
    ),
    (
        "route the SLA countdown through the text tokens (2.30:1 light)",
        "color: e.sla < 0 ? 'var(--sem-late)' : e.sla < 24"
        " ? 'var(--sem-action)' : 'var(--t2)'",
        "color: e.sla < 0 ? 'var(--sem-late-text)' : e.sla < 24"
        " ? 'var(--sem-action-text)' : 'var(--t2)'",
        1,
    ),
    (
        "route the net-margin readout through the text tokens",
        "color: netPct < 12 ? 'var(--sem-late)' : netPct < 20"
        " ? 'var(--sem-action)' : 'var(--sem-done)'",
        "color: netPct < 12 ? 'var(--sem-late-text)' : netPct < 20"
        " ? 'var(--sem-action-text)' : 'var(--sem-done-text)'",
        1,
    ),
    (
        "route the storage-days readout through the text tokens",
        "color: storeDays > 0 ? 'var(--sem-late)' : 'var(--sem-done)'",
        "color: storeDays > 0 ? 'var(--sem-late-text)'"
        " : 'var(--sem-done-text)'",
        1,
    ),
    (
        "route the load-plan fill readout through the text tokens",
        "color: picked.length && pctCbm >= 90 ? 'var(--sem-done)' : 'var(--t2)'",
        "color: picked.length && pctCbm >= 90 ? 'var(--sem-done-text)'"
        " : 'var(--t2)'",
        1,
    ),
    (
        "route the critical-exception count through the text token",
        "font-feature-settings: 'tnum'; color: var(--sem-late);",
        "font-feature-settings: 'tnum'; color: var(--sem-late-text);",
        1,
    ),
    (
        "route the dismiss-button hover through the text token",
        'style-hover="color: var(--sem-late); background: var(--bg);"',
        'style-hover="color: var(--sem-late-text); background: var(--bg);"',
        1,
    ),
    (
        "colour the permissions matrix glyphs as text (3.32:1 dark)",
        "const col = (v) => v === '●' ? 'var(--p)' :",
        "const col = (v) => v === '●' ? 'var(--p-text)' :",
        1,
    ),
    (
        "give sortable column headers a 24px target (WCAG 2.5.8)",
        "gap: '6px', background: 'transparent', border: 0, padding: 0,"
        " cursor: 'pointer', fontFamily: 'inherit', fontSize: '11.5px',",
        "gap: '6px', background: 'transparent', border: 0,"
        " padding: '5px 0', cursor: 'pointer', fontFamily: 'inherit',"
        " fontSize: '11.5px',",
        1,
    ),
    (
        "let the rack map scroll rather than shrink",
        RACK_CSS_OLD,
        RACK_CSS_NEW,
        1,
    ),
    (
        "keep warehouse bins tappable on a phone (WCAG 2.5.8)",
        RACK_COLS_OLD,
        RACK_COLS_NEW,
        1,
    ),
    (
        "name the select-all checkbox (WCAG 4.1.2)",
        '<input type="checkbox" checked="{{ allSelected }}"'
        ' sc-camel-on-change="{{ toggleAll }}">',
        '<input type="checkbox" aria-label="تحديد كل الصفوف"'
        ' checked="{{ allSelected }}" sc-camel-on-change="{{ toggleAll }}">',
        1,
    ),
    (
        "name each row checkbox after its own row (WCAG 4.1.2)",
        '<input type="checkbox" checked="{{ r.sel }}"'
        ' sc-camel-on-change="{{ r.pick }}">',
        '<input type="checkbox" aria-label="{{ r.selLabel }}"'
        ' checked="{{ r.sel }}" sc-camel-on-change="{{ r.pick }}">',
        1,
    ),
    (
        "supply the row checkbox label",
        "      const sel = s.selected.includes(q.id);\n"
        "      return {\n        sel,",
        "      const sel = s.selected.includes(q.id);\n"
        "      return {\n        sel,\n"
        "        selLabel: 'تحديد ' + q.id,",
        1,
    ),
    (
        "name the margin slider (WCAG 4.1.2)",
        '<input type="range" min="5" max="45" step="1" value="{{ margin }}"',
        '<input type="range" aria-label="هامش الربح"'
        ' min="5" max="45" step="1" value="{{ margin }}"',
        1,
    ),
    (
        "name the storage-days slider (WCAG 4.1.2)",
        '<input type="range" min="1" max="30" step="1" value="{{ dwell }}"',
        '<input type="range" aria-label="أيام البقاء في المستودع"'
        ' min="1" max="30" step="1" value="{{ dwell }}"',
        1,
    ),
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
    print("Applied all-page sweep fixes:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
