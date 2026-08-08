#!/usr/bin/env python3
"""Split the brand colour into a fill token and a text token.

`--p` was doing two incompatible jobs: it filled primary buttons (white text
sits on it) and it coloured links and accents (it sits on the page). One value
cannot satisfy both contrast directions, and in dark theme both failed --
white on the fill measured 3.88:1, and the same blue as link text measured
4.38:1 on a card.

    --p        brand fill; white text sits on it
               light #0F4C81 (white 8.6:1) · dark #33739F (white 5.13:1)
    --p-text   brand as text; sits on bg or card
               light #0F4C81 (7.5:1 on white) · dark #7FB6E4 (7.88:1 on card)

Light theme needs no split -- #0F4C81 already clears both directions -- so
--p-text simply resolves to the same value there.

Brand-as-text is written two ways in this file and both have to be routed:
`color: var(--p)` inside a style attribute, and `color: 'var(--p)'` inside a
JavaScript style object. The second form is where every "selected" state lives
-- active tab, sorted column, chosen saved view, current role, current
workspace, active bottom-nav item -- so in dark theme those all measured
3.32:1 against their own card. They are invisible to an audit of the default
view because nothing is selected until the user selects it.

Only the `color:` property is rewritten. `--p` stays correct as a border or
background fill, where the 3:1 non-text threshold applies instead.

Usage:  python3 tools/patches/brand_text_token.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

LIGHT_OLD = "      --p: #0F4C81; --p-600: #0d4270; --p-tint: #E8F0F7;"
LIGHT_NEW = "      --p: #0F4C81; --p-600: #0d4270; --p-tint: #E8F0F7; --p-text: #0F4C81;"

DARK_OLD = "      --p: #3D86C4; --p-600: #4E97D4; --p-tint: #14273C; --p2: #22C7E6;"
DARK_NEW = "      --p: #33739F; --p-600: #4E97D4; --p-tint: #14273C; --p2: #22C7E6; --p-text: #7FB6E4;"

JS_BRAND_TEXT = re.compile(r"(color: (?:[^,{}\n]*?\? )?)'var\(--p\)'")
JS_BRAND_TEXT_COUNT = 11


def apply(inner):
    applied = []
    for desc, old, new in (
        ("define --p-text in light theme", LIGHT_OLD, LIGHT_NEW),
        ("deepen dark fill and define --p-text in dark theme", DARK_OLD, DARK_NEW),
    ):
        if inner.count(old) != 1:
            raise SystemExit("patch target moved: %r (%s)" % (old[:60], desc))
        inner = inner.replace(old, new)
        applied.append(desc)

    n = inner.count("color: var(--p)")
    if n == 0:
        raise SystemExit("no brand-as-text usages found")
    inner = inner.replace("color: var(--p)", "color: var(--p-text)")
    applied.append("route %d css brand-as-text usages through --p-text" % n)

    # The JS style-object form: `color: cond ? 'var(--p)' : 'var(--t1)'`.
    # Anchored on the `color:` property so border and background uses of --p,
    # which are judged against the 3:1 non-text threshold, are left alone.
    inner, m = JS_BRAND_TEXT.subn(r"\1'var(--p-text)'", inner)
    if m != JS_BRAND_TEXT_COUNT:
        raise SystemExit(
            "expected %d js brand-as-text usages, rewrote %d"
            % (JS_BRAND_TEXT_COUNT, m)
        )
    applied.append("route %d js brand-as-text usages through --p-text" % m)
    return inner, applied


def main():
    src = bundle.read(os.path.join(ROOT, "index.html"))
    inner, applied = apply(bundle.get_template(src))
    out = bundle.set_template(src, inner)
    bundle.verify(out)
    for target in TARGETS:
        bundle.write(os.path.join(ROOT, target), out)
    print("Applied brand token split:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
