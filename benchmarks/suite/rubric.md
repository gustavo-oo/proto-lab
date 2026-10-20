# Benchmark rubric — suite v1

This file is the scoring contract for `benchmarks/suite/suite.json` (suite
`v1`). Every version of the skill is measured with **exactly** these
definitions, so `benchmarks/compare.py` can compare snapshots. Changing a
definition, a prompt, a seed or an expected artifact means bumping
`suite_version` (the comparator refuses cross-suite comparisons).

Two rules govern every judgment below:

1. **Evidence or it did not happen.** Each score cites a file path (or a
   pasted command + exit code) in the scenario's evidence directory. A
   missing artifact is `absent`, never "assumed".
2. **Scoring is done by a fresh auditor**, not by the executor that produced
   the run. The auditor may be an LLM, but it starts from the artifacts, not
   from the executor's summary.

Vocabulary (shared with plan Task 26 Step 2): `verified` / `partial` /
`absent`.

---

## `gate_checklist_pass`

- **Type:** number, **range:** 0–1, **direction:** higher is better.
- **Value:** the 12 items (a)–(l) below scored as `verified = 1`,
  `partial = 0.5`, `absent = 0`, summed and divided by 12, rounded to three
  decimals. `1.000` means every item is verified — only then does the run
  "pass the gate".
- **Evidence:** one row per item in the scenario's `gate.md` (verdict +
  path/quote).

The checklist is the pipeline audit of `SKILL.md` (steps 1–9) applied to the
scored run. Each item names the observable that decides it.

| # | Item | Verified by (observable) |
|---|---|---|
| (a) | Direction card shown with its seed **before** generation, with reroll offered | `direction.json` (seed + direction id) written at step 2 and the chat/card preview precedes the step-5 output; the transcript asks/offers a reroll before the points gate |
| (b) | The points gate was awaited — no generation before an explicit OK | `points.json` exists before `research.md`; a non-interactive run ends its turn with `research.md` absent and `variants/` holding only untouched scaffold skeletons |
| (c) | Structural variants per point (3; 2 only with `--variants 2`), not cosmetic | every point in `points/` has the configured number of variants whose skeletons differ on the declared axis (judge axis 5 agrees) |
| (d) | Research cited: URLs + observed vs inferred | `research.md` has 3–6 sources, each with a URL and an `observed`/`inferred` marker (or the `--skip-research` fallback is recorded in `decisions.md`/handoff) |
| (e) | `check_slop.py` exits 0 | the scanner command and exit code are in the evidence; exit 0 = **every scanned page** is under 4 hits (the scanner is per-page) |
| (f) | `judge-report.md` has the 5 axes **and** `## Open (not fixed)` | all five axes present with PASS/FAIL + evidence; provenance line present (`fresh-eyes …` or `fresh-eyes independence: lost (inline)`); `## Open (not fixed)` section present, even if empty ("none") |
| (g) | Evidence of the correction loop (≥1 fix applied, or "no blocker found") | `judge-report.md` round 2 (or an explicit "no blocker found" statement) + the changed artifact; a post-cap fix carries `NOT judge-verified` |
| (h) | `decisions.md` complete | chosen + rejected per point, with reasons, and every rerolled seed recorded |
| (i) | `tokens.css` + `styleguide.html` + `handoff.md` + `chosen/` present and coherent | all four exist; `tokens.css` values match the chosen direction; `chosen/` holds the picked variants. Scenario s03 may legitimately defer the pick-dependent trio — then `tokens.css` exists and the trio is recorded as pending, and (i) is `verified` only if that pending state is explicit |
| (j) | `file://` navigation clicked: gallery → canvas → variant → back | `nav.md` records the click path and the rendered result of each step, with zero cross-frame script errors |
| (k) | Caps respected: ≤ 4 points, ≤ 3 screens/variant, ≤ 6 sources, ≤ 2 judge rounds (2 variants only via `--variants 2`) | counts read from `points.json`, the variant trees, `research.md` and `judge-report.md` |
| (l) | Response in the user's language | the chat/`brief.md` prose is in the language of the frozen prompt (pt-BR for suite v1); repo docs stay English |

---

## `structural_divergence`

- **Type:** int, **range:** 0–3, **direction:** higher is better.
- **Definition:** how structurally (not cosmetically) the variants of each
  decision point differ on the point's declared axis. One level per run, so
  the scale does not depend on the number of points (1–4).
- **Scale:**
  - `3` — every point's variants differ structurally on the declared axis
    (layout, information architecture, component model or first-read); no two
    variants share a skeleton.
  - `2` — every point diverges, but exactly one documented variant pair shares
    a skeleton with a single structural change (recorded as an exception in
    `judge-report.md`).
  - `1` — at least one point is cosmetic-only: all its variants share the
    skeleton and differ by color/type/spacing.
  - `0` — two or more points are cosmetic-only, or the variants cannot be
    compared (missing/empty files).
- **Evidence:** judge axis 5 (`variant-diversity`) per point + the reviewer's
  own read of `points/<point>.html` frames.

## `slop_hits`

- **Type:** int, **range:** 0+, **direction:** lower is better.
- **Unit:** fingerprints **in the single worst page** — not a session total and
  not a count of pages.
- **Definition:** run `python3 scripts/check_slop.py` over **every generated
  `.html`** in the session (`index.html`, `points/*.html`,
  `variants/**/*.html`, `chosen/**/*.html`, `styleguide.html`) and take the
  **maximum per-page hit count**:

  ```
  slop_hits = max(hits(file) for file in <every generated .html>)
  ```

  `check_slop.py` is a per-page scanner: it counts the fingerprints inside one
  file and exits 1 iff **that file** has ≥ 4 hits. The metric keeps that unit,
  so `0` = no page carries a fingerprint and `3` = the worst page is one hit
  short of failing. This is deliberately **not a session total**: summing the
  pages would make the score a function of session size (twelve pages with one
  hit each would read as 12 and "fail" while the skill's gate passes) and gate
  item (e) would contradict the metric.
- **Gate link:** gate item (e) is `verified` iff `check_slop.py` exits 0 on
  every page, i.e. iff `slop_hits < 4`. A reproved run therefore shows
  `slop_hits ≥ 4` **and** item (e) `absent`; the two can never disagree.
- **Evidence:** one line per scanned file with its hit count and exit code (or
  a tree run plus the per-file counts) in the evidence dir.

## `judge_axes_pass`

- **Type:** int, **range:** 0–5, **direction:** higher is better.
- **Definition:** number of the five judge axes — `brief-fidelity`,
  `strangeness`, `slop-scan`, `direction-fidelity`, `variant-diversity` —
  marked `PASS` in the **final** round of `judge-report.md`. A `FAIL` counts
  0 for that axis even if a later fix landed. Fresh-eyes provenance is audited
  under gate item (f), not folded into this count.
- **Evidence:** the axis table of the final round.

## `fix_rounds`

- **Type:** int, **range:** 0–2, **direction:** lower is better.
- **Definition:** number of corrective rounds *after* the judge in which at
  least one fix was applied and re-judged. `0` = round 1 was clean or "no
  blocker found" was recorded. A post-cap fix (marked `NOT judge-verified`)
  does not increment the count because the cap is ≤ 2. More rounds = more
  defect-repair cost, i.e. worse first-pass quality; judge *activity* is
  visible in `judge_axes_pass`, not here.
- **Evidence:** `judge-report.md` rounds + the changed artifacts.

## `artifacts_complete`

- **Type:** number, **range:** 0–1, **direction:** higher is better.
- **Definition:** present expected artifacts / `len(expected_artifacts)` for
  the scenario, rounded to three decimals. "Present" = the path exists inside
  the session directory (`prototypes/<slug>-<seed>/`); a directory must be
  non-empty. Scored against **that scenario's** list (s03 is deliberately
  shorter: a pressure run may defer the pick-dependent trio).
- **Evidence:** a `find`/`ls` listing of the session dir.

## `research_sources`

- **Type:** int, **range:** 0–6, **direction:** higher is better.
- **Definition:** distinct URLs cited in `research.md`, each with an
  observed-vs-inferred marker. A URL cited twice counts once. `0` is legal
  only when research is off in the scenario config or the `--skip-research`
  fallback was recorded; otherwise it is a gate item (d) failure.
- **Evidence:** `research.md`.

## `file_nav_ok`

- **Type:** bool, **direction:** higher is better (`true` > `false`).
- **Definition:** `true` iff the path gallery (`index.html`) → comparison
  canvas (`points/<point>.html`) → a variant (`variants/…`) → back was
  actually clicked over `file://`, every step rendered, and back returned to
  the origin with zero cross-frame script errors. Not clicked = `false`;
  never assumed `true`.
- **Evidence:** `nav.md` with the click path and what rendered at each step.

## `html_bytes_total`

- **Type:** int, **range:** 0+, **direction:** lower is better (cost proxy).
- **Definition:** sum of `st_size` for every `*.html` under the session
  directory, recursive (gallery, canvases, variants, `chosen/`,
  `styleguide.html`). HTML is the dominant deliverable, so its size is the
  cost proxy. Lower is better **at equal quality**: read it next to the
  quality metrics, and explain any > 20 % jump in `summary.md`; an isolated
  `⚠` here is a flag to inspect, not an automatic veto.
- **Evidence:** `find … -name '*.html' -exec wc -c {} +`.

## `distinct_directions`

- **Type:** int, **range:** 0–3, **direction:** higher is better.
- **Scope:** scenario **s04 only** (three fixed seeds → three runs). Other
  scenarios omit the key, so `compare.py` renders no row for them.
- **Definition:** count of distinct `direction.id` values (D01–D22) across
  the three runs, read from each run's `direction.json`. `3` = three different
  directions. Record the families too (three ids in one family is legal but
  noted); the judge's independent distinctness verdict is quoted alongside.
- **Evidence:** the three `direction.json` files + the distinctness note.

---

## Multi-run scenarios — the aggregation rule

A scenario may declare more than one seed. Suite v1 has exactly one: **s04**
(`s04-a`, `s04-b`, `s04-c` → three independent runs). `summary.json` still has
**one slot per scenario × metric**, so the slot must be filled by a single
explicit rule — otherwise two versions could be scored with different
aggregations and `compare.py` would report a scoring-method delta as a skill
delta.

**Rule: every slot holds the worst run per metric.** Never a mean, never a
sum, never the best run.

| metric | aggregation | why |
|---|---|---|
| `gate_checklist_pass` | **min** | the weakest run's gate coverage |
| `structural_divergence` | **min** | the weakest run's divergence |
| `slop_hits` | **max** | the worst page anywhere in the run set (max per page, then max across runs) |
| `judge_axes_pass` | **min** | the fewest axes passed by any run |
| `fix_rounds` | **max** | the most repair rounds any run needed |
| `artifacts_complete` | **min** | the least complete run |
| `research_sources` | **min** | the thinnest research among the runs |
| `file_nav_ok` | **AND** | `true` only if every run navigated |
| `html_bytes_total` | **max** | the largest run = the worst cost |
| `distinct_directions` | **distinct count** | exception: cross-run by definition (1–3 distinct `direction.id`) |

Rule of thumb: **min for higher-is-better, max for lower-is-better, AND for
booleans**; the single exception is `distinct_directions`, which counts the
distinct `direction.id` values across the run set and cannot be derived from a
single run.

Consequences:

- For a multi-run scenario the scalar describes its **weakest run** (except
  `distinct_directions`), so one strong run cannot hide one weak run.
- **Per-run detail belongs in the per-scenario record**, not in the summary
  slot: `benchmarks/results/<version>/s04/` keeps each seed's metrics, its
  `direction.json` and the distinctness note, and `summary.md` says which run
  was the worst for each metric.
- Two versions are comparable only because both fill the slot with this same
  rule. Changing the rule is changing the instrument → bump `suite_version`.

---

## Producing a snapshot

1. **Fresh executor per scenario** — a new session/agent, skill installed from
   the repository at the version being measured. No memory of earlier
   benchmark runs.
2. **Frozen inputs** — the prompt verbatim from the scenario file, the seed(s)
   from `suite.json`, the `config` (`--points`, `--variants`, research on by
   default). A seed that `fits/fails` condemns is a **finding to record**, not
   a reason to change the suite.
3. **Run to the handoff.** s03 may end with the pick-dependent trio pending
   (recorded, never invented).
4. **Score** with this rubric: gate checklist → metrics → `env.json` →
   `summary.json` + `summary.md`.
5. **Store evidence** per scenario (`benchmarks/results/<version>/<scenario>/`)
   and cite it from `summary.json`.

## What invalidates a comparison

- A different `suite_version` (prompts, seeds, metrics, rubric) → the
  comparator exits 2.
- A different `model`/`harness` in `env.json` → the comparator prints
  `não apples-to-apples`.
- A metric missing on one side → `n/a`, never silently "same".
