# Design — `proto-lab`: skill de prototipagem HTML divergente (pré-implementação)

- **Data:** 2026-10-17
- **Status:** aguardando revisão do usuário
- **Repo do projeto:** este mesmo repositório (`proto-lab` em `~/Projects/proto-lab`, open source; nome provisório)
- **Origem:** brainstorming de 2026-10-17 (spec e anexos movidos para cá; o repo foi inicializado com eles)
- **Anexos:** `docs/research/landscape.md` (levantamento de prior art) · `docs/research/directions-draft.md` (rascunho v0.1 do catálogo de direções + fingerprints de slop)

---

## 1. Problema e objetivo

Quem vai implementar uma UI precisa **explorar opções de design antes de codar na stack real**. LLMs tendem a produzir designs homogêneos ("média" / AI-slop) — há evidência empírica disso (Design Creativity Bench, arXiv 2610.11539; homogenização em web vibe coding, arXiv 2603.13036; colapso de diversidade em T2I, ~10 de 768 dimensões efetivas). As ferramentas existentes resolvem fatias do problema: direção única (v0, Lovable, Galileo), variantes por prompt sem reprodutibilidade (Superdesign, Stitch, Magic Patterns), pesquisa de concorrentes atrás de catálogos pagos (Mobbin/Refero/UIZZE), juízes parciais (fidelity ΔE do `design-dna`, finish gate do UIZZE, self-critique do skill oficial `frontend-design`). Nenhuma combina seed reproduzível × variantes divergentes por ponto de decisão × research citado em runtime × juiz pré-humano — ver anexo `landscape.md`, seção "Gaps & opportunities".

**Objetivo:** uma skill open source que, a cada sessão, gere **opções de design estruturalmente divergentes por ponto de decisão**, em HTML estático navegável (sem build, sem servidor obrigatório, sem dependências), com:

1. **Seed reprodutível** — cada sessão sorteia uma "carta de direção" de design completamente diferente; mesmo seed → mesma carta.
2. **Pesquisa de concorrentes** no domínio do produto, citada, com padrões bons e ruins.
3. **Juiz pré-humano** — fidelidade ao brief, estranhamento (walkthrough fresh-eyes), fingerprints de AI-slop e **diversidade entre variantes** (inédito no mercado, segundo a pesquisa).
4. **Handoff para implementação** — decisões registradas, tokens, mini styleguide e notas de fidelidade.

**Não-objetivos (explicitamente fora):**
- Lógica de negócio, dados reais, backend; as variantes são "levemente navegáveis" (links funcionam; nada de regra).
- Fidelidade à stack do projeto alvo (regra: **não** ler código/UI do alvo para design; só specs/docs para requisitos — a skill não precisa respeitar a stack onde está instalada).
- Design system completo de produção (biblioteca exaustiva, theming, bindings de stack, docs site) — isso nasce na sessão de implementação, informado pelo handoff.
- Fonte definitiva de copy/imagens: copy é realista mas de protótipo; "imagens" são placeholders CSS/SVG conforme a direção (zero assets binários, zero stock).

**Sucesso =** o usuário olha a galeria e consegue escolher entre opções que são *de fato* diferentes (não reskins), sem sentir que está escolhendo "a menos média"; e a sessão de implementação seguinte consegue portar a escolha sem re-decidir design.

---

## 2. Decisões travadas no brainstorming

| # | Decisão | Valor |
|---|---------|-------|
| D1 | Local do projeto | Novo repo independente `~/Projects/proto-lab` |
| D2 | Formato/compatibilidade | `SKILL.md` no padrão agentskills.io (OpenCode, Claude Code, Codex e afins) |
| D3 | Entrega dos protótipos | HTML estático puro, zero deps; abre no browser; script opcional de servidor local |
| D4 | Variantes por ponto de decisão | 3 (configurável: `--variants 2`) |
| D5 | Definição dos pontos de decisão | Skill deriva do brief e **confirma com o usuário** antes de gerar (gate único) |
| D6 | Escopo do pipeline | Pacote completo: HTMLs + `research.md` + `judge-report.md` + `decisions.md` + handoff |
| D7 | Pós-julgamento | Auto-corrige e re-julga (≤2 rodadas) antes de mostrar ao usuário |
| D8 | Motor de divergência | **Abordagem A**: seed → 1 direção por sessão; 3 variantes **estruturais** por ponto na mesma DNA; preview + reroll barato; modo `--wild` (direção por variante) como opção |
| D9 | Handoff | `tokens.css` + `handoff.md` + `chosen/` + `styleguide.html` (mini design system estático da escolha) |
| D10 | Idioma | Repo/docs/SKILL.md em inglês; interação com o usuário no idioma dele |
| D11 | Licença | MIT (default) |

---

## 3. Pipeline

```
0. Setup       Detecta ambiente: python3? node? browser tool (agent-browser/Playwright)?
               subagents? Escolhe caminho rico (script+browser) ou degradado (ver §9).
1. Brief       Usuário descreve produto/feature; skill faz ≤3 perguntas se faltar campo
               load-bearing (produto, público, objetivo, telas-chave, restrições) → brief.md
               Seed: aleatória (ex.: "cafe-com-leite") ou informada via --seed.
2. Roll        seed → carta de direção (catálogo de 22, §5.2), filtrada por compatibilidade
               com o domínio declarado (fits/fails). Preview compacto no chat.
               Usuário pode rerrolar AQUI (custo ~0, nenhuma geração ainda).
3. Pontos      Skill deriva pontos de decisão + opções estruturais nomeadas de cada um
               → points.json (contrato: eixo + opções). Gate: OK rápido do usuário.
4. Research    3–6 concorrentes/análogos do domínio (subagent + web) → research.md
               (padrões bons/ruins citados; "observado vs inferido"). Default on;
               --skip-research desliga. Cacheado para reuso.
5. Gerar       1 subagent POR ponto de decisão, em paralelo, cada um com: carta de direção,
               contrato do ponto, brief, research.md, guardrails (§5.3) → 3 variantes HTML.
               Skill principal monta a galeria/canvas.
6. Julgar      Juiz fresh-eyes (subagent dedicado, §5.4) nos 5 eixos, code-first +
               screenshots se houver browser tool. Findings com severidade.
               Blockers/majors → corrigir → re-julgar (≤2 rodadas). Fica tudo em judge-report.md.
7. Apresentar  Abre index.html no browser + resumo no chat (pontos, opções, o que o juiz
               achou). Usuário escolhe por ponto.
8. Registrar   decisions.md: escolhido + preterido + porquês (inclusive seeds rerroladas).
9. Handoff     tokens.css + handoff.md (inventário de componentes/estados + notas de
               fidelidade) + chosen/ (cópias das variantes escolhidas) + styleguide.html
               (mini DS estático da direção escolhida).
```

**Gate único que interrompe o fluxo:** passo 3 (confirmação dos pontos). Todo o resto roda seguido até a apresentação.

---

## 4. Artefatos gerados (no projeto alvo)

Diretório: `prototypes/<slug>-<seed>/` (pasta própria; a skill não toca no resto do repo do alvo).

```
prototypes/<slug>-<seed>/
  index.html                # galeria: carta de direção + lista de pontos + links (o "figma")
  direction.json            # carta de direção (seed, direção, DNA, knobs) — fonte da verdade
  brief.md                  # brief capturado
  points.json               # pontos de decisão + contrato (eixo/opções) + status de escolha
  research.md               # concorrentes/análogos: padrões bons/ruins, citados (se ligado)
  points/
    d1-<slug>.html          # canvas de comparação: 3 frames lado a lado (iframes live,
                            # toggle desktop/mobile), labels "A — <descritor estrutural>"
  variants/
    d1-a/                   # mini-projeto navegável: 2–3 telas linkadas (index, detail, form…)
    d1-b/  d1-c/
    d2-a/  …                # (por ponto de decisão)
  judge-report.md           # juiz: PASS/FAIL por eixo + findings abertos
  decisions.md              # escolhas + descartes + porquês (inclusive rerolls)
  tokens.css                # (pós-escolha) escalas núcleo da direção escolhida
  styleguide.html           # (pós-escolha) mini DS estático: tokens visíveis + componentes
                            # principais em seus estados-chave (botão, input, card, nav, tabela…)
  handoff.md                # (pós-escolha) inventário de componentes + estados + notas de
                            # fidelidade ("isto é intencional / isto é placeholder")
  chosen/                   # (pós-escolha) cópias das variantes escolhidas por ponto
```

Regras dos artefatos:
- Cada variante é **pequena e focada no ponto** (2–3 telas que exercitam a decisão — ex.: para "modelo de navegação", a tela principal + uma secundária alcançável pela navegação), nunca um app inteiro.
- Tudo é HTML/CSS estático, sem build, sem JS exceto um mínimo inline no canvas/galeria (toggle de largura, `< 30` linhas). Galeria é **display-only**: zero scripting cross-frame (compatível com `file://`).
- Imagens: nenhuma imagem binária no repo do protótipo; "imagens" são placeholders CSS/SVG conforme a direção (halftone, hairlines, formas).
- Fontes: webfonts via CDN permitidas (≤2 famílias + ≤1 mono), **sempre** com fallback stack da mesma classe (offline mantém o register).

---

## 5. Mecanismos

### 5.1 Seed → carta de direção

- Seed = string livre (`--seed cafe-com-leite`) ou aleatória curta gerada na sessão; sempre exibida e registrada.
- Algoritmo determinístico (spec em `references/seed-algorithm.md`, implementado em `scripts/roll.py`, espelho `roll.mjs`): `sha256(seed + ":direction:v1")` → índice no catálogo (após filtro de compatibilidade); draws subsequentes do mesmo hash derivam os **knobs ortogonais**: accent dentro da lógica da direção, densidade ±1, inversão claro/escuro onde a direção permite, escolhas de ritmo (par/ímpar), voz de copy, sujeito de "imagem".
- **Fonte da verdade é o `direction.json` commitado**, não a capacidade de re-derivar: mesmo que o script não rode, o card registrado manda. Determinismo é verificado por teste (§10).
- Filtro de compatibilidade: se o brief declara domínio, direções cujo `fails` conflita são excluídas do sorteio (ex.: tabela densa de booking não cai em slow-living). Com domínio vago, sorteio 100% livre. Nunca "média" as opções — só poda incompatibilidades declaradas.
- Reroll: nova seed → nova carta; seeds preteridas + motivo vão para `decisions.md`.
- `--wild`: cada variante sorteia sua própria direção (modo extra, off por default).

### 5.2 Catálogo de direções

Base: anexo `directions-draft.md` v0.1 — 22 direções fechadas (Swiss International, Editorial Luxe, Broadsheet Newsprint, Quiet Luxury, Scandinavian Slow-Living, Neo-brutalism, Terminal/CLI, Data Control Room, Art Deco, Risograph/Zine, Blueprint/Technical, macOS-native, retro-futurismo, playful/toy, etc.), cada uma com DNA completa: tipografia (faces concretas + alternativas grátis), lógica de cor, paradigma de layout, densidade, linguagem de forma/raio/sombra, motion, estilo de imagem, voz de copy, exemplares, `fits`/`fails`, **failure modes** (quando fica barato) e **forbidden moves**.

Implementação: `references/directions.md`. Cada direção ganha tags de **família** (quiet, dark, retro, print…) para dois usos: no modo `--wild`, garantir que as 3 variantes não caiam na mesma família; e no reroll, evitar repetir a família da sessão anterior quando plausível. O filtro de compatibilidade (`fits/fails`) é ortogonal a isso.

### 5.3 Anti-slop em 4 camadas

1. **Direção fechada** — o gerador renderiza uma direção especificada (não "usa bom gosto"): a média é estruturalmente impossível de acontecer por acidente.
2. **Regras tipográficas** — faces concretas por direção; Inter/Roboto/system-ui são *tell* e só entram onde a própria direção legitima (ex.: macOS-native); alternativas grátis listadas.
3. **`check-slop.py`** — scan mecânico dos 26 fingerprints com testes concretos em HTML/CSS (ex.: `font-family: Inter`, gradiente indigo→purple, 3 cards iguais após o hero, `border-radius` uniforme, `backdrop-filter` decorativo, slate-900 dark + neon, cream+amber "warm"). Limiar: **≥4 hits = reprova**; um único item pode ser escolha legítima. Fingerprints difusos ficam para o juiz (camada 4).
4. **Juiz de diversidade** — verifica se as 3 variantes realmente diferem **no eixo declarado do contrato** e não são reskins (o gate que nenhuma ferramenta do mercado tem, cf. `landscape.md`).

### 5.4 Juiz (gate pré-humano)

- **Fresh context**: subagent dedicado que NÃO vê o raciocínio do gerador; recebe `brief.md`, `direction.json`, `points.json`, os HTMLs, `research.md`.
- **5 eixos** (rubric em `references/judge-rubric.md`):
  1. **Fidelidade ao brief** — cada variante responde ao seu ponto? Algo contradiz o brief?
  2. **Estranhamento** — walkthrough fresh-eyes: "como usuário, o que confunde, salta errado, parece quebrado?" (copy incoerente, affordance morta, ruído visual, quebra em larguras comuns).
  3. **Slop scan** — fingerprints + slop de segunda ordem (cream+Playfair+gold, fake distress, glow+purple, etc.).
  4. **Fidelidade à direção** — DNA seguida? Failure modes da direção evitados? Conflitos C2/C3 (misturar dois registros) ausentes?
  5. **Diversidade cross-variante** — implementou as opções prometidas no contrato do ponto? As opções diferem *estruturalmente* no eixo, não cosmeticamente?
- **Evidência**: code-first (HTML/CSS é o artefato; o juiz lê). Com browser tool disponível: screenshots em desktop+mobile, navegação file:// clicada, contraste e quebras. Sem: modo degradado documentado.
- **Saída**: `judge-report.md` com PASS/FAIL por eixo + findings `{severidade: blocker|major|minor, alvo, evidência, por que importa, fix sugerido}`.
- **Loop**: blockers/majors → corrigir → re-julgar (≤2 rodadas). Minors/incertezas ficam **reportados abertos** no relatório (transparência — o usuário vê o que ficou).

### 5.5 Research de concorrentes (runtime, grátis, citado)

- Subagent(s) com web search/fetch (e screenshots via browser tool quando houver).
- 3–6 fontes do domínio do brief (produtos reais; se o domínio for nichado, análogos por padrão de uso) → `research.md`: por fonte `{nome, url, categoria, padrões bons observados, padrões ruins, o que copiar, o que evitar}`.
- Disciplina: **observado vs inferido** (afirmações sobre a UI apontam a evidência da página; inferências são marcadas como tal). Toda fonte citada com URL.
- Time-boxed; `--skip-research` desliga; resultado cacheado na pasta do protótipo (reuso em sessões futuras do mesmo produto).
- Consumo: (a) derivação dos pontos de decisão (padrões do domínio sugerem decisões), (b) critérios do juiz (clichês do domínio a evitar), (c) realismo de copy/conteúdo.

### 5.6 Handoff

Pós-escolha, a skill gera:
- `tokens.css` — escalas núcleo da direção escolhida (cor, tipografia, espaçamento, raio, motion) como CSS custom properties.
- `styleguide.html` — mini design system estático da escolha: tokens visíveis + componentes principais (botão, input, card, nav, tabela…) em seus estados-chave; mesma direção, um único arquivo.
- `handoff.md` — inventário dos componentes que apareceram, estados-chave, notas de fidelidade ("intencional" vs "placeholder") e onde cada decisão foi registrada.
- `chosen/` — cópias das variantes escolhidas por ponto.

---

## 6. Estrutura do repo da skill (`proto-lab`)

```
proto-lab/
  README.md                  # o que é, instalação, demo, modelo de custo explícito
  LICENSE                    # MIT
  SKILL.md                   # workflow agent-facing, token-efficient (~350 linhas)
  references/                # progressive disclosure — SKILL.md referencia, não repete
    directions.md            #   22 direções: DNA, fits/fails, família, forbidden moves
    slop-fingerprints.md     #   26 fingerprints + testes concretos + limiar (≥4 = reprova)
    seed-algorithm.md        #   spec determinística seed → carta + knobs ortogonais (C1–C5)
    decision-points.md       #   taxonomia, como derivar, formato do contrato (axis/options)
    judge-rubric.md          #   5 eixos, severidades, template do report, modo degradado
    research-protocol.md     #   protocolo citado, "observado vs inferido", timebox
    handoff-format.md        #   formatos: decisions/tokens/styleguide/handoff
  scripts/
    roll.py                  #   seed → direction.json (stdlib only)
    roll.mjs                 #   espelho Node (runtime dos harnesses)
    check-slop.py            #   scan mecânico dos fingerprints no HTML/CSS gerado
    scaffold.py              #   cria a estrutura da sessão a partir dos templates
    serve.py                 #   opcional: servidor local p/ navegação file://-problemática
  assets/
    gallery.html             #   template da galeria/canvas de comparação (JS mínimo inline)
    variant-shell.html       #   shell de página de variante (neutro, na DNA da sessão)
  examples/
    <exemplo-real>/          #   1 sessão de exemplo completa (1 ponto) = qualidade de
                             #   referência + demo (gerada pela própria skill)
  tests/
    scenarios.md             #   cenários de pressão (linha de base RED) + critérios
    fixtures/                #   HTMLs positivos/negativos p/ o check-slop.py
```

### SKILL.md

- Frontmatter agentskills.io: `name: proto-lab` (provisório) + `description` **só com condições de disparo**, em terceira pessoa — sem resumir o workflow (lição do writing-skills/superpowers: descrição que resume vira atalho que o agente segue e pula o corpo do skill). Alvo: "Use when the user wants to explore UI design options, prototype screens/flows in HTML before implementing, or asks for design variants/mockups for a feature."
- Corpo: overview + core principle (escolher design antes de implementar; divergência por seed); quando usar/não usar; pipeline com gates (§3); quick reference de flags (`--seed`, `--skip-research`, `--points`, `--variants`, `--wild`); common mistakes; tabela de racionalizações (ex.: "a direção sorteada não combina com meu domínio, vou usar a minha" → não: se `fits/fails` condena, rerrola a seed; improvisar = violação) + red flags.
- Regras invioláveis declaradas no SKILL.md: não ler código/UI do alvo para design (só specs/docs p/ requisitos); não inventar direção fora do catálogo; não pular o juiz; não apresentar antes do juiz passar (ou reportar abertamente o que falhou).

---

## 7. Modelo de custo

- **Dominante**: geração das variantes (3 × pontos × 2–3 telas), paralelizada por subagent (1 por ponto), em modelo barato conforme config do harness.
- **Defaults**: ≤4 pontos (configurável), 3 variantes, research on (desligável), juiz 1 subagent + fixes. Piso: 1 ponto = 3 telas + canvas + galeria.
- **Alavancas de economia**: reroll (nova direção) em vez de regerar; cache de research; `--variants 2`; `--points`; `--wild` off; juiz code-first (sem screenshots quando não houver browser tool).
- **Zero custo de infraestrutura**: sem serviços pagos, sem build, sem rede obrigatória (webfonts com fallback + research opcionais).
- README documenta o modelo (custo = tokens do harness; nada além disso).

---

## 8. Degradação e prevenção

Princípio: **prevenção primeiro, degradação só para o resíduo**. Prevenção = dependências reduzidas ao que existe por definição onde a skill roda (node é o runtime dos próprios harnesses; o browser é o humano) + **artefatos como fonte da verdade** (`direction.json` commitado; não dependemos de re-sortear). As rotas de degradação remanescentes entram na bateria de testes (§10).

| Edge case | Prevenção | Sobra (fallback) |
|---|---|---|
| Sem python3/node | Harness roda em Node → `node` existe onde a skill roda; e a fonte da verdade é o `direction.json`, não o script | Agente executa o algoritmo de `seed-algorithm.md` direto; python como secundário |
| Sem browser tool | Juiz é **code-first por design** — o artefato é HTML/CSS; validação visual final é do humano (que sempre tem browser) | Juiz só-código; screenshots quando existirem |
| Offline / webfont não carrega | Fallback stack **por classe** obrigatório (offline mantém o register) + direções system-font-first (Terminal, Swiss, macOS-native) | Research off; fontes caem no stack |
| iframes em `file://` | Galeria **display-only** (zero scripting cross-frame); iframes relativos no mesmo diretório renderizam nos 3 browsers | `serve.py` p/ robustez |
| Brief ambíguo | Intake com schema mínimo (produto, público, objetivo, telas-chave, restrições); ≤3 perguntas só para campo load-bearing; gate de pontos confirma antes de gastar geração | Reroll depois do gate |
| Rejeição total | Preview da direção antes de gerar (rerrollar é grátis); `fits/fails` poda incompatibilidades declaradas; rejeitar estrutura = escolher outra variante | `--wild`, ou novo brief |
| Mistura incoerente de direções | Carta inclui **forbidden moves** + mistura role-scoped (regras C2/C3); subagent gerador recebe carta + failure modes daquela direção | Juiz eixo 4 aponta e o loop corrige |
| Harness sem subagents | Cada fase especificada para rodar **inline também** (sequencial; só custa mais contexto) | Execução inline |
| Custo estoura | Caps duros no SKILL.md (≤4 pontos, ≤3 telas/variante, ≤6 fontes, ≤2 rodadas de juiz) + stop conditions | Flags (`--points`, `--variants`…) |
| Contaminação pelo repo alvo | Regra explícita no SKILL.md: não ler código/UI do alvo para design (só specs/docs p/ requisitos) | Red flag declarada ("segui o tema existente" = violação) |

---

## 9. Verificação (TDD de skill — exigido pelo superpowers/writing-skills)

### RED — linha de base sem a skill (documentar verbatim)

1. "Faz um protótipo de um dashboard de <domínio>" → esperado: 1 design genérico (Tailwind-ish/Inter/purple ou similar), sem opções.
2. "Me dá opções de design pra essa tela" → esperado: 3 variações cosméticas do mesmo cluster (mesma estrutura, cores diferentes).
3. Sob pressão de tempo ("rápido, só um mockup"): pula pesquisa, pula julgamento, apresenta o primeiro resultado.

### GREEN — com a skill

Cenários acima produzem: carta sorteada exibida, variantes divergentes no eixo declarado, `judge-report.md` presente com PASS nos eixos, `check-slop.py` passando, diversidade verificada. Cenário 3: a skill mantém juiz + gates (ou reporta explicitamente o que foi pulado).

### REFACTOR

Racionalizações encontradas nos testes viram contadores explícitos na tabela do SKILL.md; re-testar até fechar.

### Testes mecânicos

- `roll.py`: determinismo (mesmo seed → mesma carta, 1.000 execuções); distribuição (200 seeds → cobre o catálogo; sem repetição na janela imediata); filtro `fits/fails` (seed fixa + domínio → exclui direções condenadas).
- `check-slop.py`: fixtures positivas/negativas (≥4 hits reprova; 1 hit passa); zero falso-positivo nos exemplos.
- `scaffold.py`: idempotente; estrutura de pastas exata de §4.
- Fontes: cada direção do catálogo tem fallback stack de classe correta (check automatizável sobre `directions.md`).

### Aceitação (ponta a ponta)

- Rodar a skill de verdade no repo `homelab` (ou projeto de teste) com 3 seeds diferentes → 3 saídas **visivelmente distintas** (conferir com screenshots via agent-browser: desktop + mobile); mesma seed → mesma carta.
- `examples/` do repo = uma sessão real completa (1 ponto, 3 variantes) gerada pela própria skill; serve de demo, de quality bar e de teste de aceitação.
- Rodar uma vez offline (fonts bloqueadas) e uma vez sem browser tool, conferindo as rotas de degradação de §8.

---

## 10. Riscos e questões abertas (para o plano endereçar)

- **Qualidade do catálogo v0.1**: o anexo `directions-draft.md` é rascunho; o plano deve incluir passo de formalização (famílias, `fits/fails`, forbidden moves, fallbacks de fonte, e checagem por julgamento independente de que as 22 direções são distinguíveis entre si).
- **Licença de fontes**: priorizar webfonts livres (Google Fonts) + alternativas de sistema; nenhuma face proprietária no material do repo (apenas citada como referência de classe).
- **Diversidade julgada por LLM**: parte dos eixos do juiz é julgamento (não mecânico) — mitigação: contrato de eixo explícito + critérios observáveis no rubric + o juiz sempre reporta a evidência.
- **Performance da galeria**: muitos iframes — usar `loading="lazy"` nativo nos iframes; cap de pontos por sessão segura o tamanho.
- **Nome**: `proto-lab` é provisório; renomear antes de publicar (custo zero até lá).
- **Publicação**: plano cobre o repo local + README; publicação no GitHub (org/conta, topics, licença) fica como último passo opcional.

---

## 11. Anexos

- `docs/research/landscape.md` — levantamento de prior art: skills oficiais e da comunidade, ferramentas comerciais, evidência de homogenização (papers), tooling de divergência por seed, fontes de research de concorrentes; seção final "Gaps & opportunities" fundamenta os diferenciadores da skill.
- `docs/research/directions-draft.md` — v0.1 do catálogo: 22 direções detalhadas, 26 fingerprints de AI-slop com testes concretos em HTML/CSS, e regras de coerência (C1–C5) do motor de seed.
