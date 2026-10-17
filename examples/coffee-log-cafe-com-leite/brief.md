# Brief

- **produto** — diário pessoal de cafés: registra cada café tomado, com origem,
  método de preparo e notas de sabor.
- **público** — uma pessoa que toma café todo dia, em casa ou no trabalho, e quer
  lembrar o que valeu a pena repetir. Não é barista, não é loja.
- **objetivo** — registrar um café em poucos toques, no celular, e reencontrar
  depois o que foi tomado (por origem, método ou nota).
- **telas-chave** — `index` (lista/log dos cafés) e `detail` (um café, o registro
  completo). São as duas únicas telas desta sessão.
- **restrições**
  - casual e rápido: uso diário, uma mão, no celular (390px é o alvo principal);
  - sem conta, sem servidor, sem sincronização — protótipo estático, dados de
    exemplo;
  - sem imagens binárias: qualquer "imagem" é placeholder CSS/SVG;
  - a lista carrega os dados que a pessoa registra: origem, método, notas.

## Suposições (registradas, não confirmadas silenciosamente)

- idioma da interface: português (o brief é em português; o alvo é o próprio
  autor).
- volume esperado: algumas centenas de cafés ao longo de anos; a lista precisa
  aguentar leitura rápida, não paginação sofisticada.
- notas de sabor são texto livre + uma nota de 0 a 5; escala de defeito/extração
  fica fora do escopo do ponto.

## Fora de escopo (nesta sessão)

- cadastro/edição (formulário), busca/filtro, onboarding, estados vazios,
  estatísticas. Cada um seria um ponto de decisão próprio; a sessão declara
  **1 ponto** e não os gera.
