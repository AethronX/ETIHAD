#!/usr/bin/env python3
"""Make semantic badge colours theme-aware and WCAG-legible.

The status badges carried hardcoded light-theme foregrounds, so they failed
contrast twice over: several were already short of 4.5:1 on their own tint in
light mode, and none of them changed in dark mode, where the primary-blue
badge measured 1.92:1 against a dark card.

Each foreground becomes a token defined once per theme. Ratios below were
computed against the badge's own tint composited over the card it sits on:

    token             light            dark
    money      #0F4C81  7.50:1   #7FB6E4  7.48:1
    transit    #0E7490  4.71:1   #5FD8EE  8.00:1
    action     #96450A  5.86:1   #F0A94E  6.53:1   (was #B45309, 4.42:1)
    done       #116932  6.06:1   #5FD98B  7.67:1   (was #16A34A, 2.94:1)
    late       #C21C1C  5.18:1   #F58B8B  6.51:1   (was #DC2626, 4.14:1)

Usage:  python3 tools/patches/badge_tokens.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

LIGHT_ANCHOR = "      --sem-idle: #9CA3AF;    /* خامل، لم يبدأ */"
LIGHT_TOKENS = LIGHT_ANCHOR + """
      /* نص الشارات — كل قيمة تحقق 4.5:1 على خلفية الشارة نفسها */
      --badge-money-fg: #0F4C81; --badge-transit-fg: #0E7490;
      --badge-action-fg: #96450A; --badge-done-fg: #116932;
      --badge-late-fg: #C21C1C;"""

DARK_ANCHOR = "      --p: #3D86C4; --p-600: #4E97D4; --p-tint: #14273C; --p2: #22C7E6;"
DARK_TOKENS = DARK_ANCHOR + """
      --badge-money-fg: #7FB6E4; --badge-transit-fg: #5FD8EE;
      --badge-action-fg: #F0A94E; --badge-done-fg: #5FD98B;
      --badge-late-fg: #F58B8B;"""

EDITS = [
    ("define light-theme badge tokens", LIGHT_ANCHOR, LIGHT_TOKENS, 1),
    ("define dark-theme badge tokens", DARK_ANCHOR, DARK_TOKENS, 1),
    (
        "route money badge through its token",
        "money: { c: 'var(--sem-money)', bg: 'rgba(15,76,129,0.10)', fg: 'var(--sem-money)' },",
        "money: { c: 'var(--sem-money)', bg: 'rgba(15,76,129,0.10)', fg: 'var(--badge-money-fg)' },",
        1,
    ),
    (
        "route transit badge through its token",
        "transit: { c: 'var(--sem-transit)', bg: 'rgba(0,184,217,0.14)', fg: '#0E7490' },",
        "transit: { c: 'var(--sem-transit)', bg: 'rgba(0,184,217,0.14)', fg: 'var(--badge-transit-fg)' },",
        1,
    ),
    (
        "route action badge through its token",
        "action: { c: 'var(--sem-action)', bg: 'rgba(247,147,30,0.16)', fg: '#B45309' },",
        "action: { c: 'var(--sem-action)', bg: 'rgba(247,147,30,0.16)', fg: 'var(--badge-action-fg)' },",
        1,
    ),
    (
        "route done badge through its token",
        "done: { c: 'var(--sem-done)', bg: 'rgba(34,197,94,0.13)', fg: '#16A34A' },",
        "done: { c: 'var(--sem-done)', bg: 'rgba(34,197,94,0.13)', fg: 'var(--badge-done-fg)' },",
        1,
    ),
    (
        "route late badge through its token",
        "late: { c: 'var(--sem-late)', bg: 'rgba(239,68,68,0.12)', fg: '#DC2626' },",
        "late: { c: 'var(--sem-late)', bg: 'rgba(239,68,68,0.12)', fg: 'var(--badge-late-fg)' },",
        1,
    ),
    (
        "token-ise the inline profit badge",
        "background: rgba(34,197,94,0.12); color: #16A34A; font-weight: 600;",
        "background: rgba(34,197,94,0.12); color: var(--badge-done-fg); font-weight: 600;",
        1,
    ),
    (
        "token-ise the calendar tile icon",
        "background: rgba(247,147,30,0.16); color: #B45309;",
        "background: rgba(247,147,30,0.16); color: var(--badge-action-fg);",
        1,
    ),
    (
        "token-ise the pipeline dot colour",
        "v === '◐' ? '#0E7490'",
        "v === '◐' ? 'var(--badge-transit-fg)'",
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
        applied.append(desc)
    return inner, applied


def main():
    src = bundle.read(os.path.join(ROOT, "index.html"))
    inner, applied = apply(bundle.get_template(src))
    out = bundle.set_template(src, inner)
    bundle.verify(out)
    for target in TARGETS:
        bundle.write(os.path.join(ROOT, target), out)
    print("Applied badge token fixes:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
