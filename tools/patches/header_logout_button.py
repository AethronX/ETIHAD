#!/usr/bin/env python3
"""Add a directly visible sign-out button to the header.

The sign-out control added earlier (tools/patches/logout_button.py) works,
but only lives inside the profile dropdown -- reported as "there's no
sign-out button" because nothing in the header hints it's there. Adds a
second, always-visible entry point next to the other header icon buttons,
styled with --sem-late-text (the same checked, WCAG-safe token the dropdown
item already uses) so it reads as a distinct "leave" action. Both reuse the
same `logout`/`logoutIcon` computed props -- no new navigation logic.

Also gives "تسجيل الخروج" a proper T-dictionary entry: the dropdown item was
still a hardcoded Arabic literal even in English/Chinese mode, a gap from
the original patch. Both the header button and the dropdown item now read
from the same translated label.

The new button carries data-lo="1" -- the existing "large-only" convention
this file already uses (`[data-lo] { display: none !important; }` inside
`@media (max-width: 1080px)`) -- so it hides below the mobile breakpoint
instead of crowding the header and pushing [data-hamburger] off-screen,
which is exactly what the first version of this patch did before being
caught by tools/audit/behaviour.js's mobile-drawer checks. Mobile users
still reach sign-out through the profile dropdown, which was never touched
and stays visible at every width.

Run against the inner document, not the bundle:

    python3 tools/patches/header_logout_button.py   # apply to erp/index.html + erp/Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("erp/index.html", "erp/Etihad_ERP.html")

DICT_OLD = "    lang_label: { ar: 'اللغة', en: 'Language', zh: '语言' },"
DICT_NEW = (
    DICT_OLD
    + "\n    logout_label: { ar: 'تسجيل الخروج', en: 'Log Out', zh: '退出登录' },"
)

PROPS_OLD = (
    "      zoneWarehouse: this.t('zone_warehouse'), zoneYourWork: this.t('zone_your_work'),"
)
PROPS_NEW = PROPS_OLD + "\n      logoutLabel: this.t('logout_label'),"

DROPDOWN_OLD = "              <span>تسجيل الخروج</span>"
DROPDOWN_NEW = "              <span>{{ logoutLabel }}</span>"

HEADER_OLD = (
    '        <button sc-camel-on-click="{{ toggleProfile }}" style="display: flex;'
    " align-items: center; gap: 10px; height: 40px; padding: 0 6px 0 12px; background:"
    " transparent; border: 1px solid var(--bd); border-radius: 12px; cursor: pointer;"
    ' color: var(--t1);" style-hover="background: var(--bg);">\n'
    '          <div style="width: 28px; height: 28px; border-radius: 9px; background:'
    " var(--p-tint); color: var(--p-text); display: grid; place-items: center;"
    ' font-size: 11.5px; font-weight: 700;">{{ userInitials }}</div>\n'
    '          <div data-hide-sm="1" style="text-align: right; line-height: 1.25;">\n'
    '            <div style="font-size: 12.5px; font-weight: 600; white-space: nowrap;">'
    "{{ userName }}</div>\n"
    '            <div style="font-size: 11px; color: var(--t2); white-space: nowrap;">'
    "{{ roleLabel }}</div>\n"
    "          </div>\n"
    "        </button>\n"
    "      </div>"
)
HEADER_NEW = (
    HEADER_OLD[: -len("\n      </div>")]
    + '\n        <button data-lo="1" sc-camel-on-click="{{ logout }}" title="{{ logoutLabel }}"'
    ' aria-label="{{ logoutLabel }}" style="width: 40px; height: 40px; display: grid;'
    " place-items: center; background: transparent; border: 1px solid var(--bd);"
    ' border-radius: 12px; cursor: pointer; color: var(--sem-late-text);"'
    ' style-hover="background: var(--bg); border-color: var(--sem-late-text);">\n'
    '          <span style="{{ logoutIcon }}"></span>\n'
    "        </button>\n"
    "      </div>"
)

EDITS = [
    ("give تسجيل الخروج a T-dictionary entry", DICT_OLD, DICT_NEW, 1),
    ("compute logoutLabel", PROPS_OLD, PROPS_NEW, 1),
    ("route the dropdown item through the translated label", DROPDOWN_OLD, DROPDOWN_NEW, 1),
    ("add a directly visible sign-out button to the header", HEADER_OLD, HEADER_NEW, 1),
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
    print("Applied header logout button:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
