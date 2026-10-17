# Decisions — coffee-log-cafe-com-leite
- seed: `cafe-com-leite` (recorded; source of truth is `direction.json`)
- direction: `D10 — Blueprint / Schematic`
- points: 1 (cap 4)

## Chosen
- d1 — Como o log de cafés deve se apresentar na tela principal? — chosen: variant `d1-c` — option "Feed de coluna única: uma entrada por linha, largura total, em ordem cronológica, com o registro lido como diário."
  - why: o brief é um registro de uso diário no celular: a forma da lista decide a velocidade de registrar e de reencontrar um café; uma entrada de largura total, em ordem, é lida como diário e mantém todos os campos visíveis no alvo de 390px.
  - source: `variants/d1-c/`

## Rejected (and why)
- d1-a — option "Tabela densa" — rejected because a grade alinhada por colunas esconde dose/razão/tempo abaixo de 640px, então no alvo principal (celular) ela perde justamente os campos que o usuário registra; a varredura comparativa que ela ganha não compensa a leitura cronológica que o brief pede.
- d1-b — option "Grade de cartões" — rejected because uma grade espacial quebra a cronologia em pranchas soltas: reencontrar "o que eu tomei ontem" deixa de ser uma leitura de cima para baixo e passa a ser uma varredura de blocos, oposta ao uso casual e diário declarado.
- reroll — none: the first rolled seed `cafe-com-leite` was kept; no direction was discarded or rerolled in this session.

## Dropped candidates (recorded, not generated)
- `form-pattern` (cadastro/edição), `filtering-search` (busca/filtro),
  `empty-states` e `dashboard-composition` (estatísticas) were collected as
  candidate points and dropped: each would open a screen beyond the brief's two
  (`index`, `detail`). The session declares the single highest-blast-radius point,
  `listing-pattern`.
