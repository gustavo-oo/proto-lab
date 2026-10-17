"""Contract checks for the agent-facing ``SKILL.md``.

``SKILL.md`` is the workflow an agent executes end to end: intake, seed roll,
the single decision-point gate, research, generation, judging, presentation,
recording and handoff. Two classes of failure are pinned here:

* **Trigger discipline** — the frontmatter ``description`` must state *when* to
  fire and must not summarise the workflow, or an agent can shortcut straight
  from the description and skip the body (the T02 baseline failure).
* **Mechanical surface** — the pipeline caps, the flag names and the verbatim
  baseline rationalizations the skill has to defeat must appear literally, and
  every ``references/*.md`` / ``scripts/*.py`` path it points at must exist.

These tests fail while ``SKILL.md`` is missing and pass once it exists with the
required shape.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "SKILL.md"

MAX_LINES = 400
MAX_DESCRIPTION = 500

REQUIRED_SECTIONS = (
    "## When to",
    "## Rationalizations",
    "## Red Flags",
    "## Flags",
)

# Workflow verbs banned from the description: naming one lets an agent treat
# the description as the whole instruction set and skip the body.
BANNED_DESCRIPTION_VERBS = ("roll", "generate", "judge", "research", "seed")

REQUIRED_LITERALS = (
    "--seed",
    "--skip-research",
    "--points",
    "--variants",
    "--wild",
    "≥ 4",
    "≤ 4",
    "≤ 3",
    "≤ 6",
)

# The round cap is allowed in either language (D10: repo docs in English,
# conversation in the user's language).
ROUND_CAP_ALTERNATIVES = ("≤ 2 rodadas", "≤ 2 rounds")

# Verbatim rationalizations collected from the RED baseline (T02). Each one is
# a shortcut the skill must name and counter, not a paraphrase.
BASELINE_RATIONALIZATIONS = (
    "Pula o que não for essencial",
    "sem research, sem variantes alternativas, sem perguntas",
    "uma tela basta",
    "não fiz nenhuma pergunta de esclarecimento — público, plataforma e marca "
    "... são suposições minhas",
    "no real data source or persistence — it's static prototype data",
    "as 5 não são o mesmo layout repintado",
)

PATH_RE = re.compile(
    r"(?:references/[A-Za-z0-9_.-]+\.md|scripts/[A-Za-z0-9_.-]+\.(?:py|mjs))"
)


def _parse_frontmatter(text):
    """Minimal YAML frontmatter reader (no PyYAML dependency)."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


class SkillMdTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            SKILL_PATH.is_file(),
            "missing agent-facing workflow document: %s" % SKILL_PATH,
        )
        self.text = SKILL_PATH.read_text(encoding="utf-8")
        self.lines = self.text.splitlines()

    def test_document_exists(self):
        self.assertTrue(SKILL_PATH.is_file(), "missing %s" % SKILL_PATH)

    def test_frontmatter_has_name_and_description(self):
        frontmatter = _parse_frontmatter(self.text)
        self.assertIsNotNone(frontmatter, "SKILL.md has no parseable frontmatter")
        self.assertIn("name", frontmatter)
        self.assertIn("description", frontmatter)
        self.assertEqual(frontmatter["name"], "proto-lab")
        self.assertTrue(frontmatter["description"])

    def test_description_starts_with_use_when(self):
        frontmatter = _parse_frontmatter(self.text)
        self.assertTrue(
            frontmatter["description"].startswith("Use when"),
            "description must open with 'Use when'",
        )

    def test_description_does_not_name_workflow_verbs(self):
        description = _parse_frontmatter(self.text)["description"]
        leaked = [v for v in BANNED_DESCRIPTION_VERBS if v in description]
        self.assertEqual(
            leaked,
            [],
            "description leaks workflow verbs (agent can shortcut): %s"
            % ", ".join(leaked),
        )

    def test_description_is_within_length_budget(self):
        description = _parse_frontmatter(self.text)["description"]
        self.assertLessEqual(len(description), MAX_DESCRIPTION)

    def test_file_is_within_line_budget(self):
        self.assertLessEqual(len(self.lines), MAX_LINES)

    def test_required_sections_are_present(self):
        missing = [s for s in REQUIRED_SECTIONS if s not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing sections: %s" % ", ".join(missing),
        )

    def test_required_literals_are_present(self):
        missing = [lit for lit in REQUIRED_LITERALS if lit not in self.text]
        self.assertEqual(
            missing,
            [],
            "missing required literals: %s" % ", ".join(missing),
        )

    def test_judge_round_cap_is_present(self):
        hits = [cap for cap in ROUND_CAP_ALTERNATIVES if cap in self.text]
        self.assertTrue(
            hits,
            "missing judge round cap (one of %s)"
            % ", ".join(ROUND_CAP_ALTERNATIVES),
        )

    def test_cited_paths_exist_on_disk(self):
        cited = sorted(set(PATH_RE.findall(self.text)))
        self.assertTrue(cited, "SKILL.md cites no references/ or scripts/ paths")
        missing = [p for p in cited if not (REPO_ROOT / p).is_file()]
        self.assertEqual(
            missing,
            [],
            "SKILL.md cites paths that do not exist: %s" % ", ".join(missing),
        )

    def test_baseline_rationalizations_appear_verbatim(self):
        missing = [r for r in BASELINE_RATIONALIZATIONS if r not in self.text]
        self.assertEqual(
            missing,
            [],
            "baseline rationalizations missing from the table: %s"
            % " | ".join(missing),
        )

    def test_single_gate_and_pipeline_steps_are_stated(self):
        # The single interrupting gate is the decision-point confirmation.
        self.assertRegex(self.text, r"single gate", "the single gate is not named")
        self.assertIn("step 3", self.text)
        self.assertIn("decision point", self.text.lower())
        # The pipeline is numbered 0–9 in the spec; every step must be present
        # as a numbered list item (`0. **Setup**` … `9. **Handoff**`).
        numbers = {int(n) for n in re.findall(r"(?m)^(\d+)\. \*\*", self.text)}
        missing = sorted(set(range(10)) - numbers)
        self.assertEqual(
            missing,
            [],
            "pipeline steps missing as numbered items: %s" % missing,
        )

    def test_language_rule_is_stated(self):
        # D10: the conversation follows the user, while repo docs stay English.
        self.assertIn("user's language", self.text)
        self.assertRegex(
            self.text,
            r"repo docs[\s\S]*English",
            "repo docs must be stated as English (D10)",
        )
        self.assertIn("D10", self.text)

    def test_degradation_paths_have_a_section(self):
        self.assertRegex(
            self.text,
            r"## .*Degrad",
            "no degradation section for the §8 fallback paths",
        )


if __name__ == "__main__":
    unittest.main()
