"""Documentation checks for ``references/decision-points.md``.

The decision-points document is the human-readable contract behind
``points.json`` (pipeline step 3). It defines the POINTS.JSON SCHEMA
consumed by the variant generators (T12/T14/T16) and pins the closed
``axis`` vocabulary, so the document must stay exact: the required
sections, a parseable example that matches the schema element by
element, and at least eight named axes.

These tests fail while the document is missing and pass once it exists
with the required shape.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = REPO_ROOT / "references" / "decision-points.md"

REQUIRED_SECTIONS = (
    "## Taxonomy",
    "## Derivation",
    "## Contract",
    "## Axis vocabulary",
)

# POINTS.JSON SCHEMA: top-level keys and keys per element.
POINTS_TOP_KEYS = {"slug", "points"}
POINT_KEYS = {"id", "question", "why", "axis", "options", "screens", "status", "chosen"}
OPTION_KEYS = {"key", "label", "descriptor"}

VALID_STATUS = {"pending", "chosen", "rejected"}

# The closed ``axis`` vocabulary must name at least eight axes.
MIN_AXES = 8

# The eight axes the brief calls out explicitly.
BRIEF_AXES = {
    "navigation-model",
    "listing-pattern",
    "information-density",
    "primary-action-placement",
    "form-pattern",
    "empty-states",
    "dashboard-composition",
    "onboarding-shape",
}

JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)
AXIS_ROW_RE = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`", re.MULTILINE)


class DecisionPointsDocTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            "missing decision-points document: %s" % DOC_PATH,
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

    def _axis_vocabulary_section(self):
        start = self.text.index("## Axis vocabulary")
        rest = self.text[start + len("## Axis vocabulary"):]
        end = rest.find("\n## ")
        return rest if end == -1 else rest[:end]

    def test_axis_vocabulary_lists_at_least_eight_axes(self):
        section = self._axis_vocabulary_section()
        axes = AXIS_ROW_RE.findall(section)
        self.assertGreaterEqual(
            len(axes),
            MIN_AXES,
            "expected >= %d axes in the Axis vocabulary table, found %d: %s"
            % (MIN_AXES, len(axes), ", ".join(axes)),
        )
        missing = sorted(BRIEF_AXES - set(axes))
        self.assertEqual(
            missing,
            [],
            "axis vocabulary is missing brief axes: %s" % ", ".join(missing),
        )

    def _example_block(self):
        for block in JSON_BLOCK_RE.findall(self.text):
            try:
                parsed = json.loads(block)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict) and set(parsed.keys()) == POINTS_TOP_KEYS:
                return parsed
        self.fail(
            "no fenced ```json example has exactly the POINTS top-level keys: %s"
            % ", ".join(sorted(POINTS_TOP_KEYS))
        )

    def test_example_matches_points_schema(self):
        example = self._example_block()

        self.assertIsInstance(example["slug"], str)
        self.assertIsInstance(example["points"], list)
        self.assertTrue(example["points"], "example must contain at least one point")

        declared_axes = set(AXIS_ROW_RE.findall(self._axis_vocabulary_section()))

        for point in example["points"]:
            self.assertIsInstance(point, dict)
            self.assertEqual(
                set(point.keys()),
                POINT_KEYS,
                "point %r does not have exactly the POINT keys" % point.get("id"),
            )
            self.assertIsInstance(point["id"], str)
            self.assertIsInstance(point["question"], str)
            self.assertIsInstance(point["why"], str)
            self.assertIn(point["axis"], declared_axes,
                          "axis %r is not in the declared vocabulary" % point["axis"])

            options = point["options"]
            self.assertIsInstance(options, list)
            self.assertIn(len(options), (2, 3),
                          "point %r must have 2-3 options" % point["id"])
            for option in options:
                self.assertEqual(set(option.keys()), OPTION_KEYS)
                self.assertIsInstance(option["key"], str)
                self.assertIsInstance(option["label"], str)
                self.assertIsInstance(option["descriptor"], str)

            self.assertIsInstance(point["screens"], list)
            self.assertTrue(point["screens"])
            self.assertTrue(all(isinstance(s, str) for s in point["screens"]))

            self.assertIn(point["status"], VALID_STATUS)
            self.assertTrue(
                point["chosen"] is None or isinstance(point["chosen"], str),
                "chosen must be str or null for point %r" % point["id"],
            )


if __name__ == "__main__":
    unittest.main()
