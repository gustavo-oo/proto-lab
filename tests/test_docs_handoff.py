"""Documentation checks for ``references/handoff-format.md``.

The handoff format is the human-readable contract behind the post-choice
artifacts written into ``prototypes/<slug>-<seed>/`` (pipeline §5.6): the
``decisions.md`` log, the ``tokens.css`` token scales, the ``styleguide.html``
mini design system, the ``handoff.md`` inventory and the ``chosen/`` copies.
Those artifacts are consumed downstream (T16/T19), so the document must stay
exact: a section per artifact, the two ``decisions.md`` headings, the five
``tokens.css`` custom-property prefixes, and the two ``handoff.md`` headings
(``## Components`` with name/states/fidelity and ``## Fidelity notes``).

These tests fail while the document is missing and pass once it exists with
the required shape.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = REPO_ROOT / "references" / "handoff-format.md"

# One section per artifact written after a choice is made. Order mirrors §4.
REQUIRED_SECTIONS = (
    "## decisions.md",
    "## tokens.css",
    "## styleguide.html",
    "## handoff.md",
    "## chosen/",
)

# The five custom-property prefixes the ``tokens.css`` convention names.
REQUIRED_TOKEN_PREFIXES = (
    "--color-*",
    "--font-*",
    "--space-*",
    "--radius-*",
    "--motion-*",
)

# Headings that must live, verbatim, inside the template blocks.
DECISIONS_CHOSEN = "## Chosen"
DECISIONS_REJECTED = "## Rejected (and why)"
HANDOFF_COMPONENTS = "## Components"
HANDOFF_FIDELITY = "## Fidelity notes"

# The two fidelity values a component inventory entry can carry.
REQUIRED_FIDELITY_VALUES = ("intentional", "placeholder")

FIT_LITERALS = (
    "style-snapshot.json",
    "fit mode",
    "origin: reused",
    "existing system",
    "snapshot `<hash>`",
)

CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*[ \t]*\r?\n(.*?)```", re.DOTALL)


class HandoffFormatDocTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            DOC_PATH.is_file(),
            "missing handoff format document: %s" % DOC_PATH,
        )
        self.text = DOC_PATH.read_text(encoding="utf-8")

    def test_document_exists(self):
        self.assertTrue(DOC_PATH.is_file(), "missing %s" % DOC_PATH)

    def test_artifact_sections_are_present(self):
        missing = [s for s in REQUIRED_SECTIONS if s not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing artifact sections: %s" % ", ".join(missing),
        )

    def _block_containing(self, marker):
        for block in CODE_BLOCK_RE.findall(self.text):
            if marker in block:
                return block
        self.fail("no fenced code block contains %r" % marker)

    def test_decisions_template_has_chosen_and_rejected(self):
        block = self._block_containing(DECISIONS_REJECTED)
        self.assertIn(DECISIONS_CHOSEN, block)
        self.assertIn(DECISIONS_REJECTED, block)

    def test_tokens_convention_names_the_five_prefixes(self):
        missing = [p for p in REQUIRED_TOKEN_PREFIXES if p not in self.text]
        self.assertEqual(
            missing,
            [],
            "tokens.css convention is missing prefixes: %s" % ", ".join(missing),
        )

    def test_handoff_template_has_components_and_fidelity_notes(self):
        block = self._block_containing(HANDOFF_FIDELITY)
        self.assertIn(HANDOFF_COMPONENTS, block)
        self.assertIn(HANDOFF_FIDELITY, block)

    def test_handoff_components_carry_name_states_fidelity(self):
        block = self._block_containing(HANDOFF_COMPONENTS)
        for field in ("name", "states", "fidelity"):
            self.assertIn(field, block, "handoff entry missing %r" % field)
        missing = [v for v in REQUIRED_FIDELITY_VALUES if v not in block]
        self.assertEqual(
            missing,
            [],
            "handoff fidelity values missing: %s" % ", ".join(missing),
        )

    def test_derivation_rule_is_stated(self):
        self.assertIn("chosen variants", self.text)
        self.assertIn("direction card", self.text)

    def test_fit_mode_handoff_is_documented(self):
        missing = [item for item in FIT_LITERALS if item not in self.text]
        self.assertEqual(
            missing,
            [],
            "handoff format is missing fit literals: %s" % ", ".join(missing),
        )

    def test_handoff_template_carries_the_fit_origin(self):
        block = self._block_containing(HANDOFF_COMPONENTS)
        for item in ("origin: reused", "fit mode"):
            self.assertIn(item, block)


if __name__ == "__main__":
    unittest.main()
