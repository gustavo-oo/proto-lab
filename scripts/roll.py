#!/usr/bin/env python3
"""Deterministic seed -> design direction card roller (proto-lab).

This is the Python reference implementation of ``references/seed-algorithm.md``.
Given a seed it draws exactly one direction from the 22-entry machine catalog
embedded in ``references/directions.md`` and fills the five orthogonal knobs,
all with a single SHA-256 scheme. The same seed and the same filtered catalog
always yield the same card; the card carries no timestamp for that reason.

The Node mirror ``scripts/roll.mjs`` reproduces this byte for byte, so the CLI
emits canonical JSON (``sort_keys=True``, compact separators).

Python stdlib only, Python >= 3.8.

Usage:
    python3 scripts/roll.py [--seed S] [--domain D] [--wild] [--out PATH]
                            [--catalog PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

# --- The hash scheme (verbatim from references/seed-algorithm.md) -----------

# The direction label carries its own leading colon; the hash input is exactly
# ``seed + label`` (one colon, never ``seed + ":" + label``).
DIRECTION_LABEL = ":direction:v1"
ALGORITHM = "sha256:v1"

# Each knob draws with its own independent label.
ACCENT_LABEL = ":accent"
DENSITY_LABEL = ":density"
INVERT_LABEL = ":invert"
RHYTHM_LABEL = ":rhythm"
IMAGERY_LABEL = ":imagery"

DENSITY_STEPS = (-1, 0, 1)
RHYTHMS = ("odd-first", "even-first")

# Default catalog: ``../references/directions.md`` relative to this script.
DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "references" / "directions.md"

# Task 07's machine-block regex: the catalog lives between these markers.
CATALOG_JSON_RE = re.compile(
    r"<!-- CATALOG_JSON_START -->\n(.*?)\n<!-- CATALOG_JSON_END -->",
    re.S,
)

# --- Seed generation (32 adjectives x 32 nouns = 1024 slugs) ----------------

ADJECTIVES = (
    "quiet", "brutal", "warm", "cold", "soft", "sharp", "calm", "bold",
    "pale", "deep", "bright", "muted", "crisp", "hazy", "sleek", "rugged",
    "gentle", "loud", "slow", "swift", "charcoal", "amber", "velvet", "paper",
    "neon", "dusty", "glass", "copper", "silent", "electric", "feral", "sober",
)

NOUNS = (
    "harbour", "vector", "signal", "ledger", "meadow", "canyon", "lantern",
    "archive", "orbit", "prism", "atlas", "ember", "grove", "cipher",
    "furnace", "lagoon", "meridian", "quarry", "tapestry", "velocity",
    "anchor", "beacon", "compass", "delta", "fabric", "granite", "helix",
    "inkwell", "junction", "kettle", "lattice", "monolith",
)

_SYSTEM_RANDOM = random.SystemRandom()


def draw(seed, label):
    """Reduce ``sha256(seed + label)`` to a 64-bit unsigned integer.

    Big-endian, first 8 bytes; up to 2^64 - 1. The Node mirror must use BigInt
    for this value to stay byte-identical.
    """
    digest = hashlib.sha256((seed + label).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def load_catalog(path=None):
    """Return the machine catalog, ordered by direction id.

    ``path`` defaults to ``references/directions.md`` relative to this script.
    Only the JSON block between ``CATALOG_JSON_START`` and ``CATALOG_JSON_END``
    is read.
    """
    source = Path(path) if path is not None else DEFAULT_CATALOG
    text = source.read_text(encoding="utf-8")
    match = CATALOG_JSON_RE.search(text)
    if match is None:
        raise ValueError(
            "no catalog block between <!-- CATALOG_JSON_START --> and "
            "<!-- CATALOG_JSON_END --> in %s" % source
        )
    catalog = json.loads(match.group(1))
    return sorted(catalog, key=lambda entry: entry["id"])


def excluded_by_domain(direction, domain):
    """True when any ``fails`` tag is a case-insensitive substring of domain."""
    if not domain:
        return False
    needle = domain.lower()
    return any(tag.lower() in needle for tag in direction["fails"])


def _knobs(direction, seed):
    """Fill the five orthogonal knobs for the drawn direction."""
    accents = direction["accent_options"]
    accent = accents[draw(seed, ACCENT_LABEL) % len(accents)] if accents else None

    subjects = direction["imagery_subjects"]
    imagery_subject = (
        subjects[draw(seed, IMAGERY_LABEL) % len(subjects)] if subjects else None
    )

    return {
        "accent": accent,
        "density_shift": DENSITY_STEPS[draw(seed, DENSITY_LABEL) % len(DENSITY_STEPS)],
        "inversion": bool(
            direction["inversion_allowed"] and draw(seed, INVERT_LABEL) % 2 == 1
        ),
        "rhythm": RHYTHMS[draw(seed, RHYTHM_LABEL) % len(RHYTHMS)],
        "imagery_subject": imagery_subject,
    }


def draw_card(catalog, seed, domain=None, wild=False):
    """Draw the CARD SCHEMA from a pre-loaded ``catalog`` (ordered by id)."""
    excluded = [
        entry["id"] for entry in catalog if excluded_by_domain(entry, domain)
    ]
    survivors = [
        entry for entry in catalog if not excluded_by_domain(entry, domain)
    ]
    if not survivors:
        raise ValueError(
            "domain %r excludes every direction; widen the domain" % domain
        )

    direction = survivors[draw(seed, DIRECTION_LABEL) % len(survivors)]

    return {
        "seed": seed,
        "algorithm": ALGORITHM,
        "direction_id": direction["id"],
        "direction_name": direction["name"],
        "family": direction["family"],
        "knobs": _knobs(direction, seed),
        "filters": {"domain": domain or None, "excluded": excluded},
        "wild": bool(wild),
    }


def roll(seed, domain=None, wild=False):
    """Draw the direction card for ``seed`` from the default catalog.

    ``domain`` prunes directions incompatible with the declared domain before
    the modulo; ``wild`` is recorded verbatim and never changes the draw.
    """
    return draw_card(load_catalog(), seed, domain, wild)


def new_seed():
    """Return a fresh ``adjective-noun`` slug (lowercase, ASCII, 1024 options)."""
    return "%s-%s" % (_SYSTEM_RANDOM.choice(ADJECTIVES), _SYSTEM_RANDOM.choice(NOUNS))


def dumps(card):
    """Canonical JSON: sorted keys, compact separators (parity with roll.mjs)."""
    return json.dumps(card, sort_keys=True, separators=(",", ":"))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Roll a deterministic design direction card from a seed.",
    )
    parser.add_argument("--seed", help="seed string (generated when omitted)")
    parser.add_argument("--domain", help="declared domain; prunes incompatible directions")
    parser.add_argument("--wild", action="store_true", help="record the wild variant")
    parser.add_argument("--out", help="also write the card JSON to this path")
    parser.add_argument("--catalog", help="path to directions.md (defaults to the repo copy)")
    args = parser.parse_args(argv)

    seed = args.seed
    if not seed:
        seed = new_seed()
        print("seed: %s" % seed, file=sys.stderr)

    try:
        card = draw_card(load_catalog(args.catalog), seed, args.domain, args.wild)
    except ValueError as error:
        parser.error(str(error))  # exits 2 with the message on stderr

    text = dumps(card)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
