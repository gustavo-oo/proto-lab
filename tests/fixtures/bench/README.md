# Benchmark fixtures

Fabricated result snapshots for `tests/test_compare.py` (Task 24). They are
**not** real benchmark runs: the numbers are chosen to pin each branch of
`benchmarks/compare.py` with the smallest possible difference between
`vA` and `vB`.

| snapshot | purpose |
|---|---|
| `vA` | skill `0.1.0`, suite `v1`, model `harness-model-A`, harness `opencode/cli` |
| `vB` | skill `0.1.1`, same suite/model/harness. Exactly **one** metric improved (`s01 gate_checklist_pass` 0.833 → 1.000) and exactly **one** worsened (`s02 slop_hits` 1 → 4 → the only `⚠`). Everything else holds or improves, including the lower-is-better metrics (`s01 slop_hits` 2 → 1, `s02 fix_rounds` 1 → 0, the shrinking `html_bytes_total`). |
| `vA-suite-v2` | `vA` re-recorded under `suite_version` `v2` → the comparator must refuse the comparison (exit 2). |
| `vC-env` | `vB` re-recorded on a different model/harness (`harness-model-B` / `opencode/desktop`) and with `s04 file_nav_ok` dropped → the "não apples-to-apples" warning plus the `n/a` (missing metric) row. |

Metric direction used by the fixtures (`benchmarks/suite/rubric.md`): higher
is better for `gate_checklist_pass`, `structural_divergence`,
`judge_axes_pass`, `artifacts_complete`, `research_sources`, `file_nav_ok`,
`distinct_directions`; lower is better for `slop_hits`, `fix_rounds`,
`html_bytes_total`.

Since `s04` spans three fixed seeds (three runs), its fixture values are the
**aggregated worst run per metric** — `min` for higher-is-better, `max` for
lower-is-better, `AND` for `file_nav_ok` — with `distinct_directions` as the
cross-run count (`rubric.md` §"Multi-run scenarios — the aggregation rule").
`html_bytes_total` is therefore the largest of the three sessions
(39,400 / 38,100), not a sum of three runs.
