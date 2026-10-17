"""Doc-contract tests for `references/slop-fingerprints.md`.

Pins the interface of the slop-fingerprint spec (Task 08): 26 fingerprints
F01-F26, the 22 mechanical rules R01-R22 (each carrying a detection kind of
`solid` or `heuristic`), the 4 judge-only fingerprints (F16, F18, F21, F22),
and the `≥ 4 hits = fail` threshold.

Python stdlib only.
"""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(REPO_ROOT, "references", "slop-fingerprints.md")

FINGERPRINTS = ["F%02d" % i for i in range(1, 27)]  # F01..F26
RULES = ["R%02d" % i for i in range(1, 23)]  # R01..R22
JUDGE_ONLY = ["F16", "F18", "F21", "F22"]

# A rule row is a table row whose first cell is a rule id, e.g. `| R01 | ... |`.
RULE_ROW_RE = re.compile(r"^\|\s*(R\d{2})\s*\|")


class SlopFingerprintsDocTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DOC, "r", encoding="utf-8") as fh:
            cls.text = fh.read()
        cls.lines = cls.text.splitlines()

    def test_doc_exists(self):
        self.assertTrue(os.path.isfile(DOC), "missing %s" % DOC)

    def test_all_fingerprints_present(self):
        for fp in FINGERPRINTS:
            self.assertIn(fp, self.text, "missing fingerprint %s" % fp)

    def test_all_rules_present(self):
        for rule in RULES:
            self.assertIn(rule, self.text, "missing rule %s" % rule)

    def test_every_rule_row_states_detection_kind(self):
        rule_rows = {}
        for line in self.lines:
            match = RULE_ROW_RE.match(line)
            if not match:
                continue
            rule_rows.setdefault(match.group(1), []).append(line)
        for rule in RULES:
            self.assertIn(rule, rule_rows, "no rule row defined for %s" % rule)
            for line in rule_rows[rule]:
                self.assertTrue(
                    ("solid" in line) or ("heuristic" in line),
                    "rule row for %s must say solid or heuristic: %r" % (rule, line),
                )

    def test_threshold_phrase_present(self):
        self.assertIn("≥ 4", self.text, "missing threshold phrase '≥ 4'")

    def test_judge_only_fingerprints_are_labelled(self):
        for fp in JUDGE_ONLY:
            labelled = any(
                (fp in line) and ("judge-only" in line) for line in self.lines
            )
            self.assertTrue(
                labelled, "%s must appear together with judge-only" % fp
            )


if __name__ == "__main__":
    unittest.main()
