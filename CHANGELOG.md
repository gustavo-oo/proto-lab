# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-10-28

Corrective release from the T27 adversarial hunt. No generated artifact changes:
the pipeline guidance is tighter where a guard could silently do nothing, and
the README points at the open-gap roadmap.

### Fixed

- Domain filter vocabulary: `--domain` matches only the catalogue's literal
  `fails` tags, so the skill now requires tag-shaped domain text, reading
  `filters.excluded` back and rerolling a card whose catalogue entry's `fails`
  still condemn it (a prose or pt-BR domain silently pruned nothing).
- Cap overflow: a request beyond ≤ 4 points / ≤ 3 variants is capped and stated
  in one line instead of being silently expanded.
- The free reroll must be offered as an explicit line in the card message
  ("reroll is free — say the word"), not only as an internal option — the T26
  item (a) compliance miss.
- `README.md` now points at `docs/roadmap.md` (fixed now / open gaps / not
  contemplated).

## [0.1.0] - 2026-10-17

First release of the proto-lab skill: a deterministic pipeline that turns a
short brief into structurally distinct HTML UI direction options instead of one
homogenised "AI default" mockup.

### Added

- Direction catalogue (`references/directions.md`): exactly 22 fixed directions
  (D01–D22, closed system) as prose plus a machine-readable JSON block consumed
  by the scripts.
- Seed algorithm (`references/seed-algorithm.md`): deterministic
  `sha256("<seed>:direction:v1")` mapping from a seed to a direction card, with
  no timestamp, so the same seed always yields the same card (`direction.json`
  is the source of truth); embedded word lists generate a seed when none is
  given.
- Decision points (`references/decision-points.md`): taxonomy, derivation rules
  and the `points.json` contract of 2–3 structural options per point.
- Judge rubric (`references/judge-rubric.md`): five axes, finding severities
  (`blocker`/`major`/`minor`), the report template and the fresh-eyes rule.
- Handoff format (`references/handoff-format.md`): templates and conventions for
  `decisions.md`, `tokens.css`, `styleguide.html`, `handoff.md` and `chosen/`.
- Slop fingerprints (`references/slop-fingerprints.md`): 26 fingerprints, the 22
  mechanical ones (R01–R22) mapped to concrete scan rules.
- Research protocol (`references/research-protocol.md`): cited-source rules and
  the observed-vs-inferred distinction.
- `scripts/roll.py`: seed → direction card, with domain filtering.
- `scripts/roll.mjs`: Node mirror of `roll.py` with CLI parity
  (`scripts/roll.mjs`, verified by `tests/node/roll_parity.test.mjs`).
- `scripts/check_slop.py`: mechanical fingerprint scan that fails at the `>= 4`
  hits boundary, with fixtures under `tests/fixtures/slop/`.
- `scripts/scaffold.py`: session directory structure generated from the schemas.
- `scripts/serve.py`: optional local server for browsing a generated session.
- `assets/`: static, build-free templates (gallery, comparison canvas, variant
  shell) that open over `file://`.
- `SKILL.md`: the skill workflow, gates, degraded modes and the rationalisation
  table used to pressure-test the process.
- `examples/coffee-log-cafe-com-leite/`: a full end-to-end example (one decision
  point, three variants, `file://` navigation) that doubles as the quality bar.
- Degradation routes validated in `tests/degradation-notes.md`: offline (font
  fallback stacks preserved), no browser tool (code-first judging), and no Node
  (`roll.py` alone runs the pipeline).
- Acceptance evidence in `tests/acceptance-notes.md` and `tests/scenarios.md`:
  three seeds yield three distinct directions, the same seed is reproducible, and
  GREEN pressure scenarios pass under time pressure.
- `README.md`: the open-source entry point covering install, cost model and the
  demo.
- Standard-library-only Python scripts (>= 3.8), built-in-only Node scripts
  (>= 18), MIT license and a `python3 -m unittest discover -s tests` runner.

### Changed

- Closed the workflow loopholes found in the T18 REFACTOR pass: `SKILL.md`
  rationalisation entries and gate predicates were made observable (counters and
  conditional rules instead of "prefer/consider"), so the judge step can no
  longer be skipped under time pressure.
