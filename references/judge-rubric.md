# Judge rubric

`references/judge-rubric.md` is the normative specification of pipeline step 4:
the **pre-human gate** that scores generated variants before a human ever opens
them. It defines the **JUDGE REPORT FORMAT** — the `judge-report.md` consumed by
the judge runner and by the loop fixtures (T16/T17/T19).

The judge is a *dedicated subagent with fresh context* (see **Fresh eyes**). It
scores five axes, states a binary `PASS`/`FAIL` per axis with cited evidence, and
emits a list of findings, each with a `blocker`/`major`/`minor` severity. It does
not rewrite the prototype: it reports, the loop fixes, the judge re-judges.

Caps that bind the judge: `<= 2 rodadas de juiz` (see **Loop**) and slop
`>= 4 hits` on a page (see **slop-scan**). The judge never reviews its own
round; a fresh subagent is spawned for the re-judge.

## Fresh eyes

The judge runs as a **dedicated subagent that does not see the generator's
reasoning**. It is blind to the generator's transcript, plan, prompts, diffs and
notes, and it never reads them. This is the whole point of the gate: it grades
the *artifact*, not the story told about the artifact, so it cannot inherit the
generator's blind spots or be talked into "it looks right".

The judge receives only:

- `brief.md` — the brief and its load-bearing constraints;
- `direction.json` — the direction card (the source of truth, no timestamp);
- `points.json` — the decision-point contract;
- the generated variant HTML files;
- `research.md` — the cited competitor research (domain clichés to avoid).

It must reach for the artifact first: open the HTML, read the CSS, cite file and
region. A verdict that rests on intent ("the generator meant to…") is invalid.
Because the judge is code-first by design, losing the browser tool changes only
the *kind* of evidence, not the axes or their severity (see **Degraded mode**).

## Axes

Five axes, one `PASS`/`FAIL` each. Every axis verdict must carry evidence — a
file plus the region (selector, element, line range) and the concrete
observation — never a bare adjective.

| Axis | What it verifies |
| ---- | ---------------- |
| `brief-fidelity` | Each variant answers its point and nothing contradicts the brief. |
| `strangeness` | Fresh-eyes walkthrough: what confuses, jumps wrong, or breaks. |
| `slop-scan` | 26 fingerprints + second-order slop. |
| `direction-fidelity` | The direction's DNA is followed and its failure modes avoided. |
| `variant-diversity` | The point contract holds and variants differ structurally, not cosmetically. |

### 1. `brief-fidelity`

*Every variant answers the question of the point it was generated for, and
nothing in the artifact contradicts a load-bearing constraint of the brief.*

**Required evidence:** the point's `question` plus the exact region (file +
selector/element) that answers it, for **each** variant; then each load-bearing
brief constraint (product, audience, objective, key screens, restrictions) with
where it is satisfied — or the contradiction.

**FAIL when:** a variant ignores or drifts from its declared option, the layout
answers a different question than the point asks, or the artifact contradicts a
load-bearing constraint (wrong audience, missing required screen, an objective
the brief explicitly rules out).

### 2. `strangeness`

*A fresh-eyes walkthrough of the rendered screens: as a first-time user, what
confuses me, what jumps out in the wrong order, what looks broken?*

**Required evidence:** an ordered walkthrough per variant, at desktop (~1280px)
and a common mobile width (~390px), listing concretely and by location:

- **what confuses** — ambiguous or missing labels, an affordance whose effect is
  not predictable from its shape;
- **what jumps wrong** — reading order or focal hierarchy that sends the eye to
  the wrong element first;
- **what breaks** — text clipped or overflowing, misalignment, empty regions,
  dead affordances (a control that does nothing), body contrast below 4.5:1.

Cite file + element/line + the observed symptom for every item. With a browser
tool, navigate `file://` and click through; without one, read it from code and
label the walkthrough as degraded (see **Degraded mode**).

**FAIL when:** a screen breaks at a common width, the primary affordance is dead
or misleading, body copy is not readable, or the reading order contradicts what
the point is supposed to make obvious.

### 3. `slop-scan`

*The 26 AI-slop fingerprints of §B of the directions draft, plus second-order
slop, checked mechanically against the HTML/CSS.*

**Required evidence:** for each fingerprint, the detection test that was run
(`grep`/selector) and its result, with a hits count per page. Cite the file and
the CSS/HTML that matched. A single hit may be a legitimate choice for the
direction; only a **page with `>= 4 hits` fails** (`>= 4 hits = reprova`). This
mirrors `check-slop.py` (layer 3) — the judge consumes its result when present
and never re-litigates a fingerprint the direction legitimately earns.

The judge owns the *diffuse* half of layer 4: second-order slop that rule-based
scans miss — cream + Playfair + gold, fake distress, glow + purple,
chrome-on-everything, and "luxury dark" (two luxury registers averaged).

**FAIL when:** a page reaches `>= 4` fingerprints, or a second-order slop cluster
drives the page's register (a hit the direction does not justify).

### 4. `direction-fidelity`

*The variant follows the DNA of its `direction.json` card and avoids that
direction's known failure modes.*

**Required evidence:** each direction DNA claim mapped to file evidence — the
font-family set (class match), the radius/material language, the palette
variables, the motion/easing character, the imagery genre — plus the matching
entry from §C5 (failure-mode audit) shown to be avoided. Any moment that mixes a
second register must be shown to be **role-scoped** (one framing device, one
data island) per §C2, or it is a conflict.

**FAIL when:** the DNA is only skin-deep (right colours, wrong grid/type/motion),
a §C5 failure mode is present (`D01` grid-as-decoration, `D06` softened shadows,
`D19` glow + purple, `D14` fake distress, `D05` Inter body, …), or two directions
are averaged systemically (a C2/C3 conflict) instead of resolved.

### 5. `variant-diversity`

*The cross-variant contract: did each variant implement the option promised in
`points.json`, and do the options differ structurally on the declared axis rather
than cosmetically?*

**Required evidence:** a per-variant line proving the promised option (file +
the structural region that realises it), then a structural diff on the declared
axis across the variants (2–3). The diff must be **structural** — layout,
navigation model, information density, form shape, etc. Cosmetic deltas (colour,
type scale, radius) do **not** count as diversity.

**FAIL when:** a promised option is missing or a fourth shape was invented, two
options are blended, or the variants are reskins of one option (cosmetic-only
diff). Per the point contract, this is a **blocker**.

## Severities

Every finding carries exactly one severity.

| Severity | Criterion | Loop treatment |
| -------- | --------- | -------------- |
| `blocker` | Breaks a global constraint or the point contract: a variant unusable or mis-answering its option, `>= 4` slop hits on a page, a screen breaking at a common width, a brief/direction contradiction that invalidates the direction. | Fix, then re-judge. |
| `major` | The skeleton is right but the deliverable is materially weakened: a dead affordance, body contrast `< 4.5:1`, one §C5 failure mode present, a second-order slop cluster below threshold, a variant cosmetically close to another. | Fix, then re-judge. |
| `minor` | Polish and residual doubt: wording, a single ambiguous affordance, a lone fingerprint a human might accept, an assumption that could not be verified. | Report; not fixed in the loop. Goes to `## Open (not fixed)`. |

A finding is `{"severity", "target", "evidence", "why", "fix"}` — see the report
template. `evidence` cites the artifact; `why` states the impact; `fix` states
the smallest change that clears it.

## Loop

The judge is a gate, not an editor.

1. **Round 1** — judge all five axes, emit findings.
2. **blocker / major** → the generator fixes → a **fresh** judge re-judges.
3. Repeat only while blockers/majors remain, up to the cap **`<= 2 rodadas de
   juiz`** counted as judge rounds.
4. **minor** findings and residual uncertainty are never silently dropped: they
   are written to `## Open (not fixed)` so the user sees exactly what was left.
5. If blockers survive the cap, stop and **escalate to the human** rather than
   looping again.

## Degraded mode

The judge is **code-first by design**: the artifact is HTML/CSS, and the final
visual pass belongs to the human, who always has a browser. When no browser tool
is available, the judge runs in **degraded mode** — same five axes, same
severities, only the evidence kind changes:

- no screenshots and no clicked `file://` navigation; read the HTML/CSS directly;
- reason statically about responsiveness (media queries, `clamp`), contrast
  (computed from the declared colours) and affordances (markup + handlers);
- record `mode: degraded (code-first, no browser tool)` in the report header;
- mark anything that would require rendering as an assumption — **observed vs
  inferred** stays explicit, as in the research discipline.

Degraded mode lowers no bar. It only means a claim that needs a rendered pixel is
stated as an inference instead of an observation.

## Report template

`judge-report.md` is written from this template. Copy it, replace the
placeholders, delete nothing structural — the table header and the
`## Open (not fixed)` section are the interface the loop reads.

```markdown
# Judge report — <slug>
- round: <1|2>
- mode: full | degraded (code-first, no browser tool)

| axis | verdict | evidence |
| ---- | ------- | -------- |
| brief-fidelity | PASS | <file + region; which point/constraint it answers> |
| strangeness | PASS | <walkthrough symptom + file/element + width> |
| slop-scan | FAIL | <hits N/26; file; per-hit note> |
| direction-fidelity | PASS | <DNA claim -> file; §C5 failure mode avoided> |
| variant-diversity | PASS | <option realised per variant; structural diff on the axis> |

## Findings

- {"severity": "blocker", "target": "variants/b/index.html", "evidence": "<exact HTML/CSS + where>", "why": "<impact on the deliverable>", "fix": "<smallest change that clears it>"}
- {"severity": "major", "target": "variants/a/detail.html", "evidence": "<exact HTML/CSS + where>", "why": "<impact>", "fix": "<smallest change>"}

## Open (not fixed)

- minor: <target — evidence — why it was left open>
- assumption: <what could not be verified in degraded mode>
```
