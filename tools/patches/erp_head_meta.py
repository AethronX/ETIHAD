#!/usr/bin/env python3
"""Give the ERP a real page title, and mark it non-indexable.

The bundler's loader shell -- the outer <head>, before the
__bundler/template script -- shipped with the generic exporter default
<title>Bundled Page</title>. That's both a real accessibility gap
(WCAG 2.4.2 Page Titled) and unprofessional as a browser-tab/bookmark
title, independent of anything about search engines.

Also adds <meta name="robots" content="noindex, nofollow">. This is a
deliberate choice, not an oversight: an internal, login-gated ERP is
exactly the kind of page that should never be indexed by a search
engine -- unlike the public homepage (which now scores 100/100 on
Lighthouse SEO, mobile and desktop, verified), "SEO" isn't a goal that
makes sense for this page at all. Adding noindex means this page will
correctly score below 100 on Lighthouse's is-crawlable audit, on
purpose.

This edit is unlike every other patch in this directory: <title> and
<meta> here live in the loader shell itself, not inside the escaped
__bundler/template JSON payload, so it operates on the raw file text
rather than through bundle.get_template()/set_template().

Run directly against the files, not the inner document:

    python3 tools/patches/erp_head_meta.py   # apply to erp/index.html + erp/Etihad_ERP.html
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import bundle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGETS = ("erp/index.html", "erp/Etihad_ERP.html")

OLD = '<meta charset="utf-8">\n  <title>Bundled Page</title>\n'
NEW = (
    '<meta charset="utf-8">\n'
    '  <title>نظام اتحاد لإدارة الموارد</title>\n'
    '  <meta name="robots" content="noindex, nofollow">\n'
)


def main():
    applied = []
    for target in TARGETS:
        path = os.path.join(ROOT, target)
        text = bundle.read(path)
        found = text.count(OLD)
        if found != 1:
            raise SystemExit(
                "patch target moved: expected 1 of %r, found %d in %s"
                % (OLD[:60], found, target)
            )
        text = text.replace(OLD, NEW, 1)
        bundle.verify(text)  # still a loadable bundle after a loader-shell edit
        bundle.write(path, text)
        applied.append(target)

    print("Applied ERP head metadata:")
    for target in applied:
        print("  " + target)


if __name__ == "__main__":
    main()
