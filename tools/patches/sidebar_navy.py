#!/usr/bin/env python3
"""Match the sidebar to the brand navy used across the public website.

The nav rail (`--side` / `--side-h`) used generic slate (#0F172A / #1E293B),
not the brand navy the logo, the marketing homepage, and tools/subframe's own
theme doc all agree on: #051C4A for dark surfaces, #0A2A63 for a secondary
depth inside them (website/homepage.html --navy / --navy-2; tools/subframe/01-theme.md).
The primary/accent tokens (--p, --p2, --acc, --sem-done) already matched the
website's blue/cyan/orange/green exactly -- only this one surface drifted.

Contrast re-checked by hand before writing this (WCAG 1.4.3), all comfortably
above AA on the new background:

    white on #051C4A       16.52:1  (was 17.85:1 on the old slate)
    #94A3B8 on #051C4A      6.44:1  (was  6.96:1)
    #A9B6C8 on #051C4A      8.03:1  (was  8.68:1)
    white on #0A2A63       13.78:1  (was 14.63:1 on the old slate)

The sidebar subtitle "CHINA — OMAN ERP" was hardcoded to #64748B, which was
already marginal against the old slate (3.75:1, below the 4.5:1 normal-text
floor -- invisible to the existing audits only because it's not rendered
while the sidebar is collapsed, its default state). Routed it through
--side-t2 instead (8.03:1 on the new navy) while this surface was already
open, rather than leaving a second latent failure sitting next to the fix.

Run against the inner document, not the bundle:

    python3 tools/patches/sidebar_navy.py   # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

EDITS = [
    (
        "sidebar surfaces: slate to brand navy",
        "--bg: #F8FAFC; --card: #FFFFFF; --side: #0F172A; --side-h: #1E293B;",
        "--bg: #F8FAFC; --card: #FFFFFF; --side: #051C4A; --side-h: #0A2A63;",
        1,
    ),
    (
        "sidebar subtitle: hardcoded gray to the sidebar's own muted token",
        '<div style="color: #64748B; font-size: 11px; letter-spacing: 0.06em;'
        ' white-space: nowrap; margin-top: 2px;">CHINA — OMAN ERP</div>',
        '<div style="color: var(--side-t2); font-size: 11px; letter-spacing:'
        ' 0.06em; white-space: nowrap; margin-top: 2px;">CHINA — OMAN ERP</div>',
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
    print("Applied navy sidebar:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
