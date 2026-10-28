# UX-law checks

`references/ux-laws.md` is the judge aid for the UX heuristics that can be
assessed on a static prototype. It is not a second slop scanner and not a
scorecard. The judge runs the relevant U01-U11 checks inside the existing
`strangeness` axis, cites the rule id and the law, and records `N/A` when a law
does not apply.

The reference is curated, not exhaustive. It contains ten always-on checks plus
one conditional check for prototypes with a form. The source is Laws of UX by
Jon Yablonski (https://lawsofux.com/); the checks below are proto-lab's own
paraphrases, and each rule links its source. See **Sources and licensing**.

## Quick table

| Id | Check | Laws | Typical use |
| -- | ----- | ---- | ----------- |
| U01 | Choice load | Hick's Law, Choice Overload | Navigation, filters, action bars, pricing |
| U02 | Chunking and working memory | Chunking, Miller's Law, Working Memory | Forms, long lists, settings, multi-screen flows |
| U03 | Cognitive load | Cognitive Load | Every screen, especially dense ones |
| U04 | Target acquisition | Fitts's Law | Buttons, links, rows, touch controls |
| U05 | Familiarity and mental model | Jakob's Law, Mental Model | Navigation, forms, tables, search |
| U06 | Visual grouping | Common Region, Proximity, Similarity, Uniform Connectedness, Prägnanz | Cards, forms, tables, sections |
| U07 | Simplicity and necessary complexity | Occam's Razor, Tesler's Law | Feature sets, settings, flows |
| U08 | Immediate use | Paradox of the Active User | Onboarding, empty states, first screens |
| U09 | Progress, completion and feedback | Goal-Gradient, Zeigarnik, Peak-End, Doherty | Multi-step flows, success and error states |
| U10 | Emphasis and order | Von Restorff, Serial Position | Primary actions, navigation, lists, dashboards |
| U11 | Forgiving input | Postel's Law | Only when the prototype has a form |

## U01. Choice load

**Laws:** [Hick's Law](https://lawsofux.com/hicks-law/) and
[Choice Overload](https://lawsofux.com/choice-overload/).

**Check:** Count the peer choices in the primary decision area. Are they
grouped, ranked, or progressively disclosed? Is there a recommended option or a
default? Is the primary action visually distinct from the alternatives?

**Failure signal:** A wall of equal-weight choices with no grouping, default or
recommendation. The user must compare every option before acting.

**Severity:** `major` when the choice wall blocks the primary task; `minor`
otherwise.

**Not a hard rule:** Seven is a caution, not a cap. A complex product can show
many options when they are grouped, searchable or progressive. Do not remove a
required choice to hit a number.

## U02. Chunking and working memory

**Laws:** [Chunking](https://lawsofux.com/chunking/),
[Miller's Law](https://lawsofux.com/millers-law/) and
[Working Memory](https://lawsofux.com/working-memory/).

**Check:** Are long forms, lists and settings grouped into meaningful sections?
Are labels close to their controls? Does the screen ask the user to remember a
value from a previous screen? Does a summary carry the context into the next
step?

**Failure signal:** A flat 20-field form, an ungrouped wall of items, or a flow
that makes the user memorize a value across screens.

**Severity:** `major` when the grouping failure blocks the task; `minor`
otherwise.

**Not a hard rule:** 7±2 is not a quota. Chunk by meaning, not by a number;
three to five items per group is a common heuristic, not a rule. Do not hide a
required field just to make a group smaller.

## U03. Cognitive load

**Law:** [Cognitive Load](https://lawsofux.com/cognitive-load/).

**Check:** Does the screen contain extraneous elements, competing focal points,
unexplained jargon or duplicated information? Does the user have to parse the
layout before acting? Is the primary task visually dominant?

**Failure signal:** The primary task competes with decoration, several elements
claim equal attention, or the user must decode the interface before starting.

**Severity:** `major` when the load blocks the primary task; `minor` otherwise.

**Not a hard rule:** Some complexity is intrinsic. Tesler's Law applies:
complexity can be moved, not eliminated. Do not oversimplify to the point of
ambiguity or hide a decision the user still has to make.

## U04. Target acquisition

**Law:** [Fitts's Law](https://lawsofux.com/fittss-law/).

**Check:** Are primary actions large enough and close to the content they act
on? Are touch targets spaced? Is the destructive action separated from the
primary action? Are whole rows or cards clickable where that matches the task?

**Failure signal:** Tiny text links, a primary CTA the same size as secondary
actions, or an important action far from its context.

**Severity:** `major` when the primary action is hard to hit or easy to confuse
with a destructive one; `minor` otherwise.

**Not a hard rule:** 44px is a mobile guideline, not a universal desktop law.
The real test is reachability and error cost. Do not make every action huge;
that competes with the emphasis rule (U10).

## U05. Familiarity and mental model

**Laws:** [Jakob's Law](https://lawsofux.com/jakobs-law/) and
[Mental Model](https://lawsofux.com/mental-model/).

**Check:** Do navigation, search, forms, tables and controls use conventional
locations and behaviours? Do labels match the domain's vocabulary? Is the novel
part of the screen the structure, while the control grammar stays legible?

**Failure signal:** An unconventional navigation or control with no affordance,
labels that require learning, or a form order that contradicts the domain.

**Severity:** `major` when the mismatch blocks the task; `minor` otherwise.

**Not a hard rule:** Jakob's Law does not forbid deliberate structural
divergence. Proto-lab exists to produce structural alternatives; keep the
control level familiar while the layout, density or navigation model can be
novel.

## U06. Visual grouping

**Laws:** [Law of Common Region](https://lawsofux.com/law-of-common-region/),
[Law of Proximity](https://lawsofux.com/law-of-proximity/),
[Law of Similarity](https://lawsofux.com/law-of-similarity/),
[Law of Uniform Connectedness](https://lawsofux.com/law-of-uniform-connectedness/)
and [Law of Prägnanz](https://lawsofux.com/law-of-pr%C3%A4gnanz/).

**Check:** Do related fields and actions share a container or tight spacing? Are
labels close to their controls? Do same-function elements look the same and
different-function elements look different? Is there a false connection between
unrelated items? Does the grouping add noise through nested containers?

**Failure signal:** Equal spacing everywhere, a label far from its input,
same-looking buttons with different effects, or a border or line that groups
unrelated items.

**Severity:** `major` when the grouping causes a mis-association that blocks the
task; `minor` otherwise.

**Not a hard rule:** Grouping can be whitespace, not only cards. Do not create a
card-in-card chain to satisfy "common region"; the slop fingerprints still
apply.

## U07. Simplicity and necessary complexity

**Laws:** [Occam's Razor](https://lawsofux.com/occams-razor/) and
[Tesler's Law](https://lawsofux.com/teslers-law/).

**Check:** Does every element earn its place? Is this the simplest structure
that preserves the task? Is complexity absorbed by the system through defaults
or progressive disclosure, rather than pushed to the user?

**Failure signal:** Redundant controls, feature bloat, or the opposite:
oversimplification that hides a required choice or makes the task ambiguous.

**Severity:** `major` when the simplification blocks the task; `minor`
otherwise.

**Not a hard rule:** Complexity cannot be eliminated, only moved. Do not remove
a required field or a necessary option to look simple. A long form can be the
right answer when the task genuinely needs the fields.

## U08. Immediate use

**Law:** [Paradox of the Active User](https://lawsofux.com/paradox-of-the-active-user/).

**Check:** Is the primary task visible without reading instructions? Are empty
states and onboarding action-oriented? Is help contextual and available at the
point of need?

**Failure signal:** A tutorial gate, a manual-first screen, a dead empty state,
or an essential feature that requires reading documentation.

**Severity:** `major` when the user cannot start the task; `minor` otherwise.

**Not a hard rule:** A short contextual hint is fine. The test is whether the
user can start without it, not whether every instruction is banned.

## U09. Progress, completion and feedback

**Laws:** [Goal-Gradient Effect](https://lawsofux.com/goal-gradient-effect/),
[Zeigarnik Effect](https://lawsofux.com/zeigarnik-effect/),
[Peak-End Rule](https://lawsofux.com/peak-end-rule/) and
[Doherty Threshold](https://lawsofux.com/doherty-threshold/).

**Check:** Do multi-step flows show progress and what remains? Does the final
state confirm completion and offer a next step? Do actions that imply waiting
have a feedback or loading state? Do errors offer a recovery path?

**Failure signal:** A four-step flow with no progress, a blank success screen,
an action with no feedback, or a dead-end error.

**Severity:** `major` when it blocks completion; `minor` otherwise.

**Not a hard rule:** A static prototype can only show the intended feedback
state; it cannot measure 400ms. Judge the state, not the stopwatch. Artificial
progress must not lie. Not every screen needs a progress bar; only a flow with
real steps does.

## U10. Emphasis and order

**Laws:** [Von Restorff Effect](https://lawsofux.com/von-restorff-effect/) and
[Serial Position Effect](https://lawsofux.com/serial-position-effect/).

**Check:** Is one primary action visually distinct? Are important items at the
start or end of navigation and lists? Is emphasis spread across everything? Is
colour the only signal?

**Failure signal:** Every CTA is highlighted, the primary action is buried in
the middle of a long list, several accents compete, or status is communicated
by colour alone.

**Severity:** `major` when the primary action cannot be found; `minor`
otherwise.

**Not a hard rule:** A data-dense screen may need several semantic accents;
role-scope them. One distinctive element is a guideline, not a quota. Do not
use emphasis to compensate for a weak hierarchy.

## U11. Forgiving input

**Law:** [Postel's Law](https://lawsofux.com/postels-law/).

**Applies only when the prototype has a form.** If there is no form, mark it
`N/A`.

**Check:** Do inputs accept common variants such as dates, phone formats,
surrounding whitespace and case? Are errors specific and recoverable? Does the
UI avoid rejecting a valid entry because of formatting? Is the output format
consistent?

**Failure signal:** A format-sensitive field that rejects a valid entry, a
generic error with no recovery path, or inconsistent output.

**Severity:** `major` when it blocks submission; `minor` otherwise.

**Not a hard rule:** A static prototype can show the input policy and the error
state; it cannot implement parsing. Do not use this rule to accept invalid data.

## Caveats

- **[Aesthetic-Usability Effect](https://lawsofux.com/aesthetic-usability-effect/).**
  Polish can make a design feel more usable and can mask real problems. A pretty
  screen is not evidence of a usable one. Do not add transitions, shadows or
  rounding just to satisfy this effect; the slop fingerprints still apply.
- **Miller's 7±2 is not a cap.** Chunk by meaning, not by a number. The source
  itself warns against using the number to justify unnecessary limits.
- **Jakob's Law does not forbid divergence.** It governs control-level
  familiarity; proto-lab's structural variants can still be novel. Do not
  collapse every variant into the same conventional layout.
- **Doherty is a runtime property.** A static prototype can show the intended
  feedback state, but it cannot measure 400ms. Judge the state, not the
  stopwatch.
- **Context-only laws.** [Aesthetic-Usability](https://lawsofux.com/aesthetic-usability-effect/),
  [Cognitive Bias](https://lawsofux.com/cognitive-bias/),
  [Flow](https://lawsofux.com/flow/),
  [Parkinson's Law](https://lawsofux.com/parkinsons-law/) and the
  [Pareto Principle](https://lawsofux.com/pareto-principle/) are not hard checks
  in this pipeline. Social proof, scarcity, anchoring and urgency are
  dark-pattern risks; the copy contract and the slop scan still apply.
- **Laws can conflict.** Hick's Law and Choice Overload can argue for fewer
  options; Tesler's Law can argue that a required choice must stay. Resolve with
  the brief and the point contract, not by applying every law at once.
- **N/A is a valid verdict.** If a law does not apply to the screen, record
  `N/A` and move on. Do not force a check to fill a table.

## Component applicability

Use two to four rules per component; do not run all eleven on every screen.

| Component | Primary checks | Secondary checks |
| --------- | -------------- | ---------------- |
| Form | U02, U06, U11 | U01, U03 |
| List or table | U02, U06, U10 | U01, U03 |
| Navigation | U01, U05, U10 | U04, U06 |
| Dashboard | U03, U06, U10 | U01, U02 |
| Multi-step flow | U02, U09 | U05, U11 |
| Empty or error state | U08, U09 | U03, U05 |
| Landing or hero | U01, U03, U10 | U04, U05 |
| Settings or config | U01, U07, U02 | U05, U11 |
| Detail or read view | U03, U06, U10 | U08, U09 |

A screen can combine types; take the union but keep the list short.

## Judge checklist

For each product page, pick the component types, run their primary checks, and
record:

- the rule id (`U01`-`U11`);
- the law name and link;
- the screen region (file plus selector or element);
- `PASS`, `FAIL` or `N/A`, with one line of evidence;
- for a `FAIL`, the severity (`major` when it blocks the primary task, `minor`
  otherwise).

A UX-law FAIL is not a slop fingerprint and does not count toward the `≥ 4`
visual cluster. It is a finding under `strangeness`; the normal judge loop
applies.

## Sources and licensing

Law names, short definitions and links are from **Laws of UX** by Jon Yablonski
(https://lawsofux.com/), licensed under
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). This
file paraphrases the laws for proto-lab's judge; it does not reproduce the
site's text. Follow the links for the original explanations and takeaways.

The component mapping and checklist shape were informed by two MIT-licensed
skills:

- `keysjoao/laws-of-ux-skills` (MIT): component-type mapping and a compact
  pre-ship checklist.
- `rastian/ux-laws` (MIT): evaluation criteria and severity tiers.

No text from those repositories is copied; the rules above are written for this
pipeline. `trevorgrogers/ux-designer-skills` and
`eagleisbatman/eagle-skills` were reviewed but not used: the former has no
license and the latter is an unlicensed broad bundle.
`P1tak4s/Jakobs-Law-UX` is a single-law skill and too narrow.

proto-lab itself is MIT-licensed. This reference is an independent paraphrase
with attribution; it does not include the CC BY-NC-ND text.
