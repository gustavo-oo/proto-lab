#!/usr/bin/env node
// Deterministic seed -> design direction card roller (proto-lab).
//
// Node mirror of scripts/roll.py and of references/seed-algorithm.md. Given a
// seed it draws exactly one direction from the 22-entry machine catalog embedded
// in references/directions.md and fills the five orthogonal knobs, all with a
// single SHA-256 scheme. Same seed + same filtered catalog -> same card; the
// card carries no timestamp for that reason.
//
// Stdout must be byte-identical to roll.py's for the same arguments, so the CLI
// emits canonical JSON exactly as Python's
// `json.dumps(card, sort_keys=True, separators=(",", ":"))` does — including its
// default `ensure_ascii=True`, which escapes every non-ASCII code point as
// `\uXXXX` where JSON.stringify would emit raw UTF-8.
//
// Node built-ins only, Node >= 18.

import { createHash, randomInt } from "node:crypto";
import { readFileSync, realpathSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// --- The hash scheme (verbatim from references/seed-algorithm.md) -----------

// The direction label carries its own leading colon; the hash input is exactly
// `seed + label` (one colon, never `seed + ":" + label`).
const DIRECTION_LABEL = ":direction:v1";
const ALGORITHM = "sha256:v1";

// Each knob draws with its own independent label.
const ACCENT_LABEL = ":accent";
const DENSITY_LABEL = ":density";
const INVERT_LABEL = ":invert";
const RHYTHM_LABEL = ":rhythm";
const IMAGERY_LABEL = ":imagery";

const DENSITY_STEPS = [-1, 0, 1];
const RHYTHMS = ["odd-first", "even-first"];

// Default catalog: ../references/directions.md relative to this script.
const SCRIPT_PATH = fileURLToPath(import.meta.url);
const DEFAULT_CATALOG = path.resolve(path.dirname(SCRIPT_PATH), "..", "references", "directions.md");

// The catalog lives between these markers (mirrors roll.py's CATALOG_JSON_RE).
const CATALOG_JSON_RE = /<!-- CATALOG_JSON_START -->\n([\s\S]*?)\n<!-- CATALOG_JSON_END -->/;

// --- Seed generation (32 adjectives x 32 nouns = 1024 slugs) ----------------

const ADJECTIVES = [
  "quiet", "brutal", "warm", "cold", "soft", "sharp", "calm", "bold",
  "pale", "deep", "bright", "muted", "crisp", "hazy", "sleek", "rugged",
  "gentle", "loud", "slow", "swift", "charcoal", "amber", "velvet", "paper",
  "neon", "dusty", "glass", "copper", "silent", "electric", "feral", "sober",
];

const NOUNS = [
  "harbour", "vector", "signal", "ledger", "meadow", "canyon", "lantern",
  "archive", "orbit", "prism", "atlas", "ember", "grove", "cipher",
  "furnace", "lagoon", "meridian", "quarry", "tapestry", "velocity",
  "anchor", "beacon", "compass", "delta", "fabric", "granite", "helix",
  "inkwell", "junction", "kettle", "lattice", "monolith",
];

/** Raised for the same conditions roll.py reports through ValueError. */
class ValueError extends Error {}

// --- The draw ---------------------------------------------------------------

/**
 * Reduce `sha256(seed + label)` to a 64-bit unsigned integer: big-endian, first
 * 8 bytes, up to 2^64 - 1. BigInt is mandatory here — the value overflows
 * Number.MAX_SAFE_INTEGER, and a modulo on a Number would diverge from Python.
 */
function draw(seed, label) {
  const digest = createHash("sha256").update(seed + label, "utf8").digest();
  let value = 0n;
  for (let offset = 0; offset < 8; offset += 1) {
    value = (value << 8n) | BigInt(digest[offset]);
  }
  return value;
}

/** `draw(...) % size` as a JS array index (the modulo result fits a Number). */
function pickIndex(seed, label, size) {
  return Number(draw(seed, label) % BigInt(size));
}

// --- Catalog ----------------------------------------------------------------

/** Return the machine catalog ordered by direction id. */
function loadCatalog(catalogPath) {
  const source = catalogPath ?? DEFAULT_CATALOG;
  const text = readFileSync(source, "utf8");
  const match = CATALOG_JSON_RE.exec(text);
  if (match === null) {
    throw new ValueError(
      "no catalog block between <!-- CATALOG_JSON_START --> and " +
        `<!-- CATALOG_JSON_END --> in ${source}`,
    );
  }
  let catalog;
  try {
    catalog = JSON.parse(match[1]);
  } catch (error) {
    // Python raises json.JSONDecodeError, a ValueError subclass, so main()
    // reports it the same way as a missing block.
    throw new ValueError(`invalid catalog JSON in ${source}: ${error.message}`);
  }
  return catalog
    .slice()
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
}

/** True when any `fails` tag is a case-insensitive substring of domain. */
function excludedByDomain(direction, domain) {
  if (!domain) return false;
  const needle = domain.toLowerCase();
  return direction.fails.some((tag) => needle.includes(tag.toLowerCase()));
}

// --- Card -------------------------------------------------------------------

/** Fill the five orthogonal knobs for the drawn direction. */
function knobs(direction, seed) {
  const accents = direction.accent_options;
  const subjects = direction.imagery_subjects;

  return {
    accent: accents.length
      ? accents[pickIndex(seed, ACCENT_LABEL, accents.length)]
      : null,
    density_shift: DENSITY_STEPS[pickIndex(seed, DENSITY_LABEL, DENSITY_STEPS.length)],
    inversion: Boolean(
      direction.inversion_allowed && draw(seed, INVERT_LABEL) % 2n === 1n,
    ),
    rhythm: RHYTHMS[pickIndex(seed, RHYTHM_LABEL, RHYTHMS.length)],
    imagery_subject: subjects.length
      ? subjects[pickIndex(seed, IMAGERY_LABEL, subjects.length)]
      : null,
  };
}

/** Draw the CARD SCHEMA from a pre-loaded catalog (ordered by id). */
function drawCard(catalog, seed, domain = null, wild = false) {
  const excluded = catalog
    .filter((entry) => excludedByDomain(entry, domain))
    .map((entry) => entry.id);
  const survivors = catalog.filter((entry) => !excludedByDomain(entry, domain));
  if (survivors.length === 0) {
    throw new ValueError(`domain ${pythonRepr(domain)} excludes every direction; widen the domain`);
  }

  const direction = survivors[pickIndex(seed, DIRECTION_LABEL, survivors.length)];

  return {
    seed,
    algorithm: ALGORITHM,
    direction_id: direction.id,
    direction_name: direction.name,
    family: direction.family,
    knobs: knobs(direction, seed),
    filters: { domain: domain || null, excluded },
    wild: Boolean(wild),
  };
}

/** Return a fresh `adjective-noun` slug (lowercase, ASCII, 1024 options). */
function newSeed() {
  return `${ADJECTIVES[randomInt(ADJECTIVES.length)]}-${NOUNS[randomInt(NOUNS.length)]}`;
}

// --- Canonical JSON (mirrors Python's json.dumps) ---------------------------

/**
 * Serialize like `json.dumps(value, sort_keys=True, separators=(",", ":"))`.
 *
 * sort_keys: object keys are emitted in sorted order. The card's keys are all
 * ASCII, so JS's default string order equals Python's code-point order.
 * separators: no space after `,` or `:`.
 * ensure_ascii: non-ASCII code points are escaped by pythonString below.
 */
function canonicalJson(value) {
  if (value === null) return "null";
  switch (typeof value) {
    case "boolean":
      return value ? "true" : "false";
    case "number":
      return String(value);
    case "string":
      return pythonString(value);
    case "object":
      if (Array.isArray(value)) {
        return `[${value.map(canonicalJson).join(",")}]`;
      }
      return `{${Object.keys(value)
        .sort()
        .map((key) => `${pythonString(key)}:${canonicalJson(value[key])}`)
        .join(",")}}`;
    default:
      throw new TypeError(`cannot serialize a ${typeof value}`);
  }
}

/** Escape a string exactly as Python's json encoder does with ensure_ascii. */
function pythonString(value) {
  let out = '"';
  for (const character of value) {
    const code = character.codePointAt(0);
    if (character === '"') out += '\\"';
    else if (character === "\\") out += "\\\\";
    else if (character === "\n") out += "\\n";
    else if (character === "\r") out += "\\r";
    else if (character === "\t") out += "\\t";
    else if (character === "\b") out += "\\b";
    else if (character === "\f") out += "\\f";
    else if (code >= 0x20 && code <= 0x7e) out += character;
    else if (code <= 0xffff) out += unicodeEscape(code);
    else {
      // Astral code point: Python emits the UTF-16 surrogate pair.
      const offset = code - 0x10000;
      out += unicodeEscape(0xd800 + (offset >> 10));
      out += unicodeEscape(0xdc00 + (offset & 0x3ff));
    }
  }
  return `${out}"`;
}

function unicodeEscape(code) {
  return `\\u${code.toString(16).padStart(4, "0")}`;
}

/** A close-enough Python `repr` for the string shown in error messages. */
function pythonRepr(value) {
  if (value === null || value === undefined) return "None";
  if (typeof value !== "string") return String(value);

  const quote = value.includes("'") && !value.includes('"') ? '"' : "'";
  let out = quote;
  for (const character of value) {
    const code = character.codePointAt(0);
    if (character === "\\") out += "\\\\";
    else if (character === quote) out += `\\${quote}`;
    else if (character === "\n") out += "\\n";
    else if (character === "\r") out += "\\r";
    else if (character === "\t") out += "\\t";
    else if (code < 0x20 || code === 0x7f) {
      out += `\\x${code.toString(16).padStart(2, "0")}`;
    } else out += character;
  }
  return `${out}${quote}`;
}

// --- CLI (mirrors the argparse surface of roll.py) --------------------------

const USAGE =
  "usage: roll.mjs [-h] [--seed SEED] [--domain DOMAIN] [--wild] [--out OUT]\n" +
  "                [--catalog CATALOG]";

const HELP = `${USAGE}

Roll a deterministic design direction card from a seed.

options:
  -h, --help            show this help message and exit
  --seed SEED           seed string (generated when omitted)
  --domain DOMAIN       declared domain; prunes incompatible directions
  --wild                record the wild variant
  --out OUT             also write the card JSON to this path
  --catalog CATALOG     path to directions.md (defaults to the repo copy)
`;

// Option -> shape. `--wild` takes no value; `-h`/`--help` exit immediately.
// `-h` is registered so the short flag mirrors argparse instead of being
// reported as unrecognized.
const OPTIONS = {
  "-h": "help",
  "--help": "help",
  "--seed": "value",
  "--domain": "value",
  "--wild": "flag",
  "--out": "value",
  "--catalog": "value",
};

// argparse's _negative_number_matcher: a negative number is a value, not an
// option, so `--seed -1` is accepted.
const NEGATIVE_NUMBER_RE = /^-\d+$|^-\d*\.\d+$/;

function usageError(message) {
  process.stderr.write(`${USAGE}\nroll.mjs: error: ${message}\n`);
  process.exit(2);
}

/** Resolve a long option name, honoring argparse's unambiguous prefixes. */
function resolveOption(name) {
  if (Object.hasOwn(OPTIONS, name)) return name;
  const matches = Object.keys(OPTIONS).filter((flag) => flag.startsWith(name));
  return matches.length === 1 ? matches[0] : null;
}

/** True when a token must be read as an option rather than as a value. */
function looksLikeOption(token) {
  return token.startsWith("-") && token !== "-" && !NEGATIVE_NUMBER_RE.test(token);
}

function parseArgs(argv) {
  const options = { seed: null, domain: null, wild: false, out: null, catalog: null };
  const extras = [];

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === "--") {
      // argparse has no positionals here, so the sentinel itself is consumed as
      // an unrecognized argument (and everything after it is not parsed as an
      // option): `--seed abc --` exits 2 with "unrecognized arguments: --".
      extras.push(...argv.slice(index));
      break;
    }
    if (!looksLikeOption(token)) {
      extras.push(token);
      continue;
    }

    const equals = token.indexOf("=");
    const name = equals === -1 ? token : token.slice(0, equals);
    const inline = equals === -1 ? null : token.slice(equals + 1);
    const canonical = resolveOption(name);
    if (canonical === null) {
      extras.push(token);
      continue;
    }

    const shape = OPTIONS[canonical];
    if (shape === "help") {
      if (inline !== null) {
        usageError(`argument -h/--help: ignored explicit argument ${pythonRepr(inline)}`);
      }
      process.stdout.write(HELP);
      process.exit(0);
    }
    if (shape === "flag") {
      if (inline !== null) {
        usageError(`argument ${canonical}: ignored explicit argument ${pythonRepr(inline)}`);
      }
      options[canonical.slice(2)] = true;
      continue;
    }

    let value = inline;
    if (value === null) {
      const next = argv[index + 1];
      if (next === undefined || looksLikeOption(next)) {
        usageError(`argument ${canonical}: expected one argument`);
      }
      value = next;
      index += 1;
    }
    options[canonical.slice(2)] = value;
  }

  if (extras.length > 0) usageError(`unrecognized arguments: ${extras.join(" ")}`);
  return options;
}

function main(argv) {
  const options = parseArgs(argv);

  let seed = options.seed;
  if (!seed) {
    seed = newSeed();
    process.stderr.write(`seed: ${seed}\n`);
  }

  let card;
  try {
    card = drawCard(loadCatalog(options.catalog), seed, options.domain, options.wild);
  } catch (error) {
    if (error instanceof ValueError) usageError(error.message);
    throw error;
  }

  const text = canonicalJson(card);
  if (options.out) writeFileSync(options.out, `${text}\n`, "utf8");
  process.stdout.write(`${text}\n`);
  return 0;
}

/** True when this file was launched directly, so importing it stays inert. */
function isMainModule() {
  if (process.argv[1] === undefined) return false;
  try {
    return realpathSync(process.argv[1]) === realpathSync(SCRIPT_PATH);
  } catch {
    return false;
  }
}

if (isMainModule()) {
  // Set exitCode instead of calling process.exit so stdout can drain first.
  process.exitCode = main(process.argv.slice(2));
}
