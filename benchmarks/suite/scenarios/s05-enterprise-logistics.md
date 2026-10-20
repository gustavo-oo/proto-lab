# s05 — Dense enterprise domain

| field | value |
|---|---|
| scenario id | `s05` |
| seed | `s05-anchor` (fixed) |
| config | `--points 4`, `--variants 3`, research on |
| check focus | `structural_divergence`, `slop_hits`, `html_bytes_total`, `judge_axes_pass` |

The prompt below is **frozen**: it is the benchmark input and must not be
edited. Editing the prompt or the seed breaks comparability and requires a
`suite_version` bump (`benchmarks/README.md`).

## Frozen prompt (verbatim — user's language, pt-BR)

> Dashboard de operações de uma rede de logística: status da frota, SLA por
> rota, exceções do dia e incidentes abertos. Domínio denso, muita tabela e
> número — precisa continuar legível, e não pode parecer template genérico.

## English gloss (reference only — not the input)

> Operations dashboard for a logistics network: fleet status, SLA per route,
> today's exceptions and open incidents. Dense domain, lots of tables and
> numbers — it has to stay readable, and must not look like a generic
> template.

## Why this scenario

The stress test for both extremes the skill must avoid: prettiness without
legibility, and the dashboard-cliché cluster (4 KPI cards, gradient header,
icon grid, purple accent) that `check_slop.py` fingerprints. It also runs at
the hard cap of 4 points — the largest legal generation — so it is where cost
(`html_bytes_total`) and divergence (`structural_divergence`) are under most
pressure.

## What "good" looks like

- 4 points × 3 variants, all structural; dense-data points (tables, SLA,
  incident queues) get genuinely different layouts per variant, not reskins
  (gate item (c)).
- `check_slop.py` exits 0 despite the dashboard traps (`slop_hits` ≤ 3,
  measured on the worst page).
- `html_bytes_total` stays close to the previous version at equal quality; a
  large jump is investigated and explained in `summary.md` (cost proxy).
- The judge's `brief-fidelity` and `strangeness` axes both pass: the result
  reads as this logistics domain, not as a generic admin template
  (`judge_axes_pass`).
- Caps respected: 4 points, 3 screens per variant, 6 sources, ≤ 2 judge
  rounds (gate item (k)).
