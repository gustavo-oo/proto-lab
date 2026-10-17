# Slop fingerprints

`references/slop-fingerprints.md` is the normative specification of pipeline
layer 3: the **AI-slop scan** that runs before a human ever opens a prototype.
It ports §B of the directions draft (`docs/research/directions-draft.md`) into 26
numbered `F01`–`F26` fingerprints and fixes the mechanical mapping that
`scripts/check_slop.py` (T09) implements and the judge (T16) consumes.

A fingerprint is never a verdict on its own. Any single item can be a legitimate
choice for a direction; what reads as slop is the **cluster**. Count one hit per
matching fingerprint, and **`≥ 4 hits` on a single page = fail**. A page at 3
hits passes. This is the same threshold as the global constraint (slop `≥ 4
hits` = reprova) and as `slop-scan` in `references/judge-rubric.md`.

Each hit records the fingerprint id and a confidence (`solid` = the detection
deterministically matched; `heuristic` = the pattern matched and the direction
does not justify it). Only hits whose direction does not legitimately earn the
pattern are counted.

## Fingerprints

`mechanical` fingerprints have a rule id (`R01`–`R22`) and a rule-based
detection spec; `judge-only` fingerprints have no rule and are evaluated by the
judge (T16) on the rendered artifact.

| ID | Fingerprint | Class | Rule |
| -- | ----------- | ----- | ---- |
| F01 | Inter/Roboto/system-ui as the only family | mechanical | R01 |
| F02 | Indigo-to-purple gradient on hero/CTA/glow | mechanical | R02 |
| F03 | Gradient-clipped headline text | mechanical | R03 |
| F04 | Dark mode = `#000`/`#0a0a0a`/`#0f172a`/`#111827` + one neon accent | mechanical | R04 |
| F05 | Identical soft shadow on every card | mechanical | R05 |
| F06 | `rounded-2xl` on everything | mechanical | R06 |
| F07 | Exactly three equal feature cards | mechanical | R07 |
| F08 | Lucide-style icon in a rounded square per card | mechanical | R08 |
| F09 | Emoji as icons or bullets | mechanical | R09 |
| F10 | "Now in beta" pill over the hero headline | mechanical | R10 |
| F11 | Centred hero stack: eyebrow to big h1 to subhead to 2 CTAs | mechanical | R11 |
| F12 | Glassmorphism by default | mechanical | R12 |
| F13 | Blob/mesh/aurora/"dot-grid" backgrounds | mechanical | R13 |
| F14 | Cream + amber "warm" second-wave palette | mechanical | R14 |
| F15 | Grey body text below contrast | mechanical | R15 |
| F16 | Cards nested in cards, 3-5 deep | judge-only | judge-only |
| F17 | Coloured-left-border callout boxes | mechanical | R16 |
| F18 | Uniform 8px spacing; identical section padding | judge-only | judge-only |
| F19 | shadcn defaults shipped as-is | mechanical | R17 |
| F20 | "Trusted by" logo bar with grey fake logos | mechanical | R18 |
| F21 | Invented stat row (10x, 99.9%) | judge-only | judge-only |
| F22 | No imagery, or suspiciously smooth synthetic imagery | judge-only | judge-only |
| F23 | Fade-up on everything | mechanical | R19 |
| F24 | Theme toggle on a marketing page | mechanical | R20 |
| F25 | Glowing status dot + "All systems operational" | mechanical | R21 |
| F26 | Gradient-border "AI card" glow | mechanical | R22 |

## Mechanical rules R01-R22

Every rule has a detection spec and a kind: `solid` when a deterministic match
decides it, `heuristic` when the pattern is a signal that may be earned by the
direction and needs context to count.

| Rule | Fingerprint | Detection spec (regex / heuristic) | Kind |
| ---- | ----------- | ---------------------------------- | ---- |
| R01 | F01 | `solid` regex: exactly one `font-family` declaration page-wide and its first family is one of `Inter`, `Roboto`, `system-ui`, and no other family is declared; respect the card's allowlist if the direction names a face. | solid |
| R02 | F02 | `solid` regex: `/6366f1|8b5cf6|7c3aed|a855f7/i` appearing inside a `linear-gradient(` (or a `from-indigo`/`violet-` utility). | solid |
| R03 | F03 | `solid` regex: `-webkit-background-clip:text` (or `background-clip:text`) co-occurring with a `background-image:linear-gradient(` on the same h1/h2 rule. | solid |
| R04 | F04 | `heuristic`: body background in `{#000,#0a0a0a,#0f172a,#111827}` AND at most one saturated accent hue and no midtones or warm blacks. | heuristic |
| R05 | F05 | `heuristic`: at least 5 `box-shadow` declarations whose blur is 8-24px and whose alpha is <= .15, with no distinct elevation roles. | heuristic |
| R06 | F06 | `heuristic`: at most 2 distinct `border-radius` values page-wide, at least 6 occurrences, and the values fall in 12-16px. | heuristic |
| R07 | F07 | `heuristic`: `repeat(3,1fr)` or `1fr 1fr 1fr` with exactly 3 children at the start of the body. | heuristic |
| R08 | F08 | `heuristic`: at least 3 blocks with a 24px `<svg` carrying `stroke="currentColor"` inside a container with padding and radius. | heuristic |
| R09 | F09 | `solid` regex: a unicode emoji range inside `h1`-`h6`, `button`, or `li`. | solid |
| R10 | F10 | `heuristic`: `border-radius:9999px` pill plus `/beta/i` micro-text immediately before the h1. | heuristic |
| R11 | F11 | `heuristic`: a container with `text-align:center`, an h1 at 56px or larger, and 2 sibling CTAs. | heuristic |
| R12 | F12 | `heuristic`: `backdrop-filter` plus `rgba(255,255,255,.1)` panel background plus text inside it. | heuristic |
| R13 | F13 | `heuristic`: `filter:blur(60-120px)` on absolutely-positioned gradient circles or a repeating radial-gradient dot field. | heuristic |
| R14 | F14 | `heuristic`: background in `{#faf8f4,#f5f0e8}` plus an amber/stone accent. | heuristic |
| R15 | F15 | `solid` regex: body text colour `#6b7280`, `#9ca3af`, or `#94a3b8`. | solid |
| R16 | F17 | `heuristic`: `border-left: 2-4px` plus a tinted background, at least 2 occurrences. | heuristic |
| R17 | F19 | `solid` regex: CSS vars `--primary: 221.2 83.2% 53.3%` or `--radius: 0.5rem` plus slate/zinc neutrals. | solid |
| R18 | F20 | `heuristic`: a "trusted by" line plus at least 4 svg wordmarks at `opacity:.5`. | heuristic |
| R19 | F23 | `heuristic`: `IntersectionObserver` plus a `translateY` fade-up applied to at least 4 sections. | heuristic |
| R20 | F24 | `solid` regex: `localStorage` plus `theme` on a page that has a hero. | solid |
| R21 | F25 | `solid` regex: `#22c55e` plus a box-shadow glow plus text matching `/operational/i`. | solid |
| R22 | F26 | `solid` regex: `background-clip: padding-box,border-box` plus a transparent border. | solid |

A rule row's `solid`/`heuristic` kind is the confidence recorded for its hit; a
`solid` match always counts, a `heuristic` match counts unless the direction
legitimately earns the pattern (see Fingerprints above).

## Judge-only fingerprints and second-order slop

Four fingerprints cannot be decided by a regex and are `judge-only`:

- **F16** — cards nested in cards, 3-5 deep: count the ancestor chain of
  `bg + border + radius + padding` (`.card > .card > .card`). `judge-only`.
- **F18** — uniform 8px spacing and identical section padding: at most 3 distinct
  padding values, every section at a `py-24`-equivalent, one gap everywhere. `judge-only`.
- **F21** — invented stat row: three number+label pairs whose numbers are round
  and absent from any copy or source. `judge-only`.
- **F22** — no imagery, or suspiciously smooth synthetic imagery: zero raster
  assets in the hero, or uniformly smooth 3D blobs/clay characters/mesh
  gradients. `judge-only`.

The judge also owns the **second-order slop** that rule-based scans miss, per
§C4 step 7: cream + Playfair + gold, false distress, glow + purple,
chrome-on-everything, and "luxury dark" (two luxury registers averaged). These
are reported as findings against `slop-scan` in the judge report and are never
re-litigated as a rule.

## Counting

1. Run every `R01`-`R22` detection spec against each variant page.
2. Record one hit per matching fingerprint, with its fingerprint id and
   confidence (`solid` or `heuristic`).
3. Add the `judge-only` hits (F16, F18, F21, F22) and any second-order slop
   cluster the judge confirms.
4. Sum the total hits: **`≥ 4 hits` on a page = fail**; at 3 or fewer the page
   passes. The boundary is exact — 3 passes, 4 fails.
5. The judge (`slop-scan` axis) consumes this result and never re-litigates a
   fingerprint the direction legitimately earns.
