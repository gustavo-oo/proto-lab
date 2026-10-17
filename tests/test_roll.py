"""Behavioural tests for ``scripts/roll.py`` (Task 10).

The roller maps a seed onto one **design direction card**: it reads the
22-direction machine catalog embedded in ``references/directions.md`` and
draws one direction plus its five knobs with a single SHA-256 scheme defined in
``references/seed-algorithm.md``. The same seed and catalog must always yield
the same card (no timestamp), so the committed ``direction.json`` can never be
re-derived differently.

These tests pin determinism, the exact CARD SCHEMA, catalog diversity, the
domain filter and the generated-seed shape. Python stdlib only.
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import roll  # noqa: E402  (imported after the sys.path tweak above)

SCRIPT = ROOT / "scripts" / "roll.py"

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

KNOB_KEYS = {"accent", "density_shift", "inversion", "rhythm", "imagery_subject"}

SEED_RE = re.compile(r"^[a-z]+-[a-z]+$")


def _run_cli(*args):
    """Run the roller CLI in a subprocess, returning the completed process."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


class DeterminismTest(unittest.TestCase):
    """(a) A seed always rolls the same card."""

    def test_same_seed_rolls_the_same_card(self):
        first = roll.roll("cafe-com-leite")
        second = roll.roll("cafe-com-leite")
        self.assertEqual(first, second, "same seed must yield an identical card")
        self.assertIsInstance(first, dict)


class CrossProcessDeterminismTest(unittest.TestCase):
    """(b) Two CLI processes with the same seed print identical stdout."""

    def test_cli_stdout_is_byte_identical_across_processes(self):
        first = _run_cli("--seed", "cafe-com-leite")
        second = _run_cli("--seed", "cafe-com-leite")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(
            first.stdout,
            second.stdout,
            "stdout must be byte-identical for the same seed",
        )
        self.assertEqual(json.loads(first.stdout)["seed"], "cafe-com-leite")


class CardSchemaTest(unittest.TestCase):
    """(c) The card has exactly the CARD SCHEMA keys and shapes."""

    def setUp(self):
        self.card = roll.roll("cafe-com-leite")

    def test_top_level_keys_are_exactly_the_schema(self):
        self.assertEqual(set(self.card), CARD_SCHEMA_KEYS)

    def test_algorithm_is_pinned(self):
        self.assertEqual(self.card["algorithm"], "sha256:v1")

    def test_seed_is_recorded_verbatim(self):
        self.assertEqual(self.card["seed"], "cafe-com-leite")

    def test_direction_id_and_family_are_strings(self):
        self.assertRegex(self.card["direction_id"], r"^D\d{2}$")
        self.assertIsInstance(self.card["direction_name"], str)
        self.assertTrue(self.card["direction_name"].strip())
        self.assertIsInstance(self.card["family"], str)

    def test_knobs_have_exactly_the_five_keys_and_allowed_values(self):
        knobs = self.card["knobs"]
        self.assertEqual(set(knobs), KNOB_KEYS)
        self.assertIn(knobs["density_shift"], (-1, 0, 1))
        self.assertIn(knobs["rhythm"], ("odd-first", "even-first"))
        self.assertIsInstance(knobs["inversion"], bool)
        self.assertIsInstance(knobs["accent"], (str, type(None)))
        self.assertIsInstance(knobs["imagery_subject"], (str, type(None)))

    def test_filters_object_shape(self):
        filters = self.card["filters"]
        self.assertEqual(set(filters), {"domain", "excluded"})
        self.assertIsNone(filters["domain"])
        self.assertEqual(filters["excluded"], [])

    def test_wild_defaults_to_false(self):
        self.assertIs(self.card["wild"], False)


class CatalogDiversityTest(unittest.TestCase):
    """(d) 200 seeds spread over the catalog and never leave it."""

    def test_two_hundred_seeds_hit_at_least_ten_directions(self):
        catalog_ids = {entry["id"] for entry in roll.load_catalog()}
        drawn = [roll.roll("s%d" % index)["direction_id"] for index in range(200)]
        self.assertGreaterEqual(
            len(set(drawn)),
            10,
            "200 seeds must reach >= 10 distinct directions, got %d: %s"
            % (len(set(drawn)), sorted(set(drawn))),
        )
        self.assertTrue(
            set(drawn) <= catalog_ids,
            "every drawn id must exist in the catalog: %s"
            % sorted(set(drawn) - catalog_ids),
        )


class DomainFilterTest(unittest.TestCase):
    """(e) ``--domain`` prunes incompatible directions before the draw."""

    def _seed_that_picks_d04_or_d05_unfiltered(self):
        for index in range(2000):
            seed = "f%d" % index
            picked = roll.roll(seed)["direction_id"]
            if picked in {"D04", "D05"}:
                return seed, picked
        return None, None

    def test_domain_filter_prunes_and_reroutes_the_draw(self):
        seed, unfiltered_pick = self._seed_that_picks_d04_or_d05_unfiltered()
        self.assertIsNotNone(
            seed, "no seed among f0..f1999 drew D04/D05 without a filter"
        )

        filtered = roll.roll(seed, domain="dense tables")

        self.assertNotEqual(
            filtered["direction_id"],
            unfiltered_pick,
            "the filtered draw must not land on the pruned direction",
        )
        self.assertIn("D04", filtered["filters"]["excluded"])
        self.assertIn("D05", filtered["filters"]["excluded"])
        self.assertEqual(filtered["filters"]["domain"], "dense tables")

    def test_no_filtered_seed_ever_returns_a_pruned_direction(self):
        drawn = {
            roll.roll("d%d" % index, domain="dense tables")["direction_id"]
            for index in range(200)
        }
        self.assertEqual(
            drawn & {"D04", "D05"},
            set(),
            "a dense-tables domain must never draw D04/D05: %s" % sorted(drawn),
        )


class MonochromeAccentTest(unittest.TestCase):
    """A direction with no accent options resolves the accent knob to null."""

    def test_a_monochrome_direction_has_a_null_accent(self):
        catalog = roll.load_catalog()
        monochrome = [e["id"] for e in catalog if not e["accent_options"]]
        self.assertTrue(monochrome, "expected at least one monochrome direction")
        for index in range(5000):
            card = roll.roll("m%d" % index)
            if card["direction_id"] in monochrome:
                self.assertIsNone(card["knobs"]["accent"])
                return
        self.fail("no seed drew a monochrome direction among m0..m4999")


class NewSeedTest(unittest.TestCase):
    """(f) ``new_seed()`` returns an ``adjective-noun`` slug."""

    def test_new_seed_matches_the_slug_format(self):
        for _ in range(100):
            seed = roll.new_seed()
            self.assertRegex(seed, SEED_RE, "unexpected seed shape: %r" % seed)

    def test_new_seeds_are_not_constant(self):
        self.assertGreater(len({roll.new_seed() for _ in range(50)}), 1)


if __name__ == "__main__":
    unittest.main()
