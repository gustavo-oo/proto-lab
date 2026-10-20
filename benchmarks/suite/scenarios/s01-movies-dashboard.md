# s01 — Movies dashboard

| field | value |
|---|---|
| scenario id | `s01` |
| seed | `s01-anchor` (fixed) |
| config | `--points 3`, `--variants 3`, research on |
| check focus | `gate_checklist_pass`, `structural_divergence`, `judge_axes_pass`, `slop_hits` |

The prompt below is **frozen**: it is the benchmark input and must not be
edited. Editing the prompt or the seed breaks comparability and requires a
`suite_version` bump (`benchmarks/README.md`).

## Frozen prompt (verbatim — user's language, pt-BR)

> Faz um dashboard de filmes pra eu decidir o que assistir: minha watchlist,
> o que está em cartaz no cinema e uma recomendação do dia. Quero ver
> direções visuais diferentes antes de implementar — nada de um layout só.

## English gloss (reference only — not the input)

> Build a movie dashboard to help me decide what to watch: my watchlist, what
> is in cinemas now, and a recommendation of the day. I want to see different
> visual directions before implementation — not a single layout.

## Why this scenario

The canonical demo domain from spec §9 (RED-1: "faz um protótipo de um
dashboard de <domínio>" yields one generic Tailwind-ish page). It is the
cheapest full-pipeline run (3 points, 3 variants) on a domain any reviewer can
judge without context. It pins the failure the skill exists to prevent: one
nice page, no direction, no options.

## What "good" looks like

- `direction.json` with `s01-anchor` written before any variant; the card is
  shown and a reroll is offered (gate item (a)).
- The points gate is awaited: `points.json` exists, generation starts only
  after an explicit OK (gate item (b)).
- 3 points × 3 variants, each variant a structural answer on its declared
  axis (gate item (c), `structural_divergence` ≥ 2).
- `research.md` cites 3–6 movie/product dashboards with URLs and
  observed-vs-inferred (`research_sources`).
- `check_slop.py` exits 0 (`slop_hits` ≤ 3).
- `judge-report.md`: five axes + `## Open (not fixed)` (`judge_axes_pass`).
