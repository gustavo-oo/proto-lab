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
