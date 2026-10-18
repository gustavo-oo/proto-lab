# Acceptance notes

Shared evidence file for the scenario tasks. **T19** (end-to-end example +
`file://` navigation) owns the section below; **T21** (reproducibility) appends
its own section underneath and must not edit T19's.

Screenshots are written to a temporary directory **outside the repository** and
are deliberately **not committed** — the global constraint forbids binary images
in the repo. The paths below are absolute and point at that temp directory.

## T19 — exemplo end-to-end + navegação `file://`

**Target.** `examples/coffee-log-cafe-com-leite/`, opened as a real `file://` URL
(no server) in a Chromium browser through the browser tool.

```
file:///private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-wt/t19/examples/coffee-log-cafe-com-leite/
```

**Click-through: galeria → canvas → variante → segunda tela e voltar.**

1. Opened the session gallery `index.html` (`file://…/coffee-log-cafe-com-leite/index.html`).
   Title `proto-lab — Blueprint / Schematic`; a **pending** status cell was the
   pre-choice state and now reads **chosen (c)** (re-rendered after the pick).
   → `a4-gallery-from-variant-file.png`.
2. Clicked the canvas link on the d1 row → `points/d1-coffee-log.html`
   (`file://…/points/d1-coffee-log.html`). All **3** frames mounted with relative
   `src` (`../variants/d1-a/index.html`, `d1-b`, `d1-c`) — verified via
   `document.querySelectorAll('.deck iframe')`. Toggled **desktop (1280px)** and
   **mobile (390px)** with the canvas width buttons.
   → `a5-canvas-desktop-file.png`, `a6-canvas-mobile-file.png`.
3. Opened the chosen variant directly: `variants/d1-c/index.html`
   (title `d1-c · Feed de coluna única`, URL confirmed `file://…/variants/d1-c/index.html`).
   → `a1-variant-c-index-file.png`.
4. Clicked **detalhe** inside the page → navigated to
   `file://…/variants/d1-c/detail.html` (title `… · registro`).
   → `a2-variant-c-detail-file.png`.
5. Clicked **voltar ao diário** (`.back`, `href="index.html"`) → back to
   `file://…/variants/d1-c/index.html`.
   → `a3-variant-c-voltar-file.png`.
6. Clicked **galeria** (`.topbar__back`, `href="../../index.html"`) → back to the
   session gallery (`file://…/coffee-log-cafe-com-leite/index.html`).
7. Post-choice artifacts also opened over `file://`: `chosen/d1/index.html`
   (byte-identical copy of `variants/d1-c/`, its `../../index.html` link still
   resolves) → `a7-chosen-d1-file.png`; and `styleguide.html`, which consumes
   `tokens.css` via a relative `<link>` — computed fonts confirm the D10 register
   (`"Space Mono", … monospace` body / `"Archivo Narrow", … sans-serif` display)
   → `a8-styleguide-file.png`.

**Acceptance commands (from the repo/worktree root).**

```
python3 scripts/check_slop.py examples/coffee-log-*/variants/*/*.html
# {"hits": [], "count": 0, "verdict": "pass"}   exit 0
```

**Screenshots** (temp dir `…/t19-shots/final/`, not committed): `a1`…`a8` as named
above, plus `a5`/`a6` for the two canvas widths.

**Limitations / observations.**

- **In-frame click flakiness (tooling, not an artifact failure).** The browser
  tool refused some clicks *inside* a canvas iframe with *"Element '<ref>' is
  covered by <p.annot>/<article.plate.mark>/<li.card.mark> at its click point"*,
  typically when the deck was horizontally scrolled at 1280px. Re-issuing the
  click, or targeting the frame's nav link by CSS selector, succeeded every time,
  and the navigation was confirmed by the resulting URL change. The frames' links
  themselves are correct — this is a hit-testing limitation of the automation, not
  a broken link.
- **Screenshots not committed** (binary-image constraint). Evidence lives at the
  absolute temp paths above and in the commit body.
- **Gallery register.** The scaffolded `index.html` renders in the gallery
  template's *neutral* register, not D10: the template comment says the direction
  card overrides `--accent/--font-text`, but `scaffold.py` only substitutes
  seed/direction/family/points rows. Pre-existing `assets/` template-vs-doc
  mismatch (Task 12), out of scope for T19; recorded so it is not read as a D10
  failure.
- **Webface availability.** The variant/styleguide pages link Google Fonts
  (`fonts.googleapis.com`, an allow-listed host) and rendered with the webfaces
  present. Offline the same-class fallbacks (Archivo Narrow→Arial Narrow, Space
  Mono→IBM Plex Mono/ui-monospace) keep the register; that path was reasoned from
  the declared stacks, not rendered with the network cut.
- **No subagent dispatch.** This harness exposes no subagent tool, so the pipeline
  ran inline (SKILL.md degradation row: *"Harness without subagents → each phase
  runs inline"*). The judge in `judge-report.md` is therefore **not** a fresh-eyes
  subagent; the independent part of the gate is the machine slop scan and the
  `file://` walkthrough above.

---

## T21 — aceitação visual: divergência entre seeds

**Critério (spec §9).** Rodar a skill com 3 seeds diferentes → 3 saídas
**visivelmente distintas** (conferidas por screenshots desktop **1280** + mobile
**390**); mesma seed → mesma carta.

Screenshots aqui são **evidência, não artefato**: escritos num diretório temporário
**fora do repositório** e deliberadamente **não commitados** (a constraint global
proíbe imagens binárias; a lista de arquivos desta task é só este notes). Todos os
caminhos abaixo são absolutos.

### Step 1 — as três cartas

`python3 scripts/roll.py --seed <seed>` (catálogo padrão, sem `--domain`):

| seed | `direction_id` | `direction_name` | `family` | knobs |
|---|---|---|---|---|
| `cafe-com-leite` | **D10** | Blueprint / Schematic | technical | accent `#00E5FF`, density `+1`, invert `true`, rhythm `odd-first`, imagery `crop marks` |
| `s7` | **D14** | Risograph / Zine | print | accent `#FFB81C`, density `+1`, invert `false`, rhythm `even-first`, imagery `duotone and screened photographs` |
| `termo-final2` | **D12** | Space Age / Retro-Futurism | retro | accent `#1F8A8C`, density `-1`, invert `false`, rhythm `even-first`, imagery `halftone space scenes` |

Três direções distintas (D10, D14, D12) **sem família repetida** (technical /
print / retro) — o critério do Step 1 fecha.

**Substituição de seed (R24 — colisão).** A seed do brief, `termo-final`, *colide*:
ela também cai em **D10 Blueprint / Schematic** (família `technical`), a mesma carta
de `cafe-com-leite`, e o conjunto deixaria de ter 3 direções distintas. A regra do
brief ("troque a seed que colidiu") foi aplicada e a seed substituta é
**`termo-final2` → D12 Space Age / Retro-Futurism (família `retro`)**, que mantém
três famílias distintas. Verificado: `python3 scripts/roll.py --seed termo-final`
devolve `{"direction_id":"D10","direction_name":"Blueprint / Schematic",
"family":"technical",…}` (o mesmo `direction_id`/`family` de `cafe-com-leite`).

### Step 2 — 3 gerações (tela principal) + screenshots

**Método (R25).** O harness desta sessão **não** expõe tool de subagente, então cada
geração rodou como processo **externo** `opencode run --standalone --auto`
(método T17/T18, `t18-transcripts/{run_one_t18.sh,resume_t18.sh}`). Cada agente leu
o `SKILL.md` do worktree empacotado no scratch, recebeu o **mesmo brief do exemplo**
(`examples/coffee-log-cafe-com-leite/brief.md`), a seed fixa, `--skip-research`,
`--points 1` e `--variants 1` (corte de escopo deliberado: a aceitação quer **uma
tela principal por direção**, não a sessão completa — o cap `--variants` é
exatamente o mecanismo de corte de escopo do SKILL.md; nenhuma etapa foi pulada).

**Scratch (fora do repo).**

```
/private/var/folders/vl/8fqz68bx3ksb6nxg0nnnpw9w0000gn/T/opencode/proto-lab-scratch-t21/
  _skill/{SKILL.md,references,scripts,assets}/   cópia do worktree (skill sob teste)
  prompts/{cafe-com-leite,s7,termo-final2,judge}.txt   prompts enviados
  run_one_t21.sh  resume_t21.sh  run_judge.sh  launch_all.sh   lançadores (método T18)
  log-<seed>.txt          transcript do 1º turno (para no gate)
  resume-<seed>.log       transcript do OK + geração + juiz
  log-judge.txt           transcript do juiz externo (Step 3)
  judge/                  cwd isolado do juiz (não vê os artefatos)
  <seed>/prototypes/<slug>-<seed>/…   artefatos por seed
```

**O gate (step 3 do SKILL.md) foi honrado.** Nos três 1ºs turnos os agentes
escreveram `brief.md`/`direction.json`/`points.json` + o esqueleto do
`scaffold.py` e **encerraram o turno**: `research.md` **ausente** e `variants/`
segurando **só cascas não geradas**. O OK foi relayado pelo operador com
`opencode run --standalone --auto -c "OK — aprovado…"` (o caminho "operator
relaying one" do SKILL.md). Só então a geração rodou.

**Artefatos gerados (a tela principal = `variants/d1-a/index.html`):**

```
…/proto-lab-scratch-t21/cafe-com-leite/prototypes/diario-de-cafes-cafe-com-leite/variants/d1-a/index.html
…/proto-lab-scratch-t21/s7/prototypes/cafe-diary-s7/variants/d1-a/index.html
…/proto-lab-scratch-t21/termo-final2/prototypes/diario-de-cafes-termo-final2/variants/d1-a/index.html
```

Cada direção também escreveu `judge-report.md` (juiz fresh-eyes do próprio
pipeline, ≤ 2 rodadas; `termo-final2` guarda a rodada 1 em
`judge-report-round1.md`) e, no modo sem pick, `tokens.css` + `decisions.md`, com
`chosen/`, `handoff.md` e `styleguide.html` **pendentes do pick** (regra do
SKILL.md para run não-assistido — nenhum vencedor foi inventado).

**Screenshots** (agent-browser; sessão `t21-shots` no namespace isolado `t21` —
`agent-browser --namespace t21 --session t21-shots` — para não colidir com o job
`t20` paralelo). Página aberta por `file://`, viewport **1280** e **390**, full-page:

| arquivo (absoluto, sob `…/opencode/t21-shots/`) | dimensões | o que mostra |
|---|---|---|
| `…/t21-shots/cafe-com-leite-1280.png` | 1280 × 2165 | D10: fundo de papel quadriculado azul-claro, tipo mono caixa-alta, linhas de registro, carimbo "REPETIR" ciano e bloco de título DOC/REV/SEQ/MÉTODOS/RITMO |
| `…/t21-shots/cafe-com-leite-390.png` | 390 × 2200 | a mesma tela em uma coluna, com o bloco de título no rodapé |
| `…/t21-shots/s7-1280.png` | 1280 × 1326 | D14: tinta rosa-fluor + azul federal com desregistro ("DIÁRIO DE CAFÉ" azul com contorno rosa), trama de meio-tom, faixas-cortina pretas, colofão "IMPRESSO EM CASA · TINTA GIRASSOL · PAPEL KRAFT" |
| `…/t21-shots/s7-390.png` | 390 × 1328 | a mesma zine em uma coluna |
| `…/t21-shots/termo-final2-1280.png` | 1280 × 1851 | D12: base areia pontilhada, painel ilustrado meio-século (planeta laranja, starburst, satélite teal), réguas tracejadas (HOJE/ONTEM/14 DE OUTUBRO), pills teal, botão "+ REGISTRAR" |
| `…/t21-shots/termo-final2-390.png` | 390 × 1755 | a mesma tela em uma coluna |

`sha256` das 6 imagens (para re-verificação sem commitá-las):
`cafe-com-leite-1280` `6ce6721927e756fd2e02685741e82ea1ea15d719706bc2a992b933cf57aec371`,
`cafe-com-leite-390` `0316cd1a0f0a8b80a9a6dfc23b529f995c2064ebc4f6a8f86d481150ce69d548`,
`s7-1280` `c26fffd60b03f8706b99dbd3d396d09d16d806b14d8f08781263f3435eb17437`,
`s7-390` `b78b493c1802d2c1f3ec9d133dd93d5c0f7ea63d8b15f8ebd6465fc2d8a9c74d`,
`termo-final2-1280` `251c91cffbf40a4111624f5272048d7366569b8e721ece6512371526e3a8288e`,
`termo-final2-390` `2c7651ebd686cebed765082a9a274d1cbefcf3ab8b5778b3b245dd50060e7847`.

### Step 3 — juízo visual

**`jev` indisponível.** `jev_ask` foi tentado e falhou com
**`429 Rate limit exceeded`** — a rota do brief ("se disponível; senão subagent")
usou o **fallback sancionado**: um **juiz externo fresh-eyes** via
`opencode run --standalone --auto` (R25), em cwd próprio, que **não** vê os
artefatos nem os logs dos geradores — só as 6 imagens. As probabilidades abaixo são
desse juiz (calibração própria), **não** do jev; nenhuma probabilidade foi
inventada como se viesse do jev.

Pergunta, por par: *"the two screens are clearly distinct, and each is clearly
outside the generic AI-slop defaults?"*

| par | distinto? | probabilidade | evidência (resumo) |
|---|---|---|---|
| `cafe-com-leite` (D10) vs `s7` (D14) | **sim** | **0.97** | grade de papel quadriculado azul-gelo + mono + bloco de specs **vs** kraft com tintas fluor e desregistro; sem vocabulário compartilhado |
| `cafe-com-leite` (D10) vs `termo-final2` (D12) | **sim** | **0.84** | esquema quadriculado **vs** feed de cartões areia/teal com painel atômico; `termo-final2` é o mais "convencional" dos dois |
| `s7` (D14) vs `termo-final2` (D12) | **sim** | **0.86** | chapa de impressão (trama, 2 tintas, desregistro) **vs** feed de cartões suaves meio-século |

`overall`: **sim** — "três documentos genuinamente diferentes … não é um layout
repintado três vezes", com `termo-final2` apontado como o mais fraco (fica muito na
ilustração + paleta). Slop levantado pelo juiz: **nenhum** em D10 e D14; em
`termo-final2`, `soft shadow + cantos arredondados grandes em fundo neutro-quente
(look padrão de card-feed)` e `pills de método repetidas como tags genéricas` —
2 sinais heurísticos, abaixo do limiar de 4.

Corroboração mecânica: `python3 scripts/check_slop.py` na tela de cada seed →
`{"hits": [], "count": 0, "verdict": "pass"}` (exit 0) nas três.

Saída verbatim do juiz externo (transcript em `…/proto-lab-scratch-t21/log-judge.txt`):

```json
{"pairs":[
 {"pair":"cafe-com-leite vs s7","distinct":"yes","probability":0.97,"evidence":"cafe-com-leite is a cool D10 technical drawing: pale-blue engineering grid-paper background, all-monospace uppercase runs, hairline ruled rows with corner registration ticks, and a spec footer (DOC/REV/SEQ 11/11 registros/MÉTODOS/RITMO) with teal 'REPETIR' stamps; s7 is a warm D14 risograph: kraft/cream stock, heavy condensed 'DIÁRIO DE CAFÉ' headline printed blue with pink misregistration offset, fluorescent yellow/pink spot inks, a 60-LPI halftone dot block, full-bleed black ticker strips and a 'IMPRESSO EM CASA · TINTA GIRASSOL · PAPEL KRAFT 80 G · 6 EXEMPLARES' colophon. Palettes (ice-blue grid vs fluoro-over-kraft), type systems and ornament vocabularies share nothing.","slop_hits":[]},
 {"pair":"cafe-com-leite vs termo-final2","distinct":"yes","probability":0.84,"evidence":"cafe-com-leite is the ruled graph-paper schematic described above; termo-final2 is a D12 retro-futurist card feed with a sand dotted-grid ground, a mid-century atomic illustration panel (orange ringed planet, white starburst, teal satellite), dashed section rules ('HOJE','ONTEM','14 DE OUTUBRO'), teal method pills and a teal '+ REGISTRAR' pill. Structures and palettes are plainly different, though termo-final2's body is a fairly conventional rounded soft-shadow card list.","slop_hits":["soft shadow + large rounded card corners on a warm-neutral ground (default card-feed look)","pill-shaped method chips repeated as generic tags"]},
 {"pair":"s7 vs termo-final2","distinct":"yes","probability":0.86,"evidence":"s7 is riso print — fluorescent spot inks, halftone dot screen annotated 'LPI · 2 TINTAS', misregistered display type and heavy black rules; termo-final2 is a soft mid-century card feed with warm sand/cream, teal pills, dashed rules and a retro planet illustration. The print-plate texture vs airy rounded-card contrast is unmistakable; termo-final2 is the softer of the two directions.","slop_hits":["soft shadow + large rounded card corners on a warm-neutral ground (default card-feed look)","pill-shaped method chips repeated as generic tags"]}],
 "overall":{"distinct":"yes","evidence":"Three genuinely different documents — a monochrome graph-paper schematic, a fluoro risograph zine, and a sand-and-teal mid-century space-age feed — not one layout repainted three ways, since typography, grid logic, ornament and palette all change per direction (termo-final2 is the weakest, landing mostly on its illustration and palette)."}}
```

### Step 4 — reprodutibilidade

```
python3 scripts/roll.py --seed cafe-com-leite --out A.json   # 1ª
python3 scripts/roll.py --seed cafe-com-leite --out B.json   # 2ª (mesma seed)
cmp A.json B.json            # idênticos
cmp A.json examples/coffee-log-cafe-com-leite/direction.json # idêntico ao cartão commitado
cmp A.json node(scripts/roll.mjs)                            # espelho Node idêntico
```

`sha256(A.json) = 797c60e8a87d7cdf51c5c42531a8389c307b6427b44e660157548002da0b3370`
(302 bytes) — **igual** byte a byte à 2ª rolagem, ao `direction.json` commitado do
exemplo **e** à carta gerada na sessão `cafe-com-leite` (`…/diario-de-cafes-cafe-com-leite/direction.json`).
Mesma seed → mesma carta, sem timestamp.

### Limitações / observações

- **Screenshots não commitados** (imagem binária proibida). A evidência vive nos
  caminhos absolutos + dimensões + `sha256` acima.
- **1 variante por seed** (`--variants 1`) em vez das 3 default — corte de escopo
  explícito para a aceitação comparar **uma** tela principal por direção; as demais
  etapas (roll, gate, geração, juiz) rodaram normalmente.
- **Flakiness de provider.** `jev` (429) **pendurou** o 1º turno de `s7` por ~22 min;
  o processo foi morto e o 1º turno relançado (log preservado em
  `log-s7.hung.235448.txt`). O juiz do pipeline de `cafe-com-leite` e `s7` também
  registrou o 429. Um `ECONNRESET` apareceu na borda do kill. Os artefatos são
  determinísticos (a carta vem do `roll.py`), então o relaunch não muda a direção.
- **`termo-final2` registrou um `--domain`** na carta (`filters.domain`) sem
  excluir ninguém (`excluded: []`); o `direction_id` é o mesmo D12.
- **Sem dispatch de subagente.** As etapas "de subagente" (geração e juiz) rodaram
  como processos `opencode run` externos (R25), não pelo tool de subagente — que
  não existe nesta sessão.
