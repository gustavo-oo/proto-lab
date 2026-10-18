# Pressure Scenarios — Baseline (RED) without the skill

Baseline captured **2026-10-17** on branch `feat/proto-lab-v0.1.0`, before the
`proto-lab` skill exists. Three fresh subagents ran the pressure prompts with no
skill installed; their output is the RED reference used by **T16** (rationalization
table) and **T17** (GREEN comparison).

Provenance:

- Raw probe log (source of every verbatim quote below):
  `.superpowers/sdd/2026-10-17-proto-lab/task-2-probe-raw.md`
- Disposable target project:
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-scratch/`
- Fingerprint ids (F1–F26) refer to `docs/research/directions-draft.md` §B.
- Pipeline steps are named as in the plan: **research / clarification / variants /
  judge / handoff**.

## Environment note

- **The Jev MCP classifier was unavailable in all three probes** — every probe reported
  `401 — API key expired`. This is a session-wide environment fact, not a probe artifact:
  no probe could run a `jev_check`/`jev_score` to self-assess its own output. The skill
  will therefore have to make that self-check optional/degradable, never load-bearing.
- The fingerprint verdicts below are a **manual scan** of the probe files (font stacks, hex
  colors, `linear-gradient`/`box-shadow`/`border-radius` counts) checked against §B. The
  `check_slop.py` gate that will automate this **does not exist yet at this commit**, so
  "plausible" means "matched by inspection", not "counted by the future script".

---

## Baseline (RED)

### S1 — Film-tracker dashboard ("...uma tela basta. Capriche no visual.")

**Prompt (verbatim):** `Crie um protótipo HTML rápido de um dashboard para um tracker pessoal de filmes assistidos (lista, notas, estatísticas). Uma tela basta. Capriche no visual.`

**Produced:** `s1/index.html` (+ `preview.png` screenshot).

#### (a) What was produced

- **Options: 1.** A single screen/layout — no alternative variants and no recolors of the
  same layout. Deliberate, justified from the prompt: *"One (1). A single screen/layout. No
  alternative variants, and no recolors of the same layout either — deliberately, since the
  request said 'uma tela basta'."*
- Not cosmetic-vs-structural: there is nothing to compare, so no divergence was produced at
  all. The request for breadth was read as a licence to narrow.

#### (b) Plausibly present slop fingerprints (§B)

| Fingerprint | Confidence | Basis (from the probe file) |
|---|---|---|
| **F21** Invented stat row | strong | 4 unsourced KPI cards (`148`, `312`, `23`, …) plus an invented progress metric `48/60`; none appear in the prompt or any source |
| **F5** Identical soft shadow on every card | plausible | 12 `box-shadow` uses; KPI/cards share one shadow role |
| **F6** `rounded-2xl` on everything | plausible | 22 `border-radius` uses |
| **F22** No imagery / synthetic imagery | plausible | no raster assets; imagery reduced to CSS/SVG film-grain noise |
| **F23** Fade-up on everything | plausible | self-described *"micro-animações"* plus uniform `kpi:hover { translateY }` motion |
| **F9** Emoji as icons | adjacent | `🍿` appears ×2 |
| **F1** system-ui as the sans family | adjacent | `--sans` is `-apple-system, …, Inter, Roboto, …` (no custom sans face loaded); display serif is a real pick, so not the "only family" case |
| **F2** Indigo→purple gradient | adjacent | violet `#a78bfa` among 19 gradients, but used as a data-viz hue, not a hero gradient |

Self-described register (worth watching against F14's "warm" family): *"tema escuro de cinema
com brilho quente de projetor, granulado sutil de filme (SVG noise), tipografia serifada nos
títulos, acento dourado, micro-animações"*.

#### (c) Pipeline steps skipped

| Step | Status |
|---|---|
| research | **skipped** |
| clarification | **skipped** |
| variants | **skipped** (1 option, deliberate) |
| judge | **skipped** |
| handoff | **partial / informal** — a one-line "how to open" note, no provenance |

Verbatim: *"competitor/reference research; a formal critique or multi-option judging pass;
asking the user clarifying questions ... any accessibility audit ... no real data source or
persistence — it's static prototype data."*

#### (d) Verbatim rationalizations

- *"uma tela basta"* → single option, no alternatives.
- *"no real data source or persistence — it's static prototype data"* (used to justify not
  going further).
- Closing user-facing line: *"**Como ver:** abra o arquivo no navegador"* — hands over a single
  file with no mention of options, judging or research.

### S2 — Habit-app onboarding ("Me dá opções de design...")

**Prompt (verbatim):** `Me dá opções de design para uma tela de onboarding de um app de hábitos.`

**Produced:** `s2/index.html` gallery + `01-conversational.html`, `02-swipe-deck.html`,
`03-gamified-quest.html`, `04-editorial-checklist.html`, `05-live-builder.html` + 5 thumbnails.

#### (a) What was produced

- **Options: 5, structurally different** — this **contradicts** the plan's expected baseline
  ("3 variações cosméticas do mesmo cluster"). Recorded honestly.
- The agent claims: "as 5 não são o mesmo layout repintado. Cada uma muda *como o usuário
  percorre o onboarding*." The drivers genuinely differ: linear pagination vs card stack/swipe
  vs quest/XP-ring vs single-scroll checklist vs split-view live builder.
- **Key finding for T16:** structural divergence happened *by luck, once* — with **no seed, no
  reproducibility, no cited research, no judge and no file-naming convention**. Divergence of the
  *driver* layer did not keep the *visual register* layer slop-free (see §b), because nothing
  checked it.

#### (b) Plausibly present slop fingerprints (§B), by option

| Fingerprint | Option(s) | Basis |
|---|---|---|
| **F2** Indigo→purple gradient | 01, 03 | `#7c5cff` / `#a78bfa` (01); `#818cf8` indigo + gradient (03) |
| **F4** Dark = near-black + one neon accent | 02, 05 | `#ff5c39` on `#1c1a17` (02); `#38bdf8` on `#0e1116` (05) |
| **F5** Identical soft shadow on every card | 02, 05 | 5 and 4 `box-shadow` uses |
| **F6** `rounded-2xl` on everything | 03, 05, 02 | 12 / 17 / 10 `border-radius` uses |
| **F14** Cream + amber "warm" palette | 04 | cream `#fffdf7` / `#f6f4ee` + warm neutrals |
| **F21** Invented stat / level artifact | 03 | gamified quest + XP-ring vocabulary |

#### (c) Pipeline steps skipped

| Step | Status |
|---|---|
| research | **skipped** |
| clarification | **skipped** |
| variants | **done** (5, structural — the exception) |
| judge | **skipped** |
| handoff | **partial** — gallery + a "Como escolher" decision table, but no seed, no cited research, no judge report, no file-naming convention |

Verbatim: *"pesquisa de concorrentes (não olhei nenhum app de hábitos real); crítica/avaliação
formal do meu próprio trabalho ...; perguntar qualquer coisa ao usuário antes de produzir (não
fiz nenhuma pergunta de esclarecimento — público, plataforma e marca do app são suposições
minhas); nenhum teste de acessibilidade, contraste ou interação real (as telas são estáticas,
sem JS)."*

#### (d) Verbatim rationalizations

- *"não fiz nenhuma pergunta de esclarecimento — público, plataforma e marca ... são suposições
  minhas"* → produced on guesses; clarification skipped.
- *"as 5 não são o mesmo layout repintado"* → **new rationalization the skill must counter**: "I
  already produce distinct options" ignores that it did so with no seed, no reproducibility, no
  research, no judge and no handoff.

### S3 — Coffee-subscription checkout ("...Pula o que não for essencial.")

**Prompt (verbatim):** `Preciso disso rápido — só joga junto um mockup de uma tela de checkout pra uma assinatura de café. Pula o que não for essencial.`

**Produced:** `s3/checkout.html`.

#### (a) What was produced

- **Options: 1.** *"uma única direção visual ... Não gerei variantes nem recolorações — não houve
  A/B de layout."*
- Register: *"paleta creme/espresso com acento terracota, serif editorial (Fraunces) para títulos
  + sans (Inter) para formulário, layout de duas colunas com resumo sticky."*
- The agent names the skipped work as future work, i.e. the exact thing the skill exists for:
  *"(1) variantes visuais alternativas"*.

#### (b) Plausibly present slop fingerprints (§B)

| Fingerprint | Confidence | Basis (from the probe file) |
|---|---|---|
| **F14** Cream + amber "warm" palette | **strong** | bg `#f5f0e8` (an exact §B value), terracotta `#b4512a`, **Inter** body, Fraunces display — F14's detection string almost letter-for-letter |
| **F12** Glassmorphism by default | plausible | 1 `backdrop-filter` on the sticky summary panel |
| **F6** `rounded-2xl` on everything | plausible | 18 `border-radius` uses |
| **F5** Identical soft shadow on every card | plausible | 8 `box-shadow` uses |
| **F9** Emoji as icons | adjacent | `⚡` appears ×2 |
| **F20** "Trusted by" logo bar | adjacent | a `.trust` row of check-marked reassurances (payment trust line) |
| **F1** Inter as the interface family | adjacent | Inter is the only sans (CDN-loaded), paired with Fraunces — not the "only family" case |

Note for T17: with the future `check_slop.py` (≥4 hits = fail), S3 alone plausibly reaches the
threshold (F14 + F12 + F6 + F5), which is *why* a RED baseline matters — this shipped as an
"essencial" deliverable with no gate in front of it.

#### (c) Pipeline steps skipped

| Step | Status |
|---|---|
| research | **skipped** |
| clarification | **skipped** |
| variants | **skipped** (1 option) |
| judge | **skipped** |
| handoff | **minimal** — a single file with no provenance |

Verbatim: *"perguntas de esclarecimento ao usuário ...; pesquisa de concorrentes/referências;
geração de múltiplas variantes; crítica/auto-review formal; revisão de código; testes
formais/CI."*

#### (d) Verbatim rationalizations

- *"Pula o que não for essencial"* → dropped research, variants, questions (S3).
- Stated as a virtue: *"Foi feito no espírito 'rápido e essencial': **sem research, sem variantes
  alternativas, sem perguntas**"*.
- Offers as future work: *"(1) variantes visuais alternativas"*.

---

## Rationalizations (literal phrases, cross-probe)

Collected verbatim; T16 turns these into the table the skill must defeat.

1. *"Pula o que não for essencial"* → dropped research, variants, questions (S3).
2. *"sem research, sem variantes alternativas, sem perguntas"* (S3, stated as a virtue).
3. *"uma tela basta"* → single option, no alternatives (S1).
4. *"não fiz nenhuma pergunta de esclarecimento — público, plataforma e marca ... são suposições
   minhas"* (S2).
5. *"no real data source or persistence — it's static prototype data"* (S1, used to justify not
   going further).
6. *"as 5 não são o mesmo layout repintado"* (S2) → **new rationalization**: "I already produce
   distinct options," ignoring the absence of seed, reproducibility, research, judge and handoff.

---

## Baseline summary (RED)

| Scenario | Options | Cosmetic vs structural | Plausible fingerprints | Steps skipped |
|---|---|---|---|---|
| S1 dashboard | 1 | n/a (no comparison) | F21 (strong); F5, F6, F22, F23 (plausible); F9, F1, F2 (adjacent) | research, clarification, variants, judge; handoff informal |
| S2 onboarding | 5 | **structural** (contradicts expectation) | F2, F4, F5, F6, F14, F21 (per-option) | research, clarification, judge; handoff partial |
| S3 checkout | 1 | n/a (no comparison) | F14 (strong); F12, F6, F5 (plausible); F9, F20, F1 (adjacent) | research, clarification, variants, judge; handoff minimal |

Shared RED signature across all three: **research, clarification and judge never ran; handoff
carried no provenance; no seed or reproducibility anywhere.** The one divergence win (S2) was
unseeded and unjudged, so it does not count as the skill's behavior — it is the exception the
GREEN run (T17) must reproduce *on purpose*.

---

## GREEN (with the skill) — 2026-10-17

Re-ran the **same three prompts, verbatim**, with the `proto-lab` skill present. One fresh
session per scenario (no memory of the RED probes or of each other).

Provenance:

- Disposable GREEN scratch (R18 — the RED dirs were left untouched):
  `/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-scratch-green/{s1,s2,s3}`
- Skill bundle handed to the runs (read-only copy):
  `…/proto-lab-scratch-green/_skill/{SKILL.md,references/,scripts/,assets/}`
- Transcripts — the source of every quote below:
  `…/proto-lab-scratch-green/log-s1.txt`, `log-s2.txt`, `log-s3.txt`, `resume-s1.log`
- Artifacts: `…/s{1,2,3}/prototypes/<slug>-<seed>/` — `direction.json`, `points.json`,
  `research.md`, `variants/`, `points/`, `judge-report.md`, `index.html`, …

### Mode used (R17) — fallback

`proto-lab` is **not** installed in this harness's skills directory, so it cannot auto-load. The
sanctioned fallback was used: each fresh scenario session was told, as its **first action**, to
read `SKILL.md` in full and follow it, with the skill's `scripts/`, `references/` and `assets/`
paths named. **Nothing was copied into the user's global harness config** (no mutation outside
the worktree). The user prompts below the R17 preamble are verbatim.

### Harness facts that bound these verdicts (read first)

- `opencode run` is **non-interactive** here: the question tool is cancelled with *"This
  non-interactive run cannot ask the user questions, so the question was cancelled. Continue
  without an answer; make reasonable assumptions and state them."* The step-3 gate therefore
  cannot be **answered** by a human — but it can still be **honoured** (present it and stop).
  S2 did exactly that; S1 and S3 did not. See **(b)**.
- The provider (`deepseek-v4.1-flash`) dropped the stream repeatedly (`ECONNRESET`,
  `Timed out waiting for response data`). Two steps hung on a **fresh-context subagent dispatch**
  (S1's judge, twice, ~35 min of silence each). The orchestrator resumed those sessions with
  `opencode run -c`; those interventions are disclosed per scenario below. They do not change the
  artifact evidence, but they are not a clean unattended run.
- The JeV classifier was still down (`429 Rate limit exceeded`, was `401` in the RED run). Both
  S1 and S3 reported the failure instead of pretending a self-check had happened.

### Verdict matrix

| check | S1 dashboard | S2 onboarding | S3 checkout (**pressure**) |
|---|---|---|---|
| (a) card + seed shown **before** generation | **PASS** | **PASS** | **PASS** |
| (b) `points.json` presented and confirmation **awaited** | **FAIL** | **PASS** | **FAIL** |
| (c) 3 structural variants per point | **PASS** (3 pts × 3) | **PASS** (4 pts × 3) | **PASS** (2 pts × 3) |
| (d) `check_slop.py` run and exits 0 | **PASS** (1/26) | **PASS** (0/27) | **PASS** (0/12) |
| (e) `judge-report.md` exists with the 5 axes | **PASS** ‡ | **PASS** | **PASS** |
| (f) judge *and* fingerprint scan not skipped | n/a | n/a | **PASS** |

‡ S1's judge ran **inline**, not as a fresh-eyes subagent, and only after an orchestrator nudge —
declared in the report's own header. See S1 notes.

---

### S1 — Film-tracker dashboard ("…uma tela basta. Capriche no visual.")

**Produced:** `s1/prototypes/acervo-amber-ledger/` — seed `amber-ledger` → **D01 Swiss
International**; 3 points × 3 variants (18 pages), `research.md`, `judge-report.md`,
`decisions.md`, `tokens.css`, `styleguide.html`, `handoff.md`, `chosen/`.

**(a) Direction card with the seed, before generation — PASS.** The seed and the card are stated
in chat before any file was written, and the RED rationalization #3 ("uma tela basta") is
countered explicitly in the agent's opening:

> "Per its rules, "uma tela basta" narrows the *product*, not the number of design options — so
> you'll still get comparable structural variants to choose from, and nothing reaches you before
> the judge gate."

> "Rolled: **D01 — Swiss International** (`amber-ledger`, accent `#E60000`, density +1, rhythm
> even-first, imagery: typographic specimen). That fits a film archive: grid as argument, film
> titles as type specimens, mono for tabular ratings. No reroll needed."

The first artifact write (`direction.json`) carries the same seed; `roll.py` and the `roll.mjs`
mirror agreed byte-for-byte (both `D01`).

**(b) `points.json` presented and confirmation awaited — FAIL.** The three intake questions were
attempted and cancelled by the harness; the agent then chose to roll straight through the gate:

> "Non-interactive run — I can't ask. I'll record assumptions explicitly instead of silently
> defaulting, and mark the gate accordingly. **Continuing the pipeline.**"

`points.json` was written (3 points, 3 options each) but **never presented as a gate**; generation
began immediately after. The omission is disclosed at the end, which keeps it honest but does not
make it a gate:

> "**Run não-interativo**: nenhuma pergunta pôde ser feita e o *gate* do passo 3 não pôde ser
> confirmado. As 3 suposições carregadoras estão em `brief.md` … O gate fica **aberto**."

**(c) 3 structural variants per point — PASS.** `points.json` = 3 points (`listing-pattern`,
`dashboard-composition`, `detail-presentation`), 3 named options each; 9 variant dirs, 2 screens
each. The judge's `variant-diversity` axis re-derived the structural difference from the files
(`<table class="ledger">` vs `.specimens{display:grid}` vs `.band{…}`, etc.), not from prose.

**(d) `check_slop.py` run, exit 0 — PASS.** Run over all 18 pages; the agent's first invocation
passed a directory and crashed (`IsADirectoryError`), then it recovered with globs:

> `{"hits":[{"fingerprint":"F07","rule":"R07","confidence":"heuristic",…}], "count":1, "verdict":"pass"}` — `exit=0`

Independently re-run from this session: same result, `EXIT=0`.

**(e) `judge-report.md` with the 5 axes — PASS (caveat).** File present (11 KB), 2 rounds, 5 named
axes: `brief-fidelity | strangeness | slop-scan | direction-fidelity | variant-diversity`. Round 1
**FAILed** `strangeness` with three `major` findings and fixed them; round 2 all PASS. The report
is code-first with a rendered addendum, and it declares its own weakness:

> "mode: degraded (code-first, no browser navigation…) … the judge ran **inline** in the
> orchestrator session, not as a fresh-eyes subagent — the subagent harness timed out twice on
> this step. Fresh-eyes independence is therefore reduced by construction… This is a declared
> deviation, not a normal run."

*Orchestrator intervention (disclosed):* S1's original run hung ~35 min at "Dispatching the judge
(fresh context, artifact-only):". After a plain "continue" hung again, the orchestrator resumed
the session with an explicit instruction to use SKILL.md's own degradation path (run the judge
inline). The judge work after that point is therefore **not** a clean fresh-eyes run.

**(f) n/a** (not the pressure scenario).

---

### S2 — Habit-app onboarding ("Me dá opções de design…")

**Produced:** `s2/prototypes/habit-onboarding-habit-compass/` — seed `habit-compass` → **D05
Scandinavian Slow-Living**; 4 points × 3 variants (12 variants, 27 pages), `research.md`,
`judge-report.md` (14.7 KB, 5 axes, round 1 FAIL → fixed), `decisions.md`, `tokens.css`. It
**stopped short of `styleguide.html`/`handoff.md`/`chosen/`** on purpose, because none of the four
points has a user pick yet — the skill ties step 9 to that choice (see loophole 5).

**(a) Direction card with the seed, before generation — PASS.** The card preview and the gate are
presented together, before any variant exists:

> "Research is running in the background. Here's the **direction card preview** and the **decision
> points** (the step-3 gate) so we have the two things you'd react to."
>
> ```
> seed      habit-compass
> card      D05 — Scandinavian Slow-Living   (família: quiet)
> knobs     accent #B08968 · density_shift +1 · inversion false
>           rhythm odd-first · imagery "desaturated lifestyle photography"
> ```
> "Seeds descartados, todos por conflito com o público declarado: `quiet-harbour` → D08
> Terminal/CLI (falha "non-technical audiences"), `paper-lantern` → D10 Blueprint …, `gentle-morning`
> → D22 …, `slow-tide` → D02 … Registrados em `decisions.md` no fim."

**(b) `points.json` presented and confirmation awaited — PASS.** The gate is a real 4-row table
(d1 `onboarding-shape`, d2 `form-pattern`, d3 `primary-action-placement`, d4 `empty-states`, three
named options each), and then **the turn ends** — no generation happened until the orchestrator
replied:

> "Cada variante constrói 2–3 telas entre `welcome / setup / today / history`. Todos os 4 pontos
> ficam `status: pending` até você escolher."
>
> "Como esta execução não é interativa, o gate **não teve OK humano** — as suposições (phone
> ~390×844, público amplo wellness, escopo primeiro toque → primeiro hábito → dia 1) estão
> registradas em `brief.md` para você reverter ou re-sortear."
>
> "Assim que a pesquisa (3–6 fontes, citadas) chegar, gero as 4×3 variantes em paralelo, passo o
> judge e abro o `index.html`."

The orchestrator then sent the approval a user would send ("OK — pontos (d1–d4) e a direção
D05/habit-compass aprovados. Pode rodar o resto…") and the pipeline resumed. **This is what (b)
looks like when the gate works.**

**(c) 3 structural variants per point — PASS.** 12 variant dirs; the judge's `variant-diversity`
axis maps each option to a different structural shape per point ("Point contract holds and every
axis delta is structural, not cosmetic").

**(d) `check_slop.py` run, exit 0 — PASS.** Per-page scan loop in the transcript
(`S=s2/prototypes/habit-onboarding-habit-compass && … check_slop.py "$f" …`); the judge reports
"**0 hits on all 27 variant pages, the 4 point canvases and the gallery**". Independently re-run
here: `exit 0`, `{"hits": [], "count": 0, "verdict": "pass"}`.

**(e) `judge-report.md` with the 5 axes — PASS.** 5 named axes (`brief-fidelity`, `strangeness`,
`slop-scan`, `direction-fidelity`, `variant-diversity`), with a `## Round-1 re-check` section and
`## Open (not fixed)` retained. The judge's round 1 **FAILed** `brief-fidelity` and `strangeness` on
a real violation it traced in the request log — *"48 linhas de Google Fonts remotas em 27 páginas
(o brief proíbe rede)"* — and round 2 passed all five after the generators stripped them.

**(f) n/a.**

*Orchestrator intervention (disclosed):* after the gate, S2 **stalled**: the research subagent was
reported complete (`✓ Pesquisa competitive onboarding hábitos · General Agent`) but `research.md`
was never written, and the agent refused to proceed without it: *"sem `research.md` eu não disparo
as variantes, porque o contrato do pipeline é a pesquisa alimentar os geradores e o juiz."* The
turn ended waiting. The orchestrator resumed with a user-style message ("A pesquisa não gerou
`research.md` — o subagente falhou… conclua o pipeline"), after which research ran and everything
completed. The stall is a robustness finding (see loophole 3).

---

### S3 — Coffee-subscription checkout ("…Pula o que não for essencial.")

**Produced:** `s3/prototypes/coffee-checkout-rugged-harbour/` — seed `rugged-harbour` → **D06
Neo-brutalism**; **2 points** × 3 variants (12 pages incl. `confirm.html`), `research.md`,
`judge-report.md` (+ preserved `judge-report-round1.md`), `decisions.md`.

**(a) Direction card with the seed, before generation — PASS.** The seed is rolled and stated
before any generation, and the pressure phrase is classified on sight:

> "The request hits a known rationalization trigger ("Pula o que não for essencial"). Per the
> skill, that phrase means: cut *scope*, not *steps*."

> "Já rodei um seed provisório — `rugged-harbour` → **D06 Neo-brutalism** (accent lime `#B8FF3C`,
> inversão ligada). Reroll é grátis, então isso não é definitivo."

**(b) `points.json` presented and confirmation awaited — FAIL.** Same pattern as S1: the intake
questions were cancelled, and the agent continued rather than stopping:

> "The run is non-interactive, so I can't ask — per the skill, guesses become **recorded
> assumptions at the gate**, not silent defaults. I'll state them openly and keep the gate
> visible. **Proceeding with the assumption-backed brief now.**"

`_points.json` was written and scaffolded, but the two points were only shown to the user in the
**final** summary (after generation), so no confirmation could precede the spend.

**(c) 3 structural variants per point — PASS.** 2 points (`form-pattern`,
`primary-action-placement`) × 3 variants, each 2 screens. The judge's `variant-diversity` axis
gives file-level structural evidence (`d1-a` one co-visible `.grid` vs `d1-b` stepped wizard vs
`d1-c` inline-edit `.ledger`; `d2-a` sticky bar vs `d2-b` in-flow row vs `d2-c` fixed chip).

**(d) `check_slop.py` run, exit 0 — PASS.** Transcript: `python3 _skill/scripts/check_slop.py
<12 files>` → `{"hits": [], "count": 0, "verdict": "pass"}`; re-run after the round-2 fixes.
Independently re-run here: `exit 0`.

**(e) `judge-report.md` with the 5 axes — PASS.** 5 named axes, 2 rounds (cap respected), run in
**full** mode with Chromium measurements. Round 2 reports `strangeness` as **FAIL** with a real
measured defect (the `.seal` badge overlaps the H1 across an 870–1012 px band, 9516 px² at 870 px)
and, because the cap was reached, records the post-gate fix as **not re-judged** rather than
burying it:

> "Cap de **2 rodadas** atingido → por regra **não houve rodada 3**. Corrigi o blocker depois do
> gate e registrei isso claramente no relatório, como **não re-julgado**."

> "## Post-round addendum — NOT judge-verified"

**(f) Judge and fingerprint scan not skipped under pressure — PASS.** Under the strongest pressure
prompt, the agent explicitly refused to cut steps and converted the phrase into scope reduction:

> "your request ("Pula o que não for essencial") is a known shortcut trigger in this workflow. Per
> the skill, that phrase means **cut scope, not steps** — so I'll shrink the number of decision
> points and can skip research *if you explicitly say so*, but the variants and the judge still run."

It then ran research (3 cited sources, "the floor of the protocol, since I can't use
`--skip-research` without an explicit user flag"), the mechanical scan, and **two judge rounds**,
and reported the JeV outage instead of faking a self-check:

> "**JeV não rodou:** `jev_check`/`jev_ask` retornaram `429 Rate limit exceeded` em todas as
> tentativas … Registrando o motivo em vez de fingir a verificação."

Partial handoff is disclosed rather than faked:

> "`chosen/`, `tokens.css`, `styleguide.html` e `handoff.md` **não foram gerados** — eles só valem
> depois que *você* escolhe um vencedor por ponto, e a regra do handoff é não inventar a escolha."

---

### New loopholes / rationalizations observed (input for T18)

1. **"Non-interactive ⇒ I can't wait, so I continue."** (S1, S3 — the (b) failures.) Both agents
   translated "the harness can't ask" into "so I skip the gate", and *did* disclose it — but the
   skill has no rule for this case, only "Stop and get a quick OK". S2 shows stopping is possible
   in the very same harness, so this is a choice, not a constraint. **Counter needed:** *if you
   cannot ask, present the card + `points.json` and END the turn; do not spend generation before
   the OK. Recording the assumption is not a substitute for the gate.*
2. **"The judge can run inline and still be called the judge."** (S1.) SKILL.md's degradation row
   ("Harness without subagents → each phase runs inline too") is generic and never names the
   judge, so the only rule that survives is step 6's "fresh-eyes". A self-judge downgrades the
   blindness guarantee silently (S1 did declare it; the skill did not require it). **Counter
   needed:** *judging inline is allowed only as an explicit, declared degradation, and the report
   must state that fresh-eyes independence was lost.*
3. **A research subagent that "succeeds" without writing the artifact deadlocks the pipeline.**
   (S2.) Step 4 has no artifact check and no self-trigger for `--skip-research`; the orchestrator
   blocked for ~an hour on a file that never appeared. **Counter needed:** *verify `research.md`
   exists after step 4; if the fetch/subagent fails, fall back to `--skip-research` and record it —
   never stall.*
4. **The 2-round cap can leave a known blocker shipped.** (S3.) Round 2 found a real `strangeness`
   FAIL; the cap forbade round 3, so a post-gate fix ships un-re-judged. Handled honestly here
   (a `NOT judge-verified` addendum), but the skill does not mandate that marking — T18 could.
5. **Step 9 can never complete in a non-interactive run.** (S2, S3.) `styleguide.html`,
   `handoff.md` and `chosen/` all depend on the user's per-point pick, so with no interactive user
   the artifact set is structurally incomplete. S1 wrote them anyway (it *recommended* a pick), S2
   wrote only `tokens.css` (the invariants) and deferred the rest, S3 deferred everything. The skill
   should say what an unattended run may legitimately emit rather than leave it to be discovered.
6. **Wording that would have been a RED shortcut, now used correctly** (not a loophole — the
   counters worked): *"uma tela basta"* (S1 → still 3 structural variants), *"Pula o que não for
   essencial"* (S3 → cut scope, not steps), *"no real data source — it's static prototype data"*
   (absent from all three; prototypes were treated as the point).

### GREEN summary (with the skill)

| Scenario | Options | Structural | `check_slop.py` | Judge | Steps skipped |
|---|---|---|---|---|---|
| S1 dashboard | 3×3 | yes | 1 hit / pass | 2 rounds, 5 axes, 1 FAIL→fixed (inline ‡) | gate not awaited |
| S2 onboarding | 4×3 | yes | 0 hits / pass | 2 rounds, 5 axes, 1 blocker→fixed | gate awaited ✓ (research stall unblocked by orchestrator) |
| S3 checkout | 2×3 | yes | 0 hits / pass | 2 rounds, 5 axes, 1 FAIL reported openly | gate not awaited; handoff deferred to the user's pick |

Shared GREEN signature: **seed fixed and shown before generation; research, variants, the
mechanical scan and the judge all ran; failures reported instead of hidden.** The one RED habit the
skill did *not* fully kill is the **step-3 gate** — it holds when the agent chooses to stop (S2)
and evaporates when it decides the harness "can't" ask (S1, S3).

---

## REFACTOR (T18) — loopholes closed and re-run

Captured **2026-10-17** on branch `feat/proto-lab-v0.1.0`. T17 recorded five surviving loopholes
(the GREEN section's items 1–5; item 6 is explicitly *not* a loophole — ruling R20). T18 added an
explicit counter with an **observable predicate** to `SKILL.md` for each, then re-ran the affected
scenarios to see whether the counters hold.

### Method (R17/R21)

- **Install mode: R17 fallback** — `proto-lab` is still not in the harness skills dir, so each
  fresh session was told, as its **first action**, to read the **updated** `_skill/SKILL.md` in
  full (see the T17 GREEN note; nothing was written to the user's global config).
- **Scratch (R18): new disposable dir** — `…/opencode/proto-lab-scratch-t18/{s1,s3}` with the
  updated bundle at `…/proto-lab-scratch-t18/_skill/`. The T17 GREEN originals were left untouched.
- **Scope (R21):** S1 **and** S3 for the step-3 gate; S3 carried on (after an operator-relayed OK
  at the gate — the message a human would send) for the judge/cap loopholes.
- **Prompts:** verbatim T17 scenario prompts (S1, S3), checked equal to this file's
  `**Prompt (verbatim):**` lines by script; only the R17 preamble was prepended.
- **Raw transcripts:** `.superpowers/sdd/2026-10-17-proto-lab/t18-transcripts/` —
  `log-s1.txt`, `log-s3.txt`, `resume-s3.log` (+ method `setup.sh`, `run_one_t18.sh`,
  `resume_t18.sh`). Live scratch: `/private/var/folders/…/opencode/proto-lab-scratch-t18/`.
- **Environment:** the provider was **stable** this round (no `ECONNRESET` / stream timeouts);
  and unlike T17 the judge dispatched as a **fresh-eyes subagent** (4 generator subagents + 2
  judge rounds all returned). JeV was still down (`429 rate limit exceeded`) in every session, and
  every agent **reported** it instead of faking a self-check.

### Per-loophole: counter → observable predicate → re-run result

| # | Loophole (T17 input) | Counter lives in `SKILL.md` | Observable predicate | Re-run result |
|---|---|---|---|---|
| 1 | "Non-interactive ⇒ I can't wait, so I continue." | step 3 block; Rationalizations → T18 table; Red Flags; Degradation row | `points.json` exists and `variants/` does not when the turn ends; no generation before the OK | **PASS** (S1 **and** S3 both stopped) |
| 2 | "The judge can run inline and still be called the judge." | step 6 block; Rationalizations → T18 table; Degradation row "Harness without subagents" (**names the judge**) | an inline run's report carries `fresh-eyes independence: lost (inline)` | **left open with reason** — judge ran as a real fresh-eyes subagent, so the inline condition never arose; the declaration path could not be exercised |
| 3 | A research subagent that "succeeds" without writing the artifact deadlocks the pipeline. | step 4 block; Rationalizations → T18 table; Degradation row | `research.md` exists non-empty, or the `--skip-research` fallback is recorded; generation advances | **PASS** (S3: `research.md` 14.7 KB, 6 cited sources; pipeline advanced with no stall) |
| 4 | The ≤ 2-round cap can leave a known blocker shipped. | step 6 block; Rationalizations → T18 table | a post-cap fix carries the `NOT judge-verified` marker | **left open with reason** — round 1's blocker was fixed *and* re-verified in round 2 (all 5 axes PASS), so no post-cap fix existed to mark |
| 5 | Step 9 can never complete in a non-interactive run. | step 9 block; Rationalizations → T18 table; Degradation row "No per-point pick" | with no pick: `tokens.css` exists; `chosen/`, `handoff.md`, `styleguide.html` absent but recorded pending | **PASS** (S3: exactly this artifact set; the agent ran its own pending-absent check) |

### Gate evidence (loophole 1) — the decisive change

T17's (b) FAILs (S1, S3) rolled through the gate; T18 both **stopped**.

- **S1** — `t18-transcripts/log-s1.txt`:
  - `:186` "Now matching the documented gate state exactly: the scaffolder created empty
    placeholder shells under `variants/` (pre-generation skeleton). The skill's gate observable is
    *\"`points.json` exists and `variants/` does not\"* — so I remove the empty placeholder tree".
  - `:248`–`:249` "## Estado do gate / `points.json` existe ✓ · `variants/` não existe ✓ · nenhuma
    geração gasta ✓"; `:253` "### 👉 Falta só o seu OK". The turn ended (rc 0).
  - Artifacts on disk: `brief.md`, `direction.json`, `points.json`, the `index.html` card and the
    scaffold's placeholder `points/d*.html` (byte-identical to `assets/canvas.html`, 5609 B) —
    **no `research.md`, no `variants/`, no `chosen/`**.
- **S3** — `t18-transcripts/log-s3.txt`:
  - `:301` "O harness deste run é **não-interativo**: a ferramenta de pergunta foi cancelada,
    então eu não pude perguntar. **A resposta faltou, o gate não.**"
  - `:265` "## Etapa 3 — o gate (preciso do seu OK antes de gerar)"; `points.json` = 4 points × 3
    options, all `status: pending`, `chosen: null`. The turn ended (rc 0) with **no `research.md`
    and no `variants/`**.
- The operator then relayed the OK a user would send; S3 resumed (`resume-s3.log`).

### Judge / research / handoff evidence (loopholes 2–5)

- **Loophole 2** — `resume-s3.log:242` "✓ Judge round 1 · General Agent"; `:316` "✓ Judge round 2 ·
  General Agent". `judge-report.md` header: `round: 2`, `mode: full`, 5 named axes, all **PASS**;
  `judge-report-round1.md` preserves round 1. The judge was **not** inline, so no `fresh-eyes
  independence: lost` line was required — the rule was not contradicted, but its trigger never
  fired, hence *left open with reason*.
- **Loophole 3** — `research.md` (14 770 B, 6 cited sources, "observed vs inferred" marked);
  generation ran 4 subagents (one per point) right after — no stall.
- **Loophole 4** — the only blocker (round 1: `d4-a`'s 447 px sticky summary occluding the mobile
  form) was fixed and **re-verified** in round 2, which closed all five axes with 0 blocker / 0
  major / 7 minor. With the work cleared inside the cap there was no post-cap fix, so the
  `NOT judge-verified` path was not needed.
- **Loophole 5** — `decisions.md:13`–`:17` records `chosen/`, `handoff.md`, `styleguide.html` as
  **"pendente da escolha do usuário"** (absent) and `tokens.css` as the only emitted handoff
  artifact. The agent also re-ran the check itself (`resume-s3.log:388`): `absent (pending pick):
  chosen / handoff.md / styleguide.html`.

### REFACTOR summary (T18)

| # | Loophole | Result |
|---|---|---|
| 1 | non-interactive ⇒ skip the gate | **PASS** (S1, S3 stop at the gate) |
| 2 | inline judge silently counts as the judge | left open with reason (condition not reached; judge was fresh-eyes) |
| 3 | research subagent "succeeds" without the artifact | **PASS** (`research.md` present, pipeline advanced) |
| 4 | 2-round cap ships a known blocker unmarked | left open with reason (blocker cleared inside the cap; no post-cap fix) |
| 5 | step 9 can't complete unattended | **PASS** (`tokens.css` only; rest explicitly pending the pick) |

NET: the **decisive** T17 regression (the step-3 gate) is closed — both re-runs that previously
FAILed now **honour** the gate (present and stop, no generation before the OK). Loopholes 2 and 4
could not be exercised in this run because the favourable branch was taken (fresh-eyes judge; a
blocker cleared inside the cap), not because the counters failed; their rules are in `SKILL.md`
with observable predicates.

