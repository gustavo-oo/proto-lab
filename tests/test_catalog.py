"""Documentation checks for ``references/directions.md``.

The catalog is the closed system of 22 design directions. A human reader uses
the prose sections (``### D01`` … ``### D22``) as the source for the generator,
while ``scripts`` read the machine block delimited by
``<!-- CATALOG_JSON_START -->`` / ``<!-- CATALOG_JSON_END -->``. Both halves
must describe the same 22 directions with the same ids and names.

These tests fail while the document is missing and pass once it exists with
the required shape.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = REPO_ROOT / "references" / "directions.md"

CATALOG_JSON_RE = re.compile(
    r"<!-- CATALOG_JSON_START -->\n(.*?)\n<!-- CATALOG_JSON_END -->",
    re.S,
)

# The machine interface: exactly these keys in every entry.
REQUIRED_KEYS = (
    "id",
    "name",
    "family",
    "fits",
    "fails",
    "forbidden_moves",
    "type",
    "palette_logic",
    "density",
    "motion",
    "voice",
    "imagery_options",
    "inversion_allowed",
    "system_font_first",
)

TYPE_KEYS = ("display", "body", "mono", "fallback_stack")

# Closed set of families (see global constraints: exactly 22 directions).
FAMILIES = {
    "quiet",
    "dark",
    "retro",
    "print",
    "brutalist",
    "systemic",
    "playful",
    "editorial",
    "technical",
    "luxe",
}

# A fallback stack is "same class" when it names one of these generic classes.
FALLBACK_CLASSES = ("serif", "sans-serif", "monospace", "system-ui")

EXPECTED_IDS = ["D%02d" % number for number in range(1, 23)]


class DirectionsCatalogDocTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            "missing design directions catalog: %s" % DOC_PATH,
        )
        self.text = DOC_PATH.read_text(encoding="utf-8")

        match = CATALOG_JSON_RE.search(self.text)
        self.assertIsNotNone(
            match,
            "missing machine block between <!-- CATALOG_JSON_START --> and "
            "<!-- CATALOG_JSON_END -->",
        )
        self.raw_json = match.group(1)

        try:
            self.catalog = json.loads(self.raw_json)
        except ValueError as error:  # pragma: no cover - message clarity
            self.fail("machine block does not parse as JSON: %s" % error)

    def test_document_exists(self):
        self.assertTrue(DOC_PATH.is_file(), "missing %s" % DOC_PATH)

    def test_machine_block_is_a_list_of_22_entries(self):
        self.assertIsInstance(self.catalog, list, "catalog JSON must be an array")
        self.assertEqual(
            len(self.catalog),
            22,
            "catalog must hold exactly 22 directions, found %d" % len(self.catalog),
        )

    def test_ids_are_unique_ordered_and_complete(self):
        ids = [entry.get("id") for entry in self.catalog]
        self.assertEqual(
            ids,
            EXPECTED_IDS,
            "ids must be D01..D22, unique and ordered by id",
        )

    def test_every_entry_has_exactly_the_required_keys(self):
        for entry in self.catalog:
            with self.subTest(entry=entry.get("id")):
                self.assertEqual(
                    set(entry.keys()),
                    set(REQUIRED_KEYS),
                    "entry %s must have exactly the required keys" % entry.get("id"),
                )

    def test_type_objects_have_exactly_the_four_keys(self):
        for entry in self.catalog:
            with self.subTest(entry=entry.get("id")):
                self.assertIsInstance(entry["type"], dict)
                self.assertEqual(
                    set(entry["type"].keys()),
                    set(TYPE_KEYS),
                    "type of %s must have exactly %s" % (entry["id"], ", ".join(TYPE_KEYS)),
                )

    def test_value_types_are_correct(self):
        for entry in self.catalog:
            with self.subTest(entry=entry.get("id")):
                for key in ("name", "family", "palette_logic", "density", "motion", "voice"):
                    self.assertIsInstance(entry[key], str, "%s.%s must be a string" % (entry["id"], key))
                    self.assertTrue(entry[key].strip(), "%s.%s must not be empty" % (entry["id"], key))
                for key in ("fits", "fails", "forbidden_moves", "imagery_options"):
                    self.assertIsInstance(entry[key], list, "%s.%s must be a list" % (entry["id"], key))
                    self.assertTrue(
                        all(isinstance(item, str) for item in entry[key]),
                        "%s.%s must only hold strings" % (entry["id"], key),
                    )
                for key in ("inversion_allowed", "system_font_first"):
                    self.assertIsInstance(entry[key], bool, "%s.%s must be a boolean" % (entry["id"], key))

    def test_families_are_in_the_closed_set(self):
        for entry in self.catalog:
            with self.subTest(entry=entry.get("id")):
                self.assertIn(
                    entry["family"],
                    FAMILIES,
                    "family %r of %s is outside the closed set" % (entry["family"], entry["id"]),
                )

    def test_fallback_stack_is_a_same_class_stack(self):
        for entry in self.catalog:
            with self.subTest(entry=entry.get("id")):
                stack = entry["type"]["fallback_stack"]
                self.assertIsInstance(stack, str, "%s fallback_stack must be a string" % entry["id"])
                self.assertTrue(
                    any(token in stack for token in FALLBACK_CLASSES),
                    "%s fallback_stack must name a generic class (%s): %r"
                    % (entry["id"], ", ".join(FALLBACK_CLASSES), stack),
                )

    def test_d04_and_d05_are_pruned_for_dense_tables(self):
        by_id = {entry["id"]: entry for entry in self.catalog}
        for direction_id in ("D04", "D05"):
            with self.subTest(entry=direction_id):
                self.assertIn(
                    "dense tables",
                    by_id[direction_id]["fails"],
                    "%s must carry the literal tag 'dense tables' in fails" % direction_id,
                )

    def test_every_prose_section_appears_exactly_once(self):
        for direction_id in EXPECTED_IDS:
            with self.subTest(entry=direction_id):
                self.assertEqual(
                    self.text.count("### %s" % direction_id),
                    1,
                    "prose heading '### %s' must appear exactly once" % direction_id,
                )

    def test_prose_and_json_agree_on_id_and_name(self):
        for entry in self.catalog:
            heading = "### %s · %s" % (entry["id"], entry["name"])
            with self.subTest(entry=entry["id"]):
                self.assertIn(
                    heading,
                    self.text,
                    "prose must open with %r so prose and JSON agree" % heading,
                )


if __name__ == "__main__":
    unittest.main()
