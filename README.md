# proto-lab

**Status: early, name provisional.** The pipeline, catalogue and tests work;
the name will change before publication. Nothing here is stable API.

Design options before implementation. `proto-lab` turns a rough product idea
into a **direction card** drawn from a closed catalogue of 22 directions, then
into comparable, judgeable HTML prototypes you can hand off to the
implementation session.

## What it is

`proto-lab` is a skill in the [agentskills.io](https://agentskills.io) format
(`SKILL.md` at the folder root), so it runs in any harness that reads skills —
OpenCode, Claude Code, Codex and similar. One session produces, inside the
target project:

- a **direction card** (`direction.json`): the seed, the direction, its DNA and
  knobs — the source of truth, with no timestamp, so the same seed yields the
  same card;
- **decision points** with named structural options (`points.json`), confirmed
  with you before anything is generated;
- **cited competitor research** (`research.md`) for the product's domain;
- **structural variants** per point — not recolours — as small, navigable
  static HTML mini-projects;
- a **fresh-eyes judge report** (`judge-report.md`) across five axes, with
  fixes applied before you ever see the output;
- a **handoff**: `tokens.css`, `handoff.md`, `chosen/` and `styleguide.html`.

**Why force divergence.** Language models converge on the same "average" UI.
The evidence says this is structural, not a prompting bug: the *Design
Creativity Bench* (arXiv 2610.11539) shows LLM-generated UIs are markedly more
similar to each other than to paired human references; *Interrogating Design
Homogenization in Web Vibe Coding* (arXiv 2603.13036) finds probabilistic
defaults converging toward one dominant aesthetic and argues for deliberate
"productive friction"; and *The Homogenization Problem in LLMs*
(arXiv 2601.06116) frames mode collapse as a first-class failure, not a quirk.
`proto-lab` answers with a mechanic rather than a prompt: draw **one** direction
from the catalogue, then diverge **structurally** at each decision point.

**What it is not, and its boundaries.**

- Not an app and not production code. Variants are lightly navigable static
  HTML: links work, there is no business logic, data is placeholder.
- It **does not follow the target's stack** — the skill never reads the target
  project's code or UI for design, only its specs/docs for requirements. "I
  matched the existing theme" is a violation of the skill, not a feature.
- It is **zero-dependency**: static HTML/CSS that opens over `file://`, no
  build, no bundler, no mandatory server (a small `scripts/serve.py` is
  optional), and no `pip`/`npm` install step. Fonts come from a CDN **with a
  same-class fallback stack**, so the direction's register survives offline.
- No backend and no binary images, by construction: every "image" is a CSS/SVG
  placeholder.

## Install

Installation is a **folder copy** — there is no package to build and nothing to
resolve.

1. Copy this repository's folder into the **skills directory your harness
   reads** — for example `~/.config/opencode/skills/proto-lab/`,
   `~/.claude/skills/proto-lab/`, or a project-local `.opencode/skills/proto-lab/`.
2. Keep the layout intact: `SKILL.md` at the folder root next to `references/`,
   `scripts/` and `assets/`.
3. Open a new session and describe what you want to prototype. The skill
   triggers on requests to explore design options, compare structural
   alternatives, or produce HTML mockups before implementation.

No package manager step, no build.

**Demo.** `examples/coffee-log-cafe-com-leite/` is a real session produced by the
skill (one decision point, three variants) for a personal coffee log. It is the
demo and the quality bar. Open its `index.html` over `file://` — no server — and
click through: gallery → per-point canvas (three live frames) → a variant → a
second screen and back.

## Cost model

The only cost is **harness tokens**. There is no infrastructure cost: no paid
service, no build, no required network.

**Dominant term:** variant generation — 3 variants × decision points × 2–3
screens per variant — run as one generation per point, in parallel, on whatever
cheap model the harness is configured with. **Defaults:** ≤ 4 decision points,
3 variants each, research on, and one judge plus its fix rounds.

**Levers**, cheapest first:

| Lever | Effect |
|---|---|
| Reroll the seed (pipeline step 2) | A new direction card costs ~nothing; nothing has been generated yet. |
| Cache the research | Reuse `research.md` for the same domain instead of re-fetching. |
| `--variants 2` | Two structural variants per point instead of three (floor; capped at 3). |
| `--points <n>` | Fewer decision points; the floor is 1 point (= 3 screens + canvas + gallery). |
| `--wild` off (default) | Experimental, not wired: it only records `wild: true` in the card; every variant still uses the session direction, so it adds no generation cost today (per-variant cards are an open gap in `docs/roadmap.md`). |
| Code-first judge | Skip the screenshot pass when no browser tool is available; the five axes still run. |

**Acceptance evidence.** The visual acceptance run (`tests/acceptance-notes.md`,
T21) rolled three seeds and got three distinct directions from three different
families — `cafe-com-leite` → D10 Blueprint / Schematic (technical), `s7` →
D14 Risograph / Zine (print), `termo-final2` → D12 Space Age / Retro-Futurism
(retro) — captured as desktop 1280 and mobile 390 screenshots. A fresh-eyes
judge put pairwise distinctness at 0.97, 0.84 and 0.86, and the mechanical slop
scan returned `{"hits": [], "count": 0, "verdict": "pass"}` on all three.
Reproducibility: the same seed produced a byte-identical card
(`sha256 797c60e8…b3370`), equal to the committed card of the demo session.
Figures come from that run; nothing here is estimated.

## How it works

```
0 Setup    detect python3 / node / browser tool / subagents -> rich or degraded path
1 Brief    capture the brief, pick a seed
2 Roll     seed -> direction card from the catalogue of 22 (reroll here, free)
3 Points   derive decision points + named structural options   <<< the single gate
4 Research 3-6 cited competitors/analogues of the domain
5 Generate one generation per point, in parallel -> 3 structural variants
6 Judge    5 axes, fresh eyes; blockers/majors fixed and re-judged (<= 2 rounds)
7 Present  open the gallery, summarise, you choose per point
8 Record   decisions.md: chosen + rejected + why, including rerolled seeds
9 Handoff  tokens.css + handoff.md + chosen/ + styleguide.html
```

Step 3 is the **only** gate that interrupts the flow: points and their options
are confirmed before any generation is spent. Everything else runs through,
including the judge loop. The seed selects one direction from a closed catalogue
of 22 — never an improvised direction; a bad fit is rerolled, not rewritten.

Hard caps: ≤ 4 decision points per session; 3 variants per point (2 allowed via
`--variants 2`); ≤ 3 screens per variant; ≤ 6 research sources; ≤ 2 judge
rounds; **≥ 4 slop hits fails the gate**.

The normative detail lives in [`SKILL.md`](SKILL.md) and `references/`
(`directions.md`, `decision-points.md`, `seed-algorithm.md`, `judge-rubric.md`,
`research-protocol.md`, `slop-fingerprints.md`, `handoff-format.md`). For how
the project itself evolves: [`CHANGELOG.md`](CHANGELOG.md) records **what changed
between versions**, and [`docs/roadmap.md`](docs/roadmap.md) records **what is
still open** — the corrections fixed now, the open gaps by severity and the
failure modes not yet covered.

## Requirements

- **Python ≥ 3.8, standard library only** for the optional scripts
  (`scripts/roll.py`, `scripts/scaffold.py`, `scripts/check_slop.py`,
  `scripts/serve.py`). No `pip`.
- **Node ≥ 18, built-in modules only** for the optional mirror
  (`scripts/roll.mjs`); not required.
- **A browser** to view the artifacts; a **browser tool** (agent-browser or
  Playwright) only to enable the judge's screenshot pass.
- **Network** only for the optional research step and webfont CDNs; with
  `--skip-research` and the same-class font fallbacks the pipeline runs
  offline. Without a browser tool the judge is code-first; without subagents
  every phase runs inline; with neither `python3` nor Node the agent executes
  `references/seed-algorithm.md` directly.
- **License: MIT** — see [`LICENSE`](LICENSE).
