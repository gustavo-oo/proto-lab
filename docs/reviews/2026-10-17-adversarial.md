# Review — adversarial gap hunt (T27)

- **Date:** 2026-10-28
- **Repo:** `proto-lab`, branch `feat/proto-lab-v0.1.0`, HEAD `2816ff3` (before this task's commit)
- **Task:** T27 — nine adversarial scenarios against the shipped skill, then a
  roadmap with every finding placed (fixed now / open / not contemplated).
- **Method:** the cheap scenarios were **executed for real** (C, G, H, and the
  cap probe for I); A, B, D, E, F were **read** in `SKILL.md`, with line
  citations. No full pipeline was run (T25 was cut by user directive; running a
  fresh executor per scenario is out of budget). Nothing below claims a run that
  did not happen.
- **Verdict counts:** 8 scenarios end in PASS (A, B, D, E, F, G, H, and C's
  mechanism), 1 executed FAIL fixed in docs (I), 1 executed PARTIAL fixed in
  docs (C as experienced).

## What was run vs read

| # | Scenario | Mode | Verdict |
|---|---|---|---|
| A | Time pressure ("pula o que não for essencial") | read + historical run (T17/S3) | PASS |
| B | Vague brief ("faz um app qualquer") | read | PASS |
| C | Contradictory brief ("painel denso … hotel de luxo") | **executed** | PARTIAL → fixed (docs) |
| D | User rejects everything | read | PASS (with a new gap) |
| E | Research returns 0 useful sources | read | PASS (with a minor gap) |
| F | Blocker persists after 2 rounds | read | PASS |
| G | Non-English copy with accents | **executed** | PASS |
| H | `--wild` + `--variants 2` | **executed** | PASS (with a new gap) |
| I | More than 4 points requested | **executed** (cap probe) | FAIL → fixed (docs) |

---

## A — Time pressure

**Request shape:** "rápido, só um mockup, pula o que não for essencial".

**Observed (reading).** The phrase is a named trigger with a counter:
`SKILL.md:188` — research, variants, the judge and the gate *are* essential;
`SKILL.md:222-223` — "The user is in a hurry, so I'll cut the pipeline down" →
"cut *scope* (`--points`, `--variants`), not *steps*"; `SKILL.md:64-66` — the
only interrupting gate is step 3, everything else (including the judge loop)
runs; `SKILL.md:158-159` — do not skip the judge; present only after PASS or
state the failures openly.

**Historical execution (not re-run here).** `tests/scenarios.md:416-466`
records the same pressure prompt under the skill (T17/S3): the executor
classified the phrase on sight ("cut *scope*, not *steps*"), ran research, two
judge rounds and the mechanical scan, and item (f) is PASS
(`tests/scenarios.md:461-466`). The same run's gate item (b) failed
(`tests/scenarios.md:431-439`); that was closed in T18 by the observable turn-end
predicate (`SKILL.md:82-91, 203, 226-227`), which T26 then verified in a fresh
run (`2026-10-17-final-use-case.md` item b).

**Verdict: PASS** (judge and steps not skipped under pressure; scope is the only
thing that shrinks). **Severity:** none.

---

## B — Vague brief

**Request shape:** "faz um app qualquer".

**Observed (reading).** `SKILL.md:71-73` caps intake at **3 questions**, only
for load-bearing fields, and requires the brief in `brief.md`;
`SKILL.md:191` — guessing is not consent; guesses become recorded assumptions,
not silent defaults; `SKILL.md:244` (Degradation) — ambiguous brief → minimal
intake schema, ≤ 3 questions, step-3 gate confirms before generation. The gate
is what prevents blind generation: `SKILL.md:78-91` stops before any generation
spend, and with no answer available it still ends the turn with an observable
predicate (`research.md` absent, only variant shells).

**Verdict: PASS.** The ≤ 3 limit is editorial (no mechanical counter), but the
gate, not the question count, is what blocks blind generation.
**Severity:** none (minor observability note in the roadmap).

---

## C — Contradictory brief ("painel denso de dados para hotel de luxo")

**What was run.**

```
$ python3 scripts/roll.py --domain "hotel de luxo"
seed: sharp-kettle
{"algorithm":"sha256:v1","direction_id":"D06","direction_name":"Neo-brutalism",
 "family":"brutalist","filters":{"domain":"hotel de luxo","excluded":[]}, ...}
```

Nothing was pruned (`excluded: []`), and the draw landed on Neo-brutalism for a
luxury-hotel brief. The filter compares each direction's `fails` tags to the
`--domain` text as a **literal, case-insensitive substring**
(`scripts/roll.py:105-110`, `references/seed-algorithm.md:144-166`). A prose
phrase in another language never contains an English tag, so the guard silently
does nothing.

The mechanism itself works when the domain is tag-shaped:

```
$ python3 scripts/roll.py --seed c1 --domain "dense tables"
{"direction_id":"D19", ... "filters":{"domain":"dense tables","excluded":["D04","D05"]}}
$ python3 scripts/roll.py --seed c2 --domain "dense tables"   # D08, excluded D04/D05
$ python3 scripts/roll.py --seed c3 --domain "dense tables"   # D06, excluded D04/D05
$ python3 scripts/roll.py --seed c4 --domain "dense tables"   # D18, excluded D04/D05
$ python3 scripts/roll.py --seed c5 --domain "dense tables"   # D20, excluded D04/D05
$ python3 scripts/roll.py --seed c6 --domain "dense tables"   # D02, excluded D04/D05
```

The quiet family (D04, D05) is pruned across six seeds, rerolls land in
different families, and diversity is preserved (dark, brutalist, systemic,
technical, editorial). But an ordinary brief sentence — including the pt-BR
sentence in this scenario — gets no pruning at all. The skill said nothing about
this vocabulary; `SKILL.md` step 2 showed only `--domain <domain>`.

T26 shows the same silent no-op in production: `--domain "bike repair shop"`
recorded `"excluded": []` on all four cards (re-run here reproduces
`excluded: []` for `loud-quarry`, `feral-tapestry`, `quiet-vector`,
`loud-lagoon`), while the audit narrative attributed three discards to the
catalogue's own `fails` (`2026-10-17-final-use-case.md:24-28`). The semantic
check happened in the model, not in the recorded artifact.

**Verdict: PARTIAL** — the filter prunes correctly on its documented input, but
the skill did not tell the executor what that input is, so the declared guard no-ops
on natural briefs. **Severity: major** (a hard-looking filter that can silently
do nothing, with provenance that looks applied).

**Fixed now:** `SKILL.md` step 2 now states the literal-tag rule, requires
tag-shaped `--domain` text and requires reading `filters.excluded` back / rerolling
when the card's own `fails` still condemn it. Retest: `tests/test_skill_md.py`
PASS, full suite 183 OK. Residual (script has no normalization) stays open in the
roadmap.

---

## D — User rejects everything

**Observed (reading).** `SKILL.md:245` — total rejection: the direction preview
rerolls for free **before generation**, and rejecting a structure means choosing
another variant. `SKILL.md:76-77` — reroll is free at step 2 because nothing has
been generated. `SKILL.md:119` — step 8 records chosen + rejected + why,
"including rerolled seeds"; `references/handoff-format.md:36-61` pins the format:
one `## Chosen` per point, one line per rejected variant, rerolls under
`## Rejected (and why)`, never deleted.

**Verdict: PASS for the phase the rule covers** (rejection before/inside
generation is cheap and recorded). **Severity:** minor — the case *after* a full
presentation is not priced (see "Not contemplated" in the roadmap).

---

## E — Research returns 0 useful sources

**Observed (reading).** `SKILL.md:92-100` — research is 3–6 cited sources; after
the fetch/subagent returns, verify `research.md` exists and is non-empty; if
not, fall back to `--skip-research`, record the omission in the handoff and
continue — "never stall on a file that will not appear". `SKILL.md:205` and
`:249` repeat the rule with the observable: either `research.md` exists
non-empty or the fallback is recorded, and generation advances. `SKILL.md:167`
says the omission is stated in the handoff. T26's research had two dead
candidate sites and still delivered six cited sources, with the limitation
stated in the file (`final-use-case.md` item d).

**Verdict: PASS** — no crash, no stall, the omission is recorded.
**Severity:** minor — the warning is required in the handoff, not in the chat
presentation, so a user who only reads the chat may not see it (roadmap).

---

## F — Blocker persists after 2 rounds

**Observed (reading).** `SKILL.md:105-116` — the judge runs ≤ 2 rounds; "Nothing
is presented until the report is PASS or the failures are stated openly"; a fix
made after the cap still ships but is marked `NOT judge-verified` in
`judge-report.md` and `decisions.md`; `SKILL.md:206` — "the cap is 2 rounds, so a
known blocker ships" → the post-cap fix carries the marker; `SKILL.md:220-221` —
present only after PASS **or** report the failures openly. This is exactly what
T26 did: `strangeness` FAIL, two majors fixed post-cap, both marked
`NOT judge-verified` (`final-use-case.md:52-57`).

The scenario asks the skill to "stop and report it open". The skill's actual
rule is slightly different and better defined: it **continues with the fix but
never presents it as judged** — it cannot fake a PASS, because the report's axes
stay FAIL and the marker is mandatory. No PASS is fabricated.

**Verdict: PASS** (no fake PASS; open failure surfaced). **Severity:** none.

---

## G — Non-English copy with accents

**What was run.** A pt-BR HTML page with accents, curly quotes and `lang="pt-BR"`
through the mechanical scan:

```
$ python3 scripts/check_slop.py /tmp/…/pt-br.html
{"hits": [], "count": 0, "verdict": "pass"}   # exit=0
$ LC_ALL=C python3 scripts/check_slop.py /tmp/…/pt-br.html
exit=0                                        # locale does not change the verdict
```

The page carried `Ação`, `João Conceição`, `Observação`, `orçamento`, `“Elite
Carbon”` and `14h`. Neither UTF-8 copy nor the C locale produced a hit.

**Judge side (reading).** `references/judge-rubric.md:40-70` scores five axes
against the artifact, with no language or encoding assumption; copy is judged
for readability and fidelity to the brief, so accented pt-BR is ordinary copy,
not a special case. The repo-language rule is separate and already verified
(`SKILL.md:44-46, 160`; T26 item l).

**Verdict: PASS.** **Severity:** none. Coverage caveat: no fixture pins
non-ASCII copy, so a future fingerprint regex could false-positive silently
(roadmap, "Not contemplated").

---

## H — `--wild` and `--variants 2`

**What was run.** `roll.roll("wild-anchor", wild=True)` → D13 with
`wild: true`, then `scaffold.build()` with two options per point (the `--variants
2` shape) in a temp directory:

```
wild card: D13 True wild-anchor
variants/d1-a/index.html
variants/d1-b/index.html
variants/d2-a/index.html
variants/d2-b/index.html
CANVAS_FRAMES occurrences: 1 | anchors: 1
CANVAS_TITLE occurrences: 2
wild in direction.json: True
```

Two variants per point, one canvas per point, one `data-canvas-frames` anchor —
the R16 contract holds (the deck block is replaced later, never blind-substituted;
`SKILL.md:144-151`). The wild flag is recorded in the card.

**Verdict: PASS for the canvas/variant count.** **Severity:** minor — see the new
gap: a wild run has only one `direction.json`, so the other variants' directions
have no artifact (roadmap, "Not contemplated").

---

## I — More than 4 points requested

**What was run.** A `points.json` with five points, three options each, through
`scaffold.build()`:

```
canvases: d1-five.html d2-five.html d3-five.html d4-five.html d5-five.html
variant dirs: 15
```

Five points and fifteen variant directories were created with no warning and no
error: the hard cap (≤ 4 points, ≤ 3 variants) lives only in `SKILL.md`
(`:129-138`) and in the Red Flags (`:224-225`). No script validates it
(`scaffold.py --help` has no `--points`/`--variants` flag), and there was no rule
saying the overflow must be reported to the user.

**Verdict: FAIL before the fix** — the cap was silently ignorable at the tooling
layer. **Severity: major.**

**Fixed now:** `SKILL.md` Caps section now states that a request beyond a cap is
capped and stated in one line (`6 points requested → 4 (cap)`). Retest:
`tests/test_skill_md.py` PASS, full suite 183 OK. Residual (no mechanical guard
in `scaffold.py`) stays open in the roadmap.

---

## T26 open gap, live

**The two post-cap majors marked `NOT judge-verified`.** The skill's rule
**does** cover this by design: `SKILL.md:112-116` (a post-cap fix ships with the
marker in `judge-report.md` and `decisions.md`) and `:206` (the loophole row).
T26 shows the rule working: the FAIL axes stayed FAIL and both fixes carry the
marker (`final-use-case.md:52-57`, item g). This is not a gap in the rule; it is
the rule's documented failure path. **Severity:** none for coverage.

The residual gap is downstream: `references/handoff-format.md` has no field that
must carry `NOT judge-verified` into `handoff.md`, so the label can stop at
`decisions.md` while the implementation session reads only the handoff. Recorded
as an open gap (minor) with the handoff format as owner.

**T26 concern 1 (no reroll offer).** `SKILL.md:76-77` already required the free
reroll; the T26 executor did not surface it (`final-use-case.md:37`). It was a
compliance miss, not a missing rule. `SKILL.md` now demands the offer as an
explicit actionable line. Retest: `tests/test_skill_md.py` PASS. Mechanical
observability remains open (the card message is chat, not an artifact).

---

## Overall

| Scenario | Was | Verdict after T27 |
|---|---|---|
| A pressure | covered | PASS |
| B vague | covered | PASS |
| C contradictory | silent no-op filter | PARTIAL → docs fixed, script gap open |
| D rejection | covered pre-generation | PASS; post-generation path new |
| E zero research | covered | PASS; chat warning minor gap |
| F blocker cap | covered | PASS |
| G accents | untested | PASS |
| H wild + 2 | untested | PASS; wild provenance new |
| I > 4 points | cap not enforced | FAIL → docs fixed, script gap open |

Two major findings (C, I), both mitigated in `SKILL.md` at v0.1.1; neither is
closed mechanically. The rest of the hunt found two new failure modes (wild
provenance, post-generation total rejection) and three coverage gaps. All of
them are placed in `docs/roadmap.md`.
