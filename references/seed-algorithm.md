# Seed algorithm

`references/seed-algorithm.md` is the normative specification of how a seed
becomes a **direction card**. It is implemented by `scripts/roll.py` and its
JavaScript mirror `scripts/roll.mjs`; both must produce byte-identical cards
for the same seed and catalog. The card is written to `direction.json` inside
each prototype folder.

Determinism is the whole point: **the same seed and the same filtered catalog
always yield the same card**. The card carries no timestamp for exactly this
reason.

## Algorithm

The direction is drawn from the filtered catalog with a single SHA-256 hash.

```python
import hashlib

DIRECTION_SALT = ":direction:v1"

def direction_index(seed, filtered_catalog_ordered_by_id):
    digest = hashlib.sha256(f"{seed}:direction:v1".encode("utf-8")).digest()
    n = int.from_bytes(digest[:8], "big")
    return n % len(filtered_catalog_ordered_by_id)
```

Normative rules:

1. Hash input is the seed joined to the versioned salt: `sha256(f"{seed}:direction:v1")`.
   The `":direction:v1"` suffix versions the scheme; bumping it is a breaking change.
2. The digest is reduced to an integer with `int.from_bytes(digest[:8], "big")`
   (big-endian, first 8 bytes — 64 bits).
3. `index = n % len(filtered_catalog_ordered_by_id)`. The catalog is **ordered
   by direction id** (`D01` … `D22`) before the modulo, so the mapping is stable.
4. The filtered catalog is never empty: an over-restrictive `--domain` is
   reported to the user instead of silently un-filtering.

**Source of truth.** The committed `direction.json` is authoritative. Re-running
the script is a convenience, not a requirement: even if the script, the catalog
or the seed is unavailable later, the recorded card wins. Nothing downstream
re-derives the direction.

**Reroll.** A reroll is simply a new seed, which produces a new card. Discarded
seeds, together with the reason they were discarded, are recorded in
`decisions.md`. Rerolling never mutates an existing card.

## Card schema

`direction.json` has **exactly these 8 top-level keys**, with no timestamp and
no extra metadata:

| Key              | Type                        | Meaning |
| ---------------- | --------------------------- | ------- |
| `seed`           | string                      | The seed string that produced the card. |
| `algorithm`      | string, literal `"sha256:v1"` | Scheme identifier, pinned to the `:direction:v1` salt. |
| `direction_id`   | string `D01`–`D22`          | Catalog id of the drawn direction. |
| `direction_name` | string                      | Human-readable name of the direction. |
| `family`         | string                      | Direction family (e.g. `quiet`, `dark`, `retro`, `print`). |
| `knobs`          | object                      | Orthogonal variations, see **Knobs**. |
| `filters`        | object `{domain, excluded}` | Domain filter applied at draw time. |
| `wild`           | boolean                     | Whether the variant drew its own direction (`--wild`). |

`filters` is `{"domain": str | null, "excluded": [direction ids]}`: the declared
domain (or `null` when none) and the ids pruned by the domain filter.

Example card:

```json
{
  "seed": "cafe-com-leite",
  "algorithm": "sha256:v1",
  "direction_id": "D01",
  "direction_name": "Swiss International",
  "family": "print",
  "knobs": {
    "accent": "#0018A8",
    "density_shift": 1,
    "inversion": false,
    "rhythm": "odd-first",
    "imagery_subject": "typographic specimen"
  },
  "filters": {
    "domain": null,
    "excluded": []
  },
  "wild": false
}
```

## Knobs

`knobs` holds the orthogonal variations the seed controls. The direction owns
everything else (grid, type class, radius, motion, imagery genre); these knobs
must never re-roll the direction itself.

| Key               | Type                          | Source |
| ----------------- | ----------------------------- | ------ |
| `accent`          | string \| null                | Direction's allowed accent logic. |
| `density_shift`   | `-1` \| `0` \| `1`            | Uniform draw over three steps. |
| `inversion`       | boolean                       | Only when the direction allows it. |
| `rhythm`          | `"odd-first"` \| `"even-first"` | Uniform draw over two options. |
| `imagery_subject` | string \| null                | Direction's imagery subjects. |

Each knob is drawn with its **own salt**, reusing the same hashing scheme as
the direction (`int.from_bytes(digest[:8], "big")`, then modulo the option
count):

```python
def draw(seed, salt):
    digest = hashlib.sha256(f"{seed}:{salt}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")
```

The salts are `":accent"`, `":density"`, `":invert"`, `":rhythm"` and
`":imagery"`. Distinct salts keep the knobs statistically independent.

- **accent** — `accent = direction.accent_options[draw(seed, ":accent") % len(direction.accent_options)]`.
  A direction whose allowed logic is monochrome has no accent options and
  resolves to `null`.
- **density** — `density_shift = [-1, 0, 1][draw(seed, ":density") % 3]`.
- **inversion** — `inversion = direction.inversion_allowed and (draw(seed, ":invert") % 2 == 1)`.
  `inversion_allowed` is a per-direction field; when it is false the knob is
  always `false`, so a direction that has no dark register is never inverted.
- **rhythm** — `rhythm = ["odd-first", "even-first"][draw(seed, ":rhythm") % 2]`.
- **imagery** — `imagery_subject = direction.imagery_subjects[draw(seed, ":imagery") % len(direction.imagery_subjects)]`,
  or `null` when the direction declares no imagery subjects.

## Domain filter

The domain filter prunes directions that are incompatible with a declared
domain. A direction is **excluded** when any tag in its `fails` list is a
case-insensitive substring of the `--domain` text:

```python
def excluded_by_domain(direction, domain):
    if not domain:
        return False
    needle = domain.lower()
    return any(tag.lower() in needle for tag in direction.fails)
```

Normative rules:

1. When `--domain` is omitted (or vague), nothing is excluded and the draw is
   fully free.
2. The filter only **prunes declared incompatibilities** — for example a dense
   booking table must not land on a slow-living direction. It never blends or
   averages directions.
3. The surviving catalog is ordered by id before the modulo.
4. The applied filter is recorded in the card's `filters` object as
   `{"domain": <domain or null>, "excluded": [<ids>]}`.
5. `--wild` is orthogonal to the domain filter.

## Seed generation

When `--seed` is not supplied, the seed is generated in-session and then shown
to the user and recorded in the card.

```python
import random

_rng = random.SystemRandom()

def generate_seed():
    adjective = _rng.choice(ADJECTIVES)
    noun = _rng.choice(NOUNS)
    return f"{adjective}-{noun}"
```

Normative rules:

1. Use `random.SystemRandom` (cryptographically strong, not the shared
   `random` state), so two sessions do not collide.
2. The script embeds two lists: **32 adjectives** and **32 kebab-case nouns**
   (for example `cafe-com-leite`), giving 1024 combinations.
3. The format is `adjective-noun` — lowercase, single hyphens, ASCII. Examples:
   `quiet-harbour`, `cafe-com-leite`, `brutal-vector`.
4. The generated seed is printed and stored verbatim in the card's `seed`
   field, so the draw can always be reproduced or rerolled.
