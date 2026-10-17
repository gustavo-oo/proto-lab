# Decision points

`references/decision-points.md` is the normative specification of pipeline
step 3: turning a brief into a small set of **decision points**, each with
named **structural options**, and recording them as `points.json`. It defines
the POINTS.JSON SCHEMA consumed by the variant generators and the judge.

A decision point is a question whose answer changes the *structure* of the
prototype, not its skin. "Sidebar vs top bar" is a point; "blue vs green" is
not (that belongs to the direction card, not the point). This distinction is
what keeps the variants divergent instead of cosmetic reskins.

## Taxonomy

Every point names one **axis** — a structural dimension drawn from the closed
vocabulary in **Axis vocabulary** — and 2–3 **named structural options** on
that axis. An option is a concrete, self-describing shape, written as a
kebab-case slug plus a short `label` and a one-line `descriptor`. Options must
be *incompatible shapes*, not degrees of the same shape.

The axes below are the closed set a point may declare. Each entry lists the
named shapes that are valid options on that axis (2–3 per point).

| Axis | Example structural options |
| ---- | -------------------------- |
| `navigation-model` | `sidebar-fixed`, `topbar-subnav`, `command-palette-minimal` |
| `listing-pattern` | `dense-table`, `card-grid`, `single-column-feed` |
| `information-density` | `comfortable`, `compact`, `progressive-disclosure` |
| `primary-action-placement` | `sticky-header-cta`, `inline-row-action`, `floating-primary` |
| `form-pattern` | `single-page-form`, `stepped-wizard`, `inline-edit` |
| `empty-states` | `illustrated-empty`, `inline-hint`, `zero-state-checklist` |
| `dashboard-composition` | `kpi-strip-grid`, `focus-hero-panel`, `narrative-sections` |
| `onboarding-shape` | `guided-overlay`, `inline-checklist`, `sample-data-tour` |
| `detail-presentation` | `full-page-detail`, `side-panel`, `expandable-row` |
| `filtering-search` | `persistent-filter-rail`, `command-search`, `chip-filter-bar` |

Two axes are never mixed in a single point: a point declares exactly one axis.
A variant is generated for a single point, so the option set must be small
enough to be read side by side (2–3 options, never more).

## Derivation

The skill derives candidate points from the brief, then trims them to a hard
cap. The rules are mechanical so the gate stays cheap to review.

1. **Collect 4–7 candidates.** Walk the brief for structural uncertainties:
   how people navigate, how a collection is listed, where the primary action
   lives, how a form is shaped, how empty/loading states read, how a dashboard
   is composed, how onboarding is delivered, how detail is presented and how
   filtering works. Each uncertainty that maps to a declared axis becomes a
   candidate.
2. **Trim to at most 4 points.** The cap is `<= 4 pontos/sessão`. If more than
   four survive, keep the ones with the largest blast radius on the brief's
   objective and drop the rest (record dropped candidates in `decisions.md`).
3. **Each point needs a clear question.** A point is rejected unless it can be
   phrased as one answerable question ("Where does the primary action live on
   the list screen?"). Vague prompts ("Make it feel better") are not points.
4. **Each point needs real impact.** A point is kept only if its options would
   change the structure or the flow of at least one screen. Cosmetic deltas
   (colour, radius, type scale) belong to the direction card.
5. **Declare screens.** `screens` lists the 2–3 screens the variants must
   build to exercise the point (e.g. `["index", "detail"]`). It is bounded by
   `<= 3 telas/variante`; a point never asks for a whole app.
6. **No overlapping axes.** Two kept points must not share an axis; merge them
   or drop the weaker one so divergence stays legible.

## Contract

The point is a contract between the skill, the generator and the judge.

- The **generator implements exactly the declared options.** For a point with
  options `a`, `b`, `c`, it produces one variant per option (3 variants; 2 is
  allowed via flag `--variants`). It may not invent a fourth shape, blend two
  options, or produce three reskins of one option.
- The **judge verifies the contract** on judge-rubric axis 5,
  **"variant-diversity"** (cross-variant diversity, §5.4): did each variant
  implement its promised option, and do the options differ structurally on the
  declared axis rather than cosmetically?
- Each variant is small and focused on the point: 2–3 linked screens that
  exercise the decision, never an app.
- A failing contract (missing option, blended or cosmetic variants) is a
  judge blocker and triggers a fix + re-judge within the `<= 2 rodadas` cap.

`points.json` is the wire format of this contract:

| Key | Type | Meaning |
| --- | ---- | ------- |
| `slug` | string | Session slug, matching the prototype folder. |
| `points` | array of point | The derived points (1–4 after trimming). |

Each **point** object has exactly these keys:

| Key | Type | Meaning |
| --- | ---- | ------- |
| `id` | string | Point id, `d1`…`d4`, stable across the session. |
| `question` | string | The single answerable question the point poses. |
| `why` | string | Why it matters for the brief (real impact). |
| `axis` | string | One axis from **Axis vocabulary**. |
| `options` | array of option | 2–3 named structural options. |
| `screens` | array of string | 2–3 screens the variants must build. |
| `status` | `"pending"` \| `"chosen"` \| `"rejected"` | Gate/choice state. |
| `chosen` | string \| null | The chosen option `key`, or `null`. |

Each **option** object has exactly these keys: `key` (`"a"`/`"b"`/`"c"`),
`label` (short human name) and `descriptor` (one-line structural description).

Example `points.json`:

```json
{
  "slug": "task-inbox",
  "points": [
    {
      "id": "d1",
      "question": "Where does the primary action live on the list screen?",
      "why": "The brief is action-first; placement decides the whole list layout.",
      "axis": "primary-action-placement",
      "options": [
        {"key": "a", "label": "Sticky header CTA", "descriptor": "One persistent action pinned in the header."},
        {"key": "b", "label": "Inline row action", "descriptor": "Each row carries its own primary action."},
        {"key": "c", "label": "Floating primary", "descriptor": "A single floating button over the list."}
      ],
      "screens": ["index", "detail"],
      "status": "pending",
      "chosen": null
    },
    {
      "id": "d2",
      "question": "How should the collection be listed?",
      "why": "Rows carry many fields; the listing shape drives scan speed.",
      "axis": "listing-pattern",
      "options": [
        {"key": "a", "label": "Dense table", "descriptor": "Column-aligned grid optimised for scanning."},
        {"key": "b", "label": "Card grid", "descriptor": "Card per item, hierarchical and image-friendly."}
      ],
      "screens": ["index"],
      "status": "chosen",
      "chosen": "a"
    }
  ]
}
```

## Axis vocabulary

The closed set of axes a point may declare. A point references exactly one of
these slugs; anything outside the list is not a decision point.

| Axis | Intent |
| ---- | ------ |
| `navigation-model` | How the app's top-level structure is traversed. |
| `listing-pattern` | How a collection of items is presented. |
| `information-density` | How much is shown per view and how it unfolds. |
| `primary-action-placement` | Where the main call to action sits. |
| `form-pattern` | How input is collected and committed. |
| `empty-states` | How the absence of data reads. |
| `dashboard-composition` | How summary/monitoring content is arranged. |
| `onboarding-shape` | How first-run guidance is delivered. |
| `detail-presentation` | How a single item's full record opens. |
| `filtering-search` | How users narrow and find items. |
