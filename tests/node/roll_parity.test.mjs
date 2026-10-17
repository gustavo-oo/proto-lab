// Parity tests for the Node mirror of the Python roller (Task 11, ruling R6).
//
// The contract is stdout byte-identity: for the SAME arguments, `node
// scripts/roll.mjs` must print exactly what `python3 scripts/roll.py` prints.
// That only holds if the Node side mirrors Python's `json.dumps(...,
// sort_keys=True, separators=(",", ":"))` — including its default
// `ensure_ascii=True`, which escapes every non-ASCII code point as `\uXXXX`
// (astral code points as a surrogate pair) instead of emitting raw UTF-8 the
// way `JSON.stringify` does.
//
// Behavioural, not unit: each case shells out to both CLIs and compares the
// captured stdout. Node built-ins only (node:test, node:assert, child_process).

import test from "node:test";
import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const PY = path.join(ROOT, "scripts", "roll.py");
const MJS = path.join(ROOT, "scripts", "roll.mjs");

const SEEDS = ["cafe-com-leite", "abc", "s17"];
const DOMAINS = [null, "dense tables"];
// Accented domain: "dense tables" (the pruning tag) is absent, so nothing is
// excluded and the domain is echoed verbatim into filters.domain — the one
// place user input reaches the card and forces the ensure_ascii escape path.
const ACCENTED_DOMAIN = "café tables";

function run(command, args) {
  return execFileSync(command, args, { cwd: ROOT, encoding: "utf8" });
}

/** Captured stdout of `python3 scripts/roll.py <args>`. */
function py(args) {
  return run("python3", [PY, ...args]);
}

/** Captured stdout of `node scripts/roll.mjs <args>`. */
function mjs(args) {
  return run("node", [MJS, ...args]);
}

/** Run a CLI to completion, capturing its exit status and both streams. */
function capture(command, args) {
  const result = spawnSync(command, args, { cwd: ROOT, encoding: "utf8" });
  return { status: result.status, stdout: result.stdout, stderr: result.stderr };
}

/** Exit status + stdout of both CLIs for the same arguments. */
function bothStatusAndStdout(args) {
  return {
    fromPy: capture("python3", [PY, ...args]),
    fromMjs: capture("node", [MJS, ...args]),
  };
}

function caseArgs(seed, { domain = null, extra = [] } = {}) {
  const args = ["--seed", seed];
  if (domain !== null) args.push("--domain", domain);
  return [...args, ...extra];
}

/** Write a catalog file wrapping `entries` in the machine-block markers. */
function writeCatalog(dir, name, entries) {
  const file = path.join(dir, name);
  writeFileSync(
    file,
    `<!-- CATALOG_JSON_START -->\n${JSON.stringify(entries)}\n<!-- CATALOG_JSON_END -->\n`,
  );
  return file;
}

function assertParity(args, label) {
  const expected = py(args);
  const actual = mjs(args);
  assert.equal(actual, expected, `stdout diverged for ${label}: ${JSON.stringify(args)}`);
  return { expected, actual };
}

test("seed x domain matrix is byte-identical", () => {
  for (const seed of SEEDS) {
    for (const domain of DOMAINS) {
      const args = caseArgs(seed, { domain });
      const { expected } = assertParity(args, `seed=${seed} domain=${domain}`);

      // Guard against a vacuous pass: the output is a real card for this seed.
      assert.equal(JSON.parse(expected).seed, seed);
      assert.equal(expected.endsWith("\n"), true, "CLI must end with one newline");
      assert.equal(expected.includes("\r"), false, "no CR must leak into stdout");
    }
  }
});

test("--wild parity (recorded verbatim, never changes the draw)", () => {
  for (const seed of SEEDS) {
    for (const domain of DOMAINS) {
      const args = caseArgs(seed, { domain, extra: ["--wild"] });
      const { expected } = assertParity(args, `--wild seed=${seed} domain=${domain}`);
      assert.equal(JSON.parse(expected).wild, true);
    }
  }
});

test("non-ASCII domain keeps Python's \\uXXXX escaping", () => {
  for (const seed of SEEDS) {
    const args = caseArgs(seed, { domain: ACCENTED_DOMAIN });
    const { expected } = assertParity(args, `accented domain seed=${seed}`);

    // The escape path is really exercised (not an empty-domain fallback)...
    assert.match(expected, /\\u00e9/, "expected an escaped é in filters.domain");
    // ...and the raw character never reaches stdout.
    assert.equal(expected.includes("é"), false, "raw UTF-8 leaked into stdout");
    assert.equal(JSON.parse(expected).filters.domain, ACCENTED_DOMAIN);
  }
});

test("non-ASCII seed is echoed with the same escaping", () => {
  assertParity(caseArgs("café-über"), "accented seed");
});

test("--catalog parity with an explicit path", () => {
  const args = [
    "--seed", "cafe-com-leite",
    "--domain", "dense tables",
    "--catalog", path.join("references", "directions.md"),
  ];
  assertParity(args, "explicit --catalog");
});

test("non-ASCII catalog values escape identically", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "roll-parity-uni-"));
  try {
    // A single direction, so every seed draws it and the escape assertions
    // below always have a non-ASCII card to inspect.
    const catalog = writeCatalog(dir, "unicode.md", [
      {
        id: "D02",
        name: "Açaí — Δεύτερο 🍿",
        family: "print",
        fails: ["nope"],
        accent_options: ["#C0FFEE", "#000000"],
        imagery_subjects: ["café photograph", "𝄞 score"],
        inversion_allowed: true,
      },
    ]);

    for (const seed of SEEDS) {
      const args = ["--seed", seed, "--catalog", catalog];
      const { expected } = assertParity(args, `unicode catalog seed=${seed}`);

      assert.equal(JSON.parse(expected).direction_name, "Açaí — Δεύτερο 🍿");
      assert.match(expected, /\\u00e7/, "expected an escaped ç");
      assert.match(expected, /\\ud83c\\udf7f/, "expected the astral surrogate pair");
      assert.equal(expected.includes("🍿"), false, "raw emoji leaked into stdout");
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("--out writes identical bytes and leaves stdout identical", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "roll-parity-"));
  try {
    for (const seed of SEEDS) {
      const pyOut = path.join(dir, `py-${seed}.json`);
      const mjsOut = path.join(dir, `mjs-${seed}.json`);
      const base = ["--seed", seed, "--domain", "dense tables", "--wild"];

      const pyStdout = py([...base, "--out", pyOut]);
      const mjsStdout = mjs([...base, "--out", mjsOut]);

      assert.equal(mjsStdout, pyStdout, `stdout diverged with --out (seed=${seed})`);
      assert.equal(
        readFileSync(mjsOut, "utf8"),
        readFileSync(pyOut, "utf8"),
        `file bytes diverged with --out (seed=${seed})`,
      );
      // `--out` also leaves the card on stdout, newline-terminated.
      assert.equal(readFileSync(mjsOut, "utf8"), mjsStdout);
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("--wild composes with domain and catalog", () => {
  const args = [
    "--seed", "s17",
    "--domain", ACCENTED_DOMAIN,
    "--wild",
    "--catalog", path.join("references", "directions.md"),
  ];
  assertParity(args, "--wild with domain and catalog");
});

test("a catalog without a machine block fails the same way on both CLIs", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "roll-parity-bad-"));
  try {
    const bad = path.join(dir, "bad-catalog.md");
    writeFileSync(bad, "# no CATALOG_JSON markers here\n");

    const { fromPy, fromMjs } = bothStatusAndStdout(["--seed", "abc", "--catalog", bad]);

    assert.notEqual(fromPy.status, 0, "python must reject a markerless catalog");
    assert.equal(fromMjs.status, fromPy.status, "exit codes must match");
    assert.equal(fromMjs.stdout, fromPy.stdout, "stdout must match on the error path");
    assert.equal(fromMjs.stdout, "", "the error path must not print to stdout");
    assert.notEqual(fromMjs.stderr, "", "the error path must report on stderr");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a domain that excludes every direction fails the same way on both CLIs", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "roll-parity-empty-"));
  try {
    const catalog = writeCatalog(dir, "all-out.md", [
      {
        id: "D01",
        name: "Only",
        family: "f",
        fails: ["zzz"],
        accent_options: [],
        imagery_subjects: [],
        inversion_allowed: false,
      },
    ]);

    const { fromPy, fromMjs } = bothStatusAndStdout([
      "--seed", "abc", "--catalog", catalog, "--domain", "zzz",
    ]);

    assert.notEqual(fromPy.status, 0, "python must reject an all-excluding domain");
    assert.equal(fromMjs.status, fromPy.status, "exit codes must match");
    assert.equal(fromMjs.stdout, fromPy.stdout, "stdout must match on the error path");
    assert.equal(fromMjs.stdout, "", "the error path must not print to stdout");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("-h and --help print help to stdout and exit 0, like argparse", () => {
  for (const flag of ["-h", "--help"]) {
    const { fromPy, fromMjs } = bothStatusAndStdout([flag]);

    assert.equal(fromPy.status, 0, `python ${flag} must exit 0`);
    assert.equal(fromMjs.status, fromPy.status, `${flag} exit codes must match`);
    // Behavioural parity, not byte parity: the usage line legitimately reads
    // "roll.mjs". Help is a stdout artefact and stderr stays empty.
    assert.match(fromPy.stdout, /^usage:/, `python ${flag} writes help to stdout`);
    assert.match(fromMjs.stdout, /^usage: roll\.mjs/, `${flag} writes help to stdout`);
    assert.match(fromMjs.stdout, /--seed/, `${flag} help lists the options`);
    assert.equal(fromMjs.stderr, "", `${flag} must not write to stderr`);
  }
});

test("-h acts immediately, even alongside other flags", () => {
  const { fromPy, fromMjs } = bothStatusAndStdout(["--seed", "abc", "-h"]);

  assert.equal(fromPy.status, 0);
  assert.equal(fromMjs.status, fromPy.status, "exit codes must match");
  assert.match(fromMjs.stdout, /^usage:/, "help must be printed");
  assert.equal(fromMjs.stderr, "", "-h must short-circuit before the seed is generated");
});

test("-h=x is rejected with exit 2 and empty stdout, like argparse", () => {
  const { fromPy, fromMjs } = bothStatusAndStdout(["-h=x"]);

  assert.notEqual(fromPy.status, 0, "python rejects an explicit help argument");
  assert.equal(fromMjs.status, fromPy.status, "exit codes must match");
  assert.equal(fromMjs.stdout, "", "no help is printed on this error path");
});

test("the -- sentinel is unrecognized, not a terminator (argparse parity)", () => {
  const cases = [
    ["--"],
    ["--seed", "abc", "--"],
    ["--", "--seed", "abc"],
    ["--seed", "abc", "extra", "--"],
    ["--seed", "abc", "--", "--wild"],
  ];

  for (const args of cases) {
    const { fromPy, fromMjs } = bothStatusAndStdout(args);
    const label = JSON.stringify(args);

    assert.notEqual(fromPy.status, 0, `python must reject ${label}`);
    assert.equal(fromMjs.status, fromPy.status, `exit codes must match for ${label}`);
    assert.equal(fromMjs.stdout, fromPy.stdout, `stdout must match for ${label}`);
    assert.equal(fromMjs.stdout, "", `the error path must not print a card for ${label}`);
  }
});
