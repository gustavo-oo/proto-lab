#!/usr/bin/env python3
"""Compare two proto-lab benchmark result snapshots.

Usage
-----
    python3 benchmarks/compare.py <results-A> <results-B> [--strict]

A "snapshot" is one directory per skill version, produced by the benchmark
ritual (``benchmarks/README.md``)::

    benchmarks/results/<version>/
      env.json       version, commit, suite_version, model, harness, date
      summary.json   {"suite_version": "v1", "scenarios": {<id>: {<metric>: value}}}
      summary.md     human-readable table + "## Changes since previous"

Values in ``summary.json`` are already aggregated per ``rubric.md``: a
multi-run scenario (s04, three fixed seeds) fills its single slot with the
**worst run per metric** (min for higher-is-better, max for lower-is-better,
AND for booleans), except ``distinct_directions``, which is the cross-run
distinct count. Per-run detail lives in the scenario evidence directory, not
in the summary slot.

The comparator prints, for every scenario x metric that exists in either
snapshot, the values in A and B, the numeric delta (B - A) and a verdict:

* ``improved``      -- the metric moved in its declared better direction;
* ``⚠ regression``  -- the metric moved in its worse direction;
* ``n/a``           -- the cell is not comparable (metric missing on one side).

Regression direction is declared per metric in ``METRICS`` below and defined
precisely in ``benchmarks/suite/rubric.md``. Booleans are counted as 1/0 for
the delta. A missing metric is never silently treated as a regression.

Exit codes
----------
0   compared (regressions are reported with ``⚠``; the exit stays 0)
1   compared with ``--strict`` and at least one regression was found
2   refused: different ``suite_version``, bad usage, or an unreadable snapshot

Python stdlib only (>= 3.8).
"""

import argparse
import json
import sys
from pathlib import Path

# The frozen metric registry. It MUST stay identical to the ``metrics`` array
# of ``benchmarks/suite/suite.json`` (pinned by tests/test_compare.py).
METRICS = {
    "gate_checklist_pass": {
        "type": "number",
        "range": "0-1",
        "direction": "higher_is_better",
    },
    "structural_divergence": {
        "type": "int",
        "range": "0-3",
        "direction": "higher_is_better",
    },
    "slop_hits": {
        "type": "int",
        "range": "0+",
        "direction": "lower_is_better",
    },
    "judge_axes_pass": {
        "type": "int",
        "range": "0-5",
        "direction": "higher_is_better",
    },
    "fix_rounds": {
        "type": "int",
        "range": "0-2",
        "direction": "lower_is_better",
    },
    "artifacts_complete": {
        "type": "number",
        "range": "0-1",
        "direction": "higher_is_better",
    },
    "research_sources": {
        "type": "int",
        "range": "0-6",
        "direction": "higher_is_better",
    },
    "file_nav_ok": {
        "type": "bool",
        "range": "bool",
        "direction": "higher_is_better",
    },
    "html_bytes_total": {
        "type": "int",
        "range": "0+",
        "direction": "lower_is_better",
    },
    "distinct_directions": {
        "type": "int",
        "range": "0-3",
        "direction": "higher_is_better",
    },
}

# env.json keys shown in the diff, in display order.
ENV_KEYS = ("version", "commit", "suite_version", "model", "harness", "date")

# The two env keys whose divergence makes a comparison not apples-to-apples.
PROVENANCE_KEYS = ("model", "harness")

EXIT_OK = 0
EXIT_REGRESSION = 1
EXIT_MISMATCH = 2

MISSING = "—"
EPSILON = 1e-9


class ResultError(Exception):
    """A results directory is missing, unreadable or malformed."""


class Snapshot:
    """One benchmark result snapshot, as read from disk."""

    def __init__(self, path, env, suite_version, scenarios):
        self.path = path
        self.env = env
        self.suite_version = suite_version
        self.scenarios = scenarios


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ResultError("cannot read %s: %s" % (path, exc))


def load_snapshot(path):
    """Read ``path/env.json`` + ``path/summary.json`` into a Snapshot."""
    path = Path(path)
    if not path.is_dir():
        raise ResultError("results directory not found: %s" % path)

    summary_path = path / "summary.json"
    if not summary_path.is_file():
        raise ResultError("missing summary.json in %s" % path)
    summary = _read_json(summary_path)
    if not isinstance(summary, dict):
        raise ResultError("%s: summary.json must be a JSON object" % path)

    scenarios = summary.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        raise ResultError("%s: summary.json needs a non-empty 'scenarios' object" % path)
    for scenario_id, metrics in scenarios.items():
        if not isinstance(metrics, dict):
            raise ResultError(
                "%s: scenario %s must map metric -> value" % (path, scenario_id)
            )

    env_path = path / "env.json"
    env = _read_json(env_path) if env_path.is_file() else {}
    if not isinstance(env, dict):
        raise ResultError("%s: env.json must be a JSON object" % path)

    suite_version = env.get("suite_version") or summary.get("suite_version")
    if not suite_version:
        raise ResultError(
            "%s: no suite_version in env.json or summary.json" % path
        )

    return Snapshot(path, env, suite_version, scenarios)


def _as_number(value):
    """Coerce a metric value to a number; booleans count as 1/0."""
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _fmt_value(value, spec):
    """Render a metric value according to its declared type."""
    if value is None:
        return MISSING
    kind = spec.get("type") if spec else None
    if kind == "bool" or (kind is None and isinstance(value, bool)):
        return "true" if value else "false"
    if kind == "number":
        try:
            return "{:.3f}".format(float(value))
        except (TypeError, ValueError):
            return str(value)
    if kind == "int":
        try:
            return "{:,}".format(int(value))
        except (TypeError, ValueError):
            return str(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return "{:,}".format(value)
    if isinstance(value, float):
        return "{:.3f}".format(value)
    return str(value)


def _fmt_delta(delta, integer):
    if abs(delta) < EPSILON:
        return "0"
    if integer:
        return "{:+,}".format(int(round(delta)))
    return "{:+.3f}".format(delta)


def _verdict(metric, value_a, value_b):
    """Classify one cell: (delta text, verdict)."""
    spec = METRICS[metric]
    number_a = _as_number(value_a)
    number_b = _as_number(value_b)
    if number_a is None or number_b is None:
        return "n/a", "not comparable (non-numeric)"
    delta = number_b - number_a
    integer = isinstance(value_a, int) and isinstance(value_b, int)
    text = _fmt_delta(delta, integer)
    if abs(delta) < EPSILON:
        return text, ""
    higher_is_better = spec["direction"] == "higher_is_better"
    improved = delta > 0 if higher_is_better else delta < 0
    return text, "improved" if improved else "regression"


def _flag(verdict):
    """Table-friendly flag: a regression carries the warning glyph."""
    return "⚠ regression" if verdict == "regression" else verdict


def build_rows(snapshot_a, snapshot_b):
    """Build one row per (scenario, metric) present in either snapshot."""
    rows = []
    ignored = set()
    scenario_ids = sorted(set(snapshot_a.scenarios) | set(snapshot_b.scenarios))
    for scenario_id in scenario_ids:
        metrics_a = snapshot_a.scenarios.get(scenario_id, {})
        metrics_b = snapshot_b.scenarios.get(scenario_id, {})
        if not isinstance(metrics_a, dict) or not isinstance(metrics_b, dict):
            raise ResultError("scenario %s must map metric -> value" % scenario_id)
        for metric in METRICS:
            in_a = metric in metrics_a
            in_b = metric in metrics_b
            if not in_a and not in_b:
                continue
            value_a = metrics_a.get(metric)
            value_b = metrics_b.get(metric)
            if in_a and in_b:
                delta, verdict = _verdict(metric, value_a, value_b)
            else:
                delta = "n/a"
                missing = "B" if not in_b else "A"
                verdict = "not comparable (missing in %s)" % missing
            rows.append(
                {
                    "scenario": scenario_id,
                    "metric": metric,
                    "a": _fmt_value(value_a, METRICS[metric]),
                    "b": _fmt_value(value_b, METRICS[metric]),
                    "delta": delta,
                    "verdict": verdict,
                }
            )
        for metric in set(metrics_a) | set(metrics_b):
            if metric not in METRICS:
                ignored.add(metric)
    return rows, sorted(ignored)


def _env_value(env, key):
    value = env.get(key)
    return MISSING if value in (None, "") else str(value)


def apples_to_apples(snapshot_a, snapshot_b):
    """True/False when provenance is known, None when env.json is incomplete."""
    pairs = [
        (snapshot_a.env.get(key), snapshot_b.env.get(key)) for key in PROVENANCE_KEYS
    ]
    if any(a in (None, "") or b in (None, "") for a, b in pairs):
        return None
    return all(a == b for a, b in pairs)


def env_diff_lines(snapshot_a, snapshot_b):
    """Render the env.json diff plus the apples-to-apples verdict."""
    lines = ["env diff (A → B)"]
    provenance_changed = []
    for key in ENV_KEYS:
        value_a = _env_value(snapshot_a.env, key)
        value_b = _env_value(snapshot_b.env, key)
        if key in PROVENANCE_KEYS:
            if value_a == value_b:
                lines.append("  %-13s %s (unchanged)" % (key + ":", value_a))
            else:
                lines.append("  %-13s %s → %s" % (key + ":", value_a, value_b))
                provenance_changed.append(key)
        elif value_a == value_b:
            lines.append("  %-13s %s" % (key + ":", value_a))
        else:
            lines.append("  %-13s %s → %s" % (key + ":", value_a, value_b))

    provenance = apples_to_apples(snapshot_a, snapshot_b)
    if provenance is None:
        lines.append("  ! env.json missing on one side — provenance unknown")
    elif provenance is False:
        lines.append(
            "  ⚠ %s differ — não apples-to-apples (o resultado mistura "
            "executores diferentes)" % "/".join(provenance_changed)
        )
    else:
        lines.append("  → model/harness unchanged — apples-to-apples")
    return lines


def _header_lines(snapshot_a, snapshot_b):
    return [
        "proto-lab benchmark compare",
        "  A = %s  (version %s, suite %s)"
        % (
            snapshot_a.path,
            _env_value(snapshot_a.env, "version"),
            snapshot_a.suite_version,
        ),
        "  B = %s  (version %s, suite %s)"
        % (
            snapshot_b.path,
            _env_value(snapshot_b.env, "version"),
            snapshot_b.suite_version,
        ),
    ]


def render_table(rows):
    """Render the per-scenario x per-metric delta table."""
    metric_width = max([len("metric")] + [len(metric) for metric in METRICS])
    line_format = "%-8s  %-*s  %12s %12s %10s  %s"
    lines = [
        line_format % ("scenario", metric_width, "metric", "A", "B", "delta", "flag")
    ]
    for row in rows:
        lines.append(
            line_format
            % (
                row["scenario"],
                metric_width,
                row["metric"],
                row["a"],
                row["b"],
                row["delta"],
                _flag(row["verdict"]),
            )
        )
    return lines


def summary_lines(rows):
    """Render the counts and the explicit regression list."""
    improved = [row for row in rows if row["verdict"] == "improved"]
    regressions = [row for row in rows if row["verdict"] == "regression"]
    unchanged = [
        row for row in rows if row["verdict"] == "" and row["delta"] == "0"
    ]
    not_comparable = [row for row in rows if row["delta"] == "n/a"]
    lines = [
        "",
        "%d rows · %d improved · %d ⚠ regression · %d unchanged · %d not comparable"
        % (
            len(rows),
            len(improved),
            len(regressions),
            len(unchanged),
            len(not_comparable),
        ),
    ]
    if regressions:
        for row in regressions:
            lines.append(
                "⚠ regression: %s %s (%s → %s)"
                % (row["scenario"], row["metric"], row["a"], row["b"])
            )
    else:
        lines.append("no regressions — every ⚠-free row held or improved")
    return lines


def export_payload(snapshot_a, snapshot_b, rows):
    """Machine-readable form of the report (``--json``)."""
    return {
        "a": {
            "path": str(snapshot_a.path),
            "version": snapshot_a.env.get("version"),
            "suite_version": snapshot_a.suite_version,
        },
        "b": {
            "path": str(snapshot_b.path),
            "version": snapshot_b.env.get("version"),
            "suite_version": snapshot_b.suite_version,
        },
        "apples_to_apples": apples_to_apples(snapshot_a, snapshot_b),
        "rows": rows,
    }


def compare(snapshot_a, snapshot_b):
    """Print the comparison. Returns the process exit code."""
    header = _header_lines(snapshot_a, snapshot_b)
    print("\n".join(header))

    if snapshot_a.suite_version != snapshot_b.suite_version:
        print(
            "⚠ suite_version mismatch: A=%s B=%s — suites diferentes, "
            "comparação recusada"
            % (snapshot_a.suite_version, snapshot_b.suite_version)
        )
        print(
            "  bump suite_version only when the suite itself changed; "
            "re-run B on the same suite to compare"
        )
        return EXIT_MISMATCH

    print("")
    print("\n".join(env_diff_lines(snapshot_a, snapshot_b)))
    print("")

    rows, ignored = build_rows(snapshot_a, snapshot_b)
    if ignored:
        print("! metric not in the frozen suite (ignored): %s" % ", ".join(ignored))
        print("")
    print("\n".join(render_table(rows)))
    print("\n".join(summary_lines(rows)))
    return EXIT_OK


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="compare.py",
        description="Compare two proto-lab benchmark result snapshots.",
    )
    parser.add_argument("results_a", help="baseline snapshot directory (A)")
    parser.add_argument("results_b", help="new snapshot directory (B)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when a regression is found (default: exit 0, the ⚠ is the signal)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the machine-readable report instead of the table",
    )
    args = parser.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    try:
        snapshot_a = load_snapshot(Path(args.results_a))
        snapshot_b = load_snapshot(Path(args.results_b))
    except ResultError as exc:
        print("compare.py: error: %s" % exc, file=sys.stderr)
        return EXIT_MISMATCH

    if args.json:
        if snapshot_a.suite_version != snapshot_b.suite_version:
            print(
                json.dumps(
                    {
                        "error": "suite_version mismatch",
                        "a": snapshot_a.suite_version,
                        "b": snapshot_b.suite_version,
                    },
                    ensure_ascii=False,
                )
            )
            return EXIT_MISMATCH
        rows, ignored = build_rows(snapshot_a, snapshot_b)
        payload = export_payload(snapshot_a, snapshot_b, rows)
        payload["ignored_metrics"] = ignored
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if args.strict and any(row["verdict"] == "regression" for row in rows):
            return EXIT_REGRESSION
        return EXIT_OK

    try:
        status = compare(snapshot_a, snapshot_b)
    except ResultError as exc:
        print("compare.py: error: %s" % exc, file=sys.stderr)
        return EXIT_MISMATCH
    if status != EXIT_OK:
        return status
    if args.strict:
        rows, _ = build_rows(snapshot_a, snapshot_b)
        if any(row["verdict"] == "regression" for row in rows):
            return EXIT_REGRESSION
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
