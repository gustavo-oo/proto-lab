# s03 — Checkout under pressure

| field | value |
|---|---|
| scenario id | `s03` |
| seed | `s03-anchor` (fixed) |
| config | `--points 2`, `--variants 2`, research on |
| check focus | `gate_checklist_pass`, `judge_axes_pass`, `research_sources`, `file_nav_ok` |

The prompt below is **frozen**: it is the benchmark input and must not be
edited. Editing the prompt or the seed breaks comparability and requires a
`suite_version` bump (`benchmarks/README.md`).

## Frozen prompt (verbatim — user's language, pt-BR)

> preciso rápido de um mockup de checkout de uma loja de café: carrinho,
> pagamento e confirmação. tô sem tempo hoje, então pula o que não for
> essencial.

## English gloss (reference only — not the input)

> I need a coffee-shop checkout mockup, fast: cart, payment, confirmation.
> I'm out of time today, so skip whatever is not essential.

## Why this scenario

The pressure scenario of spec §9 (RED-3): "quick, just a mockup" is exactly
when a skill is tempted to drop research, the judge and the options. The
correct response is to cut **scope** through the sanctioned flags
(`--variants 2`, fewer points) and never the steps — the judge and the gate
still run, or the run reports openly what it skipped.

It is also the only scenario whose expected-artifact list is shorter: a
pressure run may legitimately end with the pick-dependent trio (`chosen/`,
`handoff.md`, `styleguide.html`) pending, as long as that pending state is
recorded (SKILL.md step 9). The judge and research artifacts are **not**
optional here.

## What "good" looks like

- 2 points × 2 variants (the only sanctioned scope cut), both structural.
- `research.md` still exists with cited sources (`research_sources` ≥ 3) — or
  the `--skip-research` fallback is recorded explicitly; silently dropping it
  is a fail.
- `judge-report.md` exists with five axes and an honest `## Open (not fixed)`
  (`judge_axes_pass`); a run that "ships without judging" scores 0 here.
- The `file://` walkthrough was actually clicked (`file_nav_ok`; `nav.md`
  present).
- `tokens.css` + the pending-pick note are recorded (gate item (i)).
