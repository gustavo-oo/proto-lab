# Roadmap — what is fixed, what is open, what is not covered

Line references are to `SKILL.md` at v0.1.1.

**Current version: 0.1.1** (`VERSION`, `CHANGELOG.md`). The corrective release
only changes `SKILL.md` wording (domain-filter vocabulary, cap message, explicit
reroll offer), the `README.md` pointer and the version/changelog/test constants.

**No benchmark baseline exists.** T25 (the v0.1.0 benchmark run) was **cut by
user directive**, so `benchmarks/results/` is absent and no v0.1.1 result may be
invented. The harness is ready for the next release: suite v1, fixed seeds and
`benchmarks/compare.py` (`benchmarks/README.md`). The first measured version
must record `benchmarks/results/<version>/` and paste the real `compare.py`
output into its `summary.md`; until then there is no "how it changed" claim.

This file is the single place where a finding from the adversarial hunt (T27,
`docs/reviews/2026-10-17-adversarial.md`) lands. Nothing is dropped silently:
each finding appears below, and a finding may have a fixed part and an open
residual (C and I do) rather than sitting in exactly one state.

## Fixed now

Each entry names the retest that was actually run for this release.

| # | Fix | File | Retest |
|---|---|---|---|
| 1 | **Domain filter vocabulary.** Step 2 now states that `--domain` matches the catalogue's literal `fails` tags (case-insensitive substring), that tag-shaped text is required (prose/other languages prune nothing), and that `filters.excluded` must be read back and the card rerolled if the catalogue entry's `fails` still condemn it. | `SKILL.md` (step 2) | `tests.test_skill_md :: test_required_literals_are_present` asserts **literal `fails` tags**, **filters.excluded** and the **catalogue entry's `fails`** phrase; 14 tests OK, full suite 183 OK |
| 2 | **Cap message.** A request beyond a cap is now capped and stated in one line (`6 points requested → 4 (cap)`); cutting scope stays allowed, cutting a step does not. | `SKILL.md` (Caps) | `tests.test_skill_md :: test_required_literals_are_present` asserts **6 points requested → 4 (cap)**; full suite 183 OK |
| 3 | **Reroll offer made observable in the card message.** Step 2 now requires an explicit actionable line ("reroll is free — say the word"), not just an internal option — the T26 item (a) miss. | `SKILL.md` (step 2) | `tests.test_skill_md :: test_required_literals_are_present` asserts **reroll is free — say the word**; full suite 183 OK |
| 4 | **README points at this roadmap** (the step-4 requirement) as the third sibling document next to `CHANGELOG.md` and `benchmarks/README.md`. | `README.md` | `tests.test_readme :: test_prose_only_references_are_cited_not_checked` asserts **docs/roadmap.md**; 10 tests OK, full suite 183 OK |
| 5 | **Corrective version 0.1.1** with a `### Fixed` changelog entry; the version test constants follow the shipped version. | `VERSION`, `CHANGELOG.md`, `tests/test_version.py` | `tests.test_version :: test_changelog_follows_keep_a_changelog` asserts **### Fixed** inside the `[0.1.1]` section; 3 tests OK, full suite 183 OK |

Behaviour retests for the fixes from the review (not new suite tests):

- C: `python3 scripts/roll.py --domain "hotel de luxo"` still records
  `excluded: []` — the **script** was deliberately not changed; the skill now
  tells the executor to pass `--domain "dense tables hotel dashboard"` and to
  read `excluded` back. `--domain "dense tables"` prunes `D04`/`D05` across six
  seeds (review §C).
- I: the five-point scaffold probe still builds 5 canvases / 15 variants; the
  **skill** now caps and states it. The mechanical guard is open gap 2.

## Open gaps

| # | Severity | Finding | Evidence | Suggested fix | Owner |
|---|---|---|---|---|---|
| 1 | **Major** (mitigated by docs, not closed) | Domain filter is a literal substring match on English `fails` tags; a natural-language or pt-BR domain silently prunes nothing while the card records `excluded: []`. | `roll.py --domain "hotel de luxo"` → `excluded: []`; T26's `--domain "bike repair shop"` → `excluded: []` on four cards, while the audit attributed three discards to `fails` (`2026-10-17-final-use-case.md:24-28`). | Normalize the domain (tag aliases + pt-BR equivalents), accept an explicit `--domain-tags`, or warn when a non-empty domain prunes nothing. Changing the draw is a determinism change → new tests. | `scripts/roll.py`, `references/seed-algorithm.md`, `tests/test_roll.py` |
| 2 | **Major** | The hard caps are not enforced by any script: `scaffold.py` happily builds 5 points and 15 variant dirs; nothing rejects or truncates. | Five-point probe: `canvases: d1-five … d5-five`, `variant dirs: 15`; `scaffold.py --help` has no `--points`/`--variants`. | Validate in `scaffold.py` (points ≤ 4; options 2–3) and exit with one clear message; add the boundary test. | `scripts/scaffold.py`, `tests/test_scaffold.py` |
| 3 | Minor | A research omission is recorded in the handoff but not required in the chat presentation; a user reading only the chat may miss that research was skipped. | `SKILL.md:103-104, 177, 215, 226, 259` — "record the omission in the handoff"; no presentation rule. | Require one line in the step-7 summary ("research: off — fallback recorded"). | `SKILL.md` (step 4/7) |
| 4 | Minor | The `NOT judge-verified` marker does not have to travel into `handoff.md`, so the implementation session can read the handoff and never see it. | `SKILL.md:118-122` requires it in `judge-report.md` and `decisions.md`; `references/handoff-format.md` has no field for it. | Add a mandatory "judge status" line to the handoff template (carry every marker). | `references/handoff-format.md` |
| 5 | Minor | The reroll offer is now required by wording but still not mechanically observable (it lives in the chat, not an artifact). | T26 item (a) `final-use-case.md:37`; a card message is not part of the session tree. | Add "card message must contain the reroll line" to the review checklist / scenario scoring (not a file artifact). | `tests/scenarios.md`, T26 checklist |
| 6 | **Major (process)** | No benchmark baseline for v0.1.0 and no measured v0.1.1; version-to-version comparability is unproven in practice. | T25 cut by user directive; `benchmarks/results/` does not exist; this task must not fabricate one. | Run suite v1 with a fresh executor per scenario at the next version, store `benchmarks/results/<version>/` and paste real `compare.py` output. | `benchmarks/README.md` protocol, next release |
| 7 | Minor | Install/discovery by a real harness was never exercised; T26 used a copied bundle. | `2026-10-17-final-use-case.md:107-110, 140-144`. | Copy the folder into `~/.config/opencode/skills/` and run one fixed scenario; record discovery in the next review. | next acceptance review |
| 8 | Minor | Canvas frames are 1280px in a padded scroll deck: the right edge needs horizontal scroll at a 1440px window, and "abrir" opens a new tab instead of the same tab. | T26 item (j), observations 1–2 (`final-use-case.md:46`). | Scale frames via CSS clamp/transform to the deck width; offer same-tab open. | `assets/canvas.html` |
| 9 | Minor | Direction DNA can be deviated without escalation: T26 shipped 2–4px radii where D19 asks for 6–10px, logged as a minor and left open. | `2026-10-17-final-use-case.md:45, 137-139`. | Make a declared-DNA deviation a major on axis 4, or require it to be recorded in the handoff as an accepted deviation. | `references/judge-rubric.md` |
| 10 | Minor | Research depth: six text-only sources at the cap, spot-checked, no screenshots. | `2026-10-17-final-use-case.md:117-118, 145-146`. | Require screenshot/UI evidence per source when a browser tool exists; mark text-only runs as degraded. | `references/research-protocol.md` |

## Not contemplated

Failure modes the hunt found that no current rule or test covers.

| # | Severity | Failure mode | Evidence | Suggested fix | Owner |
|---|---|---|---|---|---|
| 1 | **Major** | **`--wild` has no per-variant direction artifact.** `direction.json` is singular and is the source of truth, but wild means each variant rolls its own direction. Nothing says where the other two cards live, so a wild run is not reproducible from the session tree. | H probe: `direction.json` has `wild: true` and one direction (D13) while four variant dirs exist; `SKILL.md:180` states the behaviour but names no artifact. | Specify `direction.json` as a list/an array of per-variant cards for wild runs (or `variants/<id>/**/direction.json`), and make the canvas read them. | `SKILL.md` (step 5), `references/seed-algorithm.md`, `assets/variant-shell.html` |
| 2 | Minor | **Total rejection after generation has no cheap path.** The rules price rerolling only *before* generation; a "reject everything" after presentation silently costs a full regeneration, and there is no recorded policy for what to keep. | `SKILL.md:255` ("rerolls for free before generation"); `SKILL.md:76-78`; nothing covers post-presentation rejection. | Add a degradation row: on total rejection, reroll the seed and reuse `brief.md` + research; record in `decisions.md` what was discarded. | `SKILL.md` (Degradation) |
| 3 | Minor | **`--variants 2` can be silently ignored.** The number of variants is the number of options in the hand-authored `points.json`; the flag binds to no tool, so an executor can author three options under `--variants 2` (or two under the default) with no error. | `scaffold.py --help` (no flag); H probe authored two options by hand, not because a tool enforced it. | Validate options count in `scaffold.py` and/or have `points.json` carry the requested count; make the mismatch an error. | `scripts/scaffold.py`, `SKILL.md` (Flags) |
| 4 | Minor | **Non-ASCII copy has no pinned regression.** Accented pt-BR passes the **mechanical scan** today, but rendering and judging of accented copy were not run (G: scan only), and no fixture protects the scan; a future fingerprint regex or an encoding default could false-positive without any test noticing. | G probe: pt-BR page with accents and curly quotes → `count: 0`, exit 0, also under `LC_ALL=C`; no render, no judge. | Add a non-ASCII pass fixture (and a would-be-hit variant) to `tests/fixtures/slop/`. | `tests/test_check_slop.py`, `tests/fixtures/slop/` |
