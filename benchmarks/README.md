# Benchmarks — comparable history of the skill

The benchmark answers one question: **did the skill get better or worse?**
It is not a demo and not a test suite. It is a frozen suite of scenarios run
against every released version, scored with one rubric, and compared with the
previous version.

The rule the whole directory exists for:

> **"what changed" = `CHANGELOG.md`. "how it changed" = `compare.py`.**

Read them in that order. `CHANGELOG.md` says what was touched; the comparison
run says whether the measured behavior moved — including regressions.

---

## Layout

```
benchmarks/
  README.md                  this protocol
  compare.py                 snapshot A vs snapshot B (stdlib, py >= 3.8)
  suite/
    suite.json               suite_version + scenarios + metric registry
    rubric.md                scoring contract (all metric definitions)
    scenarios/s01..s05-*.md  frozen prompts (the benchmark input)
  results/<version>/         one directory per measured skill version
    env.json                 version, commit, suite_version, model, harness, date
    summary.json             {"suite_version", "scenarios": {id: {metric: value}}}
                             (multi-run scenarios: the worst run per metric)
    summary.md               readable table + "## Changes since previous"
    <scenario>/               evidence: direction.json, judge-report.md,
                             slop.txt, nav.md, gate.md, screenshots (cited)
```

`suite/` is the fixed measuring instrument. `results/` is the measurement.
Never edit a scenario prompt or a seed to make a run look better — that is a
new instrument, i.e. a new `suite_version`.

## Suite v1

| id | scenario | fixed seed(s) | points | variants | research |
|---|---|---|---|---|---|
| s01 | Movies dashboard | `s01-anchor` | 3 | 3 | on |
| s02 | Habits onboarding | `s02-anchor` | 2 | 3 | on |
| s03 | Checkout under pressure | `s03-anchor` | 2 | 2 | on |
| s04 | Seed divergence | `s04-a`, `s04-b`, `s04-c` | 2 | 3 | on |
| s05 | Dense enterprise domain | `s05-anchor` | 4 | 3 | on |

`suite.json` is the machine-readable source (prompts, seeds, config, expected
artifacts, check focus); `prompt_file` paths are relative to
`benchmarks/suite/`. `rubric.md` defines the ten metrics and how each is
scored.

### Fixed seeds — the comparability rule

**Seeds in the suite are fixed.** Same version or different version, a
scenario is always run with the seed written in `suite.json` (`--seed`).

Random-seed exploration (`--seed` omitted, or a reroll to dodge a `fits/fails`
condemnation) belongs to the **reviews** (e.g. plan Task 26/27), never to the
benchmark. A benchmark that rerolls measures luck, not the skill. If a fixed
seed is condemned by the catalogue's `fits/fails` filter, that is a **finding
to record** (`summary.md`), not a reason to change the suite.

### Multi-run scenarios — the aggregation rule

s04 declares **three** seeds, i.e. three runs, but `summary.json` has **one
slot per scenario × metric**. Every such slot holds the **worst run per
metric**: `min` for higher-is-better, `max` for lower-is-better, logical
`AND` for booleans (`file_nav_ok`). The single exception is
`distinct_directions`, which is the **distinct count** across the run set
(1–3). Full table in `rubric.md` §"Multi-run scenarios — the aggregation rule".

So s04's scalars describe its **weakest run** (except `distinct_directions`):
a strong run cannot hide a weak one. Per-run detail — each seed's metrics, its
`direction.json`, the distinctness note — lives in
`benchmarks/results/<version>/s04/`, never in the summary slot. Changing the
rule is changing the instrument: bump `suite_version`.

## Metrics (full definitions in `rubric.md`)

| metric | type | better | meaning |
|---|---|---|---|
| `gate_checklist_pass` | 0–1 | higher | the 12 pipeline items (a)–(l), verified/partial/absent |
| `structural_divergence` | 0–3 | higher | variants diverge structurally, not cosmetically |
| `slop_hits` | int | lower | `check_slop.py` fingerprints in the **worst page** (max per page; ≥ 4 = reprova) |
| `judge_axes_pass` | 0–5 | higher | judge axes PASS in the final report |
| `fix_rounds` | 0–2 | lower | corrective rounds after the judge (defect-repair cost) |
| `artifacts_complete` | 0–1 | higher | expected artifacts present |
| `research_sources` | int | higher | distinct cited URLs (cap 6) |
| `file_nav_ok` | bool | higher | `file://` gallery→canvas→variant→back clicked |
| `html_bytes_total` | int | lower | HTML bytes in the session (cost proxy) |
| `distinct_directions` | int | higher | distinct directions across s04's three seeds |

`gate_checklist_pass` is the audit checklist of plan Task 26 Step 2, items
(a)–(l), reproduced in `rubric.md` with the observable that decides each
item.

## Running a version (the ritual)

1. **Change + test** the skill. CI green before spending benchmark money.
2. **Bump `VERSION`** (semver) and add the `CHANGELOG.md` entry — *what
   changed*.
3. **Run the suite** and store `benchmarks/results/<version>/`:
   - one **fresh executor per scenario** (new session, skill installed from
     this repo at this version; no memory of an earlier run);
   - prompt **verbatim** from the scenario file, seed(s) and config from
     `suite.json`;
   - run the pipeline through the handoff (s03 may defer the pick-dependent
     trio, recorded as pending);
   - score with `rubric.md` using a fresh auditor, cite evidence per scenario;
   - for a multi-run scenario (s04), keep the three per-seed records in
     `results/<version>/s04/` and write the **aggregated worst run** into the
     scenario's `summary.json` slot (rule above and in `rubric.md`);
   - fill `env.json` (`version`, `commit` = `git rev-parse HEAD`,
     `suite_version`, `model`, `harness`, `date`), `summary.json` and
     `summary.md`.
4. **Compare** with the previous version and paste the output into
   `summary.md` under `## Changes since previous` — *how it changed*:

   ```bash
   python3 benchmarks/compare.py benchmarks/results/<previous> benchmarks/results/<new>
   ```

5. **Commit** (`test: benchmark <version>` or the release commit).

A version measured on a subset of scenarios is fine (e.g. a corrective release
that only touches s03): the comparator reports the untouched scenarios as
`n/a` instead of inventing a value.

## `compare.py`

```bash
python3 benchmarks/compare.py <results-A> <results-B> [--strict] [--json]
```

- Prints an **env diff** first: `version`, `commit`, `suite_version`, `model`,
  `harness`, `date`.
- Then a **per-scenario × per-metric delta table**: value in A, value in B,
  delta (B − A) and a verdict. Booleans count as 1/0 for the delta.
- `⚠` marks a **regression** (the metric moved in its worse direction, as
  declared in `rubric.md`). Improvements read `improved`; unchanged rows are
  blank.
- A metric present on only one side is `n/a` (`not comparable`) — never
  silently "same", never a regression.
- Exit codes: `0` compared (regressions still exit 0 — the `⚠` is the signal);
  `1` compared with `--strict` and at least one regression; `2` refused
  (different suites, unreadable snapshot, bad usage).

Example verdict lines:

```
env diff (A → B)
  version:      0.1.0 → 0.1.1
  model:        harness-model-A (unchanged)
  harness:      opencode/cli (unchanged)
  → model/harness unchanged — apples-to-apples

scenario  metric                    A             B             delta       flag
s01       gate_checklist_pass       0.833         1.000         +0.167      improved
s02       slop_hits                 1             4             +3          ⚠ regression
s04       file_nav_ok               true          —             n/a         not comparable (missing in B)
```

### Different suites → refused

`suite.json` carries a `suite_version`. If the two snapshots were recorded
under different suite versions the comparator refuses the comparison:

```
⚠ suite_version mismatch: A=v1 B=v2 — suites diferentes, comparação recusada
```

and exits `2`. Bump `suite_version` **only** when the instrument changed
(prompt, seed, config, expected artifacts, metric definition or range). Re-run
the new version on the same suite as the baseline to get a comparison.

### Different model/harness → not apples-to-apples

`env.json` records who executed the run. If `model` or `harness` differ, the
comparator prints `⚠ model/harness differ — não apples-to-apples`: the deltas
still show, but they mix two executors and cannot be attributed to the skill
alone. Re-run the baseline on the new executor before drawing conclusions, or
mark the comparison as indicative in `summary.md`.

## Sanity commands

```bash
python3 -m unittest discover -s tests -v
node --test tests/node/roll_parity.test.mjs
```

(The directory form `node --test tests/node/` fails on Node v22.21.1 with
"Cannot find module"; use the file form or plain `node --test`.)
