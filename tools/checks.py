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
