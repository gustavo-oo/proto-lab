"""Behavioural tests for ``scripts/snapshot.py`` (fit mode).

The snapshot tool is the fit-mode counterpart of ``roll.py``: it captures an
existing visual system instead of drawing a catalogue direction, then writes a
deterministic ``style-snapshot.json`` and a FIT ``direction.json``.

These tests pin:

* the capture contract — CSS custom properties/fonts, authored ``--extra``,
  evidence levels, component/layout/voice sections;
* determinism — the same inputs produce the same canonical bytes and hash,
  independent of the process cwd;
* validation — schema, relative paths, no timestamps, caps, approved
  extensions only, and ``--check`` hash drift;
* the FIT card — exactly ten keys, a ``fit-<hash8>`` default seed, and the
  snapshot hash;
* the inherited-slop baseline — existing fingerprints are recorded, not hidden;
* the CLI — capture/check, the paired ``--card`` write, and URL/missing-source
  errors.
"""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import roll  # noqa: E402
import snapshot  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "fit"
SCRIPT = ROOT / "scripts" / "snapshot.py"

CARD_KEYS = {
    "mode",
    "seed",
    "algorithm",
    "direction_id",
    "direction_name",
    "family",
    "knobs",
    "filters",
    "wild",
    "snapshot",
}


def fixture(name):
    return str(FIXTURES / name)


def captured():
    return snapshot.capture(
        fixture("tokens.css"), fixture("extra.json"), fixture("existing.html")
    )


class CaptureTest(unittest.TestCase):
    def setUp(self):
        self.snapshot = captured()

    def test_top_level_schema_and_source(self):
        self.assertEqual(set(self.snapshot), snapshot.TOP_LEVEL_KEYS)
        self.assertEqual(self.snapshot["schema"], "style-snapshot:v1")
        self.assertEqual(self.snapshot["evidence"], "observed")
        self.assertEqual(self.snapshot["source"]["kind"], "repo")
        self.assertEqual(self.snapshot["source"]["root"], ".")
        self.assertEqual(self.snapshot["source"]["files"], ["tokens.css"])
        self.assertIsNone(self.snapshot["source"]["url"])
        self.assertRegex(self.snapshot["hash"], snapshot.HASH_RE)

    def test_token_groups_are_complete_and_classified(self):
        tokens = self.snapshot["tokens"]
        self.assertEqual(set(tokens), set(snapshot.TOKEN_GROUPS))
        self.assertEqual(
            {item["name"] for item in tokens["color"]},
            {"--color-bg", "--color-ink", "--color-accent", "--brand-500"},
        )
        self.assertEqual(
            {item["role"] for item in tokens["color"]},
            {"bg", "ink", "accent", "brand-500"},
        )
        self.assertEqual(
            {item["name"] for item in tokens["font"]},
            {"--font-body", "--font-mono"},
        )
        self.assertEqual(
            [item["name"] for item in tokens["space"]], ["--space-4"]
        )
        self.assertEqual(
            [item["name"] for item in tokens["radius"]], ["--radius-md"]
        )
        self.assertEqual(
            [item["name"] for item in tokens["shadow"]], ["--shadow-card"]
        )
        self.assertEqual(
            [item["name"] for item in tokens["motion"]], ["--motion-fast"]
        )
        self.assertEqual(
            [item["name"] for item in tokens["breakpoint"]], ["--bp-md"]
        )
        self.assertEqual(tokens["other"], [])

    def test_kebab_bp_is_a_breakpoint_not_other(self):
        # The pre-fix classifier left `--bp-md` in `other`.
        breakpoint = self.snapshot["tokens"]["breakpoint"][0]
        self.assertEqual(breakpoint["value"], "768px")
        self.assertEqual(breakpoint["source"], "tokens.css:11")

    def test_families_are_derived_from_font_tokens(self):
        self.assertEqual(self.snapshot["type"]["families"], ["Söhne", "Söhne Mono"])
        self.assertEqual(self.snapshot["type"]["scale"], [])

    def test_extra_components_layout_and_voice_are_merged(self):
        self.assertEqual([item["name"] for item in self.snapshot["components"]], ["Button"])
        button = self.snapshot["components"][0]
        self.assertEqual(button["selector"], ".btn")
        self.assertEqual(button["states"], ["default", "hover", "focus", "disabled"])
        self.assertEqual(button["facts"]["height"], "40px")
        self.assertEqual(button["evidence"], "observed")
        self.assertEqual(self.snapshot["layout"]["max_width"], "1200px")
        self.assertEqual(self.snapshot["layout"]["nav_model"], "fixed sidebar")
        self.assertEqual(
            self.snapshot["voice"]["samples"],
            ["Save changes", "No invoices yet. Create your first one."],
        )
        self.assertEqual(self.snapshot["voice"]["casing"], "sentence case")
        self.assertEqual(
            self.snapshot["constraints"], ["Flat surfaces only; no gradients."]
        )

    def test_inherited_slop_is_recorded_with_a_relative_source(self):
        inherited = {
            (item["rule"], item["fingerprint"]) for item in self.snapshot["inherited_slop"]
        }
        self.assertEqual(inherited, {("R02", "F02"), ("R15", "F15")})
        for item in self.snapshot["inherited_slop"]:
            self.assertEqual(item["source"], "existing.html")

    def test_no_gaps_when_the_capture_is_complete(self):
        self.assertEqual(self.snapshot["gaps"], [])


class DeterminismTest(unittest.TestCase):
    def test_same_inputs_produce_the_same_hash_and_bytes(self):
        first = captured()
        second = captured()
        self.assertEqual(first["hash"], second["hash"])
        self.assertEqual(snapshot._canonical(first), snapshot._canonical(second))

    def test_capture_is_independent_of_cwd(self):
        first = captured()
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                second = captured()
            finally:
                os.chdir(old)
        self.assertEqual(first["hash"], second["hash"])
        self.assertEqual(first["inherited_slop"], second["inherited_slop"])

    def test_a_snapshot_input_round_trips(self):
        first = captured()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "style-snapshot.json"
            path.write_text(snapshot._canonical(first) + "\n", encoding="utf-8")
            second = snapshot.capture(str(path))
        self.assertEqual(first["hash"], second["hash"])
        self.assertEqual(first["tokens"], second["tokens"])
        self.assertEqual(first["source"], second["source"])


class ValidationTest(unittest.TestCase):
    def setUp(self):
        self.snapshot = captured()

    def test_a_captured_snapshot_validates_with_its_hash(self):
        snapshot._validate(self.snapshot, check_hash=True)

    def test_hash_drift_is_rejected(self):
        broken = copy.deepcopy(self.snapshot)
        broken["tokens"]["color"][0]["value"] = "#000000"
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken, check_hash=True)
        self.assertIn("hash mismatch", str(caught.exception))

    def test_absolute_token_source_is_rejected(self):
        broken = copy.deepcopy(self.snapshot)
        broken["tokens"]["color"][0]["source"] = "/Users/gustavo/app/tokens.css:12"
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("relative", str(caught.exception))

    def test_timestamp_is_rejected(self):
        broken = copy.deepcopy(self.snapshot)
        broken["layout"]["captured_at"] = "2026-10-28T12:00:00Z"
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("timestamp", str(caught.exception))

    def test_unknown_top_level_key_is_rejected(self):
        broken = copy.deepcopy(self.snapshot)
        broken["captured"] = True
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("unknown", str(caught.exception))

    def test_source_file_cap_is_enforced(self):
        broken = copy.deepcopy(self.snapshot)
        broken["source"]["files"] = ["f%d.css" % index for index in range(9)]
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("cap is 8", str(caught.exception))

    def test_component_cap_is_enforced(self):
        broken = copy.deepcopy(self.snapshot)
        broken["components"] = [
            copy.deepcopy(self.snapshot["components"][0]) for _ in range(13)
        ]
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("cap is 12", str(caught.exception))

    def test_voice_sample_cap_is_enforced(self):
        broken = copy.deepcopy(self.snapshot)
        broken["voice"]["samples"] = ["sample %d" % index for index in range(6)]
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("cap is 5", str(caught.exception))

    def test_unapproved_extension_is_rejected(self):
        broken = copy.deepcopy(self.snapshot)
        broken["extensions"].append(
            {
                "role": "color",
                "name": "--color-danger",
                "value": "#b42318",
                "reason": "destructive state",
                "approved_at_gate": False,
            }
        )
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("approved_at_gate", str(caught.exception))

    def test_token_evidence_cannot_be_stronger_than_the_header(self):
        broken = copy.deepcopy(self.snapshot)
        broken["evidence"] = "declared"
        broken["tokens"]["color"][0]["evidence"] = "observed"
        with self.assertRaises(snapshot.SnapshotError) as caught:
            snapshot._validate(broken)
        self.assertIn("stronger", str(caught.exception))


class FitCardTest(unittest.TestCase):
    def setUp(self):
        self.snapshot = captured()
        self.card = snapshot.make_card(self.snapshot)

    def test_card_has_exactly_ten_keys(self):
        self.assertEqual(set(self.card), CARD_KEYS)

    def test_card_records_the_fit_mode_and_snapshot_hash(self):
        self.assertEqual(self.card["mode"], "fit")
        self.assertEqual(self.card["algorithm"], "snapshot:v1")
        self.assertEqual(self.card["direction_id"], "FIT")
        self.assertEqual(self.card["family"], "existing")
        self.assertEqual(self.card["knobs"], {})
        self.assertEqual(self.card["filters"], {"domain": None, "excluded": []})
        self.assertIs(self.card["wild"], False)
        self.assertEqual(self.card["snapshot"]["path"], "style-snapshot.json")
        self.assertEqual(self.card["snapshot"]["hash"], self.snapshot["hash"])

    def test_default_seed_is_fit_hash8(self):
        digest = self.snapshot["hash"].split(":", 1)[1]
        self.assertEqual(self.card["seed"], "fit-" + digest[:8])

    def test_named_and_unnamed_direction_names(self):
        self.assertEqual(self.card["direction_name"], "Existing system")
        named = snapshot.make_card(self.snapshot, name="Acme")
        self.assertEqual(named["direction_name"], "Existing system — Acme")

    def test_card_is_canonical_json(self):
        text = roll.dumps(self.card)
        self.assertEqual(text, json.dumps(self.card, sort_keys=True, separators=(",", ":")))
        self.assertEqual(json.loads(text), self.card)


class FlatTokenTest(unittest.TestCase):
    def test_flat_json_tokens_are_normalized(self):
        result = snapshot.capture(fixture("flat-tokens.json"))
        self.assertEqual(
            {item["name"] for item in result["tokens"]["color"]},
            {"--color-bg", "--color-ink", "--color-accent"},
        )
        self.assertEqual(
            [item["name"] for item in result["tokens"]["font"]], ["--font-body"]
        )
        self.assertEqual(result["type"]["families"], ["Söhne"])
        self.assertEqual(result["evidence"], "declared")
        self.assertEqual(result["source"]["files"], ["flat-tokens.json"])
        self.assertTrue(
            any(gap.startswith("flat token JSON") for gap in result["gaps"])
        )


class CliTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
        )

    def test_cli_writes_the_snapshot_and_card_and_check_passes(self):
        out = self.tmp / "style-snapshot.json"
        card_path = self.tmp / "direction.json"
        result = self.run_cli(
            "--from",
            fixture("tokens.css"),
            "--extra",
            fixture("extra.json"),
            "--existing-html",
            fixture("existing.html"),
            "--out",
            str(out),
            "--card",
            str(card_path),
            "--name",
            "Acme",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(out.is_file())
        self.assertTrue(card_path.is_file())
        card = json.loads(card_path.read_text(encoding="utf-8"))
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(card["snapshot"]["hash"], data["hash"])
        self.assertEqual(card["direction_name"], "Existing system — Acme")
        checked = self.run_cli("--check", str(out))
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn('"ok": true', checked.stdout)

    def test_cli_check_rejects_drift(self):
        out = self.tmp / "style-snapshot.json"
        result = self.run_cli(
            "--from",
            fixture("tokens.css"),
            "--extra",
            fixture("extra.json"),
            "--existing-html",
            fixture("existing.html"),
            "--out",
            str(out),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(out.read_text(encoding="utf-8"))
        data["tokens"]["color"][0]["value"] = "#000000"
        out.write_text(json.dumps(data), encoding="utf-8")
        checked = self.run_cli("--check", str(out))
        self.assertEqual(checked.returncode, 1)
        self.assertIn("hash mismatch", checked.stderr)

    def test_cli_rejects_a_url_without_browser_extra(self):
        result = self.run_cli(
            "--from", "https://app.example.test", "--out", str(self.tmp / "x.json")
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("URL source needs", result.stderr)

    def test_cli_rejects_a_missing_source(self):
        result = self.run_cli("--from", str(self.tmp / "missing.css"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("does not exist", result.stderr)

    def test_cli_card_without_out_writes_the_pair(self):
        card_path = self.tmp / "direction.json"
        result = self.run_cli(
            "--from",
            fixture("tokens.css"),
            "--extra",
            fixture("extra.json"),
            "--existing-html",
            fixture("existing.html"),
            "--card",
            str(card_path),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(card_path.is_file())
        self.assertTrue((self.tmp / "style-snapshot.json").is_file())
        card = json.loads(card_path.read_text(encoding="utf-8"))
        data = json.loads((self.tmp / "style-snapshot.json").read_text(encoding="utf-8"))
        self.assertEqual(card["snapshot"]["hash"], data["hash"])


if __name__ == "__main__":
    unittest.main()
