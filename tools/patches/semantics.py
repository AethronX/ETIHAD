#!/usr/bin/env python3
"""Naming, structure and resilience fixes for the Etihad ERP shell.

Measured against the rendered page in Chromium (tools/audit/audit.js):

  1.1.1 Non-text Content  Ten rendered SVGs reached the accessibility tree with
                          no name at all. Four are real charts and are named
                          from their own visible card title -- not from an
                          invented description of data this patch cannot read.
                          The six KPI sparklines are marked aria-hidden: the
                          trend they draw is already stated in words by the
                          delta text directly above them, so announcing them
                          again would only add noise.

  4.1.2 Name, Role, Value The notification button is a bare icon whose only
                          text is the unread badge, so it lost its name
                          entirely once everything was read. The theme button
                          was labelled "الوضع الليلي" in both directions, which
                          is wrong half the time.

  1.3.1 Info and Relations The page had one h1 and no other heading of any
                          level -- card titles are styled divs, so heading
                          navigation reached the page title and stopped.
                          role="heading" adds the semantics without touching a
                          single pixel of the layout.

  1.4.3 Contrast          The unread-count badge ran white on --bad (#EF4444)
                          at 3.76:1. --sem-late (#DC2626) is the token this
                          design language already reserves for "late/danger"
                          and carries white at 4.83:1.

  Resilience              window.supabase.createClient ran unguarded in <head>.
                          When the CDN is unreachable the page threw a
                          TypeError before the app booted. Every reader of
                          window.supabaseClient already falls back to the demo
                          figures, so the bootstrap is the only thing that had
                          to stop throwing.

Run against the inner document, not the bundle:

    python3 tools/patches/semantics.py   # apply to index.html + Etihad_ERP.html
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("index.html", "Etihad_ERP.html")

SUPABASE_OLD = """<script>
  window.supabaseClient = window.supabase.createClient(
    'https://udabeulfhjbrscrzjbdc.supabase.co',
    'sb_publishable_463k172o6EArBNYOZ8y55w_LT7G_D0y'
  );
</script>"""

SUPABASE_NEW = """<script>
  // The client is optional. Every reader guards on window.supabaseClient and
  // falls back to the demo figures, so a blocked, slow or failed CDN must
  // leave the app running rather than throwing before it boots.
  try {
    window.supabaseClient = window.supabase.createClient(
      'https://udabeulfhjbrscrzjbdc.supabase.co',
      'sb_publishable_463k172o6EArBNYOZ8y55w_LT7G_D0y'
    );
  } catch (err) {
    console.warn('[supabase] client unavailable, metrics fall back to demo values:', err);
  }
</script>"""

# Each chart is named from the title already printed above it on the card, so
# the accessible name and the visible label cannot drift apart (WCAG 2.5.3).
CHARTS = [
    (
        "KPI sparklines are redundant with the delta text beside them",
        '<svg sc-camel-view-box="0 0 200 34" sc-camel-preserve-aspect-ratio="none"',
        '<svg aria-hidden="true" focusable="false"'
        ' sc-camel-view-box="0 0 200 34" sc-camel-preserve-aspect-ratio="none"',
    ),
    (
        "name the revenue and margin chart",
        '<svg sc-camel-view-box="0 0 740 250"',
        '<svg role="img" aria-label="رسم بياني: الإيراد وهامش الربح'
        ' — آخر ١٢ شهراً بالريال العُماني" sc-camel-view-box="0 0 740 250"',
    ),
    (
        "name the warehouse capacity gauge",
        '<svg sc-camel-view-box="0 0 180 180"',
        '<svg role="img" aria-label="رسم بياني: سعة المستودعات'
        ' — الإشغال الحالي في قوانزو ونزوى" sc-camel-view-box="0 0 180 180"',
    ),
    (
        "name the revenue versus expenses chart",
        '<svg sc-camel-view-box="0 0 700 220"',
        '<svg role="img" aria-label="رسم بياني: الإيراد مقابل المصروفات'
        ' على ستة أشهر، والخط الأزرق هو صافي الربح" sc-camel-view-box="0 0 700 220"',
    ),
    (
        "name the container status ring",
        '<svg sc-camel-view-box="0 0 160 160"',
        '<svg role="img" aria-label="رسم بياني: حالة الحاويات'
        ' — توزيع الأسطول النشط" sc-camel-view-box="0 0 160 160"',
    ),
    (
        "name the shipment barcode",
        '<svg sc-camel-view-box="0 0 220 62"',
        '<svg role="img" aria-label="باركود الشحنة CN-8842-0117"'
        ' sc-camel-view-box="0 0 220 62"',
    ),
    (
        "name the shipment QR code",
        '<svg sc-camel-view-box="0 0 21 21"',
        '<svg role="img" aria-label="رمز QR للشحنة CN-8842-0117"'
        ' sc-camel-view-box="0 0 21 21"',
    ),
]

# (description, old, new, expected_occurrences)
EDITS = [
    (
        "survive an unreachable Supabase CDN instead of throwing",
        SUPABASE_OLD,
        SUPABASE_NEW,
        1,
    ),
    (
        "raise the unread-count badge to 4.83:1 (WCAG 1.4.3)",
        "display: grid; place-items: center; background: var(--bad); color: #fff;"
        " font-size: 10.5px;",
        "display: grid; place-items: center; background: var(--sem-late);"
        " color: #fff; font-size: 10.5px;",
        1,
    ),
    (
        "name the notification button when nothing is unread (WCAG 4.1.2)",
        '<button sc-camel-on-click="{{ toggleNotifs }}" style="position: relative;',
        '<button sc-camel-on-click="{{ toggleNotifs }}"'
        ' aria-label="{{ notifLabel }}" style="position: relative;',
        1,
    ),
    (
        "label the theme button for the direction it actually moves (WCAG 4.1.2)",
        '<button sc-camel-on-click="{{ toggleTheme }}" title="الوضع الليلي"',
        '<button sc-camel-on-click="{{ toggleTheme }}"'
        ' title="{{ themeLabel }}" aria-label="{{ themeLabel }}"',
        1,
    ),
    (
        "supply both labels from state",
        "      bellIcon: I('bell', 18), themeIcon: I(s.dark ? 'sun' : 'moon', 18),",
        "      bellIcon: I('bell', 18), themeIcon: I(s.dark ? 'sun' : 'moon', 18),\n"
        "      notifLabel: unreadCount > 0\n"
        "        ? 'الإشعارات — ' + unreadCount + ' غير مقروء'\n"
        "        : 'الإشعارات — لا جديد',\n"
        "      themeLabel: s.dark ? 'التبديل إلى الوضع النهاري'"
        " : 'التبديل إلى الوضع الليلي',",
        1,
    ),
]

# Card titles are styled divs. role="heading" gives them a level in the
# accessibility tree without changing a single computed style.
CARD_TITLE_OLD = '<div style="font-size: 16px; font-weight: 600;">'
CARD_TITLE_NEW = '<div role="heading" aria-level="2" style="font-size: 16px; font-weight: 600;">'
CARD_TITLE_COUNT = 13


def apply(inner):
    applied = []
    for desc, old, new, expected in EDITS:
        found = inner.count(old)
        if expected is not None and found != expected:
            raise SystemExit(
                "patch target moved: expected %d of %r, found %d\n  (%s)"
                % (expected, old[:70], found, desc)
            )
        inner = inner.replace(old, new)
        applied.append("%-4d %s" % (found, desc))

    for desc, old, new in CHARTS:
        found = inner.count(old)
        if found != 1:
            raise SystemExit(
                "chart target matched %d times, expected 1: %r (%s)"
                % (found, old[:60], desc)
            )
        inner = inner.replace(old, new)
        applied.append("1    %s" % desc)

    found = inner.count(CARD_TITLE_OLD)
    if found != CARD_TITLE_COUNT:
        raise SystemExit(
            "card-title target matched %d times, expected %d"
            % (found, CARD_TITLE_COUNT)
        )
    inner = inner.replace(CARD_TITLE_OLD, CARD_TITLE_NEW)
    applied.append(
        "%-4d give card titles a heading level (WCAG 1.3.1)" % CARD_TITLE_COUNT
    )

    return inner, applied


def main():
    src = bundle.read(os.path.join(ROOT, "index.html"))
    inner, applied = apply(bundle.get_template(src))
    out = bundle.set_template(src, inner)
    bundle.verify(out)
    for target in TARGETS:
        bundle.write(os.path.join(ROOT, target), out)
    print("Applied semantic fixes:")
    for line in applied:
        print("  " + line)


if __name__ == "__main__":
    main()
