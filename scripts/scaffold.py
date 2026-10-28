#!/usr/bin/env python3
"""Session scaffolder (proto-lab).

Pipeline step: after the seed rolled a **design direction card** (``roll.py``)
and the brief was turned into ``points.json``, this script lays down the session
directory — the pre-generation subset of the spec §4 tree:

    <target>/<slug>-<seed>/
      index.html                 # gallery, filled from assets/gallery.html
      direction.json             # the card, canonical JSON (source of truth)
      brief.md                   # captured brief placeholder (header only when absent)
      points.json                # the decision points, verbatim
      points/<id>-<slug>.html    # comparison canvas (assets/canvas.html)
      variants/<id>-<key>/       # one directory per option
        index.html               # variant shell (assets/variant-shell.html)

``target_dir`` is the **parent** (ruling R8): the session always lands in
``<target>/<slug>-<seed>/`` and the tree above is relative to it.

Two contracts shape the copies:

- Only ``index.html`` is *filled*. Substitution is textual and per-token:
  ``{{SEED}}``, ``{{DIRECTION_NAME}}``, ``{{FAMILY}}``, ``{{POINTS_TABLE_ROWS}}``.
- ``canvas.html`` and ``variant-shell.html`` are copied **unchanged**. In
  particular ``{{CANVAS_FRAMES}}`` is an *attribute anchor* on the deck
  container (``data-canvas-frames``), not a text token: the generator replaces
  the whole deck block later (ruling R16), so a blind ``str.replace`` over the
  canvas would corrupt the anchor it must find. ``{{CANVAS_TITLE}}`` and
  ``{{VARIANT_LABEL}}`` are likewise left for the generator.

The build is **idempotent and non-destructive**: every byte written is a
deterministic function of the inputs (the card carries no timestamp), and a file
that already exists is never rewritten. A second run over the same arguments
therefore changes nothing, the captured ``brief.md`` survives the scaffold step,
and files the later pipeline steps or the executor started are left alone. To
regenerate a session from changed inputs, remove its directory first.

Python stdlib only, Python >= 3.8.

Usage:
    python3 scripts/scaffold.py --target DIR --slug S --card card.json
                                --points points.json
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from pathlib import Path

# ``roll`` is the sibling module: it owns the canonical card encoding.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import roll  # noqa: E402  (imported after the sys.path tweak above)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

GALLERY_TEMPLATE = ASSETS / "gallery.html"
CANVAS_TEMPLATE = ASSETS / "canvas.html"
VARIANT_TEMPLATE = ASSETS / "variant-shell.html"

# The brief placeholder is created with its header only, and only when absent,
# so a brief captured in step 1 survives the step-3 scaffold.
BRIEF_HEADER = "# Brief\n"


def _write_if_absent(path, text):
    """Write ``text`` unless the file exists; existing bytes always win."""
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def _copy_if_absent(source, destination):
    """Copy ``source`` to ``destination`` unless the destination exists."""
    if not destination.exists():
        shutil.copyfile(source, destination)


def _option_summary(options):
    """``a — Sticky header CTA · b — Inline row action`` for the table cell."""
    return " · ".join(
        "%s — %s" % (option["key"], option["label"]) for option in options
    )


def _points_table_rows(points, slug):
    """One ``<tr>`` per decision point, for the gallery's table body."""
    rows = []
    for point in points.get("points", ()):
        status = point["status"]
        if point.get("chosen"):
            status = "%s (%s)" % (status, point["chosen"])
        rows.append(
            "\n".join(
                (
                    "          <tr>",
                    "            <td>%s</td>" % html.escape(str(point["id"])),
                    "            <td>%s</td>" % html.escape(str(point["axis"])),
                    "            <td>%s</td>" % html.escape(str(point["question"])),
                    "            <td>%s</td>"
                    % html.escape(_option_summary(point.get("options", ()))),
                    "            <td>%s</td>" % html.escape(str(status)),
                    '            <td><a href="points/%s-%s.html">canvas</a></td>'
                    % (html.escape(str(point["id"])), html.escape(str(slug))),
                    "          </tr>",
                )
            )
        )
    return "\n".join(rows)


def render_index(card, points, slug):
    """Fill ``assets/gallery.html`` with the card and the points table.

    Textual, token by token: the templates are the interface and stay readable.
    """
    text = GALLERY_TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("{{DIRECTION_NAME}}", html.escape(str(card["direction_name"])))
    text = text.replace("{{FAMILY}}", html.escape(str(card["family"])))
    text = text.replace("{{SEED}}", html.escape(str(card["seed"])))
    text = text.replace("{{POINTS_TABLE_ROWS}}", _points_table_rows(points, slug))
    return text


def canvas_name(point, slug):
    """Relative name of a point's comparison canvas inside ``points/``.

    ``<id>-<slug>.html`` per the spec §4 tree, where ``<slug>`` is the *session*
    slug (the same placeholder the tree uses for ``prototypes/<slug>-<seed>/``).
    """
    return "%s-%s.html" % (point["id"], slug)


def variant_name(point, option):
    """Directory name of one option's mini-project inside ``variants/``."""
    return "%s-%s" % (point["id"], option["key"])


def build(target_dir, slug, card, points):
    """Create ``<target_dir>/<slug>-<seed>/`` and return that directory.

    ``card`` is the CARD SCHEMA dict rolled from the seed; ``points`` is the
    parsed ``points.json``. Every write is **if-absent**: rerunning is a no-op at
    the byte level and never clobbers a captured brief or a started artifact.
    """
    target = Path(target_dir)
    session = target / ("%s-%s" % (slug, card["seed"]))
    points_dir = session / "points"
    variants_dir = session / "variants"
    points_dir.mkdir(parents=True, exist_ok=True)
    variants_dir.mkdir(parents=True, exist_ok=True)

    _write_if_absent(session / "index.html", render_index(card, points, slug))
    _write_if_absent(session / "direction.json", roll.dumps(card) + "\n")
    _write_if_absent(session / "points.json", roll.dumps(points) + "\n")
    _write_if_absent(session / "brief.md", BRIEF_HEADER)

    for point in points.get("points", ()):
        _copy_if_absent(CANVAS_TEMPLATE, points_dir / canvas_name(point, slug))
        for option in point.get("options", ()):
            variant_dir = variants_dir / variant_name(point, option)
            variant_dir.mkdir(parents=True, exist_ok=True)
            _copy_if_absent(VARIANT_TEMPLATE, variant_dir / "index.html")

    return session


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Scaffold a proto-lab session directory from a card and points.json.",
    )
    parser.add_argument("--target", required=True, help="parent directory of the session")
    parser.add_argument("--slug", required=True, help="session slug")
    parser.add_argument("--card", required=True, help="path to the direction card JSON")
    parser.add_argument("--points", required=True, help="path to points.json")
    args = parser.parse_args(argv)

    card = json.loads(Path(args.card).read_text(encoding="utf-8"))
    points = json.loads(Path(args.points).read_text(encoding="utf-8"))
    session = build(Path(args.target), args.slug, card, points)
    print(session)
    return 0


if __name__ == "__main__":
    sys.exit(main())
