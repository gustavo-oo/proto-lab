"""Documentation checks for ``references/seed-algorithm.md``.

The seed algorithm document is the human-readable contract behind
``scripts/roll.py`` and its ``roll.mjs`` mirror. It defines the CARD
SCHEMA consumed by later tasks, so the document must stay exact: the
deterministic hash, the section layout and a parseable example card.

These tests fail while the document is missing and pass once it exists
with the required shape.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = REPO_ROOT / "references" / "seed-algorithm.md"

REQUIRED_SECTIONS = (
    "## Algorithm",
    "## Card schema",
    "## Knobs",
    "## Domain filter",
    "## Seed generation",
)

# The CARD SCHEMA: ``direction.json`` has exactly these 8 top-level keys.
CARD_SCHEMA_KEYS = {
    "seed",
    "algorithm",
    "direction_id",
    "direction_name",
    "family",
    "knobs",
    "filters",
    "wild",
}

JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)


class SeedAlgorithmDocTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            "missing seed algorithm document: %s" % DOC_PATH,
        )
        self.text = DOC_PATH.read_text(encoding="utf-8")

    def test_document_exists(self):
        self.assertTrue(DOC_PATH.is_file(), "missing %s" % DOC_PATH)

    def test_required_sections_are_present(self):
        missing = [section for section in REQUIRED_SECTIONS if section not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing sections: %s" % ", ".join(missing),
        )

    def test_algorithm_literals_are_present(self):
        self.assertIn("sha256", self.text)
        self.assertIn('":direction:v1"', self.text)

    def test_example_card_parses_and_has_exactly_the_card_schema(self):
        blocks = JSON_BLOCK_RE.findall(self.text)
        self.assertTrue(blocks, "no fenced ```json code block found in the document")

        parsed = [json.loads(block) for block in blocks]
        exact_cards = [
            card
            for card in parsed
            if isinstance(card, dict) and set(card.keys()) == CARD_SCHEMA_KEYS
        ]
        self.assertTrue(
            exact_cards,
            "no example card has exactly the CARD SCHEMA keys: %s"
            % ", ".join(sorted(CARD_SCHEMA_KEYS)),
        )


if __name__ == "__main__":
    unittest.main()
