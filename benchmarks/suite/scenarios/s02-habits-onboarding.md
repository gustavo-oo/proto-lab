# s02 — Habits onboarding

| field | value |
|---|---|
| scenario id | `s02` |
| seed | `s02-anchor` (fixed) |
| config | `--points 2`, `--variants 3`, research on |
| check focus | `gate_checklist_pass`, `judge_axes_pass`, `artifacts_complete` |

The prompt below is **frozen**: it is the benchmark input and must not be
edited. Editing the prompt or the seed breaks comparability and requires a
`suite_version` bump (`benchmarks/README.md`).

## Frozen prompt (verbatim — user's language, pt-BR)

> Preciso do onboarding de um app de hábitos: boas-vindas, escolher os
> hábitos e definir a primeira meta. Me mostra opções de estrutura — não
> quero três telas iguais com cores diferentes.

## English gloss (reference only — not the input)

> I need the onboarding for a habits app: welcome, pick your habits, set the
> first goal. Show me structural options — I do not want three identical
> screens in different colors.

## Why this scenario

A multi-screen flow with a deliberately narrow scope (2 points). It tests
divergence on information architecture and flow — where cosmetic variants are
most tempting — while costing less generation than s01. It also exercises the
`artifacts_complete` contract: the expected set is fixed, so a run that
"saves time" by dropping the handoff shows up as a fractional score.

## What "good" looks like

- The variant options differ in flow/IA (step order, commitment model, what is
  asked when), not in palette (gate item (c), `structural_divergence`).
- The declared axis of each point is named in `points.json` and is what the
  variants actually diverge on (judge axis 5).
- All 13 expected artifacts exist at the end (`artifacts_complete` = 1.000),
  with `chosen/` non-empty after the pick.
- `judge-report.md` carries the five axes and the open-findings section
  (`judge_axes_pass`).
- The reply to the user is in pt-BR (gate item (l)).
