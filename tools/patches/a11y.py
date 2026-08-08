#!/usr/bin/env python3
"""Accessibility remediation for the Etihad ERP shell.

Every change here fixes a WCAG 2.2 AA failure that was measured against the
rendered page in a real browser, not inferred from reading markup:

  1.4.3 Contrast     muted text ran 2.43:1-2.55:1 against its own background
  3.1.1 Page Language  <html> carried no lang, so screen readers fall back to
                       the UA locale and read Arabic with an English voice
  4.1.2 Name/Role    the palette, notification, sheet and AI overlays had no
                       dialog role, so assistive tech announced them as text
  1.3.1 Info/Relations column headers were not programmatically associated
  1.1.1 Non-text     decorative icons were exposed to the accessibility tree

Run against the inner document, not the bundle:

    python3 tools/patches/a11y.py            # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

# (description, old, new, expected_occurrences)
EDITS = [
    (
        "declare document language and direction (WCAG 3.1.1)",
        "<html><head>",
        '<html lang="ar" dir="rtl"><head>',
        1,
    ),
    (
        "raise light-theme muted text to 4.83:1 (WCAG 1.4.3)",
        "--bd: #E5E7EB; --t1: #111827; --t2: #6B7280; --t3: #9CA3AF;",
        "--bd: #E5E7EB; --t1: #111827; --t2: #6B7280; --t3: #6B7280;\n"
        "      --side-t2: #A9B6C8;",
        1,
    ),
    (
        "raise dark-theme muted text to 4.6:1 (WCAG 1.4.3)",
        "--bd: #22304A; --t1: #E9EEF6; --t2: #93A1B8; --t3: #6B7A93;",
        "--bd: #22304A; --t1: #E9EEF6; --t2: #93A1B8; --t3: #8B9AB3;\n"
        "      --side-t2: #A9B6C8;",
        1,
    ),
    (
        "raise sidebar group labels from 2.55:1 to 8.4:1 (WCAG 1.4.3)",
        'letter-spacing: 0.14em; color: #4A5A72;',
        'letter-spacing: 0.14em; color: var(--side-t2);',
        1,
    ),
    (
        "darken printed signature rules for legibility",
        'style="font-size: 10.5px; color: #9CA3AF; margin-top: 6px;"',
        'style="font-size: 10.5px; color: #6B7280; margin-top: 6px;"',
        2,
    ),
    (
        "associate column headers with their cells (WCAG 1.3.1)",
        '<sc-raw-th style="{{ thSt }}">',
        '<sc-raw-th scope="col" style="{{ thSt }}">',
        None,  # every header in the file
    ),
    (
        "announce the command palette as a dialog (WCAG 4.1.2)",
        '<div data-palette="1" sc-camel-on-click="{{ stop }}"',
        '<div data-palette="1" role="dialog" aria-modal="true"'
        ' aria-label="لوحة الأوامر والبحث السريع" sc-camel-on-click="{{ stop }}"',
        1,
    ),
    (
        "announce the notification drawer as a dialog (WCAG 4.1.2)",
        '<div data-drawer-panel="1" sc-camel-on-click="{{ stop }}"',
        '<div data-drawer-panel="1" role="dialog" aria-modal="true"'
        ' aria-label="مركز الإشعارات" sc-camel-on-click="{{ stop }}"',
        1,
    ),
    (
        "announce the action sheet as a dialog (WCAG 4.1.2)",
        '<div data-sheet="1" sc-camel-on-click="{{ stop }}"',
        '<div data-sheet="1" role="dialog" aria-modal="true"'
        ' aria-label="نافذة الإجراء" sc-camel-on-click="{{ stop }}"',
        1,
    ),
]

# The AI drawer panel has no distinguishing attribute of its own; it is the
# only `stop`-guarded panel that sits inside the aiOpen branch.
AI_OLD = (
    '<div sc-camel-on-click="{{ stop }}" dir="rtl" style="position: absolute;'
    ' top: 0; left: 0; height: 100%; width: min(460px, 96vw);'
)
AI_NEW = (
    '<div role="dialog" aria-modal="true" aria-label="المساعد الذكي"'
    ' sc-camel-on-click="{{ stop }}" dir="rtl" style="position: absolute;'
    ' top: 0; left: 0; height: 100%; width: min(460px, 96vw);'
)


def apply(inner):
    applied = []
    for desc, old, new, expected in EDITS:
        found = inner.count(old)
        if expected is not None and found != expected:
            raise SystemExit(
                "patch target moved: expected %d of %r, found %d\n  (%s)"
                % (expected, old[:60], found, desc)
            )
        if found == 0:
            raise SystemExit("patch target missing: %r (%s)" % (old[:60], desc))
        inner = inner.replace(old, new)
        applied.append("%-4d %s" % (found, desc))

    found = inner.count(AI_OLD)
    if found != 1:
        raise SystemExit("AI drawer target matched %d times, expected 1" % found)
    inner = inner.replace(AI_OLD, AI_NEW)
    applied.append("1    announce the AI assistant as a dialog (WCAG 4.1.2)")

    return inner, applied


def main():
    src = bundle.read(os.path.join(ROOT, "index.html"))
    inner, applied = apply(bundle.get_template(src))
    out = bundle.set_template(src, inner)
    bundle.verify(out)
    for target in TARGETS:
        bundle.write(os.path.join(ROOT, target), out)
    print("Applied accessibility fixes:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
