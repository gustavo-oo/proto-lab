# Degradation notes

Evidence for the three degraded routes of spec §8 / `SKILL.md` §*Degradation*,
exercised against `examples/coffee-log-cafe-com-leite/` (direction **D10
Blueprint / Schematic**, seed `cafe-com-leite`, family `technical`). Consumed by
**T26** (audit) and **T27**.

Three binding rulings shape the setup:

- **No artifact is mutated (R22).** The example under test stays byte-identical:
  the degraded judge of route 2 ran against a **scratch copy**, and every offline
  page was only *read* over `file://`.
- **No binaries in the repo (R23).** Screenshots live in a git-ignored temp
  directory outside the worktree and are cited by absolute path (path + dimensions
  + what was observed), never committed.
- **Subagent-dependent steps use an external process (R25).** Route 2's code-only
  judge ran as `opencode run --standalone --auto`, the T18 method; this harness
  has no `subagent` tool.

| route | edge case (spec §8) | result | one-line evidence |
|---|---|---|---|
| 1 | Offline / webfont does not load | **holds** | with the font CDN blocked, D10's body stays monospace (`mmmm == iiii` → Menlo) and its display stays condensed sans (Archivo Narrow → Arial Narrow); 6 screenshots, before/after |
| 2 | No browser tool | **holds** | code-only judge still wrote `judge-report.md` with `mode: degraded` and the five axes; two runs, verdicts differ |
| 3 | No python3/node (here: no `node`) | **holds** | `roll.py --seed abc` exits 0 without `node` and without `roll.mjs`; all outputs byte-identical (sha256 `266f80fc…`) |

Reading order for context: spec §8 (degradation table), `SKILL.md` §*Degradation*,
`references/judge-rubric.md` §*Degraded mode*.

---

## Route 1 — Offline / webfont does not load: is the register preserved?

**Setup.** `agent-browser` 0.38.1 (Chromium 153, headless), isolated session and
namespace `t20-offline`. The font CDN was blocked two ways at once, because
neither is sufficient on its own here:

- request interception on the CDN host:
  `agent-browser network route "*fonts.googleapis.com*" --abort` and
  `agent-browser network route "*fonts.gstatic.com*" --abort`;
- browser-level offline (`agent-browser set offline on` → `navigator.onLine ===
  false`), which is the strict superset of "the webfont cannot load".

`allowedDomains: []` (the brief's first suggestion) is **not usable with
`file://`**: the allowlist guard requires a parseable hostname and rejects the
navigation with `No hostname in URL: file://…`. The route/offline pair is the
"equivalent block on the font CDN" the brief allows.

Measured in the page: `document.fonts.size` (declared `@font-face` rules) and
canvas `measureText` at 13px, reported as `mmmm/iiii` px widths — *equal widths
prove the resolved face is monospace*, and the width fingerprints identify
exactly which face won. Declared stacks under test (from the pages' own `:root`):

```
--mono : 'Space Mono','IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace
--label: 'Archivo Narrow','Arial Narrow','Helvetica Neue',Arial,sans-serif
```

| # | page | register it carries | online (CDN up) | offline (CDN blocked) | register preserved? |
|---|---|---|---|---|---|
| 1 | `variants/d1-c/index.html` (chosen listing/feed) | D10: monospace body + condensed-sans display | `faces=15`, `httpRes=1`, body **Space Mono** (`31.82/31.82`), display **Archivo Narrow** (`35.52/11.86`) | `faces=0`, CDN stylesheet `status None (aborted)`, body **Menlo** (`31.31/31.31`), display **Arial Narrow** (`35.52/9.47`) | **yes** — class held: monospace stays monospace (`mmmm==iiii`), sans stays sans; display stays *condensed* (Archivo Narrow → Arial Narrow) |
| 2 | `chosen/d1/index.html`, `chosen/d1/detail.html` | D10, frozen copy of variant c | identical to row 1 | identical to row 1 | **yes** — `cmp` says these files are byte-identical to `variants/d1-c/*`, so the same fallback applies |
| 3 | `styleguide.html` (consumes `tokens.css`) | D10 (`--font-display` / `--font-body` / `--font-mono`) | `faces=0`, `httpRes=0`: it links **no** font CDN at all, body Menlo `31.31/31.31`, display Arial Narrow `35.52/9.47` | byte-for-byte the same measurements | **yes — and independent of the network**, because this page never had a webfont to lose |
| 4 | `index.html` (session gallery), `points/d1-coffee-log.html` (canvas) | gallery-template **neutral** register (`system-ui…` text + `ui-monospace` mono), not D10 | body `44.94/12.54` (proportional `system-ui`), no network | identical (`onLine:false`, `faces=0`, same widths) | **n/a** — no webfont and no D10 register involved; the known template-vs-doc mismatch (Task 12/T19) shows up here and is not a D10 failure |

Reference fingerprints on this machine: `Menlo 31.31/31.31`, `sans-serif
43.32/11.55`, `serif 40.45/14.45`, `'Arial Narrow' 35.52/9.47`, `Arial
43.32/11.55`. Online the body stack measures `31.82` (≠ Menlo `31.31` → the
Space Mono webfont really was in use) and the display stack `11.86` (≠ Arial
Narrow `9.47` → Archivo Narrow really was in use); offline each stack lands
exactly on its local fallback.

**Before/after (screenshots, absolute paths, not committed).** All captured from
`file:///private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-wt/t20/examples/coffee-log-cafe-com-leite/`
with the browser tool; the temp dir is outside the repo:

- Online, `variants/d1-c/index.html` @1280×900 →
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-shots/s1-online-d1-c-1280.png`
- Offline, same URL @1280×900 →
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-shots/s2-offline-d1-c-1280.png`
- Offline, same URL @390×844 →
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-shots/s3-offline-d1-c-390.png`
- Online, same URL @390×844 →
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-shots/s4-online-d1-c-390.png`
- Offline, `styleguide.html` @1280×900 →
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-shots/s5-offline-styleguide-1280.png`
- Online, `styleguide.html` @1280×900 →
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-shots/s6-online-styleguide-1280.png`

(Full prefix: `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/`.)

What they show: `s1` vs `s2` (and `s4` vs `s3`) are the same page — same grid
paper, same column alignment, same line-wrapping inside every entry (`cacau,
castanha-do-pará, mel; corpo alto, final curto` breaks at the same word), the
monospace log body and the condensed `DIÁRIO` / entry titles intact; the only
difference is the face itself (Space Mono→Menlo, Archivo Narrow→Arial Narrow).
`s5` and `s6` are **byte-identical** (`md5 3e977faed0bf851f8204eb9683d67e79`),
which is the observed consequence of row 3.

**Verdict.** Register preserved. The fallback stacks keep the type **class** that
carries D10's technical register — monospace body (provably monospace: `mmmm ==
iiii`) and condensed sans display — with the webfont unavailable. Two honest
caveats:

- the *condensation* of the display fallback depends on a locally installed
  `Arial Narrow`; on a machine without it the stack degrades to `Helvetica
  Neue`/`Arial` — still the same sans class, but the narrow silhouette is lost
  (`35.52/9.47` → `44.36/11.54`);
- this is a rendered observation (the network really was cut), unlike the
  earlier T19 note, which reasoned the same fallbacks from the declared stacks
  only.

---

## Route 2 — No browser tool: the judge stays code-first and still emits the 5 axes

**Method (R25).** This harness exposes no `subagent` tool, so the no-browser-tool
judge ran as an **external** process, the same way T18's scenarios did:

```
cd <scratch>/coffee-log-cafe-com-leite
PWD=$(pwd) opencode run --standalone --auto \
  --title "T20 judge degraded (code-only, no browser)" "$(cat <scratch>/prompts/judge-degraded.txt)"
```

- **Scratch copy (R22)** — the committed example was never touched:
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/coffee-log-cafe-com-leite/`
  (a `cp -R` of `examples/coffee-log-cafe-com-leite/`).
- **Prompt**: `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/prompts/judge-degraded.txt` — it bundles the
  skill (SKILL.md + `references/` + `scripts/` + `assets/` copied to
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/_skill/`), declares "this harness has NO browser tool",
  and asks for `judge-report.md` per `references/judge-rubric.md` §*Degraded mode*
  and §*Report template*, with only `judge-report.md` allowed to change.
- **Report produced**: `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/coffee-log-cafe-com-leite/judge-report.md`
  (11 726 bytes, 46 lines, model `deepseek-v4.1-flash`); log at
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/logs/judge-degraded-run2.log` (exit `rc=0`).

**Result — the 5 axes are all present.**

| axis | verdict | evidence cited by the judge (abridged) |
|---|---|---|
| `brief-fidelity` | PASS | each variant answers point `d1` in its declared shape (`table.spec`+`colgroup` / `ul.cards` with `minmax(210px,1fr)` / `ol.feed__list`), both key screens present, no binary assets, 640px media query on the 390px target |
| `strangeness` | PASS | DOM-order walkthrough; contrasts computed from declared colours (`--muted` 8.0:1, `--annot` 6.3:1, `--ink` ≫ 4.5:1); affordances live; perceptual pass left to the human |
| `slop-scan` | PASS | machine gate **actually run**: `python3 ../_skill/scripts/check_slop.py variants/*/*.html` → `{"hits": [], "count": 0, "verdict": "pass"}`, exit 0; judge-only F16/F18/F21/F22 absent |
| `direction-fidelity` | PASS | D10 DNA → file (mono + condensed labels with same-class fallbacks, white-blue inversion, `#00E5FF` single accent, 0 radius, graph-paper substrate, `.titleblock`); C5 failure modes avoided |
| `variant-diversity` | PASS | structural diff on `listing-pattern` (comparative table vs tile grid vs chronological feed) plus three navigation models; no blended/4th shape |

The header carries `mode: degraded (code-first, no browser tool)`; the report has
`## Findings` (six `minor`, no `blocker`/`major`) and `## Open (not fixed)` with
three explicit `assumption:` lines, one of them: *"no browser tool — every
'reads/wraps/overlaps/competes' statement above is derived from markup and
declarations; the rendered check belongs to the human"*. No screenshot was taken
or looked for. `diff -rq examples/coffee-log-cafe-com-leite <scratch copy>`
reports **only** `judge-report.md` as different, so the degraded judge wrote the
report and nothing else.

**Caveat — verdicts are not stable across judge runs (honest observation).**
A first degraded run, launched the same way but with the committed full-mode
`judge-report.md` still sitting in the scratch cwd, produced the same five axes
with a different `strangeness` verdict (**FAIL**) and one `major`: the 0–5 score
gauge is carried only by `--accent #00E5FF` ticks on `#F4F7FA`, "1.43:1 … below
the 3:1 non-text floor". That arithmetic checks out independently — computed
here from the declared hexes: `#00E5FF` on `#F4F7FA` = **1.43:1** (on `#FFFFFF` =
1.54:1), while `--ink-2` on white = 11.64:1. The clean second run did not raise
it. Both reports are kept
(`/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/originals/judge-degraded-run1.md`, and the run-2 report
at the path above); the route tested here — *the judge still produces
`judge-report.md` with the five axes without a browser* — holds in both, but the
verdicts and findings are run-dependent. T26/T27 should read them as two samples,
not one truth. (Run 1 also flagged itself: *"fresh-eyes independence: lost
(inline) … the previous `judge-report.md` was in context"*.)

---

## Route 3 — No `node` (and no `roll.mjs`): the roller still produces the card

`roll.py` is the reference implementation and `direction.json` is the committed
source of truth, so the Node mirror is a convenience, never a gate.

**Proof that `node` is absent in the tested environment.** A PATH containing
only a `python3` symlink was used:

```
PATH=/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-t20-scratch/nonode-bin
$ command -v node   →  FAILED, rc=1
$ node scripts/roll.mjs --seed abc
  sh: node: command not found            rc=127
```

(The normal developer PATH does have `node` at
`/Users/gustavo/.asdf/shims/node`, so the
absence above is real, not an accident of the shell.)

**Commands and output.** Three runs, all with `--seed abc`:

```
# 1. normal PATH
$ python3 scripts/roll.py --seed abc                              # exit 0
# 2. no node (restricted PATH, worktree scripts/)
$ env PATH=<nonode-bin> python3 scripts/roll.py --seed abc        # exit 0
# 3. no node AND no roll.mjs: scripts/ + references/ copied to scratch,
#    then rm scripts/roll.mjs
$ env PATH=<nonode-bin> python3 scripts/roll.py --seed abc        # exit 0

{"algorithm":"sha256:v1","direction_id":"D03","direction_name":"Broadsheet Newsprint",
 "family":"print","filters":{"domain":null,"excluded":[]},
 "knobs":{"accent":"#C8102E","density_shift":1,"imagery_subject":"pull-quote box",
          "inversion":false,"rhythm":"odd-first"},"seed":"abc","wild":false}
```

**Verdict.** The card is produced and `roll.mjs` is not needed: all three runs
emit 291 bytes with the same digest
`266f80fc83d07480330f5c93b7cc5cac28559c734215c402676875d8026d77b1`, and the
no-`roll.mjs` copy is identical to the normal-PATH output (R22 respected — the
repo's `scripts/roll.mjs` was never touched). Supporting check for the same
principle ("the artifact is the source of truth"): `roll.py --seed cafe-com-leite`
still reproduces the committed `examples/coffee-log-cafe-com-leite/direction.json`
exactly, offline and without node.

---

## Environment facts

- Browser tool used for route 1: `agent-browser` 0.38.1 / Chromium 153 via the
  MCP tools (`agent_browser_open`, `agent_browser_eval`,
  `agent_browser_screenshot`), namespace + session `t20-offline`, plus the CLI
  for the two subcommands the MCP `core` profile does not expose (`network
  route`, `set offline`). Chromium was headless (the tool reported a
  `HeadlessChrome/153.0.0.0` user agent).
- `python3` 3.15.0 at `/opt/homebrew/bin/python3`; `node` v22.21.1 present on the
  normal PATH (`/Users/gustavo/.asdf/shims/node`) and provably absent under the
  restricted PATH above. macOS 26.6.2 (arm64).
- No artifact was modified: `git status` in the worktree stayed clean for
  `examples/` and `scripts/` throughout.
- **JeV**: not available for this task — `jev_check` returned `429: Rate limit
  exceeded. Please try again later.` on three attempts (including a trivial
  probe), so the two machine-verified judgements here (offline font-class
  preservation; card identity across the no-node runs) rest on the measurements
  and byte digests above instead of a classifier verdict.
- Provider flakiness: none observed — the two `opencode run` judge processes both
  exited `rc=0` (3 m 19 s and ~3 m 40 s wall time, model `deepseek-v4.1-flash`);
  the only flaky dependency was the JeV MCP's HTTP rate limit.
