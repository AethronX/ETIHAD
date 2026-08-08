#!/usr/bin/env python3
"""Operability fixes for the Etihad ERP shell (WCAG principle 2).

Every defect below was measured by driving the rendered page with a real
keyboard in Chromium (tools/audit/probe.js), not inferred from the markup.

  2.4.3 Focus Order      The collapsed sidebar is hidden with `opacity: 0` and
                         `pointer-events: none`. Neither removes an element
                         from the tab order, so the 31 nav controls inside it
                         stayed keyboard-reachable while being invisible: a
                         keyboard user pressed Tab 31 times through nothing
                         before reaching the first control they could see. The
                         off-canvas mobile drawer had the same defect, hidden
                         by `transform` instead. `visibility: hidden` is the
                         one hiding mechanism that also drops descendants out
                         of the tab order.

  Mobile drawer broken   That same collapse rule is written for the desktop
                         rail but was never scoped to desktop, so on a phone it
                         also applied to the off-canvas drawer -- which is
                         driven by `data-drawer`, not `data-nav`. Opening the
                         drawer slid a panel into view that was still
                         `opacity: 0; pointer-events: none`: invisible, and
                         taps fell straight through it to the backdrop, which
                         closed it again. The sidebar has been unusable on
                         phones since 3260a51 made `mini` the default, because
                         that default is what put every phone on the path.
                         The rule is now confined to `min-width: 1081px`; on
                         mobile the drawer's own rules already hide it when
                         closed and show it when open.

  2.4.3 Focus Order      The four overlays declare `aria-modal="true"`, which
                         hides the background from screen readers but does
                         nothing to keyboard focus. Tab escaped the open
                         command palette after seven stops and kept walking the
                         page behind it. `trapFocus` cycles focus within
                         whichever dialog is on screen.

  2.1.2 No Keyboard Trap Escape closed the palette, notification drawer,
                         profile menu and action sheet -- but not the AI panel
                         or the workspace menu, which could only be dismissed
                         with a pointer.

  2.4.1 Bypass Blocks    There was no way to skip the navigation. With the
                         sidebar expanded that is 31 controls repeated ahead of
                         the content on every one of the 23 pages.

  2.5.8 Target Size      The two "عرض الكل" card links measured 86x17, under
                         the 24x24 minimum. Padding grows the hit area and an
                         equal negative margin keeps the layout identical, so
                         the target changes and the design does not.

Run against the inner document, not the bundle:

    python3 tools/patches/keyboard.py    # apply to index.html + Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

SKIP_LINK_CSS = """    /* رابط التخطي: خارج الشاشة حتى يستقبل التركيز (WCAG 2.4.1) */
    [data-skip-link] {
      position: fixed; top: 10px; right: 10px; z-index: 200;
      padding: 10px 18px; background: var(--card); color: var(--p-text);
      border: 2px solid var(--p-text); border-radius: 10px;
      font-size: 14px; font-weight: 600; text-decoration: none;
      transform: translateY(calc(-100% - 16px)); transition: transform 140ms ease;
    }
    [data-skip-link]:focus { transform: none; }
    @media (prefers-reduced-motion: reduce) {
      [data-skip-link] { transition: none; }
    }
"""

RETURN_FOCUS_JS = """
  // Closing an overlay must hand focus back to whatever opened it, otherwise
  // focus falls to <body> and a keyboard user restarts from the top of the
  // page (WCAG 2.4.3).
  _overlayOpen() {
    const s = this.state || {};
    return !!(s.palette || s.notifs || s.modal || s.aiOpen || s.profile);
  }
  // The builder's runtime does not promise componentDidUpdate arguments, so
  // the previous value is tracked here rather than read from prevState.
  componentDidUpdate() {
    const now = this._overlayOpen();
    const was = !!this._overlayWas;
    this._overlayWas = now;
    if (!was && now) {
      this._returnFocus = document.activeElement;
    } else if (was && !now) {
      const back = this._returnFocus;
      this._returnFocus = null;
      if (back && document.contains(back) && back !== document.body) back.focus();
    }
  }
"""

TRAP_FOCUS_JS = """
  // aria-modal hides the background from screen readers but leaves it in the
  // tab order, so an open overlay has to contain focus itself.
  trapFocus(e) {
    const open = Array.from(document.querySelectorAll('[role="dialog"]'))
      .filter((d) => d.getBoundingClientRect().width > 0);
    const dlg = open[open.length - 1];
    if (!dlg) return;
    const items = Array.from(dlg.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), select, textarea,'
      + ' [tabindex]:not([tabindex="-1"])'
    )).filter((n) => n.getBoundingClientRect().width > 0);
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (!dlg.contains(document.activeElement)) { e.preventDefault(); first.focus(); return; }
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
"""

# (description, old, new, expected_occurrences)
EDITS = [
    (
        "confine the desktop collapse to desktop, and drop it out of the"
        " tab order there (WCAG 2.4.3)",
        '    body[data-nav="mini"] aside[data-nav-panel]'
        ' { opacity: 0; pointer-events: none; }\n',
        '    @media (min-width: 1081px) {\n'
        '      body[data-nav="mini"] aside[data-nav-panel]'
        ' { opacity: 0; pointer-events: none; visibility: hidden; }\n'
        '    }\n',
        1,
    ),
    (
        "drop the closed mobile drawer out of the tab order (WCAG 2.4.3)",
        "        transform: translateX(-100%);"
        " transition: transform 220ms cubic-bezier(0.32,0.72,0,1);",
        "        transform: translateX(-100%); visibility: hidden;"
        " transition: transform 220ms cubic-bezier(0.32,0.72,0,1),"
        " visibility 0s 220ms;",
        1,
    ),
    (
        "restore the drawer to the tab order when it opens",
        'body[data-drawer="open"] aside[data-nav-panel] { transform: none; }',
        'body[data-drawer="open"] aside[data-nav-panel]'
        ' { transform: none; visibility: visible; transition:'
        ' transform 220ms cubic-bezier(0.32,0.72,0,1); }',
        1,
    ),
    (
        "style the skip link (WCAG 2.4.1)",
        '    :focus-visible { outline: 2px solid var(--p2);'
        ' outline-offset: 2px; border-radius: 6px; }\n',
        '    :focus-visible { outline: 2px solid var(--p2);'
        ' outline-offset: 2px; border-radius: 6px; }\n' + SKIP_LINK_CSS,
        1,
    ),
    (
        "add the skip link ahead of everything focusable (WCAG 2.4.1)",
        '<div data-app-shell="1" dir="rtl"',
        '<a href="#etihad-main" data-skip-link="1">تخطّي إلى المحتوى الرئيسي</a>\n\n'
        '<div data-app-shell="1" dir="rtl"',
        1,
    ),
    (
        "give the skip link a target it can move focus to",
        '<main data-pad="1" style="flex: 1;',
        '<main id="etihad-main" tabindex="-1" data-pad="1" style="flex: 1;',
        1,
    ),
    (
        "let Escape dismiss the AI panel and workspace menu (WCAG 2.1.2)",
        "if (e.key === 'Escape') { this.setState({ palette: false,"
        " notifs: false, profile: false, modal: false });",
        "if (e.key === 'Escape') { this.setState({ palette: false,"
        " notifs: false, profile: false, modal: false, aiOpen: false,"
        " wsOpen: false });",
        1,
    ),
    (
        "hold focus inside an open dialog (WCAG 2.4.3)",
        "      if ((e.ctrlKey || e.metaKey) && k === 'b')"
        " { e.preventDefault(); this.toggleNav(); }",
        "      if ((e.ctrlKey || e.metaKey) && k === 'b')"
        " { e.preventDefault(); this.toggleNav(); }\n"
        "      if (e.key === 'Tab') this.trapFocus(e);",
        1,
    ),
    (
        "make the drawer's own hide button close the drawer on mobile",
        "  toggleNav() {\n"
        "    const mini = !this.state.mini;",
        "  toggleNav() {\n"
        "    // `mini` is the desktop rail state and has no effect on a phone,\n"
        "    // where the panel is an off-canvas drawer. Without this the\n"
        '    // drawer\'s own "إخفاء القائمة" button was inert on mobile.\n'
        "    if (this.state.isMobile) { this.setDrawer(false); return; }\n"
        "    const mini = !this.state.mini;",
        1,
    ),
    (
        'grow the shipments "عرض الكل" link to 25px tall (WCAG 2.5.8)',
        'style="background: transparent; border: 0; cursor: pointer;'
        ' font-family: inherit; font-size: 13px; color: var(--p-text);'
        ' font-weight: 500;">عرض الكل ←</button>',
        'style="background: transparent; border: 0; cursor: pointer;'
        ' font-family: inherit; font-size: 13px; color: var(--p-text);'
        ' font-weight: 500; padding: 5px 6px; margin: -5px -6px;">'
        'عرض الكل ←</button>',
        1,
    ),
    (
        'grow the quotes "عرض الكل" link to 25px tall (WCAG 2.5.8)',
        'style="background: transparent; border: 0; cursor: pointer;'
        ' font-size: 13px; color: var(--p-text);'
        ' font-weight: 500;">عرض الكل ←</button>',
        'style="background: transparent; border: 0; cursor: pointer;'
        ' font-size: 13px; color: var(--p-text);'
        ' font-weight: 500; padding: 5px 6px; margin: -5px -6px;">'
        'عرض الكل ←</button>',
        1,
    ),
    (
        "define trapFocus and the overlay focus-return (WCAG 2.4.3)",
        "\n  say(msg) { clearTimeout(this._t);",
        RETURN_FOCUS_JS + TRAP_FOCUS_JS + "\n  say(msg) { clearTimeout(this._t);",
        1,
    ),
]


def apply(inner):
    applied = []
    for desc, old, new, expected in EDITS:
        found = inner.count(old)
        if expected is not None and found != expected:
            raise SystemExit(
                "patch target moved: expected %d of %r, found %d\n  (%s)"
                % (expected, old[:70], found, desc)
            )
        if found == 0:
            raise SystemExit("patch target missing: %r (%s)" % (old[:70], desc))
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
    print("Applied keyboard fixes:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
