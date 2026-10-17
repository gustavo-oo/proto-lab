"""Doc-contract tests for ``references/research-protocol.md``.

The research protocol is the normative specification of pipeline step 2
(§5.5): the cited competitor/analogue research the skill runs at runtime,
before decision points are derived. It produces ``research.md`` — a small
corpus of SOURCE CARDS consumed downstream by the decision-point derivation
(T16) and the judge (T16/T19). Those consumers read the card fields by name,
so the document must stay exact.

Pins:

- the four sections (``## Protocol``, ``## Source card``,
  ``## Observed vs inferred``, ``## Timebox``);
- the seven source-card keys ``name``, ``url``, ``category``,
  ``good_patterns``, ``bad_patterns``, ``what_to_copy``, ``what_to_avoid``,
  carried by a parseable JSON template;
- the ``3``–``6`` source bounds (minimum 3, maximum 6);
- the ``--skip-research`` off switch.

These tests fail while the document is missing and pass once it exists with the
required shape.

Python stdlib only.
"""

import json
import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(REPO_ROOT, "references", "research-protocol.md")

# One section per concern of the protocol; order mirrors §5.5.
REQUIRED_SECTIONS = (
    "## Protocol",
    "## Source card",
    "## Observed vs inferred",
    "## Timebox",
)

# The seven keys every source card carries (pipeline §5.5).
REQUIRED_CARD_KEYS = (
    "name",
    "url",
    "category",
    "good_patterns",
    "bad_patterns",
    "what_to_copy",
    "what_to_avoid",
)

CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*[ \t]*\r?\n(.*?)```", re.DOTALL)

# "3–6" with an ASCII hyphen or an en dash between the bounds.
SOURCE_BOUNDS_RE = re.compile(r"3\s*[-\u2013]\s*6")


class ResearchProtocolDocTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DOC, "r", encoding="utf-8") as fh:
            cls.text = fh.read()

    def test_doc_exists(self):
        self.assertTrue(os.path.isfile(DOC), "missing %s" % DOC)

    def test_required_sections_are_present(self):
        missing = [s for s in REQUIRED_SECTIONS if s not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing sections: %s" % ", ".join(missing),
        )

    def _card_template(self):
        """Return the parsed JSON source-card template from the doc."""
        for block in CODE_BLOCK_RE.findall(self.text):
            if "good_patterns" not in block:
                continue
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                continue
        self.fail("no fenced JSON block defines a source card template")

    def test_source_card_template_carries_the_seven_keys(self):
        card = self._card_template()
        missing = [k for k in REQUIRED_CARD_KEYS if k not in card]
        self.assertEqual(
            missing,
            [],
            "source card template is missing keys: %s" % ", ".join(missing),
        )

    def test_good_and_bad_patterns_are_lists(self):
        card = self._card_template()
        self.assertIsInstance(
            card["good_patterns"], list, "good_patterns must be a list"
        )
        self.assertIsInstance(
            card["bad_patterns"], list, "bad_patterns must be a list"
        )

    def test_source_bounds_are_stated(self):
        self.assertRegex(
            self.text,
            SOURCE_BOUNDS_RE,
            "missing the 3-6 source bounds",
        )
        self.assertIn("3", self.text, "missing minimum source count 3")
        self.assertIn("6", self.text, "missing maximum source count 6")

    def test_skip_flag_is_stated(self):
        self.assertIn(
            "--skip-research",
            self.text,
            "missing the --skip-research off switch",
        )

    def test_observed_vs_inferred_discipline_is_stated(self):
        # The discipline is normative: UI claims cite page evidence and any
        # inference is marked. The two words must both appear in the section.
        section = self.text.split("## Observed vs inferred", 1)[1]
        self.assertIn("evidence", section.lower())
        self.assertIn("infer", section.lower())

    def test_citation_requirement_is_stated(self):
        # Every source is cited with its URL; no uncited card.
        self.assertIn("url", self.text.lower())
        self.assertIn("cit", self.text.lower())


if __name__ == "__main__":
    unittest.main()
