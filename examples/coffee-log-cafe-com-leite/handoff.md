# Handoff — coffee-log-cafe-com-leite
- direction: `D10 — Blueprint / Schematic`
- source: chosen variants in `chosen/` + `direction.json`
- tokens: `tokens.css` · styleguide: `styleguide.html`

## Components
- name: Topbar
  states: default, sticky (pinned on scroll)
  fidelity: intentional
  where: `chosen/d1/index.html` (`.topbar`) — decision: `decisions.md` (d1)
- name: Back chip
  states: default, hover, focus-visible
  fidelity: intentional
  where: `chosen/d1/index.html` (`.topbar__back`, links to `../../index.html`) — decision: `decisions.md` (d1)
- name: Nav
  states: default, current (`aria-current="page"`)
  fidelity: intentional
  where: `chosen/d1/index.html` + `chosen/d1/detail.html` (`.nav a`) — decision: `decisions.md` (d1)
- name: Feed entry
  states: default, hover, focus-visible
  fidelity: intentional
  where: `chosen/d1/index.html` (`.entry__link` row: strip / title / notes / foot) — decision: `decisions.md` (d1)
- name: Score gauge
  states: 0…5 ticks filled
  fidelity: intentional
  where: `chosen/d1/index.html` (`.gauge`, `role="img"` + `aria-label="nota N de 5"`); also `chosen/d1/detail.html` — decision: `decisions.md` (d1)
- name: Spec list
  states: default
  fidelity: intentional
  where: `chosen/d1/detail.html` (`.read__specs`, `<dl>` of dose/água/razão/tempo/moagem) — decision: `decisions.md` (d1)
- name: Annotation label
  states: default
  fidelity: intentional
  where: `chosen/d1/detail.html` (`.annot`, red margin note) — decision: `decisions.md` (d1)
- name: Title block
  states: default
  fidelity: intentional
  where: `chosen/d1/index.html` + `chosen/d1/detail.html` (`.titleblock`, sheet footer) — decision: `decisions.md` (d1)

## Fidelity notes
- intentional: the D10 register — inverted white-blue paper (`--color-bg`), a
  graph-paper field built from `repeating-linear-gradient`, zero radius, 2px
  linework rules on odd rows and hairlines on even rows (`rhythm: odd-first`),
  a single cyan accent (`--color-accent`), and the title-block footer that reads
  as a blueprint sheet. Fonts are Archivo Narrow (display) + Space Mono
  (body/mono), each with a same-class offline fallback.
- placeholder: all coffee entries are illustrative copy (invented origins,
  methods, ratios and notes — no real log data); there are no binary assets and
  no image files — "imagery" is CSS/SVG only (corner brackets, and in the
  rejected variants a hatched plate). Every link except the internal
  `index.html`/`detail.html`/`../../index.html` navigation is a dead end by
  design.
- not built: the brief's out-of-scope surfaces are not present in the chosen
  variant — no create/edit form, no search or filter, no empty state, no
  statistics. They were dropped candidate points, not omissions of this point.
