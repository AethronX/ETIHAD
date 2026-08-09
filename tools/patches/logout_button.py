#!/usr/bin/env python3
"""Add a sign-out control to the profile menu.

The homepage that now sits in front of the ERP (website/homepage.html) links
its "تسجيل الدخول" buttons at /erp -- but nothing inside the ERP itself ever
linked back out. The profile dropdown in the top bar had a role switcher and
nothing else: no way to leave the system without editing the URL by hand.

This adds a "تسجيل الخروج" item below the role list, styled with
--sem-late-text (already the checked, WCAG-safe token for this exact red) and
wired to navigate to "/", the public homepage.

Run against the inner document, not the bundle:

    python3 tools/patches/logout_button.py   # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

ICONS_OLD = (
    "    'columns-3': '<rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\"/>"
    '<path d="M9 3v18"/><path d="M15 3v18"/>\',\n  };'
)
ICONS_NEW = (
    "    'columns-3': '<rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\"/>"
    "<path d=\"M9 3v18\"/><path d=\"M15 3v18\"/>',\n"
    "    'log-out': '<path d=\"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4\"/>"
    '<polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>\',\n'
    "  };"
)

PROPS_OLD = (
    "      profileOpen: s.profile, toggleProfile: () => this.setState({"
    " profile: !s.profile, notifs: false }),"
)
PROPS_NEW = (
    PROPS_OLD
    + "\n      logoutIcon: I('log-out', 15), logout: () => { window.location.href = '/'; },"
)

MENU_OLD = (
    '          <div style="font-size: 12px; color: var(--t2); line-height: 1.7;'
    ' padding: 12px 8px 4px; border-top: 1px solid var(--bd); margin-top: 10px;">'
    "{{ roleScope }}</div>\n        </div>"
)
MENU_NEW = (
    '          <div style="font-size: 12px; color: var(--t2); line-height: 1.7;'
    ' padding: 12px 8px 4px; border-top: 1px solid var(--bd); margin-top: 10px;">'
    "{{ roleScope }}</div>\n"
    '          <div style="border-top: 1px solid var(--bd); margin-top: 10px;'
    ' padding-top: 6px;">\n'
    '            <button sc-camel-on-click="{{ logout }}" style="width: 100%;'
    " display: flex; align-items: center; gap: 10px; padding: 9px 8px;"
    " background: transparent; border: 0; border-radius: 10px; cursor: pointer;"
    ' color: var(--sem-late-text); font-size: 13px; font-weight: 600;'
    ' font-family: inherit;" style-hover="background: var(--bg);">\n'
    '              <span style="{{ logoutIcon }}"></span>\n'
    "              <span>تسجيل الخروج</span>\n"
    "            </button>\n"
    "          </div>\n"
    "        </div>"
)

EDITS = [
    ("register the log-out icon", ICONS_OLD, ICONS_NEW, 1),
    ("compute the icon and the navigate-home handler", PROPS_OLD, PROPS_NEW, 1),
    ("add the sign-out item to the profile dropdown", MENU_OLD, MENU_NEW, 1),
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
    print("Applied logout button:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
