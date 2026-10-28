"""Behavioural tests for ``scripts/scaffold.py`` (Task 14).

The scaffolder turns a rolled **direction card** plus ``points.json`` into a
session directory — the spec §4 tree, rooted at ``<target>/<slug>-<seed>/``
(ruling R8: ``target_dir`` is the *parent*). It fills ``index.html`` from the
gallery template, copies the neutral canvas and variant shell into ``points/``
and ``variants/``, and drops the two JSON artefacts in verbatim.

Two properties matter beyond the shape:

- **Determinism / idempotency** — a second run over the same inputs must not
  change a single byte, so the suite compares the ``sha256`` of every file.
- **The R16 canvas contract** — ``{{CANVAS_FRAMES}}`` is an *attribute anchor*
  on the deck container (Task 16 replaces the whole deck block). The scaffolder
  must not blind-substitute it, so ``points/*.html`` is the canvas template
  byte for byte.

Python stdlib only.
"""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import roll  # noqa: E402  (imported after the sys.path tweak above)
import scaffold  # noqa: E402

SCRIPT = ROOT / "scripts" / "scaffold.py"
ASSETS = ROOT / "assets"

SLUG = "task-inbox"
SEED = "cafe-com-leite"

# The exact spec §4 tree, relative to the created session directory. Task 14
# creates the pre-generation subset: the card index, the two JSON artefacts,
# the brief placeholder, one canvas per point and one variant shell per option.
# Post-choice artefacts (tokens.css, styleguide.html, handoff.md, chosen/, …)
# belong to later pipeline steps and are deliberately absent.
EXPECTED_FILES = {
    "index.html",
    "direction.json",
    "brief.md",
    "points.json",
    "points/d1-{slug}.html".format(slug=SLUG),
    "points/d2-{slug}.html".format(slug=SLUG),
    "variants/d1-a/index.html",
    "variants/d1-b/index.html",
    "variants/d1-c/index.html",
    "variants/d2-a/index.html",
    "variants/d2-b/index.html",
}

EXPECTED_DIRECTORIES = {
    "points",
    "variants",
    "variants/d1-a",
    "variants/d1-b",
    "variants/d1-c",
    "variants/d2-a",
    "variants/d2-b",
}


def card_fixture():
    """A real card from the roller (never a hand-written stub)."""
    return roll.roll(SEED)


def points_fixture():
    """Two points: three options on d1, two on d2 (the 3/2 variant caps)."""
    return {
        "slug": SLUG,
        "points": [
            {
                "id": "d1",
                "question": "Where does the primary action live on the list screen?",
                "why": "The brief is action-first; placement decides the whole list layout.",
                "axis": "primary-action-placement",
                "options": [
                    {
                        "key": "a",
                        "label": "Sticky header CTA",
                        "descriptor": "One persistent action pinned in the header.",
                    },
                    {
                        "key": "b",
                        "label": "Inline row action",
                        "descriptor": "Each row carries its own primary action.",
                    },
                    {
                        "key": "c",
                        "label": "Floating primary",
                        "descriptor": "A single floating button over the list.",
                    },
                ],
                "screens": ["index", "detail"],
                "status": "pending",
                "chosen": None,
            },
            {
                "id": "d2",
                "question": "How should the collection be listed?",
                "why": "Rows carry many fields; the listing shape drives scan speed.",
                "axis": "listing-pattern",
                "options": [
                    {
                        "key": "a",
                        "label": "Dense table",
                        "descriptor": "Column-aligned grid optimised for scanning.",
                    },
                    {
                        "key": "b",
                        "label": "Card grid",
                        "descriptor": "Card per item, hierarchical and image-friendly.",
                    },
                ],
                "screens": ["index"],
                "status": "chosen",
                "chosen": "a",
            },
        ],
    }


def relative_files(root):
    """Every file under ``root`` as a ``{relative path: sha256}`` map."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class ScaffoldTest(unittest.TestCase):
    """Shared setup: build one session into a throwaway target directory."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.target = Path(tmp.name)
        self.card = card_fixture()
        self.points = points_fixture()
        self.session = scaffold.build(self.target, SLUG, self.card, self.points)
        self.assertTrue(self.session.is_dir(), "build() must return the created directory")

    def read(self, relative):
        path = self.session / relative
        self.assertTrue(path.is_file(), "missing scaffolder output: %s" % relative)
        return path.read_text(encoding="utf-8")


class BuildTargetTest(ScaffoldTest):
    """R8: ``target_dir`` is the parent; the session goes in ``<slug>-<seed>/``."""

    def test_session_directory_is_slug_dash_seed_under_the_target(self):
        self.assertEqual(self.session, self.target / ("%s-%s" % (SLUG, SEED)))
        self.assertEqual(
            sorted(path.name for path in self.target.iterdir()),
            ["%s-%s" % (SLUG, SEED)],
            "the scaffolder must not write anything beside the session directory",
        )

    def test_missing_target_directories_are_created(self):
        nested = self.target / "deep" / "nested"
        session = scaffold.build(nested, SLUG, self.card, self.points)
        self.assertEqual(session, nested / ("%s-%s" % (SLUG, SEED)))
        self.assertTrue((session / "index.html").is_file())


class ExactTreeTest(ScaffoldTest):
    """(a) The created tree is exactly the spec §4 pre-generation subset."""

    def test_file_set_is_exact(self):
        self.assertEqual(sorted(relative_files(self.session)), sorted(EXPECTED_FILES))

    def test_directory_set_is_exact(self):
        directories = {
            str(path.relative_to(self.session))
            for path in sorted(self.session.rglob("*"))
            if path.is_dir()
        }
        self.assertEqual(sorted(directories), sorted(EXPECTED_DIRECTORIES))


class JsonArtefactTest(ScaffoldTest):
    """(b) ``direction.json`` == card and ``points.json`` == points."""

    def test_direction_json_equals_the_card(self):
        self.assertEqual(json.loads(self.read("direction.json")), self.card)

    def test_points_json_equals_points(self):
        self.assertEqual(json.loads(self.read("points.json")), self.points)

    def test_direction_json_is_the_canonical_roller_encoding(self):
        # Byte-parity with ``roll.py``'s canonical JSON (sorted keys, compact),
        # so a committed card can never be re-serialised differently.
        self.assertEqual(self.read("direction.json"), roll.dumps(self.card) + "\n")

    def test_points_json_is_deterministic_json(self):
        self.assertEqual(
            self.read("points.json"),
            json.dumps(self.points, sort_keys=True, separators=(",", ":")) + "\n",
        )


class IndexRenderTest(ScaffoldTest):
    """(c) ``{{SEED}}`` / ``{{DIRECTION_NAME}}`` are substituted in the index."""

    def test_seed_and_direction_name_are_substituted(self):
        index = self.read("index.html")
        self.assertNotIn("{{SEED}}", index)
        self.assertNotIn("{{DIRECTION_NAME}}", index)
        self.assertIn(self.card["seed"], index)
        self.assertIn(self.card["direction_name"], index)

    def test_family_and_points_rows_are_substituted(self):
        index = self.read("index.html")
        self.assertNotIn("{{FAMILY}}", index)
        self.assertNotIn("{{POINTS_TABLE_ROWS}}", index)
        self.assertIn(self.card["family"], index)

    def test_index_no_longer_carries_any_template_placeholder(self):
        index = self.read("index.html")
        for placeholder in ("{{SEED}}", "{{DIRECTION_NAME}}", "{{FAMILY}}", "{{POINTS_TABLE_ROWS}}"):
            self.assertNotIn(placeholder, index)

    def test_index_lists_every_point_with_axis_options_status_and_canvas_link(self):
        index = self.read("index.html")
        for point in self.points["points"]:
            self.assertIn(point["id"], index)
            self.assertIn(point["axis"], index)
            self.assertIn(point["question"], index)
            for option in point["options"]:
                self.assertIn(option["label"], index)
            self.assertIn(point["status"], index)
            self.assertIn(
                'href="points/%s-%s.html"' % (point["id"], SLUG),
                index,
                "the row must link its comparison canvas",
            )

    def test_index_is_the_gallery_template_with_no_scripting_added(self):
        index = self.read("index.html")
        self.assertIn("<!DOCTYPE html>", index)
        self.assertNotIn("<script", index, "the gallery is display-only")

    def test_fresh_session_gets_the_brief_header(self):
        self.assertEqual(self.read("brief.md"), "# Brief\n")

    def test_pre_existing_brief_survives_a_scaffold_run(self):
        # Step 1 captures the brief; step 3 runs the scaffolder. The scaffold
        # must not destroy what step 1 wrote (the pre-fix behaviour).
        brief = self.session / "brief.md"
        captured = "# Brief\n\n" + ("captured context\n" * 130)
        self.assertGreaterEqual(len(captured.encode("utf-8")), 2048)
        brief.write_text(captured, encoding="utf-8")
        scaffold.build(self.target, SLUG, self.card, self.points)
        self.assertEqual(brief.read_text(encoding="utf-8"), captured)


class CanvasCopyTest(ScaffoldTest):
    """(e) one canvas per point; R16: the canvas is copied, never substituted."""

    def test_one_canvas_per_point(self):
        for point in self.points["points"]:
            canvas = self.session / "points" / ("%s-%s.html" % (point["id"], SLUG))
            self.assertTrue(canvas.is_file(), "missing canvas for %s" % point["id"])

    def test_canvas_is_byte_identical_to_the_template(self):
        template = (ASSETS / "canvas.html").read_bytes()
        for point in self.points["points"]:
            canvas = self.session / "points" / ("%s-%s.html" % (point["id"], SLUG))
            self.assertEqual(
                canvas.read_bytes(),
                template,
                "the canvas must be copied unchanged: {{CANVAS_FRAMES}} is the "
                "deck anchor Task 16 replaces wholesale, never a text token",
            )

    def test_canvas_frames_anchor_survives_the_copy(self):
        canvas = self.read("points/d1-%s.html" % SLUG)
        self.assertIn('data-canvas-frames="{{CANVAS_FRAMES}}"', canvas)


class VariantShellTest(ScaffoldTest):
    """(e) one variant directory per option, seeded with the shell."""

    def test_one_directory_per_option(self):
        for point in self.points["points"]:
            for option in point["options"]:
                variant = self.session / "variants" / ("%s-%s" % (point["id"], option["key"]))
                self.assertTrue(
                    variant.is_dir(),
                    "missing variant directory %s-%s" % (point["id"], option["key"]),
                )

    def test_variant_entry_point_is_the_shell_unchanged(self):
        template = (ASSETS / "variant-shell.html").read_bytes()
        for point in self.points["points"]:
            for option in point["options"]:
                start = self.session / "variants" / ("%s-%s" % (point["id"], option["key"])) / "index.html"
                self.assertEqual(
                    start.read_bytes(),
                    template,
                    "the generator fills {{VARIANT_LABEL}} and the screens marker",
                )


class IdempotencyTest(ScaffoldTest):
    """(d) a second run changes no byte."""

    def test_second_run_is_byte_identical(self):
        before = relative_files(self.session)
        scaffold.build(self.target, SLUG, self.card, self.points)
        after = relative_files(self.session)
        self.assertEqual(before, after, "a second run must not change any file")
        self.assertEqual(sorted(after), sorted(EXPECTED_FILES))

    def test_second_run_keeps_unrelated_files_untouched(self):
        # The pipelines that follow the scaffolder (generator, judge) add and
        # edit files; a rerun must never prune them.
        marker = self.session / "judge-report.md"
        marker.write_text("PASS\n", encoding="utf-8")
        scaffold.build(self.target, SLUG, self.card, self.points)
        self.assertEqual(marker.read_text(encoding="utf-8"), "PASS\n")

    def test_rerun_never_clobbers_a_started_artifact(self):
        # A rerun with the same card must leave files the executor started to
        # fill alone too, not only files added by later pipeline steps.
        started = {
            "index.html": "<!DOCTYPE html><html><body>started gallery</body></html>\n",
            "direction.json": '{"started": true}\n',
            "points.json": '{"started": true}\n',
            "points/d1-%s.html" % SLUG: "<!DOCTYPE html><html><body>started canvas</body></html>\n",
            "variants/d1-a/index.html": "<!DOCTYPE html><html><body>started variant</body></html>\n",
        }
        for relative, text in started.items():
            (self.session / relative).write_text(text, encoding="utf-8")
        scaffold.build(self.target, SLUG, self.card, self.points)
        for relative, text in started.items():
            self.assertEqual(
                (self.session / relative).read_text(encoding="utf-8"),
                text,
                "a rerun must never overwrite %s" % relative,
            )

    def test_same_inputs_in_two_targets_yield_identical_bytes(self):
        other_tmp = tempfile.TemporaryDirectory()
        self.addCleanup(other_tmp.cleanup)
        other = scaffold.build(Path(other_tmp.name), SLUG, self.card, self.points)
        self.assertEqual(relative_files(self.session), relative_files(other))


class CliTest(unittest.TestCase):
    """The CLI: ``--target DIR --slug S --card card.json --points points.json``."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.target = Path(tmp.name)
        self.work = Path(tmp.name) / "in"
        self.work.mkdir()
        self.card_path = self.work / "card.json"
        self.points_path = self.work / "points.json"
        self.card_path.write_text(roll.dumps(card_fixture()) + "\n", encoding="utf-8")
        self.points_path.write_text(
            json.dumps(points_fixture()) + "\n", encoding="utf-8"
        )

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
        )

    def test_cli_scaffolds_the_same_tree_as_the_library(self):
        result = self.run_cli(
            "--target",
            str(self.target),
            "--slug",
            SLUG,
            "--card",
            str(self.card_path),
            "--points",
            str(self.points_path),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        session = self.target / ("%s-%s" % (SLUG, SEED))
        self.assertTrue(session.is_dir())
        self.assertEqual(sorted(relative_files(session)), sorted(EXPECTED_FILES))
        self.assertIn(str(session), result.stdout)

    def test_cli_requires_every_argument(self):
        result = self.run_cli("--target", str(self.target))
        self.assertEqual(result.returncode, 2)
        self.assertIn("--slug", result.stderr)


if __name__ == "__main__":
    unittest.main()
