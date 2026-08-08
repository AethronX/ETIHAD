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
`tools/checks.py` is still present. On conflict it writes
`tools/.conflict.html` and touches nothing.

The one conflict that recurs is the bundled asset id in `<head>`: each export
mints a new uuid. Keep the **new** export's id and re-add the Supabase block
beneath it.

After it runs, verify in a browser before pushing — `tools/apply.py` checks that
customizations survived, not that the page still works.

## What is customized

Nine customizations are asserted by `tools/checks.py`. Add a check there
whenever you add another, or the next export will quietly drop it.

- Supabase client + the `metric_entries` manual-metrics layer (editable daily
  revenue, inventory value, overdue receivables KPIs)
- Sidebar collapsed by default
- Receivables labelled مستحقات rather than ذمم
- Accessibility: `lang="ar"`, dialog semantics on the four overlays,
  `scope="col"` on column headers, and the contrast token work below

### Colour tokens

Two splits exist because one value could not serve two contrast directions:

- `--p` fills primary buttons (white text sits on it); `--p-text` colours brand
  text (it sits on the page). Light theme resolves both to `#0F4C81`; dark uses
  `#33739F` for fill and `#7FB6E4` for text.
- `--badge-*-fg` gives each semantic badge a per-theme foreground. Values were
  computed against each badge's own tint over its card, not eyeballed.

Both themes currently measure **zero** WCAG AA contrast failures on the
dashboard. Re-measure after changing any colour.

## Deployment

Vercel builds from `main` only. Work on a branch, but production does not move
until `main` does.

## Local checks

```bash
python3 -c "import sys; sys.path.insert(0,'tools'); import bundle, checks; \
  print(checks.run(bundle.verify(bundle.read('index.html'))))"
```

`bundle.verify()` is the important one: it catches a literal `</script>` in the
payload, which would close the wrapping script tag and truncate the entire
application. Any code that re-encodes the template must escape it as
`</`, which `bundle.set_template()` does.
