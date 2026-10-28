---
name: proto-lab
description: Use when the user wants to explore UI design options, compare structural alternatives for a screen or flow, fit a new screen to an existing visual system, or produce HTML prototypes and mockups before implementation — design first, implement later.
---

# proto-lab

proto-lab turns a rough product idea into a **design direction card**, then into
comparable, judgeable HTML prototypes you can hand off. It exists to stop the
default failure mode: a single page that "looks nice", produced in one shot with
no direction, no options, no critique and no provenance.

## Overview

One session produces, inside the target project:

```
prototypes/<slug>-<seed>/
  index.html          direction card + decision points + links (the "figma")
  direction.json      the direction card: seed, direction, DNA, knobs — source of truth
  style-snapshot.json captured existing system + provenance (fit mode only)
  brief.md            captured brief
  points.json         decision points + contract (axis/options) + choice status
  research.md         competitors/analogues, cited (when research is on)
  points/             comparison canvas per point (3 live frames side by side)
  variants/           one navigable mini-project per variant (d1-a/, d1-b/, …)
  judge-report.md     per-axis verdict + open findings
  decisions.md        chosen + rejected + why (including rerolled seeds)
  tokens.css          core token scales of the chosen direction
  styleguide.html     static mini design system of the chosen direction
  handoff.md          component/state inventory + fidelity notes
  chosen/             copies of the chosen variants
```

## Core principle

**Choose the design before implementing it, and diverge on purpose.** In
**explore** mode (default) a seed selects one direction from a closed catalogue
of 22; in **fit** mode (`--fit`) the visual direction is the captured existing
system in `style-snapshot.json`. Either way, every variant for a point is a
*structural* answer to that point, not a repaint. The direction card
(`direction.json`) is the source of truth — a committed card beats re-deriving
one. The judge is a pre-human gate: nothing reaches the user before it has been
critiqued and corrected. Improvising a direction, skipping the judge, or shipping
one option is a violation of this skill, not a speed-up.

Converse in the user's language; keep repo docs (this file, `references/`) in
English (D10). Artifacts written to the target project follow the user's
language for prose.

## When to Use

- The user wants design options or variants for a screen, flow or feature.
- The user wants HTML prototypes/mockups to react to before implementation.
- The user asks to "make it look better" and the visual direction is unresolved.
- The user is starting a new UI surface and wants a direction picked first.
- The user wants a new screen or flow to belong to an existing product's visual
  system (`--fit`).

## When Not to Use

- The user wants production code written now — this produces prototypes, not an app.
- The task is a copy/behaviour fix on a known, decided design.
- The user wants a pixel-perfect clone of one page — use the real code.
- The user wants a rebrand — fit mode preserves identity; use explore mode.
- The user explicitly wants a single throwaway one-screen sketch — say what gets
  dropped (see **Red Flags**) rather than silently skipping the pipeline.

## Pipeline

Run steps 0–9. **The single gate that interrupts the flow is step 3** (confirming
the decision points). Everything else runs through to the presentation, including
the judge loop.

0. **Setup** — Detect environment: `python3`? `node`? a browser tool
   (agent-browser/Playwright)? subagents? Choose the rich path (script + browser)
   or the degraded one (see **Degradation**).
1. **Brief** — Capture product, audience, goal, key screens, constraints into
   `"$WORK/brief.md"` (the work dir is set below). Ask **at most 3 questions**, only
   for load-bearing fields. If the user asks to fit an existing system, also record
   the source (`--fit <repo path | URL | tokens file>`) in the brief; fit mode is
   opt-in. Pick a seed (random short string, or explicit `--seed`).
   Paths below are relative to **this skill's directory** (`<skill-dir>`); commands
   run from the target project.
2. **Roll** — write the card to a known path:
   `python3 "$SKILL_DIR/scripts/roll.py" --seed "$SEED" --out "$WORK/direction.json" [--domain <domain>] [--catalog <catalog>]`
   (Node mirror: `scripts/roll.mjs`, same flags; API `roll.roll(seed, domain=None, wild=False)`).
   Shows a compact card preview in chat. Rerolling here is free — nothing has been
   generated yet — so the card message must say so as an explicit line the user can act
   on ("reroll is free — say the word"), not only perform it silently. `--wild` is off by
   default and **experimental, not wired**: it only records `wild: true` in the card;
   every variant still uses that one card's direction (see `docs/roadmap.md`).
   `--domain` matches the catalogue's **literal `fails` tags** (case-insensitive
   substring), so pass tag-shaped text (`--domain "dense tables hotel dashboard"`), not a
   prose sentence or another language, or nothing is pruned. Read `filters.excluded` back
   and reroll if the catalogue entry's `fails` still condemn it.
   **Fit mode instead of rolling:** run
   `python3 "$SKILL_DIR/scripts/snapshot.py" --from <source> --extra "$WORK/fit-extra.json"
   --out "$WORK/style-snapshot.json" --card "$WORK/direction.json" --name "<product>"`.
   It extracts CSS custom properties/fonts, merges the authored components/layout/voice,
   validates and hashes the snapshot, and writes the FIT card. A URL source is captured
   through a browser tool into `--extra`; the script never fetches. `--domain` and
   `--wild` are rejected with `--fit`; there is no visual reroll — correct the snapshot
   and re-run `--check` (see `references/fit-mode.md`).
3. **Points** *(the single gate)* — Derive decision points and their named
   structural options into `"$WORK/points.json"` (contract: axis + options). Then create
   the session skeleton with `--target <project>/prototypes` — the scaffolder's target is
   the **parent**, so the session lands at `<project>/prototypes/<slug>-<seed>/`:

   ```bash
   SKILL_DIR=/path/to/proto-lab   # the installed skill folder
   PROJECT=/path/to/project       # target project
   SLUG=task-inbox; SEED=cafe-com-leite
   WORK="${TMPDIR:-/tmp}/proto-lab-$SLUG-$SEED"; mkdir -p "$WORK"
   # step 1: write the captured brief to "$WORK/brief.md"
   python3 "$SKILL_DIR/scripts/roll.py" --seed "$SEED" --out "$WORK/direction.json"
   # step 3: write "$WORK/points.json", then scaffold and copy the brief in:
   python3 "$SKILL_DIR/scripts/scaffold.py" --target "$PROJECT/prototypes" --slug "$SLUG" --card "$WORK/direction.json" --points "$WORK/points.json"
   cp "$WORK/brief.md" "$PROJECT/prototypes/$SLUG-$SEED/brief.md"
   ```

   **Stop and get a quick OK from the user before spending any generation.**
   **Fit mode:** the gate also confirms `style-snapshot.json`; each gap becomes a
   supplied value, an approved `extensions[]` entry, or an accepted out-of-scope note.
   A correction changes the hash, so regenerate `direction.json` before generation.
   **Cannot ask?** A non-interactive harness cancels the question tool — that removes the
   *answer*, not the *gate*. Write the card + `points.json` (and the step-3 `scaffold.py`
   skeleton it names), present them, and **end the turn**; spend no generation — write no
   `research.md` and no generated variant content. Recording the assumptions is not a
   substitute for the gate. Generation starts only once an explicit OK arrives (a human, or
   the operator relaying one).
   *Observable:* the turn ends with `research.md` **absent** (step 4 never started) and the
   `variants/` tree holding **only the scaffold skeletons** — each `variants/<point>-<option>/`
   is just the untouched `index.html` copied from `assets/variant-shell.html`, with no
   generated screens or extra files beyond it.
4. **Research** — 3–6 competitors/analogues of the declared domain into
   `research.md` (good/bad patterns, cited; "observed vs inferred"). On by
   default; `--skip-research` turns it off. Cache the result for reuse.
   **Artifact check:** after the fetch/subagent returns, confirm `research.md` exists and is
   non-empty. If it does not (the subagent reported success but wrote nothing, or the fetch
   failed), **fall back to `--skip-research`**, record the omission in the handoff, and
   continue — never stall on a file that will not appear.
   *Observable:* either `research.md` exists non-empty, or the run recorded the
   `--skip-research` fallback; either way generation advances.
5. **Generate** — One subagent **per decision point**, in parallel, each with the
   direction card, the point contract, the brief, `research.md`, the copy contract
   (`references/copy-contract.md`), the UX-law checklist (`references/ux-laws.md`)
   and the guardrails; each writes 3 structural variants (2–3 linked screens). You
   assemble the gallery and the per-point comparison canvas.
   **Fit mode:** pass `style-snapshot.json` to every generator; all variants inherit
   it. No new fonts/accents/radii — a new value is only a gate-approved `extensions[]`
   entry.
6. **Judge** — A fresh-eyes judge subagent runs the 5 axes code-first (plus
   screenshots if a browser tool exists), writes findings with severity to
   `judge-report.md`. The `slop-scan` axis has two halves: the visual fingerprints
   (`≥ 4` hits fail) and the zero-tolerance copy gate
   (`references/copy-contract.md`); run `check_copy.py` once per product page.
   The `strangeness` axis runs the relevant `U01-U11` checks from
   `references/ux-laws.md` for the screen's component types; record `N/A` where a
   law does not apply. Blockers/majors → fix → re-judge, **≤ 2 rounds**. Nothing is
   presented until the report is PASS or the failures are stated openly.
   **Fit mode:** axis 4 is snapshot fidelity — every value traces to the snapshot or an
   approved extension; an unapproved token is a major, a changed register is a blocker.
   `slop-scan` reports `N new / M inherited`; inherited fingerprints are exempt, `>= 4`
   new hits fail. The copy gate is unchanged.
   **Inline judging** (no subagent available) is allowed only as an explicit, declared
   degradation: the report header must state `fresh-eyes independence: lost (inline)` —
   an inline self-review is never labelled a clean fresh-eyes judge.
   **Cap reached with a known blocker:** a fix made after the ≤ 2 rounds still ships, but is
   marked `NOT judge-verified` in `judge-report.md` and `decisions.md` — a post-cap fix is
   never presented as judged.
   *Observable:* an inline run's report carries the `fresh-eyes independence: lost (inline)`
   line; any post-cap fix carries the `NOT judge-verified` marker.
7. **Present** — Open `index.html` in the browser and summarise in chat: points,
   options, what the judge found. The user chooses per point.
8. **Record** — `decisions.md`: chosen + rejected + why, including rerolled seeds.
9. **Handoff** — `tokens.css` + `handoff.md` + `chosen/` + `styleguide.html`
   (static mini design system). Formats in `references/handoff-format.md`.
   **Fit mode:** `tokens.css` preserves the existing names/values; each `handoff.md`
   component carries `origin: reused | new | extension`.
   **No user pick?** An unattended run that could not get a per-point choice may legitimately
   emit only `tokens.css` (the chosen direction's token scales) plus its invariants, and must
   record `chosen/`, `handoff.md` and `styleguide.html` as **pending the user's pick** — never
   invent a winner.
   *Observable:* with no pick, `tokens.css` exists and `chosen/` + `handoff.md` +
   `styleguide.html` are absent but recorded as pending.

### Caps (hard)

| Cap | Value |
|---|---|
| Decision points per session | ≤ 4 |
| Variants per point | 3 (2 allowed via `--variants 2`) |
| Screens per variant | ≤ 3 |
| Research sources | ≤ 6 |
| Judge rounds | ≤ 2 rounds |
| Slop hits | ≥ 4 fails the gate |
| Copy-contract findings | any unresolved C01-C04 fails `slop-scan` |

A request beyond a cap is capped, not obeyed: apply the cap and state it in one
line (e.g. `6 points requested → 4 (cap)`). Cutting scope that way is allowed;
cutting a step is not.

Slop is scanned mechanically **once per generated `.html`**:
`python3 "$SKILL_DIR/scripts/check_slop.py" <one-page.html> [--allow-font NAME]`.
Each invocation decides that page and exits 1 iff **that page** finds **≥ 4**
hits. A call with several paths **sums** their hits into one count — that is not
a per-page verdict and must never be used as one. Details in
`references/slop-fingerprints.md`.

Copy is scanned mechanically **once per product page**:
`python3 "$SKILL_DIR/scripts/check_copy.py" <one-page.html>`. It checks C01 and
C04; C02 and C03 are judge-only. A page fails on **any** copy finding: the copy
gate is zero-tolerance, unlike the visual `≥ 4` cluster. Details in
`references/copy-contract.md`.

### Copy contract (zero tolerance)

Read `references/copy-contract.md` before generating and before judging. It
applies to every visible text node in `variants/**` and `chosen/**`; session
chrome is marked `data-session-chrome` and skipped. The four rules:

- **C01. No item-count labels.** A list is its own count. Drop `6 filmes, 4
  cinemas` and `10 registros`; keep counts that are data or state (`3 de 5`,
  `extração 1 de 2`, `nota 4/5`).
- **C02. One fact, one place.** At most one repetition per screen, and only for
  a distinct summary/detail role. An eyebrow must not restate its heading.
- **C03. No filler copy.** Every line must add information. If deleting it
  loses nothing, delete it. A direction's voice never licenses an empty slogan.
- **C04. No separator characters.** Do not join metadata with `·`, `—`, `–`,
  `|` or `•`. Use a comma, colon, conjunction or separate elements. Dates,
  ratios, ranges, hyphenated words and proper names are values, not separators.

A copy finding is not counted in the visual `≥ 4` cluster: any unresolved
C01-C04 finding fails `slop-scan`, whatever the visual count.

### UX-law checks (judge aid)

`references/ux-laws.md` curates the Laws of UX that can be judged on a static
screen as U01-U11. The generator applies only the two to four rules relevant to
the component type; the judge runs the same rules inside `strangeness` and cites
the rule id, law and screen region, or records `N/A`. These are heuristics, not
hard caps: Miller's 7±2 is not a limit, Jakob's Law does not forbid structural
divergence, and a static prototype can show intended feedback but cannot measure
the Doherty threshold.

### Canvas contract (R16)

The comparison canvas is `assets/canvas.html`. Its `{{CANVAS_FRAMES}}` token is an
attribute anchor on the deck container (`data-canvas-frames="{{CANVAS_FRAMES}}"`).
Generation **replaces the whole `<div class="deck">…</div>` block** — it is not a
token substitution. Keep that block's structure intact so the deck stays
file://-safe (`assets/gallery.html` is display-only, zero cross-frame scripting;
`assets/variant-shell.html` is the neutral variant shell).

### Fit mode (opt-in)

`--fit <source>` captures the existing visual system instead of drawing a direction.
`style-snapshot.json` is the source of truth: tokens by role, type scale, component
recipes, layout shell, optional voice samples, inherited slop and gaps, each with
provenance and an `observed`/`declared`/`inferred` evidence level. The 22-catalogue
is bypassed; never blend a catalogue direction with the existing system. The fit card
records `mode: "fit"`, `direction_id: "FIT"` and the snapshot hash. Structural
divergence at points is unchanged — fit mode is not a repaint machine. Full contract:
`references/fit-mode.md`.

## Inviolable rules

1. **Explore mode: do not read the target project's code or UI for design** — only its
   specs/docs for requirements. "I followed the existing theme" is a violation.
   **Fit mode: read only the declared visual sources** (tokens, theme, global CSS,
   component primitives, computed styles), with provenance; never business logic, API
   clients or data models. "I invented a token the snapshot does not contain" is the
   violation.
2. **Do not invent a direction outside the catalogue of 22** (`references/directions.md`).
3. **Do not skip the judge.** No presentation before the judge report passes, unless
   you report openly what failed.
4. **Conversation in the user's language; repo docs in English (D10).**

## Flags

| Flag | Default | Effect |
|---|---|---|
| `--seed <string>` | random short seed | Fixes the direction; same `--seed` → same card. Reroll = new `--seed`. |
| `--fit <source>` | off | Opt-in fit mode: capture the existing system as the direction; incompatible with `--domain`/`--wild`; no visual reroll. See `references/fit-mode.md`. |
| `--skip-research` | research on | Skips step 4; say so in the handoff. |
| `--points <n>` | 4 | Number of decision points, capped at ≤ 4. |
| `--variants <n>` | 3 | Structural variants per point; 2 allowed, capped at 3. |
| `--wild` | off | Experimental, not wired: records `wild: true` in the card; every variant still uses the session card's direction (per-variant cards are owned by `docs/roadmap.md`). |

Related interfaces (all under `$SKILL_DIR`): `scripts/roll.py`/`scripts/roll.mjs`
(`--seed --domain --wild --out --catalog`), `scripts/snapshot.py`
(`--from --extra --out --card --check`), `scripts/scaffold.py`
(`--target --slug --card --points [--snapshot]`), `scripts/check_slop.py`
(`<one-page.html> [--allow-font NAME]`), `scripts/check_copy.py`
(`<one-page.html>`), `scripts/serve.py` (`--port 8765 --dir PATH`). Seed
algorithm spec: `references/seed-algorithm.md`. Point taxonomy:
`references/decision-points.md`. Judge rubric: `references/judge-rubric.md`.
UX-law checks: `references/ux-laws.md`. Research protocol:
`references/research-protocol.md`. Handoff formats:
`references/handoff-format.md`.

## Rationalizations

Six rows below are **verbatim** shortcuts from the RED baseline (T02); the last
row is the direction shortcut named in the spec (§6). Recognize the phrase and
apply the counter — the phrase is the trigger, the counter is the rule.

| Rationalization (verbatim) | Counter |
|---|---|
| "Pula o que não for essencial" | Research, variants, the judge and the gate *are* essential. If `--skip-research` is used, it must be an explicit flag, and the judge and variants still run. |
| "sem research, sem variantes alternativas, sem perguntas" | Stated as a virtue; it is the failure. Defaults are research on, 3 variants per point, and ≤ 3 clarifying questions when a field is load-bearing. |
| "uma tela basta" | A request to narrow the *product* does not license one design option. Still 3 structural variants (≤ 3 screens each); the user compares, then chooses. |
| "não fiz nenhuma pergunta de esclarecimento — público, plataforma e marca ... são suposições minhas" | Guessing is not consent. Ask ≤ 3 questions for load-bearing fields; guesses become recorded assumptions at the gate, not silent defaults. |
| "no real data source or persistence — it's static prototype data" | Static data is the point, not a reason to stop. Prototypes are static HTML/CSS and still get variants, a judge pass and a handoff. |
| "as 5 não são o mesmo layout repintado" | Producing distinct-looking options by luck is not the workflow: no seed, no reproducibility, no research, no judge, no handoff means it does not count. Run the pipeline so divergence is purposeful. |
| "a direção sorteada não combina com meu domínio, vou usar a minha" | Do not improvise a direction. If `fits/fails` condemns the card, **reroll the seed** (free, at step 2) — never author a direction outside the catalogue. |

### Loopholes that survived the first GREEN run (T18)

The five below each survived a run with the skill present. Every counter carries an
**observable predicate** — a file, a marker or a turn boundary you can check.

| Loophole (verbatim) | Counter (observable predicate) |
|---|---|
| "Non-interactive ⇒ I can't wait, so I continue." | Present the card + `points.json` (plus the step-3 `scaffold.py` skeleton) and **end the turn**; spend no generation before the OK. At turn end `research.md` is absent and `variants/` holds only scaffold skeletons (each just an untouched `index.html`) — no generated screens. Recording the assumption is not a substitute for the gate. |
| "The judge can run inline and still be called the judge." | Inline judging is a declared degradation only: `judge-report.md` must state `fresh-eyes independence: lost (inline)`. |
| "The research subagent reported ✓, so I proceed." | Verify `research.md` exists after step 4; if it does not, fall back to `--skip-research`, record it, and continue — never stall. |
| "The cap is 2 rounds, so a known blocker ships." | A fix after the ≤ 2-round cap ships marked `NOT judge-verified` in `judge-report.md` and `decisions.md`. |
| "Step 9 can't complete unattended, so skip it." | Unattended + no pick may emit only `tokens.css` + invariants; `chosen/`, `handoff.md`, `styleguide.html` stay absent and are recorded as pending the user's pick. |

## Red Flags

Stop and correct course if you catch yourself thinking or saying:

- "This one is simple, I'll skip the judge." — The judge is the pre-human gate.
- "One option is enough here." — One option is not a comparison; produce variants.
- "Research takes too long; I'll skip it." — Either run it or use `--skip-research`
  and record the omission; do not silently drop it.
- "I'll reuse the target's existing theme so it fits." — Only in fit mode, from the
  declared snapshot; in explore mode it is a violation.
- "I'll eyeball the existing app and pick similar colours." — Fit mode captures the
  snapshot with provenance; gaps are gate-resolved.
- "I'll blend a catalogue direction with the existing system." — Two registers
  averaged; the judge fails it.
- "Inherited slop means the slop gate is off." — Inherited hits are recorded; new
  hits still fail at ≥ 4.
- "I'll invent a direction that matches this brief better." — Reroll the seed instead.
- "I'll show it now and fix the findings after." — Present only after a PASS, or
  report the failures openly.
- "The user is in a hurry, so I'll cut the pipeline down." — Pressure is exactly
  when the caps do the work; cut *scope* (`--points`, `--variants`), not *steps*.
- "5 points, 4 variants, 5 judge rounds." — Caps are hard: ≤ 4 points, 3 variants,
  ≤ 2 rounds.
- "It's non-interactive, so the gate doesn't apply." — The gate still applies: present and
  **stop**; only the answer is missing, not the rule.
- "I'll judge it myself — same thing." — Only as a declared degradation, and the report must
  say fresh-eyes independence was lost.
- "The research said ✓, so I'll wait for the file." — Check the artifact; if it is missing,
  `--skip-research` and continue.
- "The count gives useful context." — If the list already shows the items, the
  count restates its length; drop it (C01).
- "The label repeats the heading for clarity." — Repetition is noise; keep the
  fact in one place (C02).
- "The slogan gives the page personality." — Personality without information is
  filler; rewrite it as a concrete claim (C03).
- "The separator makes the metadata look designed." — Separator glyphs are
  decoration; use grammar or structure (C04).
- "The law says 7±2, so I'll cap the UI at seven items." — Chunk by meaning,
  not a magic number (U02).
- "The law justifies social proof, scarcity or anchoring." — Those are
  dark-pattern risks, not checks; the copy contract still applies (U03/C03).
- "Jakob's Law means every variant must look conventional." — Control-level
  familiarity, not structural sameness; divergence is the point (U05).
- "Aesthetic polish proves usability." — Polish can mask breakage; the judge
  tests the artifact (Aesthetic-Usability caveat).

## Degradation

Prevention first; degradation only for the residue (spec §8). Artifacts are the
source of truth, so most routes degrade without losing the direction:

| Edge case | Fallback |
|---|---|
| No python3/node | Execute the algorithm in `references/seed-algorithm.md` directly; the committed `direction.json` still wins. |
| No browser tool | Judge stays code-first; final visual validation belongs to the human. Screenshots when available. |
| Offline / webfont missing | Fallback stack per class is mandatory; research off, fonts fall back. |
| Iframes blocked on `file://` | Gallery is display-only; iframes are relative and same-directory. `scripts/serve.py` for robustness. |
| Ambiguous brief | Minimal intake schema; ≤ 3 questions only for load-bearing fields; the step-3 gate confirms before generation. Reroll after the gate. |
| Total rejection | Direction preview rerolls for free before generation; rejecting a structure = choose another variant. |
| Incoherent direction mixing | Card carries forbidden moves; mistaking roles is caught by judge axis 4 and fixed in the loop. |
| Harness without subagents | Each phase runs inline too (sequential; costs context, not correctness) — **including the judge**. Inline judging is a declared degradation: the `judge-report.md` header must state `fresh-eyes independence: lost (inline)`. |
| Non-interactive harness (cannot ask) | The answer is unavailable, not the gate: present the card + `points.json` (and the step-3 `scaffold.py` skeleton) and end the turn; generation waits for an explicit OK. The `variants/` skeletons `scaffold.py` writes are step-3 output and may exist — but no generated variant content. |
| Research subagent "succeeded" but wrote nothing | Verify `research.md` exists; if not, fall back to `--skip-research`, record it, and continue — never stall. |
| No per-point pick (unattended) | Emit `tokens.css` + invariants only; `chosen/`, `handoff.md`, `styleguide.html` stay pending the user's pick. |
| Cost blow-up | Hard caps (≤ 4 points, ≤ 3 screens/variant, ≤ 6 sources, ≤ 2 rounds) plus flags (`--points`, `--variants`). |
| Contamination by the target repo (explore) | Never read the target's code/UI for design; "followed the existing theme" is a declared red flag. |
| Fit source unavailable | Ask for a token file, URL or screenshots; do not fake a snapshot; fall back to explore mode. |
| Fit mode on a Node-only harness | `snapshot.py` is Python; write the card by hand from `references/fit-mode.md` or use Python; record the degradation. |
