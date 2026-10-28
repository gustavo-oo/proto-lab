# Fit mode

`references/fit-mode.md` is the normative specification of **fit mode**: the
second way proto-lab can source a visual direction. It defines the STYLE
SNAPSHOT, the FIT CARD and the rules that keep a fit session from becoming a
repaint machine.

Explore mode (the default) draws one of the 22 catalogue directions. Fit mode
does not draw: it captures the visual system the target already uses and treats
that captured system as the direction. The seed no longer chooses a look; it is
only the session label.

## The two modes

| Mode | Visual direction comes from | Catalogue draw | Reroll |
|---|---|---|---|
| `explore` (default) | one of the 22 directions, drawn from the seed | yes | a new seed is free at step 2 |
| `fit` (`--fit <source>`) | `style-snapshot.json`, captured from the existing system | no | not applicable; correct the snapshot instead |

Both modes keep the rest of the pipeline: the single step-3 gate, structural
variants per decision point, the fresh-eyes judge, research, the copy gate and
the handoff. **Fit mode changes where the visual language comes from; it does not
relax structural divergence.** A fit session whose variants are three recolours
of one layout fails `variant-diversity` exactly like an explore session.

Fit mode is not a pixel-copy tool and not a rebrand tool. It is for a new
surface, flow or screen that must belong to an existing product.

## When to use

- Adding a screen or flow to an existing product with a settled visual system.
- Redesigning one screen while keeping the product's identity.
- Prototyping inside an existing design system or component library.

## When not to use

- A rebrand or a new visual identity: use explore mode.
- A pixel-perfect clone of one page: use the real code and components.
- No access to the existing visual system and no one who can confirm it: ask for
  a token file, a URL or screenshots; if none arrives, use explore mode.

## Pipeline step 1 — declare the source

Fit mode is opt-in: the brief must carry `--fit <source>`, where `<source>` is
one of:

- a repository path, or a token/theme file inside it — the `declared` code-first
  path;
- a URL of the running page — the `observed` path when a browser tool exists;
- a design-token file (`tokens.json`, `design-tokens.json`, `DESIGN.md`) — the
  `declared` path when the code is not accessible.

No `--fit` means explore mode. The skill never starts a fit session by reading
the target's UI on its own. If the user asks to "match the app" without naming a
source, ask once for the URL, the token file or the repo path (within the ≤ 3
questions budget) and record the answer in `brief.md`. A source that does not
resolve is a blocker at the step-3 gate, not a reason to guess.

## Pipeline step 2 — capture, not roll

Fit mode replaces the step-2 roll with a capture:

```bash
python3 "$SKILL_DIR/scripts/snapshot.py" \
  --from <repo path | URL | tokens file> \
  --extra "$WORK/fit-extra.json" \
  --out "$WORK/style-snapshot.json" \
  --card "$WORK/direction.json" \
  --name "<product>"
```

`snapshot.py` extracts CSS custom properties and font families from the source,
merges the authored `--extra` sections (components, layout, voice, constraints,
extensions, inherited slop), validates the schema, computes the hash and writes
the fit card. A URL source never touches the network: the executor captures the
computed styles and components in `--extra`, and the script normalises them.
The snapshot is the source of truth; the card only points at its hash.

After any hand edit, run the verifier; drift stops the run:

```bash
python3 "$SKILL_DIR/scripts/snapshot.py" --check "$WORK/style-snapshot.json"
```

A hash mismatch, an absolute path, a timestamp, a missing required key or a cap
overflow is an error, not a warning. The snapshot is never silently repaired.

## Pipeline step 3 — the single gate

Fit mode does not add a second gate. The existing step-3 gate now confirms
three artifacts together:

1. `style-snapshot.json` — the captured visual system, including `gaps`;
2. `direction.json` — the fit card, whose `snapshot.hash` matches the snapshot;
3. `points.json` — the decision points and their structural options.

The gate message states the source, the evidence level, the token and component
counts, and every open gap. For each gap the user may:

- supply the missing value — edit the snapshot and re-run `--check`;
- approve an extension — add it to `extensions[]` with
  `approved_at_gate: true`;
- accept the gap as out of scope — record it and keep it visible.

A correction changes the snapshot hash, so the card is regenerated before
generation starts. Present the corrected pair, not only the changed file.

**Nothing is generated before an explicit OK.** That includes `research.md` and
variant content; the `variants/` tree may hold only the scaffolder skeletons. In
a non-interactive harness, present the snapshot + card + points and end the
turn — the answer is missing, not the gate.

*Observable:* at turn end `research.md` is absent and every
`variants/<point>-<option>/` directory holds only the untouched `index.html`
shell. A corrected snapshot has a new hash, and the card's `snapshot.hash`
matches it.

## Rules that do not bend

1. **The snapshot is the only source of visual values.** Every colour, family,
   size, spacing step, radius, shadow and motion value in a variant traces to a
   snapshot token or to an approved extension. No eyeballed equivalents.
2. **Structural divergence stays mandatory.** Each decision-point option is a
   structural answer; visual deltas never count as diversity.
3. **Read visual sources only.** Theme/tokens files, global CSS, component
   primitives, computed styles and screenshots. Never business logic, API
   clients, data models or test fixtures.
4. **Provenance or it did not happen.** Every captured value carries a source
   (file and line, selector, or URL) and an evidence level.
5. **No silent invention.** A missing value is a `gaps` entry resolved at the
   step-3 gate, never a guess the generator quietly fills in.

## Evidence levels

A snapshot is only as trustworthy as the evidence behind it. Each token and
component carries one of these levels, and the snapshot carries the strongest
level its inputs justify.

| Level | Source | Meaning |
|---|---|---|
| `observed` | a browser tool on the running page: computed styles and screenshots | the current rendered result; strongest |
| `declared` | token files, theme files, global CSS, `tailwind.config.*`, `DESIGN.md` | the system as authored; may drift from the render |
| `inferred` | heuristics over CSS or a screenshot alone | a best reading; must be confirmed at the gate |

A `declared` snapshot is the normal code-first path. Upgrade individual values
to `observed` when a browser tool can read them. An `inferred` snapshot is
allowed only when the gate confirms it; the judge records the level in the
report header.

`observed` is the strongest level: the browser reads the rendered page, so it
sees what the user sees rather than what the stylesheet intended. Capture the
computed values of the page shell and the component recipes (box metrics, type,
border, radius, shadow, colour), plus screenshots for the judge's comparison.
Screenshots are evidence, not artifacts: do not commit binary images into the
session (the no-binary-assets rule still holds). Record the URL and selectors
instead, and let the judge reopen the page when a browser is available.

`declared` is the code-first fallback: the values come from the system's own
token and theme files, which are authoritative for intent but may drift from
the rendered page (unused tokens, overrides, runtime theming).

`inferred` is the weakest level: the values come from CSS heuristics or a
screenshot with no token source. It is allowed only when the step-3 gate
confirms the reading; the snapshot must say so, and the judge treats any
rendered claim as an assumption.

## Source scope and caps

Read the smallest set of files that contains the visual source of truth:

- token/theme files (`tokens.css`, `theme.*`, `design-tokens.json`);
- global styles and reset;
- component primitives (button, input, card, nav, table/list row, badge,
  dialog) and their states;
- the page shell (max width, gutters, navigation model, density, breakpoints);
- optional voice samples from real UI strings.

Hard caps:

| Cap | Value |
|---|---|
| Source files read | ≤ 8 |
| Components captured | ≤ 12 |
| Voice samples | ≤ 5 |
| Inherited fingerprints | all found on the existing page, each with evidence |

Do not read the rest of the repository "for context". If the visual source is
not in the first eight files, ask for the token file or URL.

## Snapshot schema

`style-snapshot.json` is canonical JSON (sorted keys, compact separators), has
no timestamp and carries relative paths only. Its top-level keys are exactly
those below.

```json
{
  "schema": "style-snapshot:v1",
  "evidence": "declared",
  "source": {
    "kind": "repo",
    "root": ".",
    "files": ["src/styles/tokens.css", "src/styles/global.css"],
    "url": null,
    "notes": "logged-out shell, light theme"
  },
  "tokens": {
    "color": [
      {
        "role": "bg",
        "name": "--color-bg",
        "value": "#f7f5f0",
        "source": "src/styles/tokens.css:12",
        "evidence": "declared"
      }
    ],
    "font": [
      {
        "role": "body",
        "name": "--font-body",
        "value": "\"Söhne\", system-ui, sans-serif",
        "source": "src/styles/tokens.css:20",
        "evidence": "declared"
      }
    ],
    "space": [],
    "radius": [],
    "shadow": [],
    "motion": [],
    "breakpoint": []
  },
  "type": {
    "families": ["Söhne", "Söhne Mono"],
    "scale": [
      {
        "role": "display",
        "size": "clamp(2.5rem, 5vw, 4rem)",
        "weight": 600,
        "line_height": 1.05,
        "letter_spacing": "-0.02em",
        "source": "src/styles/tokens.css:31",
        "evidence": "declared"
      }
    ]
  },
  "components": [
    {
      "name": "Button",
      "selector": ".btn",
      "states": ["default", "hover", "focus", "disabled"],
      "facts": {
        "height": "40px",
        "padding": "0 16px",
        "radius": "6px",
        "border": "1px solid #d8d4cb",
        "font": "500 14px/1 Söhne",
        "background": "#1d1b17",
        "color": "#f7f5f0"
      },
      "source": "src/components/Button.module.css:1-40",
      "evidence": "declared"
    }
  ],
  "layout": {
    "shell": "fixed sidebar plus scrolling content",
    "max_width": "1200px",
    "gutters": "clamp(16px, 3vw, 32px)",
    "nav_model": "fixed sidebar",
    "density": "comfortable",
    "breakpoints": ["768px", "1024px"]
  },
  "voice": {
    "samples": ["Save changes", "No invoices yet. Create your first one."],
    "terminology": ["invoice", "client", "draft"],
    "casing": "sentence case"
  },
  "constraints": ["Flat surfaces only; no gradients.", "One accent per screen."],
  "extensions": [],
  "inherited_slop": [
    {
      "rule": "R05",
      "fingerprint": "F05",
      "evidence": "existing page: 5 soft box-shadows",
      "source": "https://app.example.test/invoices"
    }
  ],
  "gaps": ["Dark theme not captured.", "Table empty state not found."],
  "hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}
```

Normative rules:

1. **`schema`** is the literal `"style-snapshot:v1"`.
2. **`evidence`** is the strongest level the snapshot as a whole justifies:
   `observed`, `declared` or `inferred`. Individual entries may be weaker than
   the header only if they say so; never stronger.
3. **`source.root`** is `"."` in the canonical form; every path in `source.files`,
   token `source`, component `source` and evidence is relative to it. Absolute
   paths, home directories and timestamps are invalid.
4. **`tokens`** groups are arrays of `{role, name, value, source, evidence}`.
   Roles are semantic (`bg`, `surface`, `ink`, `muted`, `border`, `accent`,
   `accent-ink`, `success`, `warn`, `danger`); names are the existing property
   names when they exist. A role with no value is a `gaps` entry, not a blank.
5. **`components`** captures only components the new screens will use. `facts`
   holds the smallest set of values needed to reproduce the component: box
   metrics, type, border, radius, shadow, colour and the states that exist.
   Missing states are gaps; do not invent hover/focus/disabled recipes.
6. **`layout`** captures the page shell, not a screen's content layout. Structural
   content decisions belong to `points.json`.
7. **`voice`** is optional. Samples are short strings copied from the existing UI
   (≤ 5), used as tone evidence, never as copy to paste into variants.
8. **`extensions`** is the only place a new visual value may appear. Each entry
   is `{role, name, value, reason, approved_at_gate: true}`. The gate must approve
   the extension before generation; an unapproved extension fails the judge.
9. **`inherited_slop`** records the slop fingerprints the existing system already
   has, with rule id, fingerprint, evidence and source. It is a baseline, not a
   licence: new pages are judged on **new** hits.
10. **`gaps`** lists what could not be captured. A gap is resolved at the gate
    (the user supplies the value, approves an extension, or accepts the gap as
    out of scope); it is never silently filled.
11. **`hash`** is `sha256:<hex>` over the canonical JSON of the snapshot with the
    `hash` key removed. The same source and values always produce the same hash;
    the same hash always identifies the same snapshot.

## Extraction protocol

1. **Locate the source.** Prefer a running URL with a browser tool. Otherwise a
   repository path whose token/theme files are known. Otherwise a screenshot or
   a `DESIGN.md`; mark the result `inferred` and confirm it at the gate.
2. **Capture the tokens by role.** Read `:root` custom properties, theme objects,
   `@font-face` and font-family declarations. Copy values verbatim; do not
   normalise hex, rem or clamp expressions.
3. **Capture the type scale.** Families, sizes, weights, line heights and letter
   spacing for the roles the new screens will use (display, heading, body, label,
   mono/data).
4. **Capture component recipes.** For each component the new screens need, record
   its selector, the states that exist, and the facts above. Use a browser's
   computed styles when available; otherwise the component's CSS.
5. **Capture the layout shell.** Max width, gutters, nav model, density and
   breakpoints. Do not capture a full page's content grid — that is a structural
   decision.
6. **Capture voice samples (optional).** Copy at most five short strings from the
   real UI. Do not paraphrase them.
7. **Record inherited fingerprints.** If the existing page HTML is available, run
   `scripts/check_slop.py` on it and record every hit in `inherited_slop`; this
   is the baseline the judge subtracts. If no HTML is available, record an
   explicit gap.
8. **Write and verify.** Write the snapshot with `scripts/snapshot.py`, then run
   `--check`; a hash mismatch or a schema violation stops the pipeline.
9. **Gate.** Present the snapshot, the fit card and `points.json` together. The
   user confirms or corrects the snapshot before any generation. A correction
   changes the hash and therefore the card.

## Fit card

Fit mode writes a `direction.json` with the same canonical encoding as explore
mode, plus two keys. Explore cards keep exactly the eight keys in
`references/seed-algorithm.md`; fit cards have exactly these ten:

| Key | Type | Value |
|---|---|---|
| `mode` | string | literal `"fit"` |
| `seed` | string | `fit-<hash8>` by default, or an explicit `--seed` |
| `algorithm` | string | literal `"snapshot:v1"` |
| `direction_id` | string | literal `"FIT"` — a sentinel, not a 23rd catalogue direction |
| `direction_name` | string | `"Existing system — <name>"` |
| `family` | string | literal `"existing"` |
| `knobs` | object | `{}`; fit mode has no catalogue knobs |
| `filters` | object | `{"domain": null, "excluded": []}` |
| `wild` | boolean | `false`; `--wild` is incompatible with `--fit` |
| `snapshot` | object | `{"path": "style-snapshot.json", "hash": "sha256:<hex>"}` |

Rules:

- The seed is a session label. It never changes the visuals; the same snapshot
  and seed always yield the same card. There is no visual reroll — to change the
  look, correct the snapshot and regenerate the card.
- `snapshot.path` is relative to the session directory; the scaffolder copies
  the snapshot there under that name.
- `snapshot.hash` must match the snapshot's `hash`; a mismatch is an error, not a
  warning.
- `--domain` is meaningless in fit mode (no catalogue draw) and is rejected.
- `--wild` is meaningless in fit mode (no catalogue draw) and is rejected.

## Generation rules

The step-5 generators receive `style-snapshot.json` alongside the card, brief,
point contract, research and the copy/UX references.

**Every variant inherits the same snapshot.** The point changes the structure,
never the visual base: all variants in a session share one palette, one type
family set, one radius language and one motion character. A variant that
introduces its own font, accent hue or corner radius is not a different
structural option; it is a second direction and fails `direction-fidelity`.

**No new fonts, accents or radii.** The generator may not add a family, choose a
new accent colour, introduce a new radius step or swap the shadow/motion
language. Those values exist only in the snapshot. A missing role is a `gaps`
entry resolved at the gate; a genuinely new value is an `extensions[]` entry with
`approved_at_gate: true`, recorded before generation. An unapproved extension
fails the judge.

- Every visual value traces to a snapshot token or an approved extension. If the
  style property is not in the snapshot, the generator does not invent it; it
  records the gap and stops at the gate.
- Components follow the captured recipes: box metrics, type, border, radius,
  shadow and the states that exist. A new component is composed from existing
  tokens and recorded as `new` in the handoff.
- One visual register per screen. Do not blend a catalogue direction, a
  competitor's palette or a new accent into the captured system.
- Structural variants are still structural. Each option implements its declared
  shape on the point's axis; a recolour is not a variant.
- Copy still obeys `references/copy-contract.md`. Voice samples guide tone; they
  are not filler and are not pasted verbatim as product copy.
- Research still runs by default. It informs structure and domain patterns; it
  never supplies visual tokens.

## Judge rules

The five axis names and the report template stay exactly as
`references/judge-rubric.md` defines them; fit mode redefines axis 4's evidence,
not the axis list. The judge receives `style-snapshot.json` and applies these
rules:

- **`direction-fidelity`** becomes the **snapshot-fidelity** check: every colour,
  family, size, spacing step, radius, shadow, motion value and component state
  traces to `style-snapshot.json` or an approved extension. A new unapproved
  token is a `major`; a screen whose visual register no longer belongs to the
  captured system is a `blocker`.
- **`slop-scan`** reports `visual: N new / M inherited; copy: C01..C04`. The
  fingerprints recorded in `inherited_slop` are listed but do not count toward
  the `>= 4` failure threshold. Any fingerprint not in the inherited baseline
  counts as new; `>= 4` new hits fail. A hit is inherited only when the same
  fingerprint id is recorded in `inherited_slop`; a lookalike with different
  evidence is new. The copy gate stays zero-tolerance.
- **`variant-diversity`** is unchanged: structural diff on the declared axis,
  never a cosmetic diff.
- The report header carries `- fit mode: fit` and `- snapshot: <hash>` in
  addition to the existing provenance lines. The judge receives
  `style-snapshot.json`.
- If a browser tool and a URL are available, the judge may reopen the existing
  page to compare. Without one, it reads the snapshot and the artifacts
  code-first; the missing rendered comparison is an assumption, not a lower bar.
- Inherited fingerprints are a baseline, not a licence. New slop introduced by
  the fit generation still fails.

## Handoff rules

- **Derivation:** in fit mode the handoff derives from the chosen variants, the
  fit card **and** `style-snapshot.json`. A token that traces to neither is not
  written.
- **`tokens.css`:** preserve the existing property names and values where they
  exist; add role aliases only where a consumer needs the five-prefix convention.
  Every value traces to the snapshot or a chosen variant; approved extensions are
  marked.
- **`handoff.md`:** add `- mode: fit` and
  `- existing system: <source> · snapshot <hash>`. Each component entry carries
  `origin` in addition to the usual `name`/`states`/`fidelity` fields:

  ```markdown
  - name: Button
    states: default, hover, focus, disabled
    origin: reused
    fidelity: intentional
    where: `chosen/d1/`, `styleguide.html#button` — decision: `decisions.md` (d1)
  ```

  `origin` is exactly one of:

  | value | meaning |
  |---|---|
  | `reused` | the component and its recipe already exist in the snapshot |
  | `new` | composed for this session from existing snapshot tokens; no new visual value |
  | `extension` | uses a gate-approved `extensions[]` value; `decisions.md` cites the approval |

- **`tokens.css`:** keep the existing custom-property names and values. When a
  consumer needs the five-prefix convention, add role aliases (`--color-accent`)
  that point at the existing name and value; never rename or re-value the source
  token. A fit handoff is a transcription, not a second design pass.
- **`styleguide.html`:** shows the existing components in their captured states,
  in the captured register. No restyling, no new components.
- **`decisions.md`:** records every snapshot correction and approved extension
  with its reason, alongside the usual chosen/rejected points. A fit session has
  no rerolled seeds; it has corrected snapshots.

## Degradation

| Edge case | Fallback |
|---|---|
| No browser tool | Use `declared` token files; mark `inferred` where only CSS heuristics are available. The gate confirms. |
| No access to the existing system | Ask for a token file, URL or screenshots. If none arrives, do not fake a snapshot; use explore mode. |
| Inline styles only | Read computed styles if a browser exists; otherwise mark `inferred` and confirm at the gate. |
| Multiple themes | Capture the default theme; record the others in `gaps`. The gate may request a second snapshot. |
| Node-only harness | `scripts/snapshot.py` is Python. Use it when Python is available; otherwise write the card by hand from this reference and record the degradation. |
| Non-interactive harness | The gate still applies: write the snapshot, fit card and `points.json`, present them and end the turn. No generation before an explicit OK. |
| Existing page has ≥ 4 slop hits | Record them in `inherited_slop`; new pages are judged on new hits. Do not hide the baseline. |

## Red flags

- "I'll eyeball the app and pick similar colours." — Capture with provenance or
  record a gap.
- "I'll improve the existing theme while I'm here." — Fit mode does not redesign;
  use explore mode for a new identity.
- "I'll blend one catalogue direction with the existing system." — Two registers
  averaged; the judge fails it.
- "I'll read the whole repository to understand the design." — Visual sources
  only, ≤ 8 files.
- "The snapshot is close enough." — Gaps and extensions are resolved at the gate,
  not by approximation.
- "Inherited slop means the slop gate is off." — Inherited hits are recorded; new
  hits still fail.
- "Fit mode means copy the DOM." — It captures a visual language; structural
  variants are still mandatory.
- "The seed will pick a direction that fits." — Fit mode has no catalogue draw.
