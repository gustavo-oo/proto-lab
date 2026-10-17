---
name: proto-lab
description: Use when the user wants to explore UI design options, compare structural alternatives for a screen or flow, or produce HTML prototypes and mockups before implementation — design first, implement later.
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

**Choose the design before implementing it, and diverge on purpose.** A seed
selects one direction from a closed catalogue of 22; every variant for a point is
a *structural* answer to that point, not a repaint. The direction card
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

## When Not to Use

- The user wants production code written now — this produces prototypes, not an app.
- The task is a copy/behaviour fix on a known, decided design.
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
   `brief.md`. Ask **at most 3 questions**, only for load-bearing fields. Pick a
   seed (random short string, or explicit `--seed`).
2. **Roll** — `python3 scripts/roll.py --seed <seed> [--domain <domain>] [--out ...] [--catalog ...]`
   (Node mirror: `scripts/roll.mjs`, same flags; API `roll.roll(seed, domain=None, wild=False)`).
   Shows a compact card preview in chat. Rerolling here is free — nothing has been
   generated yet, so offer it. `--wild` is off by default.
3. **Points** *(the single gate)* — Derive decision points and their named
   structural options into `points.json` (contract: axis + options). Also create the
   session skeleton: `python3 scripts/scaffold.py --target <project> --slug <slug> --card <direction.json> --points <points.json>`.
   **Stop and get a quick OK from the user before spending any generation.**
4. **Research** — 3–6 competitors/analogues of the declared domain into
   `research.md` (good/bad patterns, cited; "observed vs inferred"). On by
   default; `--skip-research` turns it off. Cache the result for reuse.
5. **Generate** — One subagent **per decision point**, in parallel, each with the
   direction card, the point contract, the brief, `research.md` and the guardrails;
   each writes 3 structural variants (2–3 linked screens). You assemble the gallery
   and the per-point comparison canvas.
6. **Judge** — A fresh-eyes judge subagent runs the 5 axes code-first (plus
   screenshots if a browser tool exists), writes findings with severity to
   `judge-report.md`. Blockers/majors → fix → re-judge, **≤ 2 rounds**. Nothing is
   presented until the report is PASS or the failures are stated openly.
7. **Present** — Open `index.html` in the browser and summarise in chat: points,
   options, what the judge found. The user chooses per point.
8. **Record** — `decisions.md`: chosen + rejected + why, including rerolled seeds.
9. **Handoff** — `tokens.css` + `handoff.md` + `chosen/` + `styleguide.html`
   (static mini design system). Formats in `references/handoff-format.md`.

### Caps (hard)

| Cap | Value |
|---|---|
| Decision points per session | ≤ 4 |
| Variants per point | 3 (2 allowed via `--variants 2`) |
| Screens per variant | ≤ 3 |
| Research sources | ≤ 6 |
| Judge rounds | ≤ 2 rounds |
| Slop hits | ≥ 4 fails the gate |

Slop is scanned mechanically:
`python3 scripts/check_slop.py <paths> [--allow-font NAME]` exits 1 iff it finds
**≥ 4** hits. Details in `references/slop-fingerprints.md`.

### Canvas contract (R16)

The comparison canvas is `assets/canvas.html`. Its `{{CANVAS_FRAMES}}` token is an
attribute anchor on the deck container (`data-canvas-frames="{{CANVAS_FRAMES}}"`).
Generation **replaces the whole `<div class="deck">…</div>` block** — it is not a
token substitution. Keep that block's structure intact so the deck stays
file://-safe (`assets/gallery.html` is display-only, zero cross-frame scripting;
`assets/variant-shell.html` is the neutral variant shell).

## Inviolable rules

1. **Do not read the target project's code or UI for design** — only its specs/docs
   for requirements. "I followed the existing theme" is a violation.
2. **Do not invent a direction outside the catalogue of 22** (`references/directions.md`).
3. **Do not skip the judge.** No presentation before the judge report passes, unless
   you report openly what failed.
4. **Conversation in the user's language; repo docs in English (D10).**

## Flags

| Flag | Default | Effect |
|---|---|---|
| `--seed <string>` | random short seed | Fixes the direction; same `--seed` → same card. Reroll = new `--seed`. |
| `--skip-research` | research on | Skips step 4; say so in the handoff. |
| `--points <n>` | 4 | Number of decision points, capped at ≤ 4. |
| `--variants <n>` | 3 | Structural variants per point; 2 allowed, capped at 3. |
| `--wild` | off | Each variant rolls its own direction (extra mode). |

Related interfaces: `scripts/roll.py`/`scripts/roll.mjs` (`--seed --domain --wild --out --catalog`),
`scripts/scaffold.py` (`--target --slug --card --points`), `scripts/check_slop.py`
(`<paths> [--allow-font NAME]`), `scripts/serve.py` (`--port 8765 --dir PATH`). Seed
algorithm spec: `references/seed-algorithm.md`. Point taxonomy:
`references/decision-points.md`. Judge rubric: `references/judge-rubric.md`.
Research protocol: `references/research-protocol.md`. Handoff formats:
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

## Red Flags

Stop and correct course if you catch yourself thinking or saying:

- "This one is simple, I'll skip the judge." — The judge is the pre-human gate.
- "One option is enough here." — One option is not a comparison; produce variants.
- "Research takes too long; I'll skip it." — Either run it or use `--skip-research`
  and record the omission; do not silently drop it.
- "I'll reuse the target's existing theme so it fits." — Reading the target's UI for
  design is a violation.
- "I'll invent a direction that matches this brief better." — Reroll the seed instead.
- "I'll show it now and fix the findings after." — Present only after a PASS, or
  report the failures openly.
- "The user is in a hurry, so I'll cut the pipeline down." — Pressure is exactly
  when the caps do the work; cut *scope* (`--points`, `--variants`), not *steps*.
- "5 points, 4 variants, 5 judge rounds." — Caps are hard: ≤ 4 points, 3 variants,
  ≤ 2 rounds.

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
| Harness without subagents | Each phase runs inline too (sequential; costs context, not correctness). |
| Cost blow-up | Hard caps (≤ 4 points, ≤ 3 screens/variant, ≤ 6 sources, ≤ 2 rounds) plus flags (`--points`, `--variants`). |
| Contamination by the target repo | Never read the target's code/UI for design; "followed the existing theme" is a declared red flag. |
