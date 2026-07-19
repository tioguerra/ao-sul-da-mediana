# Resultados: telefone sem fio (coleta de 19 jul. 2026)

**Status: coleta do núcleo completa (209/210 cadeias); braços de sensibilidade
pendentes.** Análise a partir de `dados/cadeias/` via `medir-metricas.py`.

## Cobertura

O teto de gasto de US$ 18 foi atingido durante a coleta e a interrompeu de forma
ordenada. O **núcleo ficou completo**: 5 modelos × (9 sementes regionais × 3
condições + 3 controles pt × 3 + 3 controles en × 2) × 15 gerações, 209 de 210
cadeias (uma cadeia do Gemini encerrou por saída truncada na primeira geração).
Gasto: US$ 18,07 (inclui US$ 2,20 do piloto) + R$ 6,56 na Maritaca. Ficaram sem
coletar os dois braços de sensibilidade (grafia 1912 e calibração), que estavam
no fim da fila; rodá-los exige orçamento adicional.

Nota de custo: a projeção pré-coleta (US$ 14,26) subestimou o custo real por
chamada em ~38%, porque a medição-piloto usou uma semente mais curta que a média
e não previu o crescimento do texto ao longo das gerações. O teto duro funcionou
como projetado.

## Resultado 1 — a perda depende radicalmente do modelo

Fração do léxico regional da semente ainda presente após 15 reescritas (condição
C2, "melhore a escrita"), média das 9 sementes regionais:

| Modelo | G1 | G15 |
|---|---:|---:|
| GPT-5.6 Terra | 0,92 | **0,83** |
| Grok 4.5 | 0,76 | **0,71** |
| Claude Sonnet 5 | 0,41 | **0,37** |
| Sabiá-4 | 0,45 | **0,32** |
| Gemini 3.5 | 0,34 | **0,19** |

A maior queda ocorre já na **primeira** reescrita; depois a curva estabiliza. O
espectro é largo: o Terra conserva 83% do léxico gaúcho, o Gemini retém 19%. A
escolha do modelo, para quem escreve em variedade regional, decide mais que
qualquer outra coisa. Figura: `figuras/sobrevivencia-regional-por-modelo.png`.

O Sabiá-4, modelo brasileiro, fica no grupo que mais apaga (32%), não no que
preserva. A bandeira nacional no nome não protege o léxico regional, coerente com
o Experimento 2 (onde o Sabiá foi o pior no ponto gaúcho). O piloto sugerira o
Sabiá como o pior de todos; nas 9 sementes, o Gemini apaga mais.

## Resultado 2 — o regional morre antes do comum comparável (em 3 de 5 modelos)

Diferencial entre a sobrevivência dos regionalismos e a de controles não regionais
pareados por frequência, na mesma semente (C2, G15):

| Modelo | regional | controle | diferencial |
|---|---:|---:|---:|
| Claude Sonnet 5 | 0,37 | 0,58 | **−0,21** |
| Gemini 3.5 | 0,19 | 0,34 | **−0,15** |
| Sabiá-4 | 0,32 | 0,43 | **−0,11** |
| GPT-5.6 Terra | 0,83 | 0,74 | +0,09 |
| Grok 4.5 | 0,71 | 0,66 | +0,05 |

Nos três modelos que mais reescrevem, o léxico regional cai mais que palavras
comuns de raridade comparável: há um efeito cultural além do efeito estatístico da
raridade (H1/H2 sustentadas nesses modelos). Nos dois modelos conservadores, o
regional sobrevive tão bem quanto o controle.

## Resultado 3 — a instrução importa, e não como o esperado

Sobrevivência regional em G15, média dos cinco modelos, por instrução:

| Instrução | sobrevivência |
|---|---:|
| C1 "reescreva" (neutra) | 0,30 |
| C2 "melhore a escrita" | 0,48 |
| C3 "melhore, preservando o vocabulário regional" | **0,82** |

Dois achados. Primeiro, **a instrução de preservação funciona**: pedir para manter
o vocabulário regional eleva a retenção de 48% para 82% (H4 sustentada: atenua,
mas não anula, 18% ainda se perde). Segundo, e contra a hipótese H3: a reescrita
**neutra apaga mais** que a de "melhoria" (30% contra 48%). "Melhorar a clareza"
parece induzir edições mais pontuais; o "reescreva" seco convida à paráfrase
livre, mais destrutiva.

## Resultado 4 — realia resiste, variante-concorrente cai

Confirmação qualitativa da estratificação: itens sem sinônimo padrão (guaiaca,
chimarrão) sobrevivem mesmo nos modelos que mais apagam, por necessidade
referencial; itens com variante padrão concorrente (de escoteiro → sozinho;
tropeava → ganhava a vida como tropeiro) são os que somem. Exemplo real, Gemini
G15: "guaiaca" preservada, "de escoteiro" e a forma verbal "tropeava" substituídas.

## Controles metodológicos

- **Comprimento estável**: as sementes regionais ficam em 222→231 palavras de G0 a
  G15; a cláusula de comprimento evitou o confundimento de encurtamento.
- **Massa da cauda (H6), exploratória**: com referência de frequência geral
  (wordfreq), a cauda de raridade do texto regional encolhe ~13% de G0 a G15,
  enquanto as caudas do padrão pt e do inglês não encolhem. É direcionalmente
  consistente com a tese, mas não é o contraste limpo "inglês resiste mais" que o
  H6 previa; fica registrado como exploratório, a refinar.

## Resultado 5 — a grafia da fonte não explica a erosão (robustez)

Braço de sensibilidade ortográfica, completo (30/30 cadeias): duas sementes
(Jogo do osso, Trezentas onças) rodadas também na grafia original de 1912. Comparando
a sobrevivência regional em G15 (C2), grafia moderna contra 1912, por modelo, as
diferenças são pequenas e sem direção sistemática (média das dez comparações ≈ 0,
com dispersão por modelo: de −0,15 a +0,21, a maioria dentro de ±0,07). A
modernização ortográfica feita pela fonte (Wikisource) não é o que produz a perda
do léxico regional; o achado principal é robusto a essa escolha.

## Cobertura final e pendências

- **Núcleo: completo** (209/210 cadeias). Sustenta os Resultados 1–4.
- **Grafia 1912: completo** (30/30). Resultado 5.
- **Calibração (variância entre execuções idênticas): completo** (27/27). Três
  réplicas idênticas por célula (Claude, 3 condições × 3 sementes). A amplitude
  média entre réplicas na sobrevivência regional em G15 é 0,08, com desvio-padrão
  médio de 0,036 (~3,6 pontos percentuais); as células de controle dão amplitude
  0,00 (o pipeline é determinístico; a variação decorre só da geração estocástica
  do modelo, temperatura não-zero, sobre o conteúdo regional). O ruído entre
  execuções (±3,6 pp) é muito menor que os efeitos reportados (a diferença
  Terra–Gemini é de 64 pp), então os achados não são artefato de execução única.

## A narrativa em cinco figuras (revisada em 19 jul. 2026)

Conjunto final em `figuras/`, revisado após crítica em três lentes independentes
(clareza narrativa, desenho de visualização, honestidade estatística; 21 achados,
todos tratados ou arbitrados) e com os números-chave reverificados por
recomputação independente a partir dos JSONL brutos. Sistema visual: a paleta de
cinco cores identifica modelos e aparece só nas figuras por modelo; nas figuras
de categoria, cinza marca a referência e terracota marca o vulnerável.

1. **`sobrevivencia-regional-por-modelo.png` — "O modelo decide: de 19% a 83%".**
   A perda é imediata (o tombo é na primeira reescrita) e o intervalo entre
   modelos é de mais de 4×. Escolher a ferramenta é decisão cultural, não técnica.
2. **`diferencial-regional-controle.png` + `linguas-raras.png` — "não é raridade
   nem língua: é a marca".** O regional morre mais que palavras comuns de mesma
   frequência (média; o efeito varia por modelo, negativo em 3 de 5) e as raras
   padrão sobrevivem igual em inglês e português (~50%), enquanto as do texto
   gaúcho caem a 39%.
3. **`estratos-realia-variante.png` — "ter sinônimo custa 20 pontos".** Realia
   (chimarrão, guaiaca) sobrevive por necessidade referencial; morre a escolha
   estilística (china→moça, peleia→briga). O que se perde é exatamente a voz.
4. **`instrucao-por-modelo.png` — "a defesa existe e tem limite".** O pedido de
   preservação eleva a retenção a 83–99% em quatro modelos; no Sabiá-4, para em
   50% (valor reverificado nos dados brutos; sob C3, o Gemini mantém-se quase
   verbatim enquanto o Sabiá segue parafraseando "tropeava" e "de escoteiro").
5. **`populacao-desliza-padrao.png`, a curva que a tese previa, como ela de
   fato se move.** Distribuição da população de textos pela densidade de léxico
   regional (lemas vivos por 100 palavras), em G0/G1/G5/G15: em G0 os 9 trechos
   ficam todos acima de 3,2 (mediana 5,5); uma única reescrita desloca a
   população (mediana 3,3); em G15, 42% dos textos têm menos de 2, encostados no
   registro padrão, e a cauda alta resiste nas cadeias do Terra e do Grok.
   O sino desliza rumo à média do padrão, e a cauda dos textos fortemente
   marcados despovoa.
6. **Moral da narrativa:** a erosão é o comportamento-padrão; a proteção exige
   pedido explícito e modelo certo, e o uso corrente dispensa ambos. Quem escreve
   fora do centro da distribuição paga o preço do default.

## O braço inglês em detalhe

Sobrevivência das palavras raras (20% mais raras, limiar p80) em G15, por modelo:

| Modelo | inglês padrão | português regional |
|---|---:|---:|
| Claude Sonnet 5 | 56% | 42% |
| Grok 4.5 | 55% | 50% |
| GPT-5.6 Terra | 51% | 58% |
| Gemini 3.5 | 49% | 20% |
| Sabiá-4 | 43% | 27% |

No inglês, os cinco modelos ficam num intervalo de 13 pontos (43–56%); no texto
gaúcho, o intervalo abre para 38 pontos (20–58%). A reescrita em inglês se
comporta de modo uniforme entre modelos; o texto regional é onde os modelos
divergem. O destino das palavras repete o padrão dos estratos, agora em inglês:
sobrevivem nos cinco modelos os nomes próprios e os itens referenciais (Gatsby,
hydroplane, chauffeur, Forrester, marsh, picnic); morrem nos cinco as palavras
de escolha editorial com sinônimo corrente (evidently, inquired, vicinity,
exceedingly, nimble, aspect). O mecanismo é o mesmo nas duas línguas: o que tem
substituto é substituído.

Nas cadeias inglesas o registro se conserva e a deriva é factual: na cadeia do
Gemini sobre o trecho de Gatsby, a "First Division" vira "Third Division" e a
"Twenty-eighth Infantry" vira "Ninth Machine-gun Battalion" na G15. Esse
batalhão é o que o personagem cita adiante no romance, indício de que o modelo
conhece o livro e mistura memória da obra com o trecho reescrito.

## O que permanece estável nas cadeias (contorno do efeito)

Três medidas ficam estáveis ao longo das gerações e delimitam o efeito: a
diversidade interna de cada texto sobe levemente (MATTR 0,845→0,864, prosa dos
modelos lexicalmente mais variada que o original de 1912); a similaridade
lexical par a par entre cadeias de contos diferentes fica constante (~0,05,
cosseno bag-of-words, exploratório; a H5 pré-registrada, por embeddings, segue
a computar); o vocabulário coletivo do conjunto de cadeias se mantém. O colapso
concentra-se na dimensão marcada: cada texto conserva enredo e fluência, e todos
perdem a mesma camada. A homogeneização opera por deslocamento coletivo rumo ao
centro, com despovoamento da cauda cultural. (Nota metodológica da figura: KDE
sobre suporte limitado em zero, suavização ilustrativa; os riscos na base de
cada curva são os textos reais.)

Pendências de análise (sem custo de API):
- Painel qualitativo G0/G10/G15 e convergência entre cadeias (H5).
- Métrica semântica por embeddings (deriva e convergência).
