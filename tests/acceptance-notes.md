# Acceptance notes

Shared evidence file for the scenario tasks. **T19** (end-to-end example +
`file://` navigation) owns the section below; **T21** (reproducibility) appends
its own section underneath and must not edit T19's.

Screenshots are written to a temporary directory **outside the repository** and
are deliberately **not committed** — the global constraint forbids binary images
in the repo. The paths below are absolute and point at that temp directory.

## T19 — exemplo end-to-end + navegação `file://`

**Target.** `examples/coffee-log-cafe-com-leite/`, opened as a real `file://` URL
(no server) in a Chromium browser through the browser tool.

```
file:///private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-wt/t19/examples/coffee-log-cafe-com-leite/
```

**Click-through: galeria → canvas → variante → segunda tela e voltar.**

1. Opened the session gallery `index.html` (`file://…/coffee-log-cafe-com-leite/index.html`).
   Title `proto-lab — Blueprint / Schematic`; a **pending** status cell was the
   pre-choice state and now reads **chosen (c)** (re-rendered after the pick).
   → `a4-gallery-from-variant-file.png`.
2. Clicked the canvas link on the d1 row → `points/d1-coffee-log.html`
   (`file://…/points/d1-coffee-log.html`). All **3** frames mounted with relative
   `src` (`../variants/d1-a/index.html`, `d1-b`, `d1-c`) — verified via
   `document.querySelectorAll('.deck iframe')`. Toggled **desktop (1280px)** and
   **mobile (390px)** with the canvas width buttons.
   → `a5-canvas-desktop-file.png`, `a6-canvas-mobile-file.png`.
3. Opened the chosen variant directly: `variants/d1-c/index.html`
   (title `d1-c · Feed de coluna única`, URL confirmed `file://…/variants/d1-c/index.html`).
   → `a1-variant-c-index-file.png`.
4. Clicked **detalhe** inside the page → navigated to
   `file://…/variants/d1-c/detail.html` (title `… · registro`).
   → `a2-variant-c-detail-file.png`.
5. Clicked **voltar ao diário** (`.back`, `href="index.html"`) → back to
   `file://…/variants/d1-c/index.html`.
   → `a3-variant-c-voltar-file.png`.
6. Clicked **galeria** (`.topbar__back`, `href="../../index.html"`) → back to the
   session gallery (`file://…/coffee-log-cafe-com-leite/index.html`).
7. Post-choice artifacts also opened over `file://`: `chosen/d1/index.html`
   (byte-identical copy of `variants/d1-c/`, its `../../index.html` link still
   resolves) → `a7-chosen-d1-file.png`; and `styleguide.html`, which consumes
   `tokens.css` via a relative `<link>` — computed fonts confirm the D10 register
   (`"Space Mono", … monospace` body / `"Archivo Narrow", … sans-serif` display)
   → `a8-styleguide-file.png`.

**Acceptance commands (from the repo/worktree root).**

```
python3 scripts/check_slop.py examples/coffee-log-*/variants/*/*.html
# {"hits": [], "count": 0, "verdict": "pass"}   exit 0
```

**Screenshots** (temp dir `…/t19-shots/final/`, not committed): `a1`…`a8` as named
above, plus `a5`/`a6` for the two canvas widths.

**Limitations / observations.**

- **In-frame click flakiness (tooling, not an artifact failure).** The browser
  tool refused some clicks *inside* a canvas iframe with *"Element '<ref>' is
  covered by <p.annot>/<article.plate.mark>/<li.card.mark> at its click point"*,
  typically when the deck was horizontally scrolled at 1280px. Re-issuing the
  click, or targeting the frame's nav link by CSS selector, succeeded every time,
  and the navigation was confirmed by the resulting URL change. The frames' links
  themselves are correct — this is a hit-testing limitation of the automation, not
  a broken link.
- **Screenshots not committed** (binary-image constraint). Evidence lives at the
  absolute temp paths above and in the commit body.
- **Gallery register.** The scaffolded `index.html` renders in the gallery
  template's *neutral* register, not D10: the template comment says the direction
  card overrides `--accent/--font-text`, but `scaffold.py` only substitutes
  seed/direction/family/points rows. Pre-existing `assets/` template-vs-doc
  mismatch (Task 12), out of scope for T19; recorded so it is not read as a D10
  failure.
- **Webface availability.** The variant/styleguide pages link Google Fonts
  (`fonts.googleapis.com`, an allow-listed host) and rendered with the webfaces
  present. Offline the same-class fallbacks (Archivo Narrow→Arial Narrow, Space
  Mono→IBM Plex Mono/ui-monospace) keep the register; that path was reasoned from
  the declared stacks, not rendered with the network cut.
- **No subagent dispatch.** This harness exposes no subagent tool, so the pipeline
  ran inline (SKILL.md degradation row: *"Harness without subagents → each phase
  runs inline"*). The judge in `judge-report.md` is therefore **not** a fresh-eyes
  subagent; the independent part of the gate is the machine slop scan and the
  `file://` walkthrough above.
