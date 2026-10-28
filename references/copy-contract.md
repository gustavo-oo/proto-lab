# Copy contract

`references/copy-contract.md` is the normative specification of the **copy
gate**: the part of layer 3 that checks what a generated page says, not how it
looks. `references/slop-fingerprints.md` covers visual tells as a cluster
(`≥ 4 hits = fail`). This contract is **zero-tolerance**: one unresolved
C01-C04 finding fails the page's `slop-scan` axis, whatever its visual count.

The gate applies to **product copy**: every visible text node in
`variants/**` and `chosen/**`. Session artifacts (the gallery, the comparison
canvas, `styleguide.html`, `handoff.md`, `judge-report.md`) describe the
session, not the product, and are out of scope. Inside a product page, mark
session chrome (the variant label, the topbar, the title block) with
`data-session-chrome`; the checker and the judge skip that subtree.

A direction's voice sets the register. It never licenses empty copy: a
slogan-like direction must still make a concrete claim.

## C01. No item-count labels

A list is its own count. Do not label a list, table, feed or grid with how many
items it contains.

Bad:

- `6 filmes, 4 cinemas`
- `10 registros` above a table
- `4 results` above a search result list

Good:

- `filmes, cinemas`, or drop the line
- the table itself, with no count above it
- `resultados`, or drop the line

Exempt: counts that are the data or the state, not a description of the list's
length.

| Kind | Example |
| ---- | ------- |
| selection | `3 de 5 selecionados` |
| process | `extração 1 de 2`, `passo 2 de 4` |
| rating | `nota 4/5` |
| measurement | `250 ml`, `15 g`, `3:05` |
| date or ratio | `12/10`, `1:16,7` |
| KPI | a dashboard total the user came for |

**Judge check:** for every label, legend, eyebrow or heading that contains a
number, ask "Does this number tell the user something the list does not already
show?" If it only restates the list's length, C01.

## C02. One fact, one place

Within one screen, a fact appears once. At most one repetition is allowed, and
only when the second occurrence has a distinct role: a summary that leads to a
detail, or a detail that is opened from a summary. Never repeat a fact twice in
the same visual group.

Bad:

- a score gauge and a visible `nota 4/5` on the same row;
- an eyebrow `DIÁRIO` above an `h1` `Diário de cafés`;
- a card field `origem: Etiópia` repeated in the card footer.

Good:

- the gauge with an accessible `aria-label="nota 4 de 5"` and no visible
  duplicate;
- the heading alone, with the eyebrow removed or changed to a different fact;
- `origem: Etiópia` once in the card.

Exempt:

- the same fact on different screens (list and detail);
- a summary count that leads to a detail table, when the count is data (C01
  may still apply);
- repeated table headers across rows or columns (structural, not copy);
- `aria-label` or `alt` text that is the accessible name of the same visible
  fact.

"At most one repetition" means at most two visible occurrences on one screen.

**Judge check:** build a per-screen fact list (normalized value and locations),
then flag any value with two or more visible locations unless the second is a
clearly labeled summary/detail role. Check the eyebrow against the heading, the
card field against the footer, the gauge against a literal value, and repeated
sentences across sections.

## C03. No filler copy

Every headline, subhead, tagline, section intro, empty state and footer line
must add information. Delete-test: delete the line. If nothing is lost, delete
it permanently.

Bad:

- `Transforme sua visão em realidade.`
- `O futuro começa aqui.`
- `Not a feature. A platform.`
- `World-class, enterprise-grade, next-generation.`
- `Soluções inovadoras para o seu negócio.`
- `We killed the growth theater.`

Good:

- `Registre cada café, método e nota em menos de 30 segundos.`
- `Seus registros, do mais recente para o mais antigo.`
- `Filtre por origem, método ou nota.`

No generic superlatives, no forced contrasts, no "theatre" dismissals. A
slogan-like direction may use a short line, but the line must state a concrete
claim.

**Judge check:** for every headline, subhead, tagline and section intro, state
the information it adds. If none, C03. Delete the line and check whether the
page loses meaning; if it does not, it is filler.

## C04. No separator characters

Do not use separator glyphs to join metadata fragments in product copy. This
includes the middle dot `·` (U+00B7), the em dash `—`, the en dash `–`, the
pipe `|`, the bullet `•`, and similar decorative dividers.

Bad:

- `Quênia · Nyeri AA`
- `grão: SL28 · torra clara`
- `V60 | 1:16,7`
- `origem • método • nota`
- `d1-a — Tabela densa`

Good:

- `Quênia, Nyeri AA`
- `grão: SL28, torra clara`
- `V60, 1:16,7`
- `origem, método e nota`
- separate elements or rows for the fields.

Use punctuation or structure instead: a comma, colon, semicolon, conjunction
(`e`, `ou`), separate elements, separate rows, or whitespace. Do not replace
one decorative glyph with another.

Exempt: punctuation inside a value, not between metadata fields.

| Kind | Example |
| ---- | ------- |
| date | `12/10`, `15/10/2026` |
| ratio | `1:16,7`, `1:2` |
| rating | `4/5` |
| range | `0–5`, `12/10 → 16/10` |
| hyphenated word | `média-fina`, `meio-tom` |
| proper name | `Blueprint / Schematic` |

An em dash inside a sentence is punctuation, not a separator, but it is still
a copy smell. Keep it to at most one per screen and never use it to join
metadata fields. Prefer a full stop or a comma.

**Judge check:** list every visible line that joins two or more metadata
fragments, and every text node that is only a separator glyph. If it uses a
banned glyph, C04. State the replacement (comma, colon, conjunction, separate
row). A proper name or data value is exempt.

## Gate and severity

- Any unresolved C01-C04 finding is a `major`.
- It is a `blocker` when it repeats a load-bearing value (a price, a score, a
  required field), hides the only real information, or the screen's primary
  message is a slogan.
- The judge's `slop-scan` axis is FAIL while any copy finding is unresolved,
  independent of the visual `≥ 4` cluster.
- Report the two halves separately in `judge-report.md`:
  `visual: N/26; copy: C01..C04`.
- Copy findings are not counted in the visual cluster. A page with zero visual
  hits and one copy finding fails `slop-scan`.
- Inline or degraded judging still runs the copy gate. The `fresh-eyes
  independence: lost (inline)` marker applies as usual.

## Mechanical checker

`scripts/check_copy.py` scans one product page and reports the deterministic
subset:

| Rule | What it checks | Confidence |
| ---- | -------------- | ---------- |
| C01 | Number plus noun in a heading, legend, figcaption, summary, caption, or a label-like class (`label`, `eyebrow`, `kicker`, `meta`, `count`, `legend`, `subtitle`, `caption`), with unit/date/ratio/rating and data-field exemptions. | `heuristic` |
| C04 | Separator glyphs in visible text outside `data-session-chrome`: `·`, `|`, `•` are `solid`; `—` and `–` are `heuristic`. | mixed |

C02 and C03 are judge-only; a mechanical list cannot reliably decide whether
two facts have distinct roles or whether a line carries information.

A `heuristic` checker finding is still a finding. The judge may dismiss it only
by recording why the number is data or the glyph belongs to a value or proper
name. The checker is evidence, not the final gate.
