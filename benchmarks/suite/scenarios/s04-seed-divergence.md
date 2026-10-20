# s04 — Seed divergence (three fixed seeds)

| field | value |
|---|---|
| scenario id | `s04` |
| seeds | `s04-a`, `s04-b`, `s04-c` (fixed, one run each) |
| config | `--points 2`, `--variants 3`, research on |
| check focus | `distinct_directions`, `structural_divergence`, `judge_axes_pass` |

The prompt below is **frozen** and is used **unchanged for all three seeds**.
It is the benchmark input and must not be edited. Editing the prompt or the
seeds breaks comparability and requires a `suite_version` bump
(`benchmarks/README.md`).

## Frozen prompt (verbatim — user's language, pt-BR)

> Quero ver quanto a estrutura muda quando a direção muda: três opções bem
> diferentes pra uma landing de estúdio de tatuagem. Mesmo pedido, direções
> diferentes.

## English gloss (reference only — not the input)

> I want to see how much the structure changes when the direction changes:
> three clearly different options for a tattoo studio landing page. Same
> request, different directions.

## Why this scenario

The core anti-homogenization claim: the same brief under different fixed seeds
must yield visibly different directions — not three repaints. Suite v1 uses
three seeds recorded here (`s04-a`, `s04-b`, `s04-c`), so the *set* is part of
the frozen suite; the run itself must never reroll to a "nicer" seed.

Random-seed exploration is deliberately **not** part of the benchmark — it
belongs to the reviews (plan ritual). A benchmark that rerolled would measure
luck, not the skill.

## What "good" looks like

- Three `direction.json` files with three distinct `direction.id` values
  (`distinct_directions` = 3), read from the seeds above, not re-rolled.
- The families are recorded next to the ids; three ids from one family is
  legal but noted in the evidence.
- Each run independently passes the gate and the judge axes; a run that
  "borrows" the previous direction's layout is a fail.
- The variant sets differ structurally (not just in color) even where the
  direction family is shared (`structural_divergence` ≥ 2 per run).
