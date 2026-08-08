# Etihad ERP — working notes

## Read this before editing index.html

`index.html` and `Etihad_ERP.html` are **generated output**, not source. They
are exports from a visual builder: a small loader plus four
`<script type="__bundler/...">` JSON blocks, with the whole application living
as an escaped string inside the `template` block. The `sc-for`, `sc-if` and
`sc-camel-on-click` tags are that builder's template language.

The two files are byte-identical on purpose. `Etihad_ERP.html` is the named
export; `index.html` is the copy Vercel serves at the root route.

### Why this matters

Dropping a new export over the old file deletes every hand-written change made
since the last one. That has already happened twice:

| commit | what it was | what it destroyed |
| --- | --- | --- |
| `8d450d7` | export v2 | earlier hand edits |
| `6e00315` | export v3 | the entire Supabase integration, the manual-metrics layer, the sidebar default, and the receivables rename |

Both landed silently — the diff is one enormous line, so nothing looked wrong
in review.

## Applying a new export

Never copy an export over these files. Run:

```bash
python3 tools/apply.py path/to/new-export.html
```

It performs a three-way merge — previous export as base, the live site as ours,
the new export as theirs — then refuses to write unless every customization in
`tools/checks.py` is still present.

On conflict it writes the conflicted application document (readable HTML, not
the one-line bundle) to `tools/.conflict.html`, stashes the raw export beside
it, and touches nothing. Resolve the markers there, then finish with:

```bash
python3 tools/apply.py --resolved
```

which re-encodes it into the new export's bundle and re-runs every check before
writing. The second check is not skippable on purpose — a resolution that drops
a customization is the exact failure this tool exists to prevent.

The one conflict that recurs is the bundled asset id in `<head>`: each export
mints a new uuid, and the Supabase bootstrap sits directly beneath it. Keep the
**new** export's id and re-add the Supabase block below it.

`tools/apply.py` proves customizations survived, not that the page still works.
Before pushing, open it in a browser and run both audits below.

## What is customized

Twenty customizations are asserted by `tools/checks.py`. Add a check there
whenever you add another, or the next export will quietly drop it. Every check
fails against the file as it stood before its fix, so none of them is a
tautology — verify that with `git show <commit>:index.html` if you add one.

- Supabase client + the `metric_entries` manual-metrics layer (editable daily
  revenue, inventory value, overdue receivables KPIs). The bootstrap is wrapped
  in `try/catch`: readers already fall back to demo figures, so an unreachable
  CDN must not throw before the app boots.
- Sidebar collapsed by default
- Receivables labelled مستحقات rather than ذمم
- Accessibility, applied by `tools/patches/*.py` and measured by
  `tools/audit/*.js` — see below

### Accessibility

Two things bite here, and both are invisible in the markup:

**Hiding is not un-focusing.** The collapsed sidebar was hidden with
`opacity: 0` and `pointer-events: none`, and the mobile drawer with a
`transform`. None of those leave the tab order, so 31 invisible controls stayed
keyboard-reachable — a keyboard user pressed Tab 31 times through nothing
before reaching anything they could see. `visibility: hidden` is the one
mechanism that hides *and* un-focuses. Use it for any panel you hide.

**`aria-modal` does not contain Tab.** It hides the background from screen
readers only. Focus still walks the page behind an open overlay, so the
overlays carry an explicit `trapFocus`, plus a `componentDidUpdate` that hands
focus back to whatever opened them.

The rest: `lang="ar"`, dialog semantics on the four overlays, `scope="col"` on
column headers, a skip link to `#etihad-main`, named charts (the six KPI
sparklines are `aria-hidden` on purpose — the delta text beside them already
says it in words), `role="heading"` on card titles, and the colour tokens
below.

Chart names come from each card's own visible title, so the accessible name and
the visible label cannot drift apart. If you retitle a card, retitle its chart.

### Colour tokens

Two splits exist because one value could not serve two contrast directions:

- `--p` fills primary buttons (white text sits on it); `--p-text` colours brand
  text (it sits on the page). Light theme resolves both to `#0F4C81`; dark uses
  `#33739F` for fill and `#7FB6E4` for text.
- `--badge-*-fg` gives each semantic badge a per-theme foreground. Values were
  computed against each badge's own tint over its card, not eyeballed.

The unread-count badge uses `--sem-late`, not `--bad`: white on `--bad`
measures 3.76:1, white on `--sem-late` measures 4.83:1.

Both themes currently measure **zero** WCAG AA contrast failures on the
dashboard. Re-measure after changing any colour.

## Deployment

Vercel builds from `main` only. Work on a branch, but production does not move
until `main` does.

## Local checks

Three layers, and they answer different questions.

**Is the bundle loadable, and are the customizations still there?**

```bash
python3 -c "import sys; sys.path.insert(0,'tools'); import bundle, checks; \
  print(checks.run(bundle.verify(bundle.read('index.html'))))"
```

`bundle.verify()` is the important one: it catches a literal `</script>` in the
payload, which would close the wrapping script tag and truncate the entire
application. Any code that re-encodes the template must escape it as
`</`, which `bundle.set_template()` does.

**Does the rendered page still meet its budgets?**

```bash
node tools/audit/a11y.js        # contrast, names, targets, overflow, tab order
node tools/audit/behaviour.js   # skip link, focus return, focus trap, drawers
```

Both need Playwright and drive real Chromium against `file://index.html` — set
`CHROME_PATH` if Chromium is not on Playwright's default search path. Both exit
non-zero on failure, so they gate a release.

Every budget in `a11y.js` is currently **0** and every assertion in
`behaviour.js` passes. A non-zero reading means the page regressed, not that
the budget is wrong.

These exist because markup assertions cannot see resolved colours, computed box
sizes, or where the Tab key actually goes. `checks.py` proves a customization is
*present*; the audits prove the page still *behaves*.
