"""Assertions that every hand-written customization survived an export merge.

Each entry is (name, why_it_matters, predicate). `apply.py` refuses to write
the site if any predicate fails, which turns a silent regression -- the failure
mode that lost the Supabase integration twice -- into a loud one.

When you add a customization to the site, add a check for it here.
"""

import collections
import re

Report = collections.namedtuple("Report", "passed failed")


def _count(inner, needle):
    return inner.count(needle)


CHECKS = (
    (
        "Supabase client",
        "the metrics layer silently no-ops without it",
        lambda s: "window.supabaseClient" in s and "supabase-js@2" in s,
    ),
    (
        "manual metrics layer",
        "editable KPIs read and write the metric_entries table",
        lambda s: "metric_entries" in s and "loadMetrics" in s and "editMetric" in s,
    ),
    (
        "editable KPI wiring",
        "revenue, inventory and receivables cards fall back to demo numbers without it",
        lambda s: all(k in s for k in ("daily_revenue", "inventory_value", "overdue_receivables")),
    ),
    (
        "sidebar collapsed by default",
        "deliberate default from 3260a51",
        lambda s: "mini: true" in s,
    ),
    (
        "receivables terminology",
        "user-facing labels use مستحقات, not ذمم",
        lambda s: "مستحقات" in s and not re.search(r"'[^']*\bذمم\b[^']*'\s*}", s),
    ),
    (
        "document language",
        "screen readers need lang to pick an Arabic voice (WCAG 3.1.1)",
        lambda s: 'lang="ar"' in s,
    ),
    (
        "dialog semantics",
        "overlays must announce as dialogs (WCAG 4.1.2)",
        lambda s: s.count('role="dialog"') >= 4 and 'aria-modal="true"' in s,
    ),
    (
        "table header scope",
        "column headers must be associated with their cells (WCAG 1.3.1)",
        lambda s: 'scope="col"' in s,
    ),
    (
        "readable secondary text",
        "muted text must clear 4.5:1 (WCAG 1.4.3)",
        lambda s: "--t3: #6B7280" in s and "--side-t2: #A9B6C8" in s,
    ),
    (
        "hidden nav leaves the tab order",
        "opacity alone keeps 31 invisible controls keyboard-reachable (WCAG 2.4.3)",
        lambda s: 'pointer-events: none; visibility: hidden;' in s
        and 'transform: none; visibility: visible;' in s,
    ),
    (
        "dialog focus trap",
        "aria-modal does not contain Tab; trapFocus does (WCAG 2.4.3)",
        lambda s: "trapFocus(e)" in s and "if (e.key === 'Tab') this.trapFocus(e);" in s,
    ),
    (
        "overlay focus return",
        "closing an overlay must hand focus back to its trigger (WCAG 2.4.3)",
        lambda s: "_returnFocus" in s and "componentDidUpdate()" in s,
    ),
    (
        "Escape dismisses every overlay",
        "the AI panel and workspace menu were pointer-only (WCAG 2.1.2)",
        lambda s: re.search(
            r"e\.key === 'Escape'.*?aiOpen: false.*?wsOpen: false", s
        )
        is not None,
    ),
    (
        "skip link",
        "31 nav controls precede the content on all 23 pages (WCAG 2.4.1)",
        lambda s: 'data-skip-link="1"' in s
        and 'href="#etihad-main"' in s
        and 'id="etihad-main"' in s,
    ),
    (
        "named charts",
        "four charts carry a name; the six sparklines are deliberately hidden "
        "(WCAG 1.1.1)",
        lambda s: s.count('<svg role="img" aria-label=') >= 6
        and '<svg aria-hidden="true" focusable="false"' in s,
    ),
    (
        "icon-button names",
        "the bell loses its only text when nothing is unread (WCAG 4.1.2)",
        lambda s: "notifLabel" in s and "themeLabel" in s,
    ),
    (
        "card titles are headings",
        "without a level, heading navigation stops at the page title "
        "(WCAG 1.3.1)",
        lambda s: s.count('role="heading" aria-level="2"') >= 13,
    ),
    (
        "unread badge contrast",
        "white on --bad measured 3.76:1; --sem-late carries it at 4.83:1 "
        "(WCAG 1.4.3)",
        lambda s: "background: var(--sem-late); color: #fff; font-size: 10.5px;" in s,
    ),
    (
        "touch target size",
        'the two "عرض الكل" links measured 86x17 (WCAG 2.5.8)',
        lambda s: s.count("padding: 5px 6px; margin: -5px -6px;") == 2,
    ),
    (
        "resilient Supabase bootstrap",
        "an unreachable CDN threw before the app booted",
        lambda s: "window.supabaseClient = window.supabase.createClient" in s
        and re.search(r"try \{\s*window\.supabaseClient", s) is not None,
    ),
)


def run(inner):
    passed, failed = [], []
    for name, why, predicate in CHECKS:
        try:
            ok = bool(predicate(inner))
        except Exception:
            ok = False
        (passed.append(name) if ok else failed.append((name, why)))
    return Report(passed=passed, failed=failed)
