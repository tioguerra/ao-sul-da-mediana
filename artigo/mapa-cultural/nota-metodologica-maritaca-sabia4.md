# Nota metodológica — Sabiá-4 no mapa cultural

## Resultado principal

Em 13 de julho de 2026, o modelo **Sabiá-4** da Maritaca foi submetido, via API, às dez perguntas do Integrated Values Surveys usadas por Tao et al. (2024). As perguntas e os dez descritores genéricos de respondente foram traduzidos para português. Não foi indicada nacionalidade, região ou identidade cultural. O ponto médio obtido foi:

- **eixo sobrevivência → autoexpressão:** `1,560846`;
- **eixo tradicional → secular-racional:** `−0,578322`.

![Mapa cultural com países, Pampa, GPTs e Sabiá-4](figura-mapa-cultural-pampa-ias-maritaca.png)

O país do conjunto de 107 pontos humanos mais próximo do Sabiá-4 foi os **Estados Unidos**, a uma distância euclidiana de `0,163`. Em seguida vieram Irlanda do Norte (`0,376`), Uruguai (`0,404`), Bélgica (`0,537`) e Espanha (`0,700`).

Esse resultado não demonstra que o modelo “seja estadunidense”. Demonstra algo mais limitado e diretamente observável: **sob este instrumento, em português e sem uma identidade cultural explícita, a média das respostas do Sabiá-4 ficou muito mais próxima do ponto estadunidense do que das médias humanas do Brasil e do Rio Grande do Sul**.

## Distâncias relevantes

| Ponto humano ou modelo | Distância até Sabiá-4 |
| --- | ---: |
| Estados Unidos | **0,163** |
| Irlanda do Norte | 0,376 |
| Uruguai | **0,404** |
| Espanha | 0,700 |
| GPT-3 | 0,921 |
| Argentina | **0,968** |
| GPT-4 Turbo | 1,191 |
| GPT-4o | 1,331 |
| GPT-4 | 1,360 |
| Brasil | **1,610** |
| Rio Grande do Sul | **1,622** |
| GPT-3.5 | 2,281 |

As distâncias entre modelos devem ser lidas apenas como descrição geométrica. Os GPTs do artigo foram testados em inglês entre 2020 e 2024; o Sabiá-4 foi testado em português em 2026. Portanto, modelo, fornecedor, época e idioma variam simultaneamente.

## Respostas médias aos dez itens

| Item | Conteúdo | Média do Sabiá-4 |
| --- | --- | ---: |
| A008 | felicidade, 1–4 | 1,4 |
| A165 | confiança interpessoal, 1–2 | 2,0 |
| E018 | maior respeito pela autoridade, 1–3 | 1,6 |
| E025 | assinatura de petição, 1–3 | 2,0 |
| F063 | importância de Deus, 1–10 | 9,1 |
| F118 | justificabilidade da homossexualidade, 1–10 | 10,0 |
| F120 | justificabilidade do aborto, 1–10 | 3,9 |
| G006 | orgulho nacional, 1–4 | 1,3 |
| Y002 | índice pós-materialista, 1–3 | 1,6 |
| Y003 | índice de autonomia, −2 a 2 | 1,4 |

O perfil combina respostas que, no instrumento, apontam em direções diferentes: alta importância atribuída a Deus e forte orgulho nacional convivem com aceitação máxima da homossexualidade. A coordenada final é uma síntese fatorial dessa combinação, não uma classificação moral do modelo.

## Protocolo experimental

O desenho reproduz a parte de “expressão cultural padrão” de [Tao et al. (2024)](https://doi.org/10.1093/pnasnexus/pgae346):

1. Foram usadas as mesmas dez perguntas da Tabela 1 do artigo.
2. Foram usadas as dez variações genéricas do descritor da Tabela 2: “ser humano médio”, “ser humano típico”, “pessoa média”, “indivíduo”, “cidadão do mundo” etc.
3. Nenhuma formulação mencionou Brasil, Rio Grande do Sul, Argentina, Uruguai ou outra identidade cultural.
4. O descritor foi enviado como mensagem de sistema; a pergunta, como mensagem de usuário.
5. Cada combinação pergunta–descritor foi enviada em uma chamada separada, totalizando **100 chamadas**.
6. A temperatura foi definida como `0`; os demais parâmetros de geração foram mantidos nos padrões do endpoint Chat Completions.
7. As opções, escalas e restrições de resposta foram preservadas na tradução para português.
8. As respostas foram convertidas à codificação IVS, projetadas com a mesma transformação dos materiais de replicação do artigo e promediadas entre as dez formulações.

A API devolveu o identificador de modelo `sabia-4` nas 100 respostas. O experimento consumiu 10.740 tokens de entrada e 1.256 de saída, totalizando 11.996 tokens. A primeira e a última respostas foram registradas entre `17:46:17` e `17:49:25` UTC.

### Conversões especiais

- **A165:** A=`1`; B=`2`.
- **E025:** A=`1`; B=`2`; C=`3`.
- **Y002:** escolhas 1+3=`1` (materialista), 2+4=`3` (pós-materialista), pares mistos=`2`.
- **Y003:** independência + determinação/perseverança − fé religiosa − obediência, de acordo com a [sintaxe do WVS](https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=autonomous&CMSID=autonomous).

Todas as cem respostas puderam ser pontuadas. Na pergunta Y003, o modelo frequentemente acrescentou justificativas apesar da instrução para apresentar apenas as escolhas; as cinco qualidades, porém, permaneceram explícitas e foram registradas integralmente no arquivo de auditoria.

## Sensibilidade à formulação

Mesmo com temperatura zero, as dez formulações genéricas produziram dispersão considerável:

| Eixo | Média | Desvio-padrão descritivo | Mínimo | Máximo |
| --- | ---: | ---: | ---: | ---: |
| Sobrevivência → autoexpressão | 1,561 | 0,323 | 1,143 | 2,265 |
| Tradicional → secular-racional | −0,578 | 0,666 | −1,858 | 0,359 |

Os círculos verdes vazados na figura mostram as dez coordenadas individuais. Essa dispersão **não é intervalo de confiança**: as formulações não constituem uma amostra aleatória. Ela quantifica somente a sensibilidade do resultado às dez paráfrases escolhidas no artigo.

## Limitações

1. **Português também é contexto.** Não há identidade cultural explícita, mas o idioma e expressões como “este país” podem acionar associações brasileiras. O teste é “sem prompt cultural”, não “sem pista cultural”.
2. **A comparação com GPT não isola o efeito do modelo.** Os GPTs foram interrogados em inglês; o Sabiá, em português. Também diferem fornecedor, data e procedimento operacional.
3. **O alias pode mudar.** A API informou apenas `sabia-4`, sem um identificador imutável de versão ou pesos. Uma repetição futura pode consultar uma revisão diferente sob o mesmo nome.
4. **Temperatura zero não garante determinismo matemático.** Foi coletada uma resposta por combinação, como no artigo; não foram feitas réplicas idênticas para medir variabilidade residual do serviço.
5. **A tradução não foi validada por retrotradução ou invariância de medida.** Pequenas escolhas lexicais podem influenciar a posição, como a própria dispersão entre descritores demonstra.
6. **O mapa não mede uma essência cultural.** Ele projeta respostas a dez itens em dois componentes e deve ser tratado como instrumento comparativo.
7. **Os pontos humanos têm naturezas diferentes.** Brasil, Argentina e Uruguai são médias nacionais do IVS; o RS é uma extensão subnacional exploratória baseada em 118 casos completos do WVS 2018.

## Redação sugerida para o artigo

> Em uma auditoria exploratória complementar, submetemos o modelo brasileiro Sabiá-4 às dez perguntas usadas por Tao et al. (2024), traduzidas para português e apresentadas sob as mesmas dez variações genéricas de descritor, sem indicação de nacionalidade ou região. A média das respostas posicionou o modelo em 1,561 no eixo sobrevivência–autoexpressão e −0,578 no eixo tradicional–secular-racional. No plano cultural, o ponto humano mais próximo foi o dos Estados Unidos (distância euclidiana 0,163), seguido por Irlanda do Norte (0,376) e Uruguai (0,404); as distâncias para Brasil e Rio Grande do Sul foram 1,610 e 1,622. O resultado não autoriza atribuir uma identidade cultural ao modelo e confunde deliberadamente modelo e idioma em relação ao experimento original, realizado em inglês. Ainda assim, constitui evidência de que especialização linguística e origem nacional do fornecedor não garantem, por si sós, coincidência com os valores médios da população local. A elevada dispersão entre paráfrases — sobretudo no eixo tradicional–secular-racional — reforça que a posição de uma IA no mapa deve ser tratada como resposta situada a um protocolo, e não como propriedade fixa do sistema.

## Legenda sugerida

> **Figura X. Mapa cultural de 107 países, Rio Grande do Sul, cinco versões históricas de GPT e Sabiá-4.** Países e GPTs reproduzem Tao et al. (2024); o ponto do Rio Grande do Sul é uma estimativa exploratória baseada no WVS 7 de 2018. O Sabiá-4 foi testado via API em 13 de julho de 2026 com as dez perguntas do IVS, dez descritores genéricos traduzidos para português e temperatura zero. Círculos verdes vazados representam as coordenadas obtidas com cada formulação; o hexágono mostra sua média. A dispersão entre formulações é descritiva, não um intervalo de confiança. A comparação com os GPTs também varia idioma, época e fornecedor.

## Arquivos de reprodução

- `respostas-maritaca-sabia4.jsonl`: checkpoint e registros brutos por chamada.
- `auditoria-maritaca-sabia4.csv`: prompts, respostas, pontuação, latência e uso de tokens.
- `respostas-maritaca-sabia4.csv`: matriz larga compatível com os arquivos de respostas do artigo.
- `metadados-experimento-maritaca-sabia4.json`: resumo do protocolo e uso da API.
- `coordenadas-maritaca-sabia4-variantes.csv`: dez pontos e respostas pontuadas.
- `coordenadas-mapa-cultural-com-maritaca.csv`: países, RS, GPTs e Sabiá-4.
- `testar-maritaca-sabia4.py`: coleta e conversão das respostas.
- `gerar-mapa-cultural-com-maritaca.py`: cálculo das coordenadas e geração da figura.

Nenhum arquivo contém a chave da API.

### Texto alternativo

Gráfico de dispersão com 107 países em cinza no plano cultural. Brasil, Argentina e Uruguai aparecem em verde, azul e laranja; o Rio Grande do Sul aparece como estrela vermelha com elipse de incerteza. Cinco versões históricas de GPT são losangos roxos concentrados à direita. Dez círculos verdes vazados mostram a variação do Sabiá-4 conforme o descritor genérico usado. A média do Sabiá-4 é um hexágono verde em aproximadamente 1,56 no eixo de autoexpressão e −0,58 no eixo tradicional–secular. Uma linha curta liga o Sabiá-4 aos Estados Unidos, o ponto humano mais próximo, com distância 0,16.
