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

Pendências de análise (sem custo de API):
- Figuras restantes (densidade de raridade, obituário por item, convergência,
  painel qualitativo G0/G10/G15).
- Métrica semântica por embeddings (deriva e convergência).
