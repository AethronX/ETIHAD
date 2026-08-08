"""Read and rewrite the inner document of an Etihad ERP bundle export.

The published file is a generated artifact: a small loader plus four
`<script type="__bundler/...">` blocks, each holding a JSON payload. The real
application markup lives in the `template` block as a single JSON string.

Editing that payload by hand is what these helpers exist for -- see
tools/apply.py for the pipeline that uses them.
"""

import json
import re

SECTIONS = ("manifest", "ext_resources", "page_order", "template")

_SECTION_RE = '<script type="__bundler/%s">\n(.*?)\n  </script>'


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def section(text, name):
    """Return (start, end, raw_json) for one bundler section."""
    match = re.search(_SECTION_RE % name, text, re.S)
    if not match:
        raise KeyError("no __bundler/%s section in this file" % name)
    return match.start(1), match.end(1), match.group(1)


def get_template(text):
    """Decode the inner application document."""
    return json.loads(section(text, "template")[2])


def set_template(text, inner):
    """Re-encode `inner` back into the bundle.

    A literal ``</script>`` inside the payload would close the wrapping
    ``<script type="__bundler/template">`` tag and truncate the whole
    application, so the slash is escaped exactly as the bundler emits it.
    """
    start, end, _ = section(text, "template")
    payload = json.dumps(inner, ensure_ascii=False).replace("</", "<\\u002F")
    return text[:start] + payload + text[end:]


def verify(text):
    """Raise if `text` is not a loadable bundle. Returns the inner document."""
    raw = section(text, "template")[2]
    if "</script>" in raw:
        raise ValueError("literal </script> in payload would truncate the page")
    for name in SECTIONS:
        try:
            json.loads(section(text, name)[2])
        except json.JSONDecodeError as exc:
            raise ValueError("%s section is not valid JSON: %s" % (name, exc))
    return json.loads(raw)
