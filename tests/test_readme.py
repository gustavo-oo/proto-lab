"""Doc-contract tests for the top-level ``README.md``.

The README is the open-source entry door (T22): what the skill is, how to
install it, what it costs, how the pipeline works and what it requires. It is
also the only place that points a reader at the sibling documents produced
by neighboring tasks -- ``CHANGELOG.md`` ("what changed between versions") and
``docs/roadmap.md`` ("what is still open").

Pins:

- the five required sections (``## What it is``, ``## Install``,
  ``## Cost model``, ``## How it works``, ``## Requirements``);
- the ``examples/`` pointer AND the existence of that one path -- it is the
  **only** path this test existence-checks;
- the ``docs/roadmap.md`` pointer (T27 step 4), asserted in prose only;
- the zero-dependency claim and the "does not follow the target's stack" rule;
- the homogenization papers' arXiv ids, read from
  ``docs/research/landscape.md`` (§5) rather than hardcoded here;
- the "early, name provisional" status line.

**R28 (binding):** ``CHANGELOG.md`` is cited in *prose only*. It was produced by
a parallel task, so this test must not existence-check it -- doing so would
create a cross-batch dependency the plan explicitly avoids. (The sibling
``benchmarks/README.md`` reference was removed with the harness in 0.2.0.)

These tests fail while the README is missing and pass once it exists with the
required shape.

Python stdlib only.
"""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(REPO_ROOT, "README.md")
LANDSCAPE = os.path.join(REPO_ROOT, "docs", "research", "landscape.md")

# One section per concern of the entry door; order mirrors the reading order.
REQUIRED_SECTIONS = (
    "## What it is",
    "## Install",
    "## Cost model",
    "## How it works",
    "## Requirements",
)

# The single path whose existence the README pins. Everything else it cites is
# prose-only (R28) or illustrative.
EXISTENCE_CHECKED_PATHS = ("examples",)

# Cited in prose only -- see R28 in the module docstring. No existence check.
PROSE_ONLY_REFERENCES = ("CHANGELOG.md",)

# T27 step 4: the README must point at the open-gap roadmap. Unlike the R28
# reference above, docs/roadmap.md exists on this branch; the pointer is still
# asserted as prose, not existence-checked.
ROADMAP_POINTER = "docs/roadmap.md"

# The homogenization section of the prior-art survey; its arXiv ids must show up
# in the README (they are the empirical reason the skill forces divergence).
LANDSCAPE_SECTION = "## 5. Design homogenization"
ARXIV_RE = re.compile(r"arXiv\s+(\d{4}\.\d{4,5})")


class ReadmeDocTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(README, "r", encoding="utf-8") as fh:
            cls.text = fh.read()
        cls.lower = cls.text.lower()

    def test_readme_exists(self):
        self.assertTrue(os.path.isfile(README), "missing %s" % README)

    def test_required_sections_are_present(self):
        missing = [s for s in REQUIRED_SECTIONS if s not in self.text]
        self.assertEqual(missing, [], "missing sections: %s" % ", ".join(missing))

    def test_examples_pointer_and_existence(self):
        # `examples/` is the demo pointer and the one path this test checks.
        self.assertIn(
            "examples/",
            self.text,
            "README must point at the bundled demo under examples/",
        )
        for name in EXISTENCE_CHECKED_PATHS:
            path = os.path.join(REPO_ROOT, name)
            self.assertTrue(os.path.isdir(path), "missing %s" % path)

    def test_only_examples_is_existence_checked(self):
        # The pin is intentional and exclusive (R28): if a future edit adds
        # another existence check here, this test forces the ruling to be
        # revisited rather than silently creating a cross-task dependency.
        self.assertEqual(EXISTENCE_CHECKED_PATHS, ("examples",))

    def test_prose_only_references_are_cited_not_checked(self):
        for ref in PROSE_ONLY_REFERENCES:
            self.assertIn(
                ref,
                self.text,
                "README must point at %s in prose" % ref,
            )
            # Deliberately no os.path check: these do not exist on this branch
            # (R28). Assert the intent rather than the file.
            self.assertNotIn(ref, EXISTENCE_CHECKED_PATHS)

        self.assertIn(
            ROADMAP_POINTER,
            self.text,
            "README must point at %s" % ROADMAP_POINTER,
        )

    def test_is_zero_dependency(self):
        normalized = self.lower.replace("-", " ")
        self.assertRegex(
            normalized,
            r"zero dependenc",
            "README must state the project is zero-dependency",
        )

    def test_does_not_follow_target_stack(self):
        self.assertRegex(
            self.lower,
            r"not follow\w*\s+the\s+target'?s?\s+stack",
            "README must state that the skill does not follow the target's stack",
        )

    def test_fit_mode_is_documented(self):
        for literal in ("--fit", "style-snapshot.json", "fit-mode.md"):
            self.assertIn(
                literal,
                self.text,
                "README must document fit mode with %s" % literal,
            )

    def test_cites_the_homogenization_papers(self):
        with open(LANDSCAPE, "r", encoding="utf-8") as fh:
            landscape = fh.read()
        section = landscape.split(LANDSCAPE_SECTION, 1)[1].split("\n## ", 1)[0]
        ids = ARXIV_RE.findall(section)
        self.assertGreaterEqual(
            len(ids),
            3,
            "expected >= 3 homogenization arXiv ids in %s" % LANDSCAPE_SECTION,
        )
        missing = [i for i in ids if i not in self.text]
        self.assertEqual(missing, [], "README must cite arXiv ids: %s" % ", ".join(missing))

    def test_status_line_names_early_provisional(self):
        self.assertIn(
            "early, name provisional",
            self.lower,
            "README must carry the 'early, name provisional' status line",
        )

    def test_install_is_copying_into_a_skills_directory(self):
        section = self.text.split("## Install", 1)[1].split("\n## ", 1)[0].lower()
        self.assertIn("skills", section, "install must mention the skills directory")
        self.assertIn("copy", section, "install must be a folder copy, not a package install")
        self.assertNotIn("pip install", section)
        self.assertNotIn("npm install", section)


if __name__ == "__main__":
    unittest.main()
