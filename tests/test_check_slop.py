"""Behavioural tests for ``scripts/check_slop.py`` (Task 09).

The scanner ports the mechanical rules ``R01``-``R22`` of
``references/slop-fingerprints.md`` into a deterministic HTML/copy scan. This
suite pins the public interface and, above all, the exact boundary of the
verdict: **3 hits pass, 4 hits fail**.

Fixtures live under ``tests/fixtures/slop/``:

- ``good_clean.html``   - no fingerprint at all -> 0 hits, ``pass``.
- ``slop_full.html``    - a cluster (F01 + F02 + F07 + F11) -> ``fail``.
- ``boundary_three.html`` - exactly 3 fingerprints (F02, F05, F09) -> ``pass``.
- ``boundary_four.html``  - the same page plus a 4th fingerprint -> ``fail``.

Python stdlib only.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_slop  # noqa: E402  (imported after the sys.path tweak above)

FIXTURES = ROOT / "tests" / "fixtures" / "slop"
SCRIPT = ROOT / "scripts" / "check_slop.py"

# The rule table: ``(rule_id, fingerprint)`` pairs, in order. R01-R15 map onto
# F01-F15 one-to-one; the remaining rules skip the four judge-only fingerprints.
EXPECTED_RULE_PAIRS = [
    ("R01", "F01"), ("R02", "F02"), ("R03", "F03"), ("R04", "F04"),
    ("R05", "F05"), ("R06", "F06"), ("R07", "F07"), ("R08", "F08"),
    ("R09", "F09"), ("R10", "F10"), ("R11", "F11"), ("R12", "F12"),
    ("R13", "F13"), ("R14", "F14"), ("R15", "F15"),
    ("R16", "F17"), ("R17", "F19"), ("R18", "F20"),
    ("R19", "F23"), ("R20", "F24"), ("R21", "F25"), ("R22", "F26"),
]

FINDING_KEYS = {"fingerprint", "rule", "confidence", "evidence"}


def _run_cli(*args):
    """Run the scanner CLI in a subprocess, returning the completed process."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


def _fps(findings):
    return {hit["fingerprint"] for hit in findings}


def _fingerprints(result):
    return _fps(result["hits"])


class RuleTableTest(unittest.TestCase):
    def test_rules_is_a_list_of_22_four_tuples(self):
        self.assertEqual(len(check_slop.RULES), 22)
        for entry in check_slop.RULES:
            self.assertEqual(len(entry), 4)
            rule_id, fingerprint, confidence, matcher = entry
            self.assertRegex(rule_id, r"^R\d{2}$")
            self.assertRegex(fingerprint, r"^F\d{2}$")
            self.assertIn(confidence, ("solid", "heuristic"))
            self.assertTrue(callable(matcher))

    def test_rule_and_fingerprint_pairs_match_the_spec(self):
        pairs = [(entry[0], entry[1]) for entry in check_slop.RULES]
        self.assertEqual(pairs, EXPECTED_RULE_PAIRS)

    def test_threshold_is_four(self):
        self.assertEqual(check_slop.THRESHOLD, 4)


class GoodCleanTest(unittest.TestCase):
    """(a) A page with no fingerprint passes with zero hits."""

    def test_good_clean_has_no_hits_and_passes(self):
        result = check_slop.check_paths([FIXTURES / "good_clean.html"])
        self.assertEqual(result["hits"], [])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["verdict"], "pass")


class SlopFullTest(unittest.TestCase):
    """(b) A cluster of slop fails the scan."""

    def test_slop_full_fails_with_a_cluster(self):
        result = check_slop.check_paths([FIXTURES / "slop_full.html"])
        self.assertGreaterEqual(result["count"], 4)
        self.assertEqual(result["verdict"], "fail")
        self.assertTrue(
            {"F01", "F02", "F07", "F11"} <= _fingerprints(result),
            "expected F01/F02/F07/F11, got %s" % sorted(_fingerprints(result)),
        )

    def test_every_finding_has_the_documented_shape(self):
        result = check_slop.check_paths([FIXTURES / "slop_full.html"])
        for hit in result["hits"]:
            self.assertEqual(set(hit), FINDING_KEYS)
            self.assertIn(hit["confidence"], ("solid", "heuristic"))
            self.assertTrue(hit["evidence"].strip())


class BoundaryTest(unittest.TestCase):
    """(c) The verdict boundary is exact: 3 passes, 4 fails."""

    def test_boundary_three_is_exactly_three(self):
        result = check_slop.check_paths([FIXTURES / "boundary_three.html"])
        self.assertEqual(
            result["count"], 3, "unexpected hits: %s" % result["hits"]
        )
        self.assertEqual(_fingerprints(result), {"F02", "F05", "F09"})
        self.assertEqual(result["verdict"], "pass")

    def test_boundary_three_cli_exit_zero(self):
        proc = _run_cli(str(FIXTURES / "boundary_three.html"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["count"], 3)

    def test_boundary_four_fingerprints_are_pinned(self):
        result = check_slop.check_paths([FIXTURES / "boundary_four.html"])
        self.assertEqual(result["count"], 4, result["hits"])
        self.assertEqual(_fingerprints(result), {"F02", "F05", "F09", "F15"})
        self.assertEqual(result["verdict"], "fail")

    def test_boundary_four_cli_exit_one(self):
        proc = _run_cli(str(FIXTURES / "boundary_four.html"))
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertEqual(_fingerprints(json.loads(proc.stdout)), {"F02", "F05", "F09", "F15"})


class FalsePositiveTest(unittest.TestCase):
    """Precision guards at the gate: only real fingerprints count.

    F15 is ``solid`` (counts unconditionally), and F09 is ``solid`` too, so a
    spurious match on a legitimate page can flip a 3-hit page to ``fail``.
    These tests forbid matching a property that merely *ends* in ``color`` and
    forbid treating a decorative arrow as an emoji.
    """

    def test_border_color_grey_does_not_fire_f15(self):
        html = '<style>.card { border-color: #6b7280; }</style><h1>Report</h1>'
        self.assertNotIn("F15", _fps(check_slop.check_html(html)))

    def test_background_color_grey_does_not_fire_f15(self):
        html = "<style>.card { background-color: #94a3b8; }</style>"
        self.assertNotIn("F15", _fps(check_slop.check_html(html)))

    def test_grey_text_color_still_fires_f15(self):
        html = "<style>p { color: #9ca3af; }</style>"
        self.assertIn("F15", _fps(check_slop.check_html(html)))

    def test_grey_border_only_fixture_is_clean(self):
        result = check_slop.check_paths([FIXTURES / "grey_border_only.html"])
        self.assertEqual(result["count"], 0, result["hits"])
        self.assertEqual(result["verdict"], "pass")

    def test_arrow_in_heading_does_not_fire_f09(self):
        html = "<h1>Next → step</h1>"
        self.assertNotIn("F09", _fps(check_slop.check_html(html)))

    def test_emoji_in_heading_still_fires_f09(self):
        html = "<h1>Launch 🚀</h1>"
        self.assertIn("F09", _fps(check_slop.check_html(html)))


class AllowFontTest(unittest.TestCase):
    """(d) ``--allow-font`` removes a named family from the F01 tell set."""

    def test_f01_fires_by_default(self):
        result = check_slop.check_paths([FIXTURES / "slop_full.html"])
        self.assertIn("F01", _fingerprints(result))

    def test_allow_font_inter_suppresses_f01_but_keeps_f02(self):
        result = check_slop.check_paths(
            [FIXTURES / "slop_full.html"], allow_fonts=["Inter"]
        )
        self.assertNotIn("F01", _fingerprints(result))
        self.assertIn("F02", _fingerprints(result))

    def test_allow_font_inter_via_cli(self):
        proc = _run_cli(
            "--allow-font", "Inter", str(FIXTURES / "slop_full.html")
        )
        fingerprints = _fingerprints(json.loads(proc.stdout))
        self.assertNotIn("F01", fingerprints)
        self.assertIn("F02", fingerprints)


class CliJsonTest(unittest.TestCase):
    """(e) The CLI prints valid JSON on stdout."""

    def test_cli_prints_valid_json(self):
        proc = _run_cli(str(FIXTURES / "good_clean.html"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIn("hits", data)
        self.assertIn("count", data)
        self.assertIn("verdict", data)
        self.assertEqual(data["verdict"], "pass")


if __name__ == "__main__":
    unittest.main()
