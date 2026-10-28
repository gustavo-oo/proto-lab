"""Doc-contract tests for `references/copy-contract.md`.

The copy contract is the zero-tolerance half of the anti-slop gate: C01
(item-count labels), C02 (repeated facts), C03 (filler copy) and C04
(separator glyphs). It is deliberately separate from the visual fingerprint
cluster in `references/slop-fingerprints.md`, which keeps its own `>= 4 hits`
threshold.

Python stdlib only.
"""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(REPO_ROOT, "references", "copy-contract.md")

RULES = ("C01", "C02", "C03", "C04")
BANNED_GLYPHS = ("·", "—", "–", "|", "•")


class CopyContractDocTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DOC, "r", encoding="utf-8") as handle:
            cls.text = handle.read()
        cls.normalized = re.sub(r"\s+", " ", cls.text)

    def test_doc_exists(self):
        self.assertTrue(os.path.isfile(DOC), "missing %s" % DOC)

    def test_all_rules_are_present(self):
        missing = [rule for rule in RULES if rule not in self.text]
        self.assertEqual(missing, [], "missing copy rules: %s" % ", ".join(missing))

    def test_zero_tolerance_is_stated(self):
        self.assertRegex(
            self.text,
            r"zero[- ]tolerance",
            "the copy gate must be declared zero-tolerance",
        )

    def test_separator_ban_is_stated(self):
        self.assertIn("Do not use separator glyphs", self.text)
        for glyph in BANNED_GLYPHS:
            self.assertIn(glyph, self.text, "banned glyph %r is not named" % glyph)

    def test_item_count_examples_are_present(self):
        self.assertIn("6 filmes, 4 cinemas", self.text)
        self.assertIn("10 registros", self.text)

    def test_repetition_limit_is_stated(self):
        self.assertIn("At most one repetition", self.text)
        self.assertIn("at most two visible occurrences", self.text)

    def test_filler_delete_test_is_stated(self):
        self.assertIn("Delete-test", self.normalized)
        self.assertIn("delete it permanently", self.normalized)

    def test_session_chrome_marker_is_documented(self):
        self.assertIn("data-session-chrome", self.text)

    def test_scope_is_product_copy(self):
        self.assertIn("product copy", self.text)
        self.assertIn("`variants/**`", self.text)
        self.assertIn("`chosen/**`", self.text)

    def test_copy_is_separate_from_the_visual_cluster(self):
        self.assertIn("not counted in the visual cluster", self.text)
        self.assertIn("visual: N/26; copy: C01..C04", self.text)

    def test_mechanical_checker_is_documented(self):
        self.assertIn("scripts/check_copy.py", self.text)
        self.assertIn("C02 and C03 are judge-only", self.text)

    def test_no_separator_mandate_is_left(self):
        # The contract must not accidentally restore the old "use ·" rule.
        self.assertNotIn("Use `·`", self.text)
        self.assertNotRegex(self.text, r"one separator:\s*`·`")


if __name__ == "__main__":
    unittest.main()
