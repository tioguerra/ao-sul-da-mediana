# Telefone sem fio: a marca regional some primeiro?

**Plano experimental, versão 1.4 (18 de julho de 2026)**

| Versão | Data | Mudanças |
|---|---|---|
| 1.7 | 18/07/2026 | Política de decodificação por provedor após levantamento documental: Claude Sonnet 5 rejeita amostragem não-default (envia-se temperature=1.0 e omite-se top_p, não documentado); Gemini 3.x tem recomendação oficial de omitir os parâmetros (omitidos, com defaults documentados 1.0/0.95 registrados); Terra e Grok enviam 1.0/1.0; Sabiá-4 envia 0.7/0.95 (documentados). Fontes registradas por chamada no JSONL. Lista congelada: 90 lexemas com nível de evidência (68 dicionário geral, 22 léxico especializado), 17 expressões, 8 bandeiras de homografia; método da lista adaptado (anotador 1 + verificação lexicográfica em duas camadas, por decisão do autor). |
| 1.6 | 18/07/2026 | Decisões da seção 13 tomadas com o autor: 20 gerações fixas (sem extensão automática); C3 nos cinco modelos; braço de calibração condicional aos tetos; cinco modelos mantidos; braço de grafia 1912 reinstaurado com transcrição própria do fac-símile do Commons (2 sementes, +600 chamadas); âncora da surpresal: modelo pequeno multilíngue da família Qwen; obras inglesas confirmadas; curadoria da lista: anotador 1 enxuga para ~80 itens, autor veta. Descoberta registrada: a transcrição do Wikisource é modernizada; a fonte da grafia original é o fac-símile (djvu no Commons, digitalização Google Books/Univ. da Califórnia, 228 páginas). |
| 1.5 | 18/07/2026 | Instruções dos prompts em linha única, sem quebras internas (a única quebra separa a instrução do bloco TEXTO). Corpus-fonte adquirido e registrado: Wikisource (edição de 1912, 19 contos) e Project Gutenberg (#67535 Lima Barreto, #55797 Machado, #64317 Fitzgerald, #1156 Lewis, #65636 Cather). |
| 1.4 | 18/07/2026 | Falha transitória de API deixa de gerar censura: a cadeia pausa e retoma do ponto exato; censura fica reservada ao irrecuperável. Braço em inglês (3 sementes de prosa padrão dos anos 1920, C1 e C2) para testar a vantagem de casa da língua de treinamento, com hipótese H6 e métrica de cauda comparável entre línguas. |
| 1.3 | 18/07/2026 | Teto de gasto por backend (Maritaca: R$ 30, dentro do saldo disponível) com regra pré-registrada de redução proporcional do desenho inteiro caso algum teto seja atingido na projeção do piloto. Figura F1b (distribuição entre cadeias, formato de sino) acrescentada à seção 9. |
| 1.2 | 18/07/2026 | Orçamento com teto (alvo US$ 15, teto duro US$ 18): 20 gerações, 12 sementes (9 regionais + 3 controles). Instrução de comprimento fixo nos três prompts. Figuras de densidade de raridade lexical e de surpresal como visualizações-manchete da cauda. |
| 1.1 | 18/07/2026 | Revisão após crítica adversarial em três lentes (metodologia, linguística, engenharia): sementes-controle coetâneas; desfecho redefinido com regra de absorção e censura; diferencial regional−controle como desfecho primário; pareamento por frequência no próprio corpus; `max_tokens` e registro de decodificação corrigidos; terminologia ajustada. |
| 1.0 | 18/07/2026 | Rascunho inicial. |

> **Status: planejado, não executado.** Este documento registra o desenho, as hipóteses e as regras de análise antes de qualquer coleta. Nenhuma chamada a modelo foi feita para este experimento até a data acima.

## 1. Pergunta

Quando um texto com léxico marcado regionalmente passa por reescritas sucessivas de um modelo de linguagem, esse léxico desaparece mais rápido que o vocabulário comum de raridade comparável? As cadeias que partem de textos diferentes convergem para textos parecidos entre si? E o mesmo processo, aplicado a texto padrão em inglês (a língua de quase 90% do treinamento desses modelos), preserva mais a cauda do que preserva em português?

O desenho, em uma frase: cadeias de transmissão iterada (cada geração é a reescrita da geração anterior, sem memória do original), com cinco modelos, três instruções e quinze textos-semente (nove regionais gaúchos, três controles coetâneos em português padrão e três controles em inglês padrão da mesma época), ao longo de vinte gerações, medindo a sobrevivência do léxico regional contra controles pareados, a diversidade lexical, a convergência entre cadeias e a comparação entre línguas.

Sobre os termos: o objeto medido é o léxico escrito marcado regionalmente, não fonética nem prosódia; "sotaque" fica fora do vocabulário técnico deste plano. Para o fenômeno estatístico usamos homogeneização ou convergência. "Regionalismo" é usado na acepção diatópica registrada em dicionário, com a fonte anotada item a item (seção 8).

Este é o terceiro experimento do projeto. O primeiro mostrou que a língua e o lugar do pedido mudam o conteúdo da resposta. O segundo mostrou onde os valores expressos pelos modelos caem no mapa cultural. Este testa o mecanismo temporal da hipótese central: a mediação generativa repetida comprime a distribuição, e o culturalmente marcado vive na cauda.

## 2. Fundamentação

A literatura recente estabelece o fenômeno em loops de treinamento e aponta o caminho para a variante por inferência usada aqui:

- **Shumailov et al. (2024, Nature)** definem o colapso de modelo como processo em dois estágios: primeiro o modelo perde as caudas (eventos de baixa probabilidade) da distribuição; depois converge para uma distribuição estreita, de variância reduzida.
- **Perez et al. (2024, arXiv:2407.04503)** mostram que cadeias de transmissão iterada apenas por inferência, sem nenhum retreino, convergem em dezenas de gerações para atratores estreitos nas propriedades do texto. É o precedente metodológico direto deste plano, com código público.
- **Dohmatob et al. (2024, ICML)** mostram que uma única geração já produz cauda truncada na distribuição de perplexidade, com o corte controlado pelos parâmetros de decodificação (temperatura e top-p).
- **Guo et al. (2024, NAACL Findings)** medem, em seis iterações de retreino sobre as próprias saídas, queda consistente de diversidade lexical, sintática e semântica, maior nas tarefas mais criativas, e visualizam as palavras raras desaparecendo geração a geração.
- **Padmakumar e He (2024, ICLR)** mostram que a homogeneização ocorre mesmo sem retreino: co-escrever com um modelo ajustado por instruções reduziu a diversidade de conteúdo entre autores diferentes.

Até onde a busca alcançou (julho de 2026), não há experimento publicado com semente em português nem com léxico regional como variável. Há um position paper argumentando que o colapso ameaça desproporcionalmente comunidades de baixo recurso (arXiv:2605.04127), sem experimento próprio. Esta é a lacuna que o experimento busca ocupar. O braço em inglês dá a régua do lado privilegiado: nos corpora documentados, o inglês domina o treinamento (89,7% no Llama 2, contra 0,09% de português; Touvron et al., 2023), e a predição é que a cauda de quem joga em casa resista mais.

Delimitação honesta: cadeias de reescrita por inferência modelam o uso repetido da ferramenta (um texto que passa muitas vezes pela mediação), não o retreino de modelos sobre saídas sintéticas. As conclusões falam de mediação em escala; a ponte com o colapso de treinamento é analogia fundamentada, e será apresentada como tal.

## 3. Hipóteses e desfecho primário

**Desfecho primário (H1 a H4): o diferencial de decaimento.** A quantidade central é a diferença, geração a geração, entre a taxa de sobrevivência dos regionalismos e a dos controles pareados do mesmo texto (seção 8). Sobrevivência bruta é função mecânica do comprimento do texto; o desenho ataca esse confundimento duas vezes: na origem, com a instrução de comprimento fixo (seção 6), e na análise, com o diferencial como desfecho. A sobrevivência bruta é reportada como descritiva.

**H1 (perda da cauda regional).** Nas condições sem instrução de preservação, o diferencial é negativo e cresce em magnitude com as gerações: o regional morre mais rápido que o comum comparável.

**H2 (o regional morre antes do raro).** O diferencial permanece negativo mesmo contra controles de raridade comparável no corpus-semente. O pareamento aproxima a separação entre efeito cultural e efeito estatístico de raridade, sem a garantia de isolá-los por completo (limitação declarada na seção 11).

**H3 (a instrução de melhoria acelera a perda).** O diferencial em C2 ("melhore a escrita") é mais negativo que em C1 ("reescreva").

**H4 (a instrução de preservação atenua, sem anular).** O diferencial em C3 é menos negativo que em C2, e ainda assim negativo em vinte gerações.

**H5 (convergência coletiva).** A similaridade entre cadeias de sementes diferentes cresce com a geração além do que crescem as cadeias dos controles coetâneos não regionais na mesma condição. A convergência absoluta não conta: textos que genericizam ficam parecidos por construção; o que interessa é o excesso sobre essa linha de base.

**H6 (vantagem de casa).** Nas sementes em inglês padrão, a redução da massa da cauda de raridade (métrica adimensional da seção 8, comparável entre línguas) é menor que nas sementes regionais em português, em C1 e C2. Se a cauda inglesa resistir e a gaúcha não, o experimento mostra em miniatura o custo de escrever de fora do centro do treinamento.

**Controle de época (transversal às hipóteses).** As três sementes coetâneas em português padrão separam a atualização de um texto antigo do apagamento da marca regional; as três em inglês padrão, da mesma época literária, separam o efeito da língua do efeito da idade do texto. O sinal de H6 é a diferença entre línguas com a época controlada.

**Critério de falseamento (a calibrar no piloto).** Se, agregado sobre C1 e C2 e sobre os cinco modelos, o intervalo de confiança do diferencial regional−controle na geração 20 incluir zero, H1 e H2 ficam enfraquecidas e o resultado será publicado do mesmo modo. O piloto simulará trajetórias sob o agrupamento real dos dados para conferir se o critério discrimina; o critério será congelado por hash antes da coleta completa, junto com as listas.

## 4. Desenho experimental

| Fator | Níveis | Detalhe |
|---|---|---|
| Modelo | 5 | os mesmos do Experimento 2, com identificadores e provedores fixados |
| Condição | 3 (pt) / 2 (en) | C1 neutra, C2 melhoria, C3 preservação; o braço em inglês roda só C1 e C2, porque "preservar o vocabulário regional" não se aplica a texto padrão |
| Semente | 15 | 9 regionais + 3 controles coetâneos em português + 3 controles em inglês (seção 5) |
| Geração | 20 | G0 é a semente; G1 a G20 são reescritas sucessivas |

A unidade experimental é a cadeia (modelo × condição × semente): 5 × (12 × 3 + 3 × 2) = 210 cadeias, 20 chamadas sequenciais cada, 4.200 chamadas no núcleo. Somam-se o braço de sensibilidade ortográfica (2 sementes regionais em versão com grafia original de 1912, transcrita do fac-símile: 2 × 3 × 5 × 20 = 600 chamadas) e, condicional aos tetos após o piloto, o braço de calibração (540 chamadas): 4.800 chamadas firmes, 5.340 no máximo. Cada chamada recebe apenas o texto da geração anterior e a instrução fixa; o modelo nunca vê o original, o histórico da cadeia ou qualquer menção ao experimento. Todas as cadeias serão publicadas brutas, inclusive as que derem errado.

**Interrupção não é morte.** Falha transitória (queda de rede, limite de taxa, saldo esgotado) não encerra cadeia: o estado vive no JSONL e a coleta retoma do ponto exato, no mesmo dia ou dias depois, com a data-hora de cada retomada registrada. A ressalva honesta de retomadas com intervalo longo é que provedores atualizam modelos silenciosamente; o registro das datas deixa isso auditável, e intervalos longos serão reportados. A **censura à direita** fica reservada ao genuinamente irrecuperável: o modelo ou o provedor fixado deixa de existir na rota, saída truncada ou recusa repetida (seção 7), ou interrupção definitiva pelo teto de gasto. Nesses casos, os itens vivos até a última geração observada contam como "vivos até ali", nunca como mortos: culpar o fenômeno por uma indisponibilidade técnica inflaria o resultado.

## 5. Corpus semente

**Sementes regionais (9).** *Contos Gauchescos* (João Simões Lopes Neto, 1912). O autor morreu em 1916; a obra está em domínio público, o que permite publicar sementes e cadeias completas. Nove trechos narrativamente autocontidos, de 150 a 250 palavras, cada um com ao menos oito itens da lista de regionalismos, retirados de contos diferentes (candidatos: "Trezentas onças", "No manantial", "O boi velho", "Contrabandista"; seleção final em `corpus-semente/proveniencia.md`).

**Sementes-controle coetâneas em português (3).** Prosa literária brasileira não regional da mesma época, em domínio público (candidatos: Lima Barreto, Machado de Assis; seleção final na proveniência). Mesma faixa de tamanho, mesma preparação. Elas respondem à objeção central: "isso não é perda do regional, é atualização de texto antigo".

**Sementes-controle em inglês (3).** Prosa literária americana padrão dos anos 1920, com vocabulário próximo do inglês contemporâneo que domina os corpora de treinamento, em domínio público nos Estados Unidos e no Brasil (candidatos: F. Scott Fitzgerald, morto em 1940; Sinclair Lewis, 1951; Willa Cather, 1947; obras de 1922 a 1925; verificação de domínio público nas duas jurisdições registrada na proveniência). Mesma faixa de tamanho. A escolha de prosa literária da mesma década controla registro e época: a comparação de H6 é língua contra língua, não romance contra enciclopédia.

**Preparação ortográfica versionada.** Verificação nossa mostrou que a transcrição do Wikisource já usa ortografia atualizada (zero formas arcaicas nos 19 contos), preservando as grafias que representam oralidade regional ("pra", "inda", "vancê"): as sementes regionais entram como estão, e a atualização supradialetal é da transcrição-fonte. As regras explícitas de modernização, uma a uma e congeladas por hash, aplicam-se aos controles em português vindos do Gutenberg com grafia de época (tabela completa em `corpus-semente/proveniencia.md`), com os originais preservados; sem isso, os grupos entrariam no experimento com roupas ortográficas diferentes. As sementes inglesas dos anos 1920 já usam ortografia atual. **Braço de sensibilidade ortográfica:** duas sementes regionais (as duas mais densas: "Jogo do osso" e "Trezentas onças") rodarão também em versão com a grafia original de 1912, transcrita por nós do fac-símile da primeira edição (arquivo `Contos gauchescos (1912).djvu` no Wikimedia Commons, digitalização Google Books do exemplar da Universidade da Califórnia), com verificação automática de que o diff contra a versão modernizada só toca ortografia, nunca vocabulário.

**Viés reconhecido:** as sementes regionais vêm de um único autor e de um registro literário de época. Isso dá controle (léxico verificável em glossários publicados) ao custo de generalização: as conclusões valerão para este autor e registro, com extensão a textos contemporâneos anotada na seção 11.

## 6. Prompts

As instruções, congeladas antes da coleta (o arquivo `prompts.py` guardará as strings exatas e seus hashes). Em português, para as sementes em português:

**C1, neutra:**

```
Reescreva o texto abaixo. O texto reescrito deve ter aproximadamente o mesmo número de palavras do texto original. Responda somente com o texto reescrito, sem comentários.

TEXTO:
{texto}
```

**C2, melhoria (o uso escolar típico):**

```
Reescreva o texto abaixo melhorando a clareza e a qualidade da escrita. O texto reescrito deve ter aproximadamente o mesmo número de palavras do texto original. Responda somente com o texto reescrito, sem comentários.

TEXTO:
{texto}
```

**C3, preservação (a defesa explícita):**

```
Reescreva o texto abaixo melhorando a clareza e a qualidade da escrita, preservando o estilo e o vocabulário regional do texto original. O texto reescrito deve ter aproximadamente o mesmo número de palavras do texto original. Responda somente com o texto reescrito, sem comentários.

TEXTO:
{texto}
```

Em inglês, para as sementes em inglês (C1 e C2, traduções diretas):

```
Rewrite the text below. The rewritten text should have approximately the same number of words as the original. Respond only with the rewritten text, without comments.

TEXT:
{texto}
```

```
Rewrite the text below improving the clarity and the quality of the writing. The rewritten text should have approximately the same number of words as the original. Respond only with the rewritten text, without comments.

TEXT:
{texto}
```

A instrução é uma linha única; a única quebra de linha do prompt é a que separa a instrução do bloco TEXTO.

Racional do desenho: C2 reproduz o pedido mais comum do uso real ("melhora esse texto"); C1 isola o que a simples reescrita já faz, sem a pressão da melhoria; C3 testa a defesa disponível ao usuário. A comparação C2 contra C1 estima o custo da melhoria; C3 contra C2, o valor da instrução de preservação; o par inglês contra português, com instruções equivalentes, o peso da língua.

A cláusula de comprimento cumpre três funções: remove na origem o principal confundimento do desfecho (texto que encurta mata palavra por matemática, não por escolha lexical), torna as distribuições de vocabulário comparáveis entre gerações sem reponderação, e estabiliza o custo da coleta. O preço reconhecido: o pedido real raramente fixa tamanho, então as condições ficam um passo mais artificiais; os modelos obedecem só aproximadamente, e o comprimento efetivo será registrado por geração e mantido como covariável.

Invariantes: sem prompt de sistema; instrução idêntica em todas as gerações da cadeia; instrução na língua da semente; sem exemplos; `{texto}` é substituído pela geração anterior, sem cabeçalho adicional.

## 7. Protocolo de coleta

- **Modelos e acesso:** os cinco modelos do Experimento 2, pelos mesmos backends (OpenRouter e Maritaca). No OpenRouter, o roteamento será fixado (`provider.allow_fallbacks: false`, com `provider.order` quando preciso), porque o mesmo alias pode rotear para provedores com decodificação e quantização distintas. O `model` e o `provider` retornados serão gravados por chamada; se o provedor fixado deixar de existir no meio de uma cadeia, a cadeia é encerrada ali com censura (continuar em outro provedor mudaria o objeto medido).
- **Decodificação explícita:** temperatura e top-p serão enviados explicitamente, com os valores documentados como padrão de cada modelo (APIs não devolvem parâmetros que não foram enviados, então "usar o padrão sem enviar" seria irregistrável). A escolha do padrão do provedor é deliberada: temperatura zero truncaria caudas por conta própria (Dohmatob et al., 2024) e superestimaria o efeito. `max_tokens` = 4096, folga ampla sobre a maior semente (~500 tokens): saída truncada no meio da frase contaminaria todas as gerações seguintes. O `finish_reason` será gravado por chamada; `length` é anomalia: uma nova tentativa e, na segunda, cadeia encerrada ali, com censura.
- **Teto de gasto no código:** o coletor manterá uma estimativa acumulada de custo (tokens × preço por modelo, tabela registrada no script) com dois tetos: **US$ 18 no total** e **R$ 30 no backend da Maritaca** (o saldo disponível é R$ 39,61; preços vigentes do Sabiá-4: R$ 5/M entrada, R$ 20/M saída, projeção ≈ R$ 8 com o braço em inglês). Se a projeção feita a partir do piloto exceder qualquer teto, o desenho inteiro será reduzido proporcionalmente (primeiro em gerações, depois em sementes), mantendo os cinco modelos com o mesmo número de chamadas, e este documento será atualizado antes da coleta. Atingido um teto durante a coleta, a interrupção é ordenada; a coleta pode ser retomada depois de novo aporte, sem censura, ou encerrada em definitivo, com censura.
- **Falha transitória pausa, não mata:** erros de infraestrutura (429, 5xx, timeout, saldo esgotado) recebem backoff exponencial e, se persistirem, pausam a cadeia para retomada posterior do ponto exato, com data-hora registrada; nenhuma censura decorre disso (seção 4). Anomalias de conteúdo (saída vazia, recusa) têm uma única nova tentativa; na segunda, a cadeia é encerrada naquela geração, com censura. Recusas são dado, não defeito: ficam no registro, como no Experimento 2.
- **Registro:** um JSONL de auditoria por cadeia, uma linha por chamada, com data-hora, identificador de modelo e provedor retornados, parâmetros enviados, `finish_reason`, hash da instrução, texto de entrada, texto de saída bruto, texto pós-filtro e contagem de tokens. O estado da cadeia permite retomar coletas interrompidas sem repetir chamadas.
- **Filtro de moldura:** preâmbulos ("Aqui está o texto...", "Here is the text...") e posfácios serão removidos por heurística estrutural (linha curta nas bordas com vocabulário metalinguístico, cercas de código, aspas envolventes), com cada remoção registrada e a regra versionada por hash. O bruto fica no JSONL, então o filtro é reprocessável. No piloto e em todas as G1 da coleta completa, o filtro será auditado manualmente antes de prosseguir.
- **Piloto:** 1 modelo × 3 condições × 3 sementes (1 regional + 1 controle pt + 1 controle en, esta só em C1 e C2) × 5 gerações, para validar pipeline, filtro, preços por token e a calibração do critério de falseamento (seção 3). O piloto fica separado dos dados definitivos.
- **Publicação responsável:** antes de publicar as ~4.200 saídas brutas, uma triagem leve (lista de termos + leitura dos casos sinalizados) anotará, sem apagar, conteúdo potencialmente ofensivo, com nota no README; os termos de redistribuição de saídas dos provedores serão conferidos e registrados aqui.

## 8. Métricas

**Lista de regionalismos, estratificada.** De 60 a 100 itens lexicais com marca diatópica sulista, construída a partir das sementes e estratificada em dois tipos, reportados separadamente: **realia** (referentes sem sinônimo padrão corrente: chimarrão, bombacha, minuano) e **itens com variante padrão concorrente** (guri/menino, china/moça, peleia/briga, querência/terra natal). A distinção importa porque realia tende a sobreviver por necessidade referencial; o segundo tipo é onde a escolha entre variante regional e padrão de fato aparece. Cada item terá lema, variantes ortográficas e flexões, classe gramatical, marca "também arcaísmo (sim/não)" e a fonte que atesta a marca diatópica (dicionário nomeado com marca regional; atlas e projetos de variação, como ALiB e VARSUL, quando aplicável), em `lista-regionalismos.csv`. Dois anotadores classificarão os itens, com concordância reportada. A lista será congelada por hash antes da coleta.

**Controles pareados, mesmo pipeline.** Para cada regionalismo, uma palavra não regional presente nas mesmas sementes, pareada primariamente pela frequência dentro do próprio corpus-semente, com classe gramatical e comprimento como covariáveis de pareamento (frequência de corpus geral, via `wordfreq`, apenas como conferência secundária: ela funde variedades do português e mede dispersão global, não concentração diatópica). Os controles recebem exatamente o mesmo tratamento dos regionalismos: lema, variantes curadas à mão e detecção pelo mesmo código, para não inflar a sobrevivência de um grupo por artefato de pipeline. Registro em `lista-controle-pareado.csv`, congelado junto.

**Regra de morte e reaparição.** Um item está ausente numa geração se nenhum lema ou variante casa com o texto normalizado. A morte é definida por regra de absorção explícita: ausência por *k* gerações consecutivas, com *k* = 3 na análise principal e sensibilidade reportada para *k* = 2 e *k* = 5. Reaparições após a morte são contadas e reportadas como estatística própria. Cadeia encerrada antes da G20 gera censura à direita, nunca morte.

**Massa da cauda, a métrica comparável entre línguas (insumo de H6).** Distribuições de raridade não se comparam diretamente entre línguas (tokenização e referenciais de frequência diferentes). A métrica adimensional: na G0 de cada língua, define-se o limiar de cauda como o percentil 80 da raridade dos tokens daquela língua; a massa da cauda de uma geração é a fração dos seus tokens acima desse limiar fixo; o desfecho de H6 é a redução proporcional dessa massa entre G0 e G20, comparada entre o grupo regional português e o grupo padrão inglês (e, como referência interna, o padrão português). Referenciais de frequência: o próprio corpus-semente complementado por `wordfreq` na língua correspondente, congelados antes da coleta.

**Colapso de comprimento.** Cadeia cujo texto cai abaixo de 50 palavras é marcada como colapsada: as métricas de diversidade ficam indefinidas dali em diante (NA) e o colapso em si vira desfecho reportado, com a geração em que ocorreu. Com a cláusula de comprimento no prompt, esse desfecho também mede desobediência à instrução.

**Secundárias, por geração e cadeia:**

- diversidade lexical: MATTR (janela de 50 palavras) e MTLD;
- distinct-1/2/3 e contagem de hapax legomena;
- comprimento em palavras (checagem da cláusula de comprimento e covariável);
- razão de compressão gzip como proxy de homogeneização, sempre reportada com o comprimento ao lado (confundimento conhecido; Shaib et al., 2024);
- similaridade semântica por embeddings multilíngues (`paraphrase-multilingual-mpnet-base-v2` com `max_seq_length` elevado a 512; para textos maiores, média de janelas de ~100 palavras; procedimento registrado): (a) de cada geração com a semente da própria cadeia, medindo deriva; (b) par a par entre cadeias de sementes diferentes na mesma geração e condição, para H5, sempre em contraste com a linha de base das sementes-controle;
- **raridade lexical por token e surpresal** (insumos das figuras; seção 9): para cada token do texto, a raridade s = −log₁₀ da frequência da palavra no referencial fixo da língua; e, por frase, a surpresal média sob um modelo-âncora aberto e fixo rodado localmente, no espírito da figura de caudas de Dohmatob et al. (2024).

## 9. Análise e figuras planejadas

**Inferência primária:** modelo de sobrevivência com efeitos aleatórios cruzados por item, por semente e por modelo, sobre o diferencial regional−controle. Mortes de itens dentro da mesma cadeia não são independentes; tratá-las como se fossem multiplicaria o *n* artificialmente. O bootstrap sobre sementes permanece como apresentação descritiva dos intervalos, com a ressalva de que as sementes vêm de um único autor.

**A curva com a cauda encolhendo (resposta à pergunta "como mostrar uma curva se o dado é categórico").** A presença de uma palavra é categórica, mas cada palavra tem uma raridade contínua. Pontuando cada token do texto com s = −log₁₀ da sua frequência no referencial fixo, o texto de uma geração vira uma nuvem de raridades, e a densidade dessa nuvem é uma curva: em G0 ela tem cauda direita pesada (palavras raras, os regionalismos entre elas); se a hipótese estiver certa, a cauda esvazia geração a geração e a curva estreita em torno do vocabulário comum. Como a cláusula de comprimento mantém o número de tokens aproximadamente constante, as densidades são comparáveis entre gerações sem reponderação.

**Figuras:**

- **F1 (manchete): densidade da raridade lexical por geração.** Curvas sobrepostas de G0, G5, G10 e G20 (agregadas por condição), com gradiente de cor e, na base, marcas tipo tapete na posição de cada regionalismo, acesas enquanto ele vive e apagadas quando morre. É a figura da cauda sumindo, no formato contínuo que a hipótese pede. Nota de leitura: esta distribuição tem uma cauda de interesse (a direita, das palavras raras); a esquerda são as palavras gramaticais de que todo texto precisa, e não esvazia.
- **F1b (o sino que estreita): distribuição entre cadeias de um escore contínuo por texto.** Cada cadeia vira um ponto por geração (por exemplo, a raridade média do seu texto); a densidade desses pontos é uma curva em formato de sino que estreita com as gerações: é a variância da população de textos encolhendo, o análogo empírico direto da curva normal perdendo as caudas usada no artigo e nos slides.
- **F2 (companheira rigorosa): densidade da surpresal por geração**, sob o modelo-âncora fixo, espelhando a figura de caudas truncadas de Dohmatob et al. (2024) com dados próprios.
- **F3 (a figura que decide H1–H4):** o diferencial regional−controle × geração, por condição, com intervalos.
- **F4:** curvas de sobrevivência (fração viva × geração) por condição e modelo, regionalismos e controles sobrepostos, estratos realia e variante-concorrente separados.
- **F5:** convergência entre cadeias × geração, sementes regionais contra a linha de base das sementes-controle.
- **F6:** painel qualitativo com o mesmo trecho em G0, G10 e G20, regionalismos destacados.
- **F7 (a régua da vantagem de casa, decide H6):** redução proporcional da massa da cauda entre G0 e G20, barras por grupo (regional pt, padrão pt, padrão en) e condição, com as curvas de massa da cauda × geração ao lado.
- **T1:** tabela-obituário: geração mediana de morte por item, com estrato e condição ("chimarrão sobrevive até a geração x; guaiaca morre na geração y").

Comparações entre modelos são secundárias: os parâmetros padrão diferem entre provedores, e a comparação primária é sempre dentro do mesmo modelo, entre condições.

## 10. Custo e duração estimados

Aritmética por chamada, já com a cláusula de comprimento (textos de ~200 palavras ≈ 300 tokens): instrução (~70 tokens) + entrada (~310) + saída (~300) ≈ 680 tokens. Com 4.800 chamadas firmes (núcleo + grafia 1912), o total fica em torno de 3,3 milhões de tokens; a estimativa central fica **entre US$ 14 e 19**, com os tetos duros da seção 7 (US$ 18 total; R$ 30 na Maritaca, projeção ≈ R$ 9) governando: o braço de calibração (540 chamadas) entra somente se a projeção do piloto mantiver tudo sob os tetos, e a regra de redução proporcional cobre o caso de os preços virem acima do estimado. O piloto, que custa centavos, confirma os preços por token antes da coleta completa; se a projeção estourar um teto, vale a regra de redução proporcional da seção 7. As 210 cadeias são paralelizáveis; cada uma tem 20 chamadas sequenciais. Com limites de taxa respeitados, a coleta completa cabe em poucas horas de execução; preparação do corpus e das listas em um ou dois dias de trabalho; métricas e figuras em outro. O modelo-âncora da surpresal roda localmente, sem custo de API.

## 11. Limitações e extensões anotadas

- Cadeias por inferência não são retreino; a analogia com o colapso de treinamento é conceitual e será sinalizada no texto.
- O escopo das conclusões é este autor e este registro; a extensão com textos regionais contemporâneos (crônicas, transcrições de fala) e com outra variedade (espanhol rioplatense como espelho) fica anotada para rodada futura.
- O braço em inglês usa texto padrão, não regional; um braço com inglês dialetal (escocês, sulista americano) completaria o quadrado língua × marcação e fica anotado como extensão.
- O pareamento por frequência aproxima, sem isolar, a separação entre raridade e marca cultural; a estratificação realia/variante-concorrente reduz a ambiguidade restante.
- A cláusula de comprimento fixa uma condição que o uso real não fixa; o ganho de controle foi julgado maior que a perda de realismo, e a limitação será declarada.
- Sem réplicas por célula no desenho principal (variabilidade tratada pelos efeitos aleatórios; braço de calibração opcional na decisão em aberto nº 3).
- Os modelos são alvos móveis: identificadores, provedores e datas registrados, sem promessa de replicabilidade bit a bit; retomadas com intervalo longo ficam auditáveis pelo registro de data-hora.
- A lista de regionalismos tem juízo humano na curadoria; congelamento por hash, fonte diatópica por item e dupla anotação com concordância reduzem, sem eliminar, o arbítrio.

## 12. Estrutura planejada da pasta

```
artigo/telefone-sem-fio/
├── README.md                     # resumo e status
├── plano-experimental.md         # este documento
├── prompts.py                    # strings congeladas das condições (pt e en)
├── corpus-semente/               # 9 sementes regionais + 3 controles pt + 3 controles en + proveniencia.md
├── lista-regionalismos.csv       # itens, lemas, variantes, estrato, fonte (congelada por hash)
├── lista-controle-pareado.csv    # controles pareados, mesmo esquema
├── rodar-cadeias.py              # coleta com retomada, backoff, tetos de gasto e auditoria JSONL
├── medir-metricas.py             # métricas da seção 8
├── gerar-figuras.py              # figuras da seção 9
└── dados/cadeias/                # um JSONL por cadeia (publicados brutos, com triagem anotada)
```

## 13. Decisões tomadas com o autor (18 de julho de 2026)

1. **Profundidade: 20 gerações fixas.** Sem extensão automática para 30, mesmo com folga no piloto.
2. **C3 nos cinco modelos.** Desenho fatorial completo em português.
3. **Braço de calibração: sim, condicional aos tetos.** Três réplicas de 1 modelo × 3 condições × 3 sementes × 20 gerações (540 chamadas); entra apenas se a projeção do piloto mantiver o total sob os tetos.
4. **Modelos: os mesmos cinco do Experimento 2.** Continuidade narrativa entre os três experimentos.
5. **Grafia 1912: teste completo.** Duas sementes transcritas do fac-símile rodam também com a grafia original (600 chamadas extras); ver seção 5.
6. **Modelo-âncora da surpresal: modelo pequeno multilíngue da família Qwen** (~1–2B, base), rodando localmente; identificador exato e revisão congelados em `proveniencia.md` antes da coleta.
7. **Obras do braço em inglês confirmadas:** Fitzgerald (1925), Lewis (1922), Cather (1923).
8. **Curadoria das listas:** o anotador 1 (Claude) enxuga a lista de 184 para ~80 itens com marca diatópica clara e estratos equilibrados; o autor veta ou reclassifica pontualmente; congela-se por hash em seguida.

## 14. Referências

- Dohmatob, E. et al. (2024). A tale of tails: model collapse as a change of scaling laws. *ICML 2024* (PMLR v235). arXiv:2402.07043.
- Guo, Y. et al. (2024). The curious decline of linguistic diversity: training language models on synthetic text. *Findings of NAACL 2024*. arXiv:2311.09807.
- Padmakumar, V.; He, H. (2024). Does writing with language models reduce content diversity? *ICLR 2024*. arXiv:2309.05196.
- Perez, J. et al. (2024). When LLMs play the telephone game: cumulative changes and attractors in iterated cultural transmissions. arXiv:2407.04503.
- Shaib, C. et al. (2024). Standardizing the measurement of text diversity. arXiv:2403.00553.
- Shumailov, I. et al. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755–759.
- Simões Lopes Neto, J. (1912). *Contos Gauchescos*. Pelotas. (Domínio público.)
- Touvron, H. et al. (2023). Llama 2: open foundation and fine-tuned chat models. arXiv:2307.09288 (Tabela 10: composição de línguas).
