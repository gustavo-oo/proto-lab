"""Behavioural tests for ``scripts/check_copy.py``.

The checker implements the deterministic half of ``references/copy-contract.md``:
C01 (item-count labels) and C04 (separator glyphs). C02 and C03 are judge-only.
The gate is zero-tolerance, so any finding fails the page.

Fixtures live under ``tests/fixtures/copy/``:

- ``clean.html``          - product copy with commas, data values and chrome -> 0 findings.
- ``item_counts.html``    - four C01 labels -> 4 findings.
- ``separator_soup.html`` - six C04 lines -> 6 findings.
- ``false_positives.html`` - dates, ratios, ranges, units, data fields and chrome -> 0 findings.

Python stdlib only.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_copy  # noqa: E402  (imported after the sys.path tweak above)

FIXTURES = ROOT / "tests" / "fixtures" / "copy"
SCRIPT = ROOT / "scripts" / "check_copy.py"

FINDING_KEYS = {"rule", "confidence", "evidence", "tag", "class"}


def _run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


class RuleTableTest(unittest.TestCase):
    def test_rules_are_c01_and_c04(self):
        self.assertEqual(check_copy.RULES, ("C01", "C04"))

    def test_c02_and_c03_are_judge_only(self):
        self.assertNotIn("C02", check_copy.RULES)
        self.assertNotIn("C03", check_copy.RULES)


class CleanTest(unittest.TestCase):
    def test_clean_page_passes(self):
        result = check_copy.check_paths([FIXTURES / "clean.html"])
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["verdict"], "pass")


class ItemCountTest(unittest.TestCase):
    def test_item_counts_flags_c01(self):
        result = check_copy.check_paths([FIXTURES / "item_counts.html"])
        self.assertEqual(result["count"], 4, result["findings"])
        self.assertEqual({hit["rule"] for hit in result["findings"]}, {"C01"})
        self.assertEqual(
            {hit["evidence"] for hit in result["findings"]},
            {"10 registros", "6 filmes", "4 cinemas", "4 results"},
        )
        self.assertTrue(
            all(hit["confidence"] == "heuristic" for hit in result["findings"])
        )
        self.assertEqual(result["verdict"], "fail")

    def test_selection_units_and_data_fields_are_exempt(self):
        html = (
            '<p class="meta">3 de 5 selecionados</p>'
            '<p class="meta">250 ml, 12/10, 1:16,7</p>'
            "<dl><dt>2 quartos</dt><dd>10 registros</dd></dl>"
            '<header data-session-chrome>10 registros · 6 filmes</header>'
        )
        self.assertEqual(check_copy.check_html(html), [])


class SeparatorTest(unittest.TestCase):
    def test_separator_soup_flags_c04(self):
        result = check_copy.check_paths([FIXTURES / "separator_soup.html"])
        self.assertEqual(result["count"], 6, result["findings"])
        self.assertEqual({hit["rule"] for hit in result["findings"]}, {"C04"})
        self.assertEqual(
            {hit["evidence"] for hit in result["findings"]},
            {
                "Quênia · Nyeri AA",
                "grão: SL28 · torra clara",
                "V60 | 1:16,7",
                "origem • método • nota",
                "d1-a — Tabela densa",
                "a – b",
            },
        )
        self.assertEqual(result["verdict"], "fail")

    def test_every_banned_glyph_is_flagged(self):
        cases = (
            ("<h1>a · b</h1>", "solid"),
            ("<h1>a | b</h1>", "solid"),
            ("<h1>a • b</h1>", "solid"),
            ("<h1>a — b</h1>", "heuristic"),
            ("<h1>a – b</h1>", "heuristic"),
        )
        for html, confidence in cases:
            findings = check_copy.check_html(html)
            self.assertEqual(len(findings), 1, html)
            self.assertEqual(findings[0]["rule"], "C04", html)
            self.assertEqual(findings[0]["confidence"], confidence, html)

    def test_value_punctuation_is_not_a_separator(self):
        html = (
            '<p class="meta">0–5, 12/10 → 16/10, média-fina, '
            "meio-tom, Blueprint / Schematic</p>"
        )
        self.assertEqual(check_copy.check_html(html), [])

    def test_title_and_style_are_ignored(self):
        html = (
            "<title>10 registros · 6 filmes</title>"
            "<style>/* 10 registros · 6 filmes */</style>"
            "<h1>Diário</h1>"
        )
        self.assertEqual(check_copy.check_html(html), [])


class FalsePositiveTest(unittest.TestCase):
    def test_false_positive_fixture_is_clean(self):
        result = check_copy.check_paths([FIXTURES / "false_positives.html"])
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["verdict"], "pass")


class FindingShapeTest(unittest.TestCase):
    def test_every_finding_has_the_documented_shape(self):
        for name in ("item_counts.html", "separator_soup.html"):
            result = check_copy.check_paths([FIXTURES / name])
            for hit in result["findings"]:
                self.assertEqual(set(hit), FINDING_KEYS)
                self.assertIn(hit["rule"], check_copy.RULES)
                self.assertIn(hit["confidence"], ("solid", "heuristic"))
                self.assertTrue(hit["evidence"].strip())


class CliTest(unittest.TestCase):
    def test_cli_prints_json_and_exit_codes(self):
        clean = _run_cli(str(FIXTURES / "clean.html"))
        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.assertEqual(json.loads(clean.stdout)["verdict"], "pass")

        bad = _run_cli(str(FIXTURES / "item_counts.html"))
        self.assertEqual(bad.returncode, 1, bad.stderr)
        data = json.loads(bad.stdout)
        self.assertEqual(data["count"], 4)
        self.assertEqual(data["verdict"], "fail")

    def test_cli_keeps_utf8_evidence(self):
        proc = _run_cli(str(FIXTURES / "separator_soup.html"))
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("·", proc.stdout)
        self.assertIn("—", proc.stdout)
        data = json.loads(proc.stdout)
        self.assertEqual(data["count"], 6)


class MultiPathTest(unittest.TestCase):
    def test_a_multi_path_call_sums_the_findings(self):
        result = check_copy.check_paths(
            [FIXTURES / "clean.html", FIXTURES / "item_counts.html"]
        )
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
