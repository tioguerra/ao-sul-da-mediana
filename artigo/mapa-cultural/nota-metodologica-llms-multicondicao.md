# Nota metodológica — cinco LLMs em quatro condições linguístico-culturais

## Resultado principal

Em 13 de julho de 2026, cinco modelos foram submetidos às dez perguntas do Integrated Values Surveys usadas por Tao et al. (2024), sob dez formulações do descritor do respondente e quatro condições:

1. perguntas e descritores em inglês, sem identidade nacional;
2. perguntas e descritores em português brasileiro, sem identidade nacional;
3. português brasileiro com identidade brasileira explícita;
4. português brasileiro com identidade gaúcha e residência no Rio Grande do Sul explícitas.

O desenho completo contém **2.000 respostas observadas**: 5 modelos × 4 condições × 10 formulações × 10 perguntas. Dessas, **1.989 foram pontuadas**. Onze respostas do Gemini 3.5 Flash foram preservadas como não pontuáveis, sem imputação.

![Mapa cultural multilíngue com cinco LLMs](figura-mapa-cultural-llms-multicondicao.png)

### Coordenadas centrais

Cada ponto central resulta da projeção das médias de cada uma das dez perguntas entre as formulações válidas. O primeiro número é o eixo sobrevivência–autoexpressão; o segundo, o eixo tradicional–secular-racional.

| Modelo | Inglês | Português | Prompt Brasil | Prompt RS | Respostas pontuadas |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sabiá-4 | (1,061; 0,849) | (1,561; −0,578) | (1,244; −0,808) | (1,782; −1,803) | 400/400 |
| Claude Sonnet 5 | (1,301; −0,410) | (1,484; 0,405) | (0,714; −0,412) | (0,709; −1,027) | 400/400 |
| GPT-5.6 Terra | (2,213; 1,806) | (1,984; 2,020) | (1,161; 0,760) | (1,225; 0,288) | 400/400 |
| Gemini 3.5 Flash | (2,381; 1,015) | (2,084; 0,583) | (1,567; −0,165) | (1,442; −0,365) | 389/400 |
| Grok 4.5 | (2,062; 0,900) | (2,195; 0,630) | (0,229; −0,984) | (0,521; −0,526) | 400/400 |

Os pontos humanos de referência são Brasil **(−0,037; −0,376)**, Argentina **(0,628; −0,320)**, Uruguai **(1,184; −0,434)** e Rio Grande do Sul **(0,266; 0,398)**. Os três primeiros reproduzem médias nacionais de Tao et al.; o último é uma estimativa exploratória da subamostra gaúcha do WVS 2018, com 118 casos completos.

## Efeitos observados

Para isolar o efeito da identidade cultural do efeito do idioma, a comparação principal usa a condição em português sem identidade como linha de base. Valores positivos na última coluna de cada alvo indicam redução da distância; valores negativos indicam afastamento.

| Modelo | Deslocamento inglês→português | Distância ao Brasil: português→prompt Brasil | Mudança relativa | Distância ao RS: português→prompt RS | Mudança relativa |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sabiá-4 | 1,513 | 1,610 → 1,351 | +16,1% | 1,622 → 2,673 | **−64,8%** |
| Claude Sonnet 5 | 0,835 | 1,710 → 0,752 | +56,0% | 1,218 → 1,492 | **−22,5%** |
| GPT-5.6 Terra | 0,313 | 3,135 → 1,651 | +47,3% | 2,363 → 0,966 | +59,1% |
| Gemini 3.5 Flash | 0,524 | 2,327 → 1,618 | +30,5% | 1,827 → 1,402 | +23,3% |
| Grok 4.5 | 0,301 | 2,448 → 0,663 | +72,9% | 1,943 → 0,958 | +50,7% |

Quatro resultados são diretamente úteis ao position paper:

1. **O idioma alterou todos os modelos, mas sem direção comum.** O deslocamento inglês→português variou de 0,301 no Grok a 1,513 no Sabiá. No Sabiá, a mudança ocorreu sobretudo no eixo tradicional–secular; no Claude, o mesmo eixo mudou no sentido oposto.
2. **Português não equivale a identidade brasileira.** A simples tradução para português quase não mudou a distância ao Brasil no Sabiá, Terra e Grok; aproximou o Gemini e afastou o Claude.
3. **O prompt brasileiro aproximou os cinco modelos do Brasil, mas não os fez coincidir com a população humana.** A redução relativa variou de 16,1% a 72,9%. Os pontos condicionados mais próximos foram Grok (distância 0,663) e Claude (0,752).
4. **O prompt gaúcho não produziu alinhamento uniforme.** Terra, Gemini e Grok se aproximaram do ponto humano do RS; Sabiá e Claude se afastaram. O Sabiá deslocou-se fortemente para a direção tradicional, chegando a distância 2,673 do RS. Portanto, uma persona regional pode ativar um estereótipo ou combinação de valores diferente da média observada na amostra humana.

Esses resultados não medem a “cultura” interna de um modelo. Eles mostram que **idioma, identidade solicitada e pequenas variações de formulação alteram sistematicamente as respostas que seriam usadas para representar um respondente médio**. A falta de convergência uniforme ao alvo humano é compatível com a tese de que prompting cultural não é uma correção garantida.

## Protocolo experimental

### Modelos e rotas

| Rótulo | Identificador solicitado | Endpoint | Provedor informado na resposta |
| --- | --- | --- | --- |
| Claude Sonnet 5 | `anthropic/claude-sonnet-5` | OpenRouter | Amazon Bedrock |
| GPT-5.6 Terra | `openai/gpt-5.6-terra` | OpenRouter | OpenAI |
| Gemini 3.5 Flash | `google/gemini-3.5-flash` | OpenRouter | Google |
| Grok 4.5 | `x-ai/grok-4.5` | OpenRouter | xAI |
| Sabiá-4 | `sabia-4` | Maritaca API | Maritaca |

Os identificadores foram confirmados no catálogo público do OpenRouter no momento da coleta: [Claude Sonnet 5](https://openrouter.ai/anthropic/claude-sonnet-5), [GPT-5.6 Terra](https://openrouter.ai/openai/gpt-5.6-terra), [Gemini 3.5 Flash](https://openrouter.ai/google/gemini-3.5-flash) e [Grok 4.5](https://openrouter.ai/x-ai/grok-4.5). O Sabiá seguiu a [documentação da Maritaca](https://docs.maritaca.ai/pt/api/comeco-rapido).

### Perguntas, formulações e chamadas

- Foram mantidas as dez perguntas, escalas e codificações de Tao et al. (2024).
- A condição inglesa usa os dez descritores originais: “average human being”, “typical person”, “world citizen” etc.
- As condições em português usam traduções equivalentes dos dez descritores.
- No prompt Brasil, cada descritor acrescenta que a pessoa é brasileira, nasceu e vive no Brasil.
- No prompt RS, cada descritor acrescenta que a pessoa é gaúcha, nasceu e vive no Rio Grande do Sul, Brasil.
- O descritor foi enviado como mensagem de sistema e a pergunta como mensagem de usuário.
- Cada pergunta–descritor foi uma chamada independente. Não houve histórico compartilhado entre itens.
- A temperatura `0` foi solicitada em todas as chamadas. O catálogo do OpenRouter não anunciava suporte nativo ao parâmetro para Claude Sonnet 5 e GPT-5.6 Terra; portanto, sua aplicação efetiva nesses dois modelos não é verificável.
- Os demais parâmetros ficaram nos padrões dos endpoints.

A janela total dos registros foi de 17:46:17 a 18:26:40 UTC. O OpenRouter informou custo de **US$ 1,9472** para as 1.600 chamadas feitas por essa rota; a Maritaca não informou custo no payload. O conjunto registrou 321.790 tokens de entrada e 226.510 de saída, dos quais 202.168 foram classificados pelos provedores como tokens de raciocínio.

## Pontuação, recusas e dados ausentes

As conversões seguem a codificação IVS do artigo. Para perguntas numéricas, o parser aceita apenas um número explícito e válido na última linha da resposta. Essa regra evita transformar a frase “não posso escolher; opiniões variam de 1 a 10” em resposta `1`.

O Gemini produziu onze respostas não pontuáveis:

- quatro saídas malformadas (`10of`, `1of`, `1of`, `5of`);
- sete recusas ou comentários sem uma escolha numérica final inequívoca.

As onze ocorrências concentraram-se nas condições inglês (6), português (3) e prompt Brasil (2); não houve falha no prompt RS. Nenhuma resposta foi reconsultada apenas para substituir uma recusa observada e nenhum valor foi imputado.

Para cada condição, o ponto central foi calculado como no material de Tao et al.: primeiro se obtém a média de cada item entre as formulações pontuáveis; depois, as dez médias são projetadas nos dois componentes. Assim, os pontos centrais do Gemini usam de 7 a 10 respostas por item. Os pontos translúcidos da figura mostram apenas formulações com os dez itens completos: 6 em inglês, 7 em português, 8 no prompt Brasil e 10 no prompt RS. Nos demais modelo–condição, são 10 de 10.

## Sensibilidade à formulação

Os dez descritores não são réplicas idênticas e não constituem amostra aleatória. A dispersão dos pontos translúcidos é, portanto, uma análise de sensibilidade, não um intervalo de confiança. Mesmo com temperatura zero solicitada, houve diferenças grandes. No Grok em português sem identidade, por exemplo, o eixo tradicional–secular variou de −0,741 a 4,560 entre formulações completas; no GPT-5.6 Terra, de 0,731 a 4,292. Isso mostra que palavras aparentemente intercambiáveis como “pessoa”, “indivíduo” e “cidadão do mundo” podem ativar perfis diferentes.

## Limitações

1. **O instrumento é estreito.** Dez itens projetados em dois eixos não esgotam cultura, voz, identidade ou criatividade.
2. **O modelo simula um respondente.** Respostas de LLMs não são crenças e não autorizam atribuir nacionalidade ou personalidade ao sistema.
3. **A tradução não foi validada por retrotradução ou teste de invariância.** Parte do efeito de idioma pode ser efeito lexical.
4. **As identidades solicitadas são rótulos curtos.** “Brasileiro” e “gaúcho” podem acionar estereótipos; não fornecem biografia, classe, gênero, geração, raça, município ou pertencimento rural/urbano.
5. **O ponto gaúcho é exploratório.** A amostra do WVS é nacional, a subamostra do RS é pequena e a elipse não incorpora o desenho amostral completo.
6. **Argentina e Uruguai são médias nacionais.** Não representam exclusivamente a região do Pampa.
7. **Aliases e rotas podem mudar.** Uma repetição futura sob o mesmo identificador pode atingir pesos, provedores ou políticas de moderação diferentes.
8. **Temperatura zero não garante determinismo.** Foi feita uma observação por combinação, como no desenho de referência; não há réplicas idênticas para estimar variabilidade residual.
9. **As distâncias são descritivas.** Não foram feitos testes inferenciais entre modelos ou condições.
10. **A auditoria foi executada por APIs diferentes.** OpenRouter e Maritaca podem aplicar envelopes, roteamento e padrões operacionais distintos.

## Redação sugerida para o artigo

> Em uma auditoria exploratória, submetemos cinco LLMs a 2.000 combinações das dez perguntas usadas no mapa cultural de Tao et al. (2024), dez variações do descritor do respondente e quatro condições linguístico-culturais. A tradução do inglês para o português deslocou todos os modelos, mas em magnitudes e direções distintas. Acrescentar uma identidade brasileira aproximou os cinco pontos da média humana do Brasil, com reduções de distância entre 16,1% e 72,9%, sem produzir coincidência. Já a identidade gaúcha aproximou três modelos da estimativa humana do Rio Grande do Sul e afastou dois: no Sabiá-4, a distância aumentou 64,8%; no Claude Sonnet 5, 22,5%. O resultado sugere que prompts culturais funcionam como intervenções fortes, porém não como mecanismos confiáveis de representação. Em alguns casos, parecem ativar um perfil estereotipado que se afasta da amostra humana que deveria representar.

## Legenda sugerida

> **Figura X. Cinco LLMs no mapa cultural de 107 países sob quatro condições linguístico-culturais.** Cada símbolo grande projeta as médias por pergunta obtidas em dez formulações do descritor; os pontos translúcidos representam formulações com os dez itens completos. Brasil, Argentina e Uruguai são médias nacionais reproduzidas de Tao et al. (2024); o Rio Grande do Sul é uma estimativa exploratória do WVS 2018, com 118 casos completos. Foram observadas 2.000 respostas em 13 de julho de 2026, das quais 1.989 foram pontuadas. A temperatura zero foi solicitada em todas as chamadas, mas seu suporte não pôde ser confirmado para Claude Sonnet 5 e GPT-5.6 Terra. Distâncias e dispersões são descritivas.

## Arquivos de reprodução

- `analise-resultados-distancias-llms.md`: discussão substantiva das distâncias, dos países vizinhos e dos itens que explicam os deslocamentos.
- `distancias-modelos-paises-interesse-e-vizinhos.csv`: distâncias dos vinte pontos a Brasil, Argentina, Uruguai e RS, com os três países mais próximos entre os 107.
- `deslocamentos-modelos-entre-condicoes.csv`: vetores e distâncias entre todas as combinações de condições de cada modelo.
- `efeitos-prompts-culturais-alvos.csv`: efeito dos prompts brasileiro e gaúcho sobre seus alvos declarados.
- `efeitos-prompts-todas-referencias.csv`: efeito de cada prompt cultural sobre as quatro referências humanas.
- `contribuicoes-itens-deslocamentos-culturais.csv`: decomposição linear dos deslocamentos pelos dez itens do questionário.
- `analisar-distancias-resultados.py`: reprodução das cinco tabelas anteriores.
- `auditoria-llms-multicondicao.csv`: prompts, respostas, pontuação, status, uso e rota de cada chamada.
- `respostas-llms-multicondicao-wide.csv`: matriz modelo–condição–formulação usada na projeção.
- `metadados-llms-multicondicao.json`: resumo de cobertura, tokens, custos, versões e provedores.
- `coordenadas-llms-multicondicao-medias.csv`: vinte pontos centrais e estatísticas de cobertura/sensibilidade.
- `coordenadas-llms-multicondicao-variantes.csv`: duzentos perfis de formulação, inclusive os incompletos.
- `distancias-llms-multicondicao.csv`: distâncias de cada ponto a Brasil, Argentina, Uruguai e RS.
- `testar-llms-multicondicao.py`: prompts, coleta, parser, checkpoint e consolidação.
- `gerar-mapa-cultural-llms-multicondicao.py`: projeção, cálculo de distâncias e geração da figura.

Nenhum arquivo contém chaves de API.

### Texto alternativo

Figura em quatro painéis, todos com os mesmos 107 países em cinza e os pontos humanos de Brasil, Argentina, Uruguai e Rio Grande do Sul destacados. Cada painel mostra as médias de Sabiá-4, Claude Sonnet 5, GPT-5.6 Terra, Gemini 3.5 Flash e Grok 4.5. Em inglês e português sem identidade, a maioria dos modelos aparece à direita e acima das referências sul-americanas. Com identidade brasileira, todos se movem em direção ao Brasil, mas permanecem dispersos. Com identidade gaúcha, Terra, Gemini e Grok se aproximam do ponto do RS, enquanto Claude e, sobretudo, Sabiá se deslocam para baixo, na direção tradicional, afastando-se da estimativa humana gaúcha. Pontos translúcidos revelam variação considerável entre formulações.
