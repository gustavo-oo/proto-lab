# Handoff format

`references/handoff-format.md` is the normative specification of pipeline step 5
(§5.6): the **post-choice artifacts** the skill writes into
`prototypes/<slug>-<seed>/` once a human has picked a winner per decision point.
It defines the HANDOFF ARTIFACTS that downstream consumers read (T16/T19) —
`decisions.md`, `tokens.css`, `styleguide.html`, `handoff.md` and `chosen/` — so
the shapes below are an interface, not a suggestion.

After the choice, the loop is over: the judge has already gated the variants,
the human has picked, and what remains is to hand the picks off **faithfully**.
The generator is not allowed to redesign at this step; it only transcribes.

## The derivation rule

> **Everything in the handoff is derived only from the chosen variants + the
> direction card** (and, in fit mode, `style-snapshot.json`).

This is the load-bearing rule of the whole step. The handoff is a lossless
extraction, not a new design pass:

- every token value comes from a value that already exists in a chosen variant
  or from `direction.json` (the source of truth, no timestamp);
- every component documented in `handoff.md` is one that actually appears in a
  chosen variant, in the states it appears in;
- nothing new is invented, "cleaned up", or averaged. If a chosen variant has no
  table, the styleguide has no table. If two chosen variants disagree, the
  `decisions.md` log records which one won and why — it never blends them.

If a value cannot be traced to a chosen variant or the direction card, it does
not go in the handoff. Derivation is what makes the artifacts trustworthy: a
consumer can always walk back from a token to the variant that earned it.

## decisions.md

The choice log. It records, for every decision point, **what was chosen** and
**what was rejected and why** — including rerolls (a discarded seed and its
reason, per `references/seed-algorithm.md`). It is the one artifact where the
"why" lives; `chosen/` holds only the winners.

Copy the template, replace the placeholders, delete nothing structural:

```markdown
# Decisions — <slug>-<seed>
- seed: `<seed>` (recorded; source of truth is `direction.json`)
- direction: `<DNN> — <direction name>` (fit mode: `FIT — Existing system`)
- snapshot: `<hash>` (fit mode only)
- points: <N> (cap 4)

## Chosen
- d1 — <point question> — chosen: variant `d1-b` — option "<structural description>"
  - why: <one line tying the pick to the brief/point, no new rationale invented>
  - source: `variants/d1-b/`
- d2 — <point question> — chosen: variant `d2-a` — option "<structural description>"
  - why: <...>
  - source: `variants/d2-a/`

## Rejected (and why)
- d1-a — option "<...>" — rejected because <structural reason: closer to another
  option, weaker on the declared axis, did not answer the point>
- d1-c — option "<...>" — rejected because <...>
- reroll — seed `<discarded seed>` → direction `<DNN>` discarded because
  <reason: family repeat, comfort pick, brief conflict>; replaced by the seed above.
```

Rules: one `## Chosen` entry per point, matching a folder copied into `chosen/`;
one line per rejected variant; rerolls are `Rejected`, not deleted. A point with
no explicit pick is not a choice — say so and stop.

## tokens.css

The core scales of the chosen direction, expressed as CSS custom properties. It
is a single flat file — no build, no imports — so a consumer can drop it into
any page and open it via `file://`. Only values traceable to a chosen variant or
the direction card appear here.

Convention: **every** custom property is namespaced by role with one of five
prefixes. No unprefixed variables, no ad-hoc names.

| prefix | holds | examples |
| ------ | ----- | -------- |
| `--color-*` | palette roles | `--color-bg`, `--color-ink`, `--color-accent`, `--color-muted` |
| `--font-*` | families + type scale | `--font-body`, `--font-display`, `--font-mono`, `--font-size-*` |
| `--space-*` | spacing scale | `--space-1`…`--space-8` |
| `--radius-*` | corner language | `--radius-sm`, `--radius-md`, `--radius-pill` |
| `--motion-*` | durations + easing | `--motion-fast`, `--motion-slow`, `--motion-ease` |

```css
/* tokens.css — core scales of <DNN>, derived from the chosen variants. */
:root {
  /* --color-* : palette roles (accent within the direction's logic) */
  --color-bg: #...;
  --color-ink: #...;
  --color-accent: #...;
  --color-muted: #...;

  /* --font-* : <=2 families + <=1 mono, each with a same-class fallback */
  --font-display: "<webface>", <same-class fallback stack>;
  --font-body: "<webface>", <same-class fallback stack>;
  --font-mono: "<mono>", ui-monospace, monospace;
  --font-size-step: <clamp(...)>;

  /* --space-* : one spacing scale */
  --space-1: ...;
  --space-2: ...;

  /* --radius-* : the direction's form language (uniform radius is a slop tell) */
  --radius-sm: ...;
  --radius-md: ...;

  /* --motion-* : durations + easing character */
  --motion-fast: <duration>;
  --motion-ease: <easing>;
}
```

Rules: the font stacks carry a **same-class fallback** (offline must keep the
register, §5.3); colors come from the variant palette, not a fresh pick;
`styleguide.html` and any downstream component must consume these variables
rather than re-declaring literals.

**Fit mode.** Keep the existing custom-property names and values. When a
consumer needs the five-prefix convention, add role aliases that point at the
existing name and value; never rename or re-value the source token. An approved
extension is marked in the file and cites its gate approval in `decisions.md`.

## styleguide.html

The static mini design system of the pick: **one file**, no build, opens via
`file://`. It makes the tokens visible and shows the main components in their
key states — same direction as the chosen variants, nothing restyled.

It must contain:

- a **token panel** that renders the `tokens.css` scales visibly (color swatches,
  type specimens, spacing/radius/motion samples) — the visual index of the file
  above;
- the **principal components** that actually appeared across the chosen variants
  (e.g. button, input, card, nav, table — only the ones that appeared), each
  shown in its key states (default / hover / focus / active / disabled, or the
  states the variants used);
- a link to `tokens.css` (`<link rel="stylesheet" href="tokens.css">`) so the
  page is the single source for token usage in markup;
- at most a minimal inline script (`< = 30` lines) if a state toggle is needed;
  no cross-frame scripting.

Empty by construction if no chosen variant had a component: the styleguide
invents nothing.

## handoff.md

The component inventory for whoever implements from the prototype. It lists what
exists, its states, and — honestly — **what is intentional and what is a
placeholder**. It also points back to where each decision was recorded.

```markdown
# Handoff — <slug>-<seed>
- direction: `<DNN> — <direction name>` (fit mode: `FIT — Existing system`)
- source: chosen variants in `chosen/` + `direction.json` (fit mode: + `style-snapshot.json`)
- existing system: `<source>` · snapshot `<hash>` (fit mode only)
- tokens: `tokens.css` · styleguide: `styleguide.html`

## Components
- name: Button
  states: default, hover, focus, active, disabled
  origin: reused | new | extension (fit mode)
  fidelity: intentional
  where: `chosen/d1/`, `styleguide.html#button` — decision: `decisions.md` (d1)
- name: Card
  states: default, hover
  origin: reused | new | extension (fit mode)
  fidelity: placeholder
  where: `chosen/d2/` — decision: `decisions.md` (d2); image area is a CSS/SVG placeholder
- name: Nav
  states: default, collapsed
  origin: reused | new | extension (fit mode)
  fidelity: intentional
  where: `chosen/d1/index.html` — decision: `decisions.md` (d1)

## Fidelity notes
- intentional: <what is deliberate — the grid, the type scale, the motion
  character, the placeholder-imagery genre per the direction>.
- placeholder: <what stands in for real content — copy is lorem/illustrative,
  images are CSS/SVG placeholders (no binary assets, §4), links are dead ends
  by design>.
- not built: <screens/states the prototype never covered — out of scope for the
  point, not implied by the handoff>.
```

Rules: one entry per component that **actually appears** in a chosen variant;
`fidelity` is exactly `intentional` or `placeholder` (no third value); every
entry cites where it lives and which `decisions.md` point it came from; the
`## Fidelity notes` section restates the placeholder policy (CSS/SVG imagery,
illustrative copy) so nothing is mistaken for production-ready.

## chosen/

The winners, copied — not linked, not symlinked (the prototype folder must
survive being zipped and moved; `file://` opening must work). One subfolder per
decision point, holding the chosen variant's mini-project as-is:

```
chosen/
  d1/            # copy of variants/d1-b/ (the pick for point d1)
  d2/            # copy of variants/d2-a/
```

Rules: exactly one picked variant per point — no "runner-up" copies; the copies
are byte-identical to the `variants/` source (paths inside must stay relative so
navigation still works via `file://`); the mapping from `chosen/<point>/` back to
its point and its rationale is written in `decisions.md` (`## Chosen`). `chosen/`
carries no rationale of its own — it is the artifact, the log is the story.
