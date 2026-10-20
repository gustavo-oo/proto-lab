"""Behavioural tests for the benchmark harness (Task 24).

Two deliverables are pinned here:

* ``benchmarks/compare.py`` -- the version-to-version comparator. The fixtures
  under ``tests/fixtures/bench/`` are fabricated result snapshots:

  - ``vA`` (skill 0.1.0) and ``vB`` (skill 0.1.1) differ in exactly one
    improved metric (``s01 gate_checklist_pass`` 0.833 -> 1.000) and exactly
    one worsened metric (``s02 slop_hits`` 1 -> 4). Everything else is equal
    or better, so the ``⚠`` marks must single out the regression;
  - ``vA-suite-v2`` is ``vA`` recorded under a different ``suite_version``
    (``v2``) -> the comparison is refused with exit 2;
  - ``vC-env`` is ``vB`` recorded on a different model/harness (and with
    ``s04 file_nav_ok`` dropped) -> the "não apples-to-apples" warning plus
    the not-comparable row.

* ``benchmarks/suite/`` -- the frozen suite (``suite.json`` + ``rubric.md`` +
  the five scenario prompts) every future version is measured against. The
  metric registry in ``compare.py`` must stay identical to the one in
  ``suite.json`` (drift guard).

Python stdlib only.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPARE = ROOT / "benchmarks" / "compare.py"
SUITE_DIR = ROOT / "benchmarks" / "suite"
SUITE_JSON = SUITE_DIR / "suite.json"
RUBRIC = SUITE_DIR / "rubric.md"
FIXTURES = ROOT / "tests" / "fixtures" / "bench"

sys.path.insert(0, str(ROOT / "benchmarks"))

import compare  # noqa: E402  (imported after the sys.path tweak above)

# The ten metrics the suite freezes. Names are part of the interface every
# future version is compared through.
METRIC_IDS = [
    "gate_checklist_pass",
    "structural_divergence",
    "slop_hits",
    "judge_axes_pass",
    "fix_rounds",
    "artifacts_complete",
    "research_sources",
    "file_nav_ok",
    "html_bytes_total",
    "distinct_directions",
]

# Fixed seeds: the comparability rule ("seeds are fixed in the suite;
# random-seed exploration belongs to the reviews").
EXPECTED_SEEDS = {
    "s01": ["s01-anchor"],
    "s02": ["s02-anchor"],
    "s03": ["s03-anchor"],
    "s04": ["s04-a", "s04-b", "s04-c"],
    "s05": ["s05-anchor"],
}

REQUIRED_SCENARIO_FIELDS = (
    "id",
    "prompt_file",
    "seeds",
    "config",
    "expected_artifacts",
    "check_focus",
)

# A rendered table row: scenario, metric, A, B, delta, free-form flag.
ROW_RE = re.compile(r"^(s\d{2})\s+([a-z_]+)\s+(\S+)\s+(\S+)\s+(\S+)(.*)$")


def run_compare(results_a, results_b, *extra):
    """Run the comparator CLI in a subprocess, returning the completed process."""
    return subprocess.run(
        [sys.executable, str(COMPARE), str(results_a), str(results_b), *extra],
        capture_output=True,
        text=True,
    )


def parse_rows(output):
    """Parse the delta table into ``{(scenario, metric): row}``."""
    rows = {}
    for line in output.splitlines():
        match = ROW_RE.match(line)
        if match:
            rows[(match.group(1), match.group(2))] = {
                "a": match.group(3),
                "b": match.group(4),
                "delta": match.group(5),
                "flag": match.group(6).strip(),
            }
    return rows


class CompareDeltaTest(unittest.TestCase):
    """(a) correct deltas and (b) a ⚠ on the worsened metric only."""

    @classmethod
    def setUpClass(cls):
        cls.proc = run_compare(FIXTURES / "vA", FIXTURES / "vB")
        cls.output = cls.proc.stdout + cls.proc.stderr
        cls.rows = parse_rows(cls.output)

    def test_table_covers_both_snapshots(self):
        self.assertEqual(self.proc.returncode, 0, self.output)
        self.assertIn(("s01", "gate_checklist_pass"), self.rows)
        self.assertIn(("s05", "html_bytes_total"), self.rows)
        # distinct_directions is an s04-only metric: no row elsewhere.
        self.assertNotIn(("s01", "distinct_directions"), self.rows)

    def test_improved_metric_has_the_correct_numeric_delta(self):
        row = self.rows[("s01", "gate_checklist_pass")]
        self.assertEqual(row["a"], "0.833")
        self.assertEqual(row["b"], "1.000")
        self.assertEqual(row["delta"], "+0.167")
        self.assertNotIn("⚠", row["flag"])

    def test_worsened_metric_has_the_correct_numeric_delta(self):
        row = self.rows[("s02", "slop_hits")]
        self.assertEqual(row["a"], "1")
        self.assertEqual(row["b"], "4")
        self.assertEqual(row["delta"], "+3")
        self.assertIn("⚠", row["flag"])

    def test_lower_is_better_improvements_are_not_regressions(self):
        # slop_hits is lower-is-better: 2 -> 1 must read as an improvement.
        row = self.rows[("s01", "slop_hits")]
        self.assertEqual(row["delta"], "-1")
        self.assertNotIn("⚠", row["flag"])
        # html_bytes_total is the cost proxy: shrinking is an improvement.
        row = self.rows[("s05", "html_bytes_total")]
        self.assertEqual(row["a"], "96,400")
        self.assertEqual(row["b"], "95,400")
        self.assertEqual(row["delta"], "-1,000")
        self.assertNotIn("⚠", row["flag"])
        # fix_rounds is lower-is-better too.
        row = self.rows[("s02", "fix_rounds")]
        self.assertEqual(row["delta"], "-1")
        self.assertNotIn("⚠", row["flag"])

    def test_warning_appears_only_on_the_worsened_metric(self):
        flagged = sorted(
            key for key, row in self.rows.items() if "⚠" in row["flag"]
        )
        self.assertEqual(flagged, [("s02", "slop_hits")])

    def test_regressions_are_summarised(self):
        self.assertIn("s02 slop_hits", self.output)
        self.assertIn("regression", self.output)

    def test_default_exit_is_zero_even_with_a_regression(self):
        # The ⚠ is the signal (plan ritual); a CI gate opts in explicitly.
        self.assertEqual(self.proc.returncode, 0)

    def test_strict_flag_exits_one_on_regression(self):
        proc = run_compare(FIXTURES / "vA", FIXTURES / "vB", "--strict")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)


class SuiteMismatchTest(unittest.TestCase):
    """(c) different suites -> warning + exit 2."""

    def test_suite_version_mismatch_warns_and_exits_2(self):
        proc = run_compare(FIXTURES / "vA", FIXTURES / "vA-suite-v2")
        output = proc.stdout + proc.stderr
        self.assertEqual(proc.returncode, 2, output)
        self.assertIn("suite_version mismatch", output)
        self.assertIn("v1", output)
        self.assertIn("v2", output)
        # No comparison is attempted when the suites differ.
        self.assertEqual(parse_rows(output), {})


class EnvDiffTest(unittest.TestCase):
    """(d) env.json diff (model/harness) flagged "não apples-to-apples"."""

    def test_model_and_harness_diff_is_flagged(self):
        proc = run_compare(FIXTURES / "vA", FIXTURES / "vC-env")
        output = proc.stdout + proc.stderr
        self.assertIn("não apples-to-apples", output)
        self.assertIn("harness-model-A", output)
        self.assertIn("harness-model-B", output)
        self.assertIn("opencode/cli", output)
        self.assertIn("opencode/desktop", output)
        self.assertIn("model", output)
        self.assertIn("harness", output)

    def test_identical_env_is_declared_apples_to_apples(self):
        proc = run_compare(FIXTURES / "vA", FIXTURES / "vB")
        output = proc.stdout + proc.stderr
        self.assertNotIn("não apples-to-apples", output)
        self.assertIn("apples-to-apples", output)

    def test_metric_present_in_only_one_snapshot_is_not_comparable(self):
        proc = run_compare(FIXTURES / "vA", FIXTURES / "vC-env")
        rows = parse_rows(proc.stdout + proc.stderr)
        row = rows[("s04", "file_nav_ok")]
        self.assertEqual(row["a"], "true")
        self.assertEqual(row["b"], "—")
        self.assertEqual(row["delta"], "n/a")
        self.assertNotIn("⚠", row["flag"])
        self.assertEqual(proc.returncode, 0)


class CompareUsageTest(unittest.TestCase):
    def test_missing_snapshot_is_an_error(self):
        proc = run_compare(FIXTURES / "does-not-exist", FIXTURES / "vB")
        output = proc.stdout + proc.stderr
        self.assertEqual(proc.returncode, 2, output)
        self.assertIn("does-not-exist", output)

    def test_json_report_is_machine_readable(self):
        proc = run_compare(FIXTURES / "vA", FIXTURES / "vB", "--json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["apples_to_apples"])
        self.assertEqual(payload["a"]["suite_version"], "v1")
        regressions = [
            (row["scenario"], row["metric"])
            for row in payload["rows"]
            if row["verdict"] == "regression"
        ]
        self.assertEqual(regressions, [("s02", "slop_hits")])

    def test_snapshot_without_env_json_reports_unknown_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "vA-no-env"
            shutil.copytree(FIXTURES / "vA", copied)
            (copied / "env.json").unlink()
            proc = run_compare(copied, FIXTURES / "vB")
            output = proc.stdout + proc.stderr
            self.assertEqual(proc.returncode, 0, output)
            self.assertIn("provenance unknown", output)
            self.assertNotIn("não apples-to-apples", output)
            # suite_version still resolves from summary.json.
            rows = parse_rows(output)
            self.assertEqual(rows[("s01", "gate_checklist_pass")]["delta"], "+0.167")


class SuiteDefinitionTest(unittest.TestCase):
    """(e) suite.json parses; the 5 scenario files exist with fixed seeds."""

    @classmethod
    def setUpClass(cls):
        cls.suite = json.loads(SUITE_JSON.read_text(encoding="utf-8"))
        cls.scenarios = cls.suite["scenarios"]

    def test_suite_json_parses_with_version_and_metrics(self):
        self.assertEqual(self.suite["suite_version"], "v1")
        metrics = [entry["id"] for entry in self.suite["metrics"]]
        self.assertEqual(metrics, METRIC_IDS)

    def test_the_five_scenarios_have_the_required_fields(self):
        self.assertEqual(
            [scenario["id"] for scenario in self.scenarios],
            ["s01", "s02", "s03", "s04", "s05"],
        )
        for scenario in self.scenarios:
            for field in REQUIRED_SCENARIO_FIELDS:
                self.assertIn(field, scenario, scenario["id"])
            self.assertTrue(scenario["prompt_file"].endswith(".md"))
            self.assertTrue(scenario["expected_artifacts"], scenario["id"])
            self.assertTrue(scenario["check_focus"], scenario["id"])

    def test_seeds_are_fixed_and_exact(self):
        for scenario in self.scenarios:
            self.assertEqual(
                scenario["seeds"], EXPECTED_SEEDS[scenario["id"]], scenario["id"]
            )

    def test_scenario_prompt_files_exist_and_quote_their_seeds(self):
        for scenario in self.scenarios:
            prompt_file = SUITE_DIR / scenario["prompt_file"]
            self.assertTrue(prompt_file.is_file(), str(prompt_file))
            text = prompt_file.read_text(encoding="utf-8")
            self.assertGreater(len(text), 200, str(prompt_file))
            for seed in scenario["seeds"]:
                self.assertIn(seed, text, str(prompt_file))

    def test_config_respects_the_pipeline_caps(self):
        for scenario in self.scenarios:
            config = scenario["config"]
            self.assertEqual(set(config), {"points", "variants", "research"})
            self.assertTrue(1 <= config["points"] <= 4, scenario["id"])
            self.assertIn(config["variants"], (2, 3), scenario["id"])
            self.assertIsInstance(config["research"], bool, scenario["id"])

    def test_check_focus_is_a_subset_of_the_frozen_metrics(self):
        for scenario in self.scenarios:
            for metric in scenario["check_focus"]:
                self.assertIn(metric, METRIC_IDS, scenario["id"])

    def test_metric_registry_matches_compare_py(self):
        suite_metrics = {
            entry["id"]: (entry["type"], entry["direction"])
            for entry in self.suite["metrics"]
        }
        code_metrics = {
            name: (spec["type"], spec["direction"])
            for name, spec in compare.METRICS.items()
        }
        self.assertEqual(suite_metrics, code_metrics)

    def test_rubric_defines_every_metric(self):
        rubric = RUBRIC.read_text(encoding="utf-8")
        for metric in METRIC_IDS:
            # (?m) because assertRegex does not take the MULTILINE flag.
            pattern = r"(?m)^#{2,3} `%s`[ \t]*$" % re.escape(metric)
            self.assertRegex(rubric, pattern, metric)

    def test_rubric_carries_the_twelve_gate_items(self):
        rubric = RUBRIC.read_text(encoding="utf-8")
        items = re.findall(r"^\| \(([a-l])\) \|", rubric, re.MULTILINE)
        self.assertEqual(
            items, [chr(ord("a") + i) for i in range(12)], rubric[:200]
        )


if __name__ == "__main__":
    unittest.main()
