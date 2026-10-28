# Judge report — coffee-log-cafe-com-leite
- round: 2
- mode: full

| axis | verdict | evidence |
| ---- | ------- | -------- |
| brief-fidelity | PASS | `variants/d1-a/index.html` (table `.spec`, cols data/origem/método/nota), `variants/d1-b/index.html` (`.cards`, one `.card` per coffee), `variants/d1-c/index.html` (`.feed__list`, one `.entry` per coffee) each answer the d1 question "Como o log de cafés deve se apresentar na tela principal?" with the promised listing shape; every variant carries the two brief screens (`index.html` + `detail.html`) and lists origem/método/notas, the three fields the brief names as load-bearing. |
| strangeness | PASS | Walkthrough over `file://` at 1280px and 390px (shots a1-a6): variant C opened `variants/d1-c/index.html` → clicked `detalhe` → detail → `voltar ao diário` → index → `galeria` → session `index.html`; no clipped text, no dead affordance, no empty region. The title-block table (`.titleblock`) at the foot of every screen reads as the D10 sheet footer, not as primary content. |
| slop-scan | PASS | One invocation per generated page, 11 separate runs: gallery `index.html`, canvas `points/d1-coffee-log.html`, `styleguide.html`, the 6 variant pages (`variants/d1-{a,b,c}/{index,detail}.html`) and the 2 `chosen/d1/` copies. `for f in $(find examples/coffee-log-cafe-com-leite -name '*.html'); do python3 scripts/check_slop.py "$f"; done` → every file returned `{"hits": [], "count": 0, "verdict": "pass"}`, exit 0 (each count is per-page, not a summed multi-path count). Zero of the 22 mechanical fingerprints fire on any of the 11 pages; the four judge-only fingerprints (F16/F18/F21/F22) are absent: no nested card-in-card chain (F16), spacing is the variant's 2/6/10/14/18/22px ramp rather than a uniform 8px grid (F18), no invented stat row (F21), and "imagery" is a declared CSS/SVG placeholder genre — halftone plate (B), hatched plate + line-drawing (B detail), corner-bracket linework (all) — not smooth synthetic 3D (F22). No second-order cluster (no cream+gold, no fake distress, no glow+purple, no luxury-dark averaging). |
| direction-fidelity | PASS | `direction.json` = D10 Blueprint / Schematic, family `technical`, knobs `inversion:true`, `density_shift:1`, `accent:#00E5FF`, `rhythm:odd-first`, `imagery_subject:crop marks`. Mapped to file: inverted white-blue field (`body{background-color:#F4F7FA}` + graph-paper `repeating-linear-gradient` grid, `variants/d1-a/css` L36-38); zero radius (no `border-radius` anywhere); monochrome linework + one cyan accent (`--accent:#00E5FF`, `--ink-2:#1A3A5C`, `--annot:#B3182B`); font set = Archivo Narrow (display) + Space Mono (body/mono), 2 families + 1 mono, each with a same-class fallback stack. §C5 failure modes avoided: no D01 grid-as-decoration (the grid is the sheet field, content sits on `.panel`/`.plate` opaque plates), no D06 softened shadows (no `box-shadow` at all), no D19 glow+purple, no D05 Inter body. |
| variant-diversity | PASS | Axis `listing-pattern`. `d1-a` = `dense-table`: `<table class="spec">` with `<colgroup>`, 7 columns, rows that shrink to data/origem/método/nota under 640px (`CSS_A`, `@media` hides `.c-dose/.c-ratio/.c-time`). `d1-b` = `card-grid`: `ul.cards` on `grid-template-columns:repeat(auto-fill,minmax(210px,1fr))`, one `.card` per coffee with an aspect-ratio plate. `d1-c` = `single-column-feed`: `ol.feed__list` of full-width `.entry` rows in chronology, `nth-child(odd)` 2px rule / `nth-child(even)` hairline. The diff is structural on the declared axis (column alignment vs. spatial grid vs. linear chronology) and in the navigation model (row-target `a` inside a `<td>`; whole-card `a`; whole-entry `a`), not cosmetic — the three variants share the D10 skin by design but not their listing structure. |

## Round history (round 1 → round 2)

- round 1 (inline) found one **major**: `variants/d1-c/index.html` printed each
  entry's score twice — a 5-tick `<span class="gauge" role="img"
  aria-label="nota N de 5">` **and** a literal `<span class="entry__score">nota
  N/5</span>` on the same `.entry__foot` line, in all 10 rows.
- fix: removed the literal `entry__score` span and pinned the gauge right with
  `.entry__foot .gauge{margin-left:auto}` (the gauge's `aria-label` stays the
  accessible value). Re-generated, re-scanned (still 0 hits, exit 0), re-rendered
  in the browser (shots a1/a2/a3): each entry now shows the score once.
- round 2 re-judges the same five axes above; no blocker/major remains.

## Findings

- none open in round 2 (no `blocker`, no `major`). The round-1 major is recorded
  above and closed; the loop cap (`<= 2 rodadas`) was not reached.

## Open (not fixed)

- minor: `variants/d1-a/index.html` — at ≤640px `.spec` keeps `origem` wrapping
  to a second line ("Brasil · Cerrado, Fz. Boa Vista") while neighbour rows stay
  single-line, so row heights are uneven in the listing (observed in canvas
  frame A, mobile). Left open: cosmetic polish in a **rejected** variant, and the
  chosen `d1-c` does not inherit it.
- minor: `variants/d1-b/index.html` — `.card__foot` is not bottom-pinned, so in a
  row of unequal-height cards the `método · razão` + gauge line sits at a
  different y per card (observed in canvas frame B). Left open: cosmetic
  alignment in a rejected variant.
- minor: `index.html` (the scaffolded gallery) renders in its deliberate neutral
  register, not D10: `scaffold.py` substitutes only seed/direction/family/points
  rows and the template documents that it does not inject card tokens. The
  neutral chrome is intentional (no half-themed page); applying the direction's
  tokens to the gallery is recorded as an open gap in `docs/roadmap.md`
  (owner: T12/T14), not a D10 failure.
- assumption: the judge ran **inline** — this harness has no subagent-dispatch
  tool, so no fresh-eyes subagent was spawned. Per the rubric's *Fresh eyes* rule
  this is weaker than a blind judge; the independent part of the evidence is the
  machine gate (`check_slop.py` exit 0) and the real `file://` walkthrough.
- assumption: the Google-Fonts CDN link (`fonts.googleapis.com`) was observed
  with the webfaces available; the offline same-class fallbacks (Archivo
  Narrow→Arial Narrow, Space Mono→IBM Plex Mono/ui-monospace) were reasoned from
  the declared stacks, not rendered with the network cut.
