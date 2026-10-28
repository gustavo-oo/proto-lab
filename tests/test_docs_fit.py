"""Documentation checks for ``references/fit-mode.md``.

Fit mode is the opt-in second direction source: the existing visual system is
captured into ``style-snapshot.json`` and used instead of a catalogue draw.
This reference is the contract behind that path, so the test pins:

* the section layout (modes, evidence levels, capture, gate, schema, fit card,
  generation, judge, handoff, degradation, red flags);
* the snapshot schema example and its exactly-thirteen top-level keys;
* the three evidence levels and the capture caps;
* the ten FIT-card keys;
* the scripts the reference binds to (they must exist on disk).
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = REPO_ROOT / "references" / "fit-mode.md"

REQUIRED_SECTIONS = (
    "## The two modes",
    "## When to use",
    "## When not to use",
    "## Pipeline step 1 — declare the source",
    "## Pipeline step 2 — capture, not roll",
    "## Pipeline step 3 — the single gate",
    "## Evidence levels",
    "## Source scope and caps",
    "## Snapshot schema",
    "## Extraction protocol",
    "## Fit card",
    "## Generation rules",
    "## Judge rules",
    "## Handoff rules",
    "## Degradation",
    "## Red flags",
)

REQUIRED_LITERALS = (
    "style-snapshot:v1",
    "observed",
    "declared",
    "inferred",
    "snapshot:v1",
    "direction_id",
    "FIT",
    "inherited_slop",
    "origin: reused",
    "approved_at_gate",
    "scripts/snapshot.py",
    "scripts/check_slop.py",
    "≤ 8",
    "≤ 12",
    "≤ 5",
)

SNAPSHOT_KEYS = {
    "schema",
    "evidence",
    "source",
    "tokens",
    "type",
    "components",
    "layout",
    "voice",
    "constraints",
    "extensions",
    "inherited_slop",
    "gaps",
    "hash",
}

FIT_CARD_KEYS = (
    "mode",
    "seed",
    "algorithm",
    "direction_id",
    "direction_name",
    "family",
    "knobs",
    "filters",
    "wild",
    "snapshot",
)

CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*[ \t]*\r?\n(.*?)```", re.DOTALL)


class FitModeDocTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            "missing fit-mode reference: %s" % DOC_PATH,
        )
        self.text = DOC_PATH.read_text(encoding="utf-8")

    def test_required_sections_are_present(self):
        missing = [section for section in REQUIRED_SECTIONS if section not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing fit-mode sections: %s" % ", ".join(missing),
        )

    def test_required_literals_are_present(self):
        missing = [literal for literal in REQUIRED_LITERALS if literal not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing fit-mode literals: %s" % ", ".join(missing),
        )

    def test_snapshot_schema_example_parses_and_has_the_expected_keys(self):
        examples = []
        for block in CODE_BLOCK_RE.findall(self.text):
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict) and data.get("schema") == "style-snapshot:v1":
                examples.append(data)
        self.assertEqual(
            len(examples),
            1,
            "expected exactly one style-snapshot:v1 JSON example",
        )
        self.assertEqual(set(examples[0]), SNAPSHOT_KEYS)

    def test_fit_card_table_names_all_ten_keys(self):
        section = self.text.split("## Fit card", 1)[1].split("\n## ", 1)[0]
        for key in FIT_CARD_KEYS:
            self.assertRegex(
                section,
                r"`%s`" % re.escape(key),
                "fit card table misses %r" % key,
            )

    def test_evidence_levels_are_all_defined_in_the_table(self):
        section = self.text.split("## Evidence levels", 1)[1].split("\n## ", 1)[0]
        for level in ("observed", "declared", "inferred"):
            self.assertIn("`%s`" % level, section)

    def test_cited_scripts_exist_on_disk(self):
        for relative in ("scripts/snapshot.py", "scripts/check_slop.py"):
            self.assertTrue(
                (REPO_ROOT / relative).is_file(),
                "fit-mode reference cites a missing path: %s" % relative,
            )


if __name__ == "__main__":
    unittest.main()
