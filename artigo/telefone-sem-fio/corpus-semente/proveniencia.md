# Proveniência do corpus-semente

**18 de julho de 2026 · status: rascunho, aguardando revisão do segundo anotador.**
O congelamento por hash (plano, seções 5 e 8) será registrado aqui após essa revisão.

## Fontes

| Grupo | Obra | Fonte | Domínio público |
|---|---|---|---|
| Regional (9) | *Contos gauchescos*, J. Simões Lopes Neto, Pelotas: Echenique & C., 1912 | [Wikisource pt, "Contos gauchescos (1912)"](https://pt.wikisource.org/wiki/Contos_gauchescos_(1912)) | autor † 1916 (Brasil: vida+70); publicação < 1930 (EUA) |
| Controle pt (2) | *Triste Fim de Polycarpo Quaresma*, Lima Barreto, 1911 | [Gutenberg #67535](https://www.gutenberg.org/ebooks/67535) | autor † 1922; publicação 1911 |
| Controle pt (1) | *Memorial de Ayres*, Machado de Assis, 1908 | [Gutenberg #55797](https://www.gutenberg.org/ebooks/55797) | autor † 1908; publicação 1908 |
| Controle en (1) | *The Great Gatsby*, F. Scott Fitzgerald, 1925 | [Gutenberg #64317](https://www.gutenberg.org/ebooks/64317) | autor † 1940; publicação 1925 (EUA: DP desde 2021) |
| Controle en (1) | *Babbitt*, Sinclair Lewis, 1922 | [Gutenberg #1156](https://www.gutenberg.org/ebooks/1156) | autor † 1951; publicação 1922 (EUA: DP desde 2018) |
| Controle en (1) | *A Lost Lady*, Willa Cather, 1923 | [Gutenberg #65636](https://www.gutenberg.org/ebooks/65636) | autora † 1947; publicação 1923 (EUA: DP desde 2019) |

Nota sobre a transcrição do Wikisource: a edição de referência é a de 1912, mas a
transcrição usa **ortografia atualizada**, preservando as grafias que representam
oralidade regional ("vancê", "inda", "pra"). Verificação nossa: zero ocorrências de
formas arcaicas ("elle", "aquella", "commigo" etc.) nos 19 contos baixados. Por isso
as sementes regionais foram usadas **sem modernização nossa**; a atualização
supradialetal foi feita pela transcrição-fonte. A grafia original de 1912 está
disponível no fac-símile que respalda essa transcrição (seção "Grafia 1912"
abaixo), e a conferência contra o fac-símile revelou **três erros de palavra na
camada do Wikisource**, corrigidos nas nossas sementes (lista na mesma seção).

## Seleção das sementes regionais

Doze contos candidatos foram processados (um agente de leitura por conto), cada um
propondo o melhor trecho de 150–250 palavras, verbatim e contíguo, com máximo de
léxico regional e fecho natural. Todos os trechos foram verificados
programaticamente como substrings exatas dos arquivos-fonte. Ranque por
regionalismos distintos verificados no trecho:

| Conto | Regionalismos | Palavras | Decisão |
|---|---:|---:|---|
| Jogo do osso | 29 | 256→204¹ | semente 04 |
| Trezentas onças | 27 | 236 | semente 09 |
| Os cabelos da china | 25 | 252→247¹ | semente 07 |
| Correr eguada | 23 | 202 | semente 03 |
| Penar de velhos | 22 | 232 | semente 08 |
| O negro Bonifácio | 18 | 246 | semente 06 |
| No manantial | 18 | 172 | semente 05 |
| Contrabandista | 18 | 214 | semente 02 |
| Chasque do Imperador | 18 | 247 | semente 01 |
| Melancia — coco verde | 18 | 243 | descartado (empate; menor autocontenção) |
| Batendo orelha | 17 | 194 | descartado |
| O boi velho | 15 | 252 | descartado |

¹ Aparado no fim de frase, por fatiamento (sem reformatação interna), para caber no
teto de 250 palavras do plano; o corte está registrado no histórico desta pasta.

## Controles em português: modernização por tabela explícita

Os trechos de Lima Barreto e Machado vieram do Gutenberg com a grafia da época
(581 formas arcaicas no romance de 1911). Para não criar assimetria com as
sementes regionais (já modernizadas pela fonte), os três controles pt foram
modernizados por substituições explícitas, palavra a palavra, aplicadas por
`montar_corpus.py` (regra = par exato, com variante capitalizada automática):

hábito(s), Policarpo, às, anos, Saindo, frutas, francesa, forma, aí, pisar,
exatamente, aparição, eclipse, enfim, fenômeno, matematicamente, à, há, quase,
própria, burocráticos, subsecretário, pretensão, caráter, mínima, aquela, delas,
ele, despesas, coisa, letra, contrário, acrescentava, malícia, armazéns,
abundância, Ismênia, ela, também, estranha, gentilíssima, Quis, além, ali,
espiá-la, distância, Entramos, enfiamos, apresentou, viúva, Andaraí,
esperássemos; "em quanto"→"enquanto"; pontuação: «»→aspas curvas, "--"→travessão.

Os trechos **originais, sem modernização**, estão preservados em
[`originais/`](originais/). Os controles em inglês (anos 1920) já usam ortografia
atual e não foram alterados. Nenhuma outra edição foi feita em nenhum trecho.

## Grafia 1912: transcrição diplomática do fac-símile

O braço de sensibilidade ortográfica (plano, seções 4–5 e decisão nº 5) usa duas
sementes na grafia original, transcritas do fac-símile da primeira edição:
arquivo [`Contos gauchescos (1912).djvu`](https://commons.wikimedia.org/wiki/File:Contos_gauchescos_(1912).djvu)
no Wikimedia Commons (digitalização Google Books do exemplar da Universidade da
Califórnia, 228 páginas), páginas do livro 13–14 ("Trezentas onças") e 170–171
("Jogo do osso").

**Critério (transcrição diplomática):** grafia e pontuação como impressas,
inclusive espaço tipográfico antes de "!" e "?" e as formas "E'", "Tópo", "doña";
hifenização de fim de linha desfeita; quebras de parágrafo preservadas.
Transcrição feita por leitura direta das imagens ampliadas (não por OCR), com
verificação automática de que o diff contra a versão modernizada contém apenas
substituições ortográficas 1-para-1 (15 em "Jogo do osso", 20 em "Trezentas
onças") e uma única anomalia registrada: "fui-me à água" (moderna) corresponde a
"fui me á agua" (1912, sem hífen). Leituras com ressalva, a conferir pelo autor
no fac-símile: "solíto" (acento agudo aparente no impresso) e "ali" (mancha
tipográfica sobre o "i").

**Erros da camada Wikisource detectados na conferência e corrigidos nas sementes
modernas** (a fonte impressa prevalece sobre a transcrição):

| Onde | Wikisource | Fac-símile 1912 |
|---|---|---|
| regional-04 | "Nesse dia **Unha** vindo" | "Nesse dia **tinha** vindo" |
| regional-04 | "O **mano** contra a Lalica" | "O **ruano** contra a Lalica" |
| regional-04 | "valeu? Topo!" (fala fundida) | "—Jogo-te o tostado, aperado, valeu ?" / "—Tópo !" (dois turnos) |
| regional-04 | "E culo!..." (sem travessão) | "— E culo !..." (novo turno) |
| regional-09 | "**dava-me** para acompanhar-me" | "**dava-lhe** para acompanhar-me" |

## Responsabilidade textual (transcritores e versionistas)

Cada camada textual usada tem responsável nomeado:

- ***Contos gauchescos* (transcrição e atualização ortográfica):** comunidade do
  Wikisource em português (edição colaborativa; responsáveis por página no
  [histórico da edição](https://pt.wikisource.org/w/index.php?title=Contos_gauchescos_(1912)&action=history)
  e nos históricos das subpáginas). Acesso em 18 jul. 2026.
- ***Contos gauchescos* (grafia original, 2 sementes):** transcrição diplomática
  do fac-símile por Claude (Anthropic), assistente do projeto, com leitura em
  imagem ampliada; revisão do autor (R. S. Guerra) pendente e registrada quando
  ocorrer.
- ***Triste Fim de Polycarpo Quaresma*:** transcrição de Laura Natal Rodrigues
  (Free Literature), sobre imagens da Biblioteca Nacional do Brasil (crédito do
  cabeçalho do Gutenberg #67535).
- ***Memorial de Ayres*:** transcrição de Laura Natal Rodriguez e Marc D'Hooghe
  (Free Literature) (Gutenberg #55797).
- ***The Great Gatsby*:** produção de Alex Cabal (Standard Ebooks), sobre
  transcrição do Project Gutenberg Australia (Gutenberg #64317).
- ***Babbitt*:** produção original de Charles Keller e David Widger, renovada por
  Chuck Greif e a equipe PG Online Distributed Proofreading (Gutenberg #1156).
- ***A Lost Lady*:** transcrição de Laura Natal Rodrigues (Free Literature), sobre
  imagens da HathiTrust Digital Library (Gutenberg #65636).
- **Atualização ortográfica dos controles em português:** regras explícitas
  (tabela acima) aplicadas por Claude (Anthropic); conferência do autor pendente.

## Congelamento do pré-registro (18 de julho de 2026)

**Método da lista, como executado.** A dupla anotação humana prevista no plano foi
substituída, por decisão do autor, por: anotação do anotador 1 (Claude) +
verificação lexicográfica em duas camadas com fonte nomeada por item: (1)
dicionários gerais online com marca diatópica (Michaelis "Reg (RS)/(S.)", Aulete,
Priberam); (2) para itens sem marca nos gerais, léxicos gauchescos especializados
(Romaguera Corrêa, *Vocabulário Sul Rio-Grandense*, 1898; Callage, *Vocabulário
Gaúcho*, 1926; Schlee, *Dicionário da Cultura Pampeana Sul-Rio-Grandense*, 2019;
glossário das obras de Simões Lopes Neto rev. Aurélio Buarque de Holanda). Cada
item registra o nível de evidência na coluna `nivel_evidencia`; análise de
sensibilidade restrita ao nível 1 fica prevista. Resultado: **90 lexemas** (68
nível 1, 22 nível 2) e 17 expressões descritivas; 8 itens mantidos com bandeira
de homografia parcial (conferência manual de contexto na medição): apurado, baio,
boliche, carona, gambeta, mate, pampa, traíra. Único item rechecado sem atestação
em nenhuma camada: "mui" (marca de oralidade, não diatópica), cortado.

**Hashes congelados (SHA-256, prefixo 16):**

```
433c73e008c5dcdb  lista-regionalismos.csv
8eeda220c7546d2a  lista-controle-pareado.csv
a455e650ee55ccf8  prompts.py
```

Hashes completos dos prompts individuais: pt-C1 03f3fcd7…, pt-C2 13007f21…,
pt-C3 ff40dfeb…, en-C1 4b5c12c8…, en-C2 ce3f522e… (íntegros em `prompts.py`,
que os imprime ao ser executado). Os hashes das 15 sementes e das 2 versões em
grafia de 1912 são os da seção seguinte, que deixa de ser rascunho e passa a
valer como registro congelado.

## Hashes (SHA-256, prefixo 16) — congelados em 18 jul. 2026

```
2dde6abab1b74085  controle-en-01-gatsby.txt
79a880d822fcce2b  controle-en-02-babbitt.txt
8810bb3a20b4d864  controle-en-03-lost-lady.txt
23a9404d282dee95  controle-pt-01-policarpo-abertura.txt
1aa25af4c7b518a7  controle-pt-02-policarpo-albernaz.txt
15be3d50612ae540  controle-pt-03-memorial-ayres.txt
e83d3c016df8972c  grafia-1912/regional-04-jogo-do-osso-1912.txt
104386b0677f4c19  grafia-1912/regional-09-trezentas-oncas-1912.txt
b26e2435517c0994  regional-01-chasque-do-imperador.txt
e248c745a54a80bb  regional-02-contrabandista.txt
b3798a24747291b6  regional-03-correr-eguada.txt
c42a09d1bad7d4e6  regional-04-jogo-do-osso.txt
84259b64cc10a810  regional-05-no-manantial.txt
933e1299d2d90601  regional-06-o-negro-bonifacio.txt
cb4dd99942dce988  regional-07-os-cabelos-da-china.txt
e868cc435d93ed6d  regional-08-penar-de-velhos.txt
6c4b5d135824f98d  regional-09-trezentas-oncas.txt
```

## Listas (rascunhos do anotador 1)

- [`../lista-regionalismos.csv`](../lista-regionalismos.csv): 184 itens distintos
  extraídos das 9 sementes, com glosa, classe (lexema/expressão), estrato proposto
  (realia / variante-concorrente) e fonte diatópica candidata. A curadoria do
  segundo anotador deve reduzir a lista para os 60–100 itens mais claros do plano,
  privilegiando marca diatópica atestável em dicionário.
- [`../lista-controle-pareado.csv`](../lista-controle-pareado.csv): 162 pares
  propostos automaticamente por frequência no próprio corpus-semente (empate
  desfeito por comprimento e ordem alfabética); curadoria pendente. Expressões
  multipalavra não recebem par e ficam fora do diferencial primário (descritivas).
