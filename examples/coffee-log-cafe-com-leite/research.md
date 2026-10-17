# Research — diário pessoal de cafés

- domain: registro pessoal de cafés tomados (food and beverage, uso próprio)
- sources used: 3 (cap 6, floor 3)
- mode: fetch (markup e texto visível das páginas citadas). Sem clique em fluxo
  logado e sem screenshots nesta etapa; o que não foi visto está marcado como
  `inferred:`.

Ninguém loga um café por vaidade de dados: o hábito que as pessoas querem copiar
do Untappd é o *check-in* — "registrar a taça, dar uma nota, ver o que os amigos
bebem" (fonte 3, observado). O que muda entre os apps é o que se registra: o
preparo em casa, o lugar, ou o pacote de grãos.

## 1. Beanconqueror — direct-competitor

```json
{
  "name": "Beanconqueror",
  "url": "https://beanconqueror.com/",
  "category": "direct-competitor",
  "good_patterns": [
    "O loop de duas telas é explícito: 'Brew Overview — A complete overview of your brewings' seguido de 'Brew details — Get any detail you want from your brews' (observed: cards de feature da home, seções 'Brew Overview' e 'Brew details')",
    "Registro é a unidade da lista: cada brew tem dose, tempo, moagem e uma nota (observed: 'Record and adjust over 30 brewing parameters like grind size, brew time, and water amount')",
    "O app se apresenta como caderno pessoal, não rede: sem feed de amigos (observed: seção 2 da fonte 3 descreve 'no friend feed, no café map, no community ratings')",
    "Dados ficam no aparelho e funcionam offline (observed: review da App Store citado na home: 'making monthly exported backups, as all data is stored on your phone')"
  ],
  "bad_patterns": [
    "Densidade de instrumento: a home lista ~20 balanças compatíveis, refratômetros e sensores de pressão antes de qualquer menção ao ato de registrar (observed: seção 'Compatible Devices' com listas longas)",
    "O vocabulário é de laboratório ('brew monitoring', 'pressure profiling'), não de hábito diário (observed: headings 'Powerful and stylish', 'Visualize your brews', 'Freeze function')",
    "inferred: a navegação de um app com 30+ parâmetros por brew provavelmente não cabe em um uso casual de uma mão"
  ],
  "what_to_copy": "A lista é feita de registros, cada um abrindo em um detalhe completo; e a ausência de camada social é uma escolha de produto, não uma falta.",
  "what_to_avoid": "Importar a densidade de instrumento: uma home que lista equipamento compatível antes do log transforma um diário casual em um painel de laboratório."
}
```

## 2. iBrewCoffee — direct-competitor

```json
{
  "name": "iBrewCoffee — Coffee Journal",
  "url": "https://play.google.com/store/apps/details?id=coffee.ibrew.ibrewcoffee&hl=en_US",
  "category": "direct-competitor",
  "good_patterns": [
    "Fluxo declarado em dois passos, na ordem do uso: '1) save a Product (bag of specialty coffee), 2) record your Brews, experiment, rate, compare' (observed: seção 'About this app')",
    "Cada brew guarda exatamente os campos do brief: método, razão, temperatura, tempo, perfil de sabor e nota geral (observed: lista de campos em 'Brew')",
    "A razão e o rendimento são derivados, não digitados: 'Brew ratio and extraction yield are calculated automatically!' (observed: mesma seção)",
    "Avaliação de leitor pede o cartão com a imagem grande e origem logo abaixo: 'an image of the bag that takes up a large portion of the card and then right underneath the roaster (+country) and origin are displayed' (observed: review de Vivek Garimella, 21/03/2025)"
  ],
  "bad_patterns": [
    "Entrada de dados dirigida por catálogo antes de existir log: '3 000 roasteries, 2 000 coffee regions, 300 varietals' para escolher (observed: seção 'Product')",
    "Exportar para PDF/Excel e 'share on your favorite social networks' como função de primeira classe (observed: seções 'PDF Export' e 'Sharing')",
    "Review de Jorge Rodríguez relata que o arquivo fica preso a um aparelho sem assinatura (observed: review, 27/05/2024) — sinal de que a persistência é assunto de produto, não detalhe"
  ],
  "what_to_copy": "Mostrar o essencial de cada registro direto na lista (método, razão, nota) e calcular os derivados em vez de pedir.",
  "what_to_avoid": "Abrir o registro com seletores de catálogo (roastery/region/varietal) e colocar exportação e compartilhamento no caminho principal de quem só quer anotar o café de hoje."
}
```

## 3. Crumble — guia "Untappd for Coffee" — category-reference

```json
{
  "name": "Crumble — Untappd for Coffee: 7 Apps to Log Every Cup",
  "url": "https://crumble.me/guides/untappd-for-coffee",
  "category": "category-reference",
  "good_patterns": [
    "O hábito é nomeado sem rodeios: 'What people actually mean by \"Untappd for coffee\" is the check-in habit: log the cup, rate it, see what your friends are drinking' (observed: parágrafo de abertura)",
    "A opção de baixa fricção é descrita pelo que ela omite: Brewlio é 'a simple Android app for recording each cup you brew with the essentials and nothing more', um 'searchable diary of your daily cups' (observed: seção 6)",
    "O guia separa três trabalhos diferentes — preparo em casa, lugar, pacote — e diz que nenhum app faz os três (observed: parágrafo de abertura e 'How to choose')"
  ],
  "bad_patterns": [
    "Camada social e de conquistas é a norma da categoria: badges por país (Kava), seguir baristas (Coffunity), feed de amigos (Tasting Grounds) (observed: seções 3, 4 e 5)",
    "Sem escala própria nem notas por item, o log degenera em favoritos: 'a star is not a rating. There's no scale of your own, no per-drink notes' (observed: seção 7, sobre listas do Google Maps)",
    "Profundidade de parâmetros afasta o uso casual: 'the depth that delights gear nerds can overwhelm someone who just wants to remember that Tuesday's Ethiopian pour-over was great' (observed: seção 2)",
    "O próprio guia declara conflito de interesse (a Crumble é um dos apps listados) — peso de referência, não de avaliação neutra (observed: 'Full disclosure' e 'How we chose these apps')"
  ],
  "what_to_copy": "Registrar a xícara com nota e notas de sabor é o núcleo do hábito; o resto (mapa, badges, feed) é opcional e não deve ocupar o caminho principal.",
  "what_to_avoid": "Tratar social/badges como requisito do diário pessoal, e trocar a nota por um 'favorito' sem escala nem nota por item."
}
```

## O que a pesquisa muda nos pontos

- A convenção da categoria é **lista → detalhe** (fontes 1 e 2): o ponto desta
  sessão não pergunta *se* existe detalhe, e sim **como a lista se apresenta** —
  daí `listing-pattern` como único eixo.
- Os clichês específicos do domínio entram no juiz como critérios de `slop-scan`
  / `direction-fidelity`: densidade de instrumento (fonte 1), catálogo antes do
  log (fonte 2), camada social/badges (fonte 3), favorito sem escala (fonte 3).
- Vocabulário de conteúdo (para o copy ilustrativo): origem, região/produtor,
  método (V60, prensa, espresso, moka), moagem, razão, tempo, perfil de sabor,
  nota. Vem das fontes 1 e 2.
