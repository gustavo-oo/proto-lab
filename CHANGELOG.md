# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-10-28

### Added

- Fit mode (`--fit <source>`): capture an existing product's visual system as
  the direction instead of drawing one of the 22. `references/fit-mode.md`
  defines the style-snapshot schema, the `observed`/`declared`/`inferred`
  evidence levels, the extraction protocol, the FIT card, the
  generation/judge/handoff rules, caps and degradation.
- `scripts/snapshot.py`: deterministic capture from CSS/token sources or
  authored `--extra`, schema validation, sha256 hashing and `--check`,
  inherited-slop baseline via `check_slop.py`, and `--card` FIT-card emission.
- `style-snapshot.json` in the session tree (fit mode only), with `tokens`,
  `type`, `components`, `layout`, `voice`, `constraints`, `extensions`,
  `inherited_slop`, `gaps` and a stable hash.

### Changed

- `SKILL.md`: two modes (explore default, fit opt-in), the `--fit` flag, the
  step-2 capture branch, the step-3 snapshot gate, per-variant snapshot
  inheritance, snapshot-fidelity judging, the fit handoff and a mode-scoped
  inviolable rule 1.
- `README.md`: fit-mode entry point, cost lever and requirements.
- `references/judge-rubric.md` and `references/handoff-format.md`: fit-mode
  evidence, inherited-vs-new slop, and `origin: reused | new | extension`.
- `docs/roadmap.md`: fit-mode extraction gaps (Tailwind/styled components,
  scripted URL capture, multi-theme snapshots, automatic component extraction).

## [0.4.0] - 2026-10-28

### Added

- UX-law reference (`references/ux-laws.md`): a curated U01-U11 checklist for
  the laws that can be judged on a static screen. Each rule names its law, links
  the source, states the check, failure signal, severity and a "not a hard rule"
  caveat.
- `tests/test_docs_ux.py`: doc-contract tests for the reference, its caveats,
  component table, judge checklist and licensing.
- UX-law literals and report-template coverage in `tests/test_skill_md.py` and
  `tests/test_docs_judge.py`.

### Changed

- `SKILL.md`, `references/judge-rubric.md` and `README.md` wire the checklist
  into generation and the `strangeness` axis. The judge cites `U01-U11` and
  records `N/A` for inapplicable laws; the five-axis contract is unchanged.
- The bundled example's judge report records a UX-law pass for the list/table,
  card grid, feed and detail views. U01/U09/U11 are N/A; U02-U08 and U10 pass.

## [0.3.0] - 2026-10-28

### Added

- Copy contract (`references/copy-contract.md`): zero-tolerance C01-C04 rules
  against item-count labels, repeated facts, filler copy, and separator glyphs
  in product copy. Copy findings are reported separately from the visual
  fingerprint cluster.
- `scripts/check_copy.py`: mechanical C01 and C04 scan, run once per product
  page; C02 and C03 stay judge-only.
- Copy fixtures under `tests/fixtures/copy/` and `tests/test_check_copy.py`,
  covering the clean page, item counts, separator soup and the precision
  guards (dates, ratios, ranges, units, data fields, session chrome).

### Changed

- `SKILL.md`, `references/judge-rubric.md`, `references/slop-fingerprints.md`
  and `README.md` wire the copy gate into generation and the `slop-scan` axis;
  any unresolved C01-C04 finding fails `slop-scan` regardless of the visual
  hit count.
- `assets/variant-shell.html` and the example's product pages mark session
  chrome with `data-session-chrome`, so the checker and judge skip the variant
  label and title block.
- The bundled example's product copy replaces separator glyphs with grammar or
  structure, removes the `10 registros` and `10 pranchas` count labels, and
  records the copy pass in its judge report.

### Fixed

- The example no longer labels a list with a count (C01) or joins metadata with
  `·` and `—` (C04).

## [0.2.0] - 2026-10-28

### Removed

- The benchmark harness is gone: `benchmarks/` (suite v1, metrics rubric,
  `compare.py`), its fabricated fixtures (`tests/fixtures/bench/`) and
  `tests/test_compare.py`. Measuring every release cost more tokens than it
  returned, and no baseline was ever recorded. `CHANGELOG.md` remains the
  "what changed" record and `docs/roadmap.md` the open-gap record.
- The benchmark scenario examples (`benchmarks/suite/scenarios/`). Example
  sessions are created only when the user asks for them.

### Changed

- `README.md` no longer points at `benchmarks/README.md`; `tests/test_readme.py`
  and `tests/test_version.py` drop the benchmark references, and the roadmap
  loses the baseline gap.

## [0.1.1] - 2026-10-28

Corrective release from the T27 adversarial hunt and the final whole-branch
review. No pipeline output changes shape: the guidance is tighter where a guard
could silently do nothing, the scaffolder stops overwriting captured input, and
the README points at the open-gap roadmap.

### Fixed

- Scaffolder: `brief.md` gets the `# Brief` header only when absent, and no
  existing scaffolded file is rewritten — step 1's captured brief survives
  step 3, and a started artifact is never clobbered by a rerun.
- Slop scan is documented as **one invocation per generated page**; a
  multi-path call sums hits and is not a per-page verdict (the example report
  now records the per-file counts).
- Pipeline commands are relative to the skill directory, and
  `scaffold.py --target` is documented as `<project>/prototypes` (the parent),
  with a copy-pasteable roll → scaffold sequence.
- `--wild` is documented as experimental/not wired (it only records the flag);
  the gallery drops the token-injection promise and keeps deliberate neutral
  chrome. The example's `lang` attributes are `pt-BR`.
- Judge rubric: the cap now stops the loop and presents the open failures with
  `NOT judge-verified`; the report template carries the `fresh-eyes
  independence` and `judge status` provenance lines.
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
