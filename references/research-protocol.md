# Research protocol

`references/research-protocol.md` is the normative specification of pipeline
step 2 (§5.5): the **runtime, cited competitor research** the skill runs *before*
decision points are derived. It defines the `research.md` format — a small corpus
of SOURCE CARDS — that downstream consumers read by name: the decision-point
derivation (T16) and the judge (T16/T19).

The research answers one question for the brief's domain: **what do real
products in this space already do, and which of those choices are clichés to
avoid?** It is evidence gathering, not design. It never reads the target
project's code or UI (only the brief and its specs/docs supply requirements);
everything here comes from the open web.

The output is free, small and cited: **3–6 sources**, each with a URL, written to
`research.md` inside the prototype folder. It is cached there and reused by later
sessions on the same product.

## Protocol

The research step turns the brief's **domain** into a bounded set of sources and
mines each one for good and bad patterns.

**How many.** Use **3–6 sources**: minimum **3** (fewer is not a sample, it is an
anecdote) and maximum **6** (the pipeline cap — more does not change the
directions, it only spends time). If direct competitors are scarce, reach for
usage-pattern analogues and category references to make the floor; only when even
those are unavailable, record the shortfall honestly in the header instead of
padding with off-domain pages.

**Choosing sources**, in priority order — stop when the budget is spent:

1. **Direct competitors** — products that do the same job for the same audience
   (the brief's product category). These give the strongest read on the domain's
   conventions and its clichés.
2. **Usage-pattern analogues** — products from other categories that solve the
   *same structural problem* (e.g. for an admin tool: a dense analytics console;
   for onboarding: a consumer app's first-run flow). Use these when the domain is
   niche and direct competitors are few or inaccessible.
3. **Category references** — catalogued or editorial sources for the category
   (design galleries, platform HIG-style references). Weakest signal; use to fill
   the floor of 3 only when 1 and 2 run out.

Prefer real, shipped products over mockups and marketing pages: a screenshot of
an actual flow is evidence, a landing-page hero is not.

**How.** A dedicated subagent (fresh context) runs web search + fetch against
each chosen source. When a browser tool is available, add screenshots and click
the real flow (`file://`-free, live pages); screenshots are first-class evidence.
When it is not available, work from fetched markup, visible text and public
documentation, and downgrade every unrendered claim to an inference (see below).
No paid catalogs are required — direct browsing of competitors is the free
substitute (§7 of the landscape report).

**Stop condition.** The step ends when the budget is spent, the source bound is
reached, or new sources stop adding new patterns — whichever comes first.

## Source card

One card per source, all sharing the same seven keys. This is the interface the
downstream consumers read by name; a card missing a key is not a card.

```json
{
  "name": "<product / site name>",
  "url": "https://<exact page(s) studied>",
  "category": "direct-competitor | usage-analogue | category-reference",
  "good_patterns": [
    "<observed pattern> — evidence: <what was actually seen and where>"
  ],
  "bad_patterns": [
    "<observed pattern> — evidence: <what was actually seen and where>"
  ],
  "what_to_copy": "<one or two lines: the pattern worth borrowing and why>",
  "what_to_avoid": "<one or two lines: the cliché/failure worth steering away from>"
}
```

Rules for a card:

- `name` and `url` are mandatory — **every source is cited with its URL**, no
  uncited pattern. Cite the specific page(s) studied, not just the homepage.
- `category` is exactly one of `direct-competitor`, `usage-analogue`,
  `category-reference` (the priority order above).
- `good_patterns` and `bad_patterns` are **lists of observed items**, each with
  its inline evidence. Both may be empty for a source — an empty list is a
  finding, not a gap to fill with guesses.
- `what_to_copy` / `what_to_avoid` are the distilled one-or-two-line takeaways
  the generators and the judge actually consume. They must be traceable to the
  observed lists above; never introduce a claim that no evidence supports.

`research.md` is the header (brief domain, sources used, mode) followed by one
card per source, in JSON or in the equivalent markdown block per source.

## Observed vs inferred

The load-bearing discipline: **a claim about a UI cites page evidence; anything
that is not directly seen is marked as inference.** (This mirrors the
first-party guidance of catalog tools like Mobbin: treat it as evidence, cite
sources, don't infer causality.)

- **Observed** — you saw it on the page: a selector, a region of markup, visible
  copy, or a screenshot. Write what was seen *and where*. `"sticky filter rail on
  the results page (evidence: left column persists while the grid scrolls,
  screenshot #2)"` is an observation.
- **Inferred** — you are reasoning past what you saw: intent, causality ("they do
  X because Y"), or behaviour on a screen you could not open. Mark it
  explicitly, e.g. `"inferred: the rail likely collapses on mobile"`.
- **Never** present an inference as an observation, and never let a plausible
  guess sit in `good_patterns` / `bad_patterns` without its evidence or its
  `inferred:` marker.
- If a source could not be opened at all, record that as such — a known unknown
  is more useful to the generators than a confident fabrication.

Inferences are still useful: they are **hypotheses** the point derivation and
the judge may act on, clearly labelled so they are never mistaken for facts.
Degraded or not, the bar is the same: the difference between observation and
inference stays visible in the artifact.

## Timebox

The research is **time-boxed** — it is a means to better directions, not a
project in its own right. Give it a fixed slice, and when it runs out, finish the
cards for the sources already studied and mark the rest as not reached. A
half-filled, honest `research.md` beats an exhaustive one that delayed the
prototype.

**When to disable it.** Pass `--skip-research` to turn the step off entirely. Use
it when:

- the domain is already well known internally and the sources would only confirm
  conventions the team already holds;
- the brief forbids external reference or the network/browser tools are
  unavailable;
- the run is a re-roll or a rerun where `research.md` already exists and is still
  valid (reuse, not re-fetch — see below);
- time pressure: research is the first thing to cut, because it is the cheapest
  step to redo later.

With `--skip-research`, no `research.md` is produced and the consumers run
without it; nothing else in the pipeline changes.

**Cache and reuse.** Write `research.md` once, into the prototype folder (the
same folder as `direction.json`, `points.json` and the variants). Later sessions
on the same product **reuse the cached file** rather than re-running the search:
re-deriving directions from unchanged research must not depend on what the web
returns that day. Refresh it only when the domain changes, the cache is stale by
the team's own judgement, or a source is known to have shipped a redesign — and
when you refresh, replace the file; the cache is a single current corpus, not an
append log.

## How the result is used

`research.md` feeds three consumers; it changes none of their contracts:

1. **Decision points.** Patterns the domain shares (and the places competitors
   diverge) suggest candidate structural decisions. A pattern observed across
   most sources is a convention the variants should consciously keep or break; a
   structural divergence between competitors is a ready-made point axis.
2. **The judge.** The cited bad patterns and clichés become domain-specific
   `slop-scan` / `direction-fidelity` criteria: the judge checks the variants
   against the domain's own failure modes, not only the generic fingerprints.
3. **Copy and content realism.** Real domain vocabulary, entity names and
   screen vocabulary make illustrative copy read like the product rather than
   like lorem — improving `brief-fidelity` and the fresh-eyes `strangeness` pass.

Research informs; it never dictates. The decision points still come from the
brief's structural uncertainties, the direction still comes from the seed card,
and only observed evidence (or clearly marked inference) may be cited.
