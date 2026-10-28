"""Doc-contract tests for `references/ux-laws.md`.

The UX-law reference is the judge aid behind the `strangeness` axis: a curated
set of U01-U11 checks, each linked to its Laws of UX source, with explicit
caveats against over-application. It is deliberately not a 30-law scorecard.

Python stdlib only.
"""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(REPO_ROOT, "references", "ux-laws.md")

RULES = ["U%02d" % i for i in range(1, 12)]

LAW_URLS = (
    "https://lawsofux.com/hicks-law/",
    "https://lawsofux.com/choice-overload/",
    "https://lawsofux.com/chunking/",
    "https://lawsofux.com/millers-law/",
    "https://lawsofux.com/working-memory/",
    "https://lawsofux.com/cognitive-load/",
    "https://lawsofux.com/fittss-law/",
    "https://lawsofux.com/jakobs-law/",
    "https://lawsofux.com/mental-model/",
    "https://lawsofux.com/law-of-common-region/",
    "https://lawsofux.com/law-of-proximity/",
    "https://lawsofux.com/law-of-similarity/",
    "https://lawsofux.com/law-of-uniform-connectedness/",
    "https://lawsofux.com/law-of-pr%C3%A4gnanz/",
    "https://lawsofux.com/occams-razor/",
    "https://lawsofux.com/teslers-law/",
    "https://lawsofux.com/paradox-of-the-active-user/",
    "https://lawsofux.com/goal-gradient-effect/",
    "https://lawsofux.com/zeigarnik-effect/",
    "https://lawsofux.com/peak-end-rule/",
    "https://lawsofux.com/doherty-threshold/",
    "https://lawsofux.com/von-restorff-effect/",
    "https://lawsofux.com/serial-position-effect/",
    "https://lawsofux.com/postels-law/",
)

CONTEXT_ONLY_URLS = (
    "https://lawsofux.com/aesthetic-usability-effect/",
    "https://lawsofux.com/cognitive-bias/",
    "https://lawsofux.com/flow/",
    "https://lawsofux.com/parkinsons-law/",
    "https://lawsofux.com/pareto-principle/",
)

COMPONENTS = (
    "Form",
    "List or table",
    "Navigation",
    "Dashboard",
    "Multi-step flow",
    "Empty or error state",
    "Landing or hero",
)


class UxLawsDocTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DOC, "r", encoding="utf-8") as handle:
            cls.text = handle.read()
        cls.normalized = re.sub(r"\s+", " ", cls.text)

    def test_doc_exists(self):
        self.assertTrue(os.path.isfile(DOC), "missing %s" % DOC)

    def test_all_rules_are_present(self):
        missing = [rule for rule in RULES if rule not in self.text]
        self.assertEqual(missing, [], "missing UX-law rules: %s" % ", ".join(missing))

    def test_each_rule_has_check_failure_severity_and_caveat(self):
        for marker in (
            "**Check:**",
            "**Failure signal:**",
            "**Severity:**",
            "**Not a hard rule:**",
        ):
            self.assertEqual(
                self.text.count(marker),
                len(RULES),
                "%s should appear once per rule" % marker,
            )

    def test_each_rule_links_its_law(self):
        missing = [url for url in LAW_URLS if url not in self.text]
        self.assertEqual(missing, [], "missing law links: %s" % ", ".join(missing))

    def test_context_only_laws_are_linked(self):
        missing = [url for url in CONTEXT_ONLY_URLS if url not in self.text]
        self.assertEqual(
            missing, [], "missing context-only links: %s" % ", ".join(missing)
        )

    def test_caveats_are_present(self):
        for phrase in (
            "Aesthetic-Usability Effect",
            "Miller's 7±2 is not a cap",
            "Jakob's Law does not forbid divergence",
            "Doherty is a runtime property",
            "Context-only laws",
            "N/A is a valid verdict",
            "Laws can conflict",
        ):
            self.assertIn(phrase, self.normalized, "missing caveat: %s" % phrase)

    def test_component_table_is_present(self):
        for component in COMPONENTS:
            self.assertIn(component, self.text, "missing component: %s" % component)
        self.assertIn(
            "Use two to four rules per component; do not run all eleven",
            self.normalized,
        )

    def test_judge_checklist_is_present(self):
        for phrase in (
            "UX-law FAIL is not a slop fingerprint",
            "does not count toward the `≥ 4` visual cluster",
            "the rule id (`U01`-`U11`)",
            "PASS`, `FAIL` or `N/A`",
        ):
            self.assertIn(phrase, self.normalized, "missing judge checklist: %s" % phrase)

    def test_scope_is_curated_not_a_scorecard(self):
        self.assertIn("curated, not exhaustive", self.normalized)
        self.assertIn("ten always-on checks plus one conditional check", self.normalized)
        self.assertIn("not a scorecard", self.normalized)
        self.assertNotIn("all 30", self.text.lower())

    def test_u11_is_conditional_on_a_form(self):
        self.assertIn("Applies only when the prototype has a form.", self.normalized)

    def test_sources_and_licensing_are_present(self):
        for phrase in (
            "Laws of UX",
            "https://lawsofux.com/",
            "CC BY-NC-ND 4.0",
            "keysjoao/laws-of-ux-skills",
            "rastian/ux-laws",
            "No text from those repositories is copied",
            "proto-lab itself is MIT-licensed",
        ):
            self.assertIn(phrase, self.text, "missing source note: %s" % phrase)


if __name__ == "__main__":
    unittest.main()
