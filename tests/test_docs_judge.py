"""Documentation checks for ``references/judge-rubric.md``.

The judge rubric is the human-readable contract behind ``judge-report.md``
(pipeline step 4, the pre-human gate). It defines the JUDGE REPORT FORMAT
consumed by the judge runner and by the loop fixtures (T16/T17/T19), so the
document must stay exact: the five axis names, the three severities, a
copy-pasteable report template (table header + ``## Open (not fixed)``), and
the two required sections describing how the judge stays honest
(``## Degraded mode``) and blind to the generator (``## Fresh eyes``).

These tests fail while the document is missing and pass once it exists with
the required shape.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = REPO_ROOT / "references" / "judge-rubric.md"

# The five axes the judge scores, one verdict each. Order is the rubric order.
REQUIRED_AXES = (
    "brief-fidelity",
    "strangeness",
    "slop-scan",
    "direction-fidelity",
    "variant-diversity",
)

# Findings carry exactly one severity; the report also reports the residue.
REQUIRED_SEVERITIES = ("blocker", "major", "minor")

# Verdicts are binary per axis.
REQUIRED_VERDICTS = ("PASS", "FAIL")

# Sections that pin the judge's operating discipline.
REQUIRED_SECTIONS = (
    "## Degraded mode",
    "## Fresh eyes",
)

# The report template lives in a fenced block and must carry, verbatim, the
# table header and the open-findings section.
TABLE_HEADER = "| axis | verdict | evidence |"
OPEN_SECTION = "## Open (not fixed)"

CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*[ \t]*\r?\n(.*?)```", re.DOTALL)


class JudgeRubricDocTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            "missing judge rubric document: %s" % DOC_PATH,
        )
        self.text = DOC_PATH.read_text(encoding="utf-8")

    def test_document_exists(self):
        self.assertTrue(DOC_PATH.is_file(), "missing %s" % DOC_PATH)

    def test_five_axis_names_are_present(self):
        missing = [axis for axis in REQUIRED_AXES if axis not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing axis names: %s" % ", ".join(missing),
        )

    def test_severities_are_present(self):
        missing = [sev for sev in REQUIRED_SEVERITIES if sev not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing severities: %s" % ", ".join(missing),
        )

    def test_verdicts_are_present(self):
        missing = [v for v in REQUIRED_VERDICTS if v not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing verdicts: %s" % ", ".join(missing),
        )

    def test_required_sections_are_present(self):
        missing = [s for s in REQUIRED_SECTIONS if s not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing sections: %s" % ", ".join(missing),
        )

    def _report_template_block(self):
        for block in CODE_BLOCK_RE.findall(self.text):
            if TABLE_HEADER in block and OPEN_SECTION in block:
                return block
        self.fail(
            "no fenced code block contains both %r and %r"
            % (TABLE_HEADER, OPEN_SECTION)
        )

    def test_report_template_has_table_and_open_section(self):
        block = self._report_template_block()
        self.assertIn(TABLE_HEADER, block)
        self.assertIn(OPEN_SECTION, block)

    def test_report_template_lists_all_five_axes(self):
        block = self._report_template_block()
        missing = [axis for axis in REQUIRED_AXES if axis not in block]
        self.assertEqual(
            missing,
            [],
            "report template is missing axis rows: %s" % ", ".join(missing),
        )


if __name__ == "__main__":
    unittest.main()
