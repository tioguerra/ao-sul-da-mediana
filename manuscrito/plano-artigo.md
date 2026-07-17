# Plano do artigo — "Ao sul da mediana: IA generativa e a hipótese da mediocridade cognitiva"

**Gênero:** position paper acadêmico (Simpósio 31 — IA e gêneros textuais: interfaces pedagógicas ao sul do Equador)

**Versão:** consolidada em 14 de julho de 2026, a partir de duas linhas de trabalho paralelas — uma pesquisa profunda multiagente (Claude) e a auditoria própria com bibliografia dirigida deste repositório (ChatGPT + APIs reais). Este arquivo substitui a versão anterior, que era uma cópia do plano inicial de 8 seções e havia ficado desatualizada em relação à estrutura já revisada em [`artigo/banco-de-evidencias.md`](../artigo/banco-de-evidencias.md#7-estrutura-revisada-do-artigo).

**Tese central (reformulada):** quando uma mesma infraestrutura generativa medeia, em escala, atos de escrita, síntese e decisão, ela pode elevar o desempenho médio individual ao mesmo tempo que comprime a variância do repertório coletivo. Como o centro estatístico dessa infraestrutura é culturalmente situado, a compressão é assimétrica: sujeitos periféricos são atraídos não para uma média universal, mas para uma média produzida por corpora, instituições e critérios de alinhamento dominantes. Nome técnico proposto: **hipótese da compressão culturalmente assimétrica da variância** — "mediocridade cognitiva" permanece no título como formulação provocativa, desde que definida como perda de caudas, desvio e pluralidade, não como queda da nota média.

---

## Nota sobre a correção do mecanismo (importante para a redação)

A frase do resumo original — "função de custo que premia a aderência à mediana" — é tecnicamente imprecisa e deve ser evitada na forma literal no corpo do artigo. A entropia cruzada não computa nem busca uma "resposta mediana"; a concentração em modos de alta probabilidade emerge da combinação entre distribuição dos dados de treinamento, objetivo autorregressivo, ajuste por instruções/preferências, filtros de segurança e estratégia de decodificação. Ver a formulação de substituição pronta em [`artigo/banco-de-evidencias.md`, seção 2](../artigo/banco-de-evidencias.md#2-correção-técnica-indispensável).

## Resolução da citação "Kirk et al., 2024" do resumo original

O resumo cita "(KIRK *et al.*, 2024; TAO *et al.*, 2024)" para sustentar que, mesmo após ajuste fino e RLHF, os modelos seguem incorporando nuances culturais, éticas e estilísticas. Existem **dois papers reais e distintos de 2024 com primeiro autor Kirk**, e cada um sustenta uma metade diferente dessa frase — não é necessário escolher apenas um:

- **Kirk, Hannah Rose et al. (2024).** *The PRISM Alignment Project.* NeurIPS 2024. 1.500 participantes de 75 países, 8.011 conversas, 21 modelos — mostra que "alinhamento por feedback humano" depende de **quais humanos** avaliam, logo o resultado do alinhamento carrega os valores culturais e éticos de um grupo específico de avaliadores. Sustenta a metade "nuances **culturais, éticas**" da frase. Usar na Frente 1 (seção "quem alinha o modelo também importa").
- **Kirk, Robert et al. (2024).** *Understanding the Effects of RLHF on LLM Generalisation and Diversity.* ICLR 2024, arXiv:2310.06452. Mostra que o RLHF reduz a diversidade de saída mais que o SFT sozinho, tanto para um mesmo input quanto entre inputs diferentes, fenômeno que os autores chamam de "mode collapse". Sustenta a metade "nuances **estilísticas**" e é evidência direta para o mecanismo técnico da Seção 2 (RLHF reduz diversidade). Citação verificada manualmente, com números, em `banco-de-evidencias.md` desta sessão de pesquisa (Claude), seção "Seção 2 (mecanismo)".

**Redação sugerida:** citar os dois separadamente e por extenso na primeira ocorrência (Kirk, H. R. et al., 2024; Kirk, R. et al., 2024), já que ambos são 2024 e a confusão é real.

---

## Estrutura revisada (9 seções, com proporção sugerida)

| # | Seção | Função | Evidências principais | Proporção |
| --- | --- | --- | --- | ---: |
| 1 | Ao sul da mediana | Problema, lugar de enunciação e tese | Vinheta de autocomplete + formulação da compressão assimétrica | 8% |
| 2 | Da probabilidade ao "centro" | Explicar mecanismo sem antropomorfismo | McCoy et al. 2024; Kirk, R. et al. 2024 (RLHF/diversidade); objetivo autorregressivo, alinhamento, decodificação | 11% |
| 3 | A mediana tem geografia | Concentração linguística e institucional | Llama 2 (Touvron et al. 2023); AI Index (Stanford HAI); Kwet 2019; Couldry & Mejias 2019; Ricaurte 2019; Mohamed, Png & Isaac 2020 | 14% |
| 4 | Quando o centro escreve conosco | Deslocamento cultural em interação real | Tao et al. 2024; Agarwal, Naaman & Vashistha 2025; Hofmann et al. 2024; Kirk, H.R. et al. 2024 (PRISM); **auditoria própria de 5 LLMs em 4 condições (Sabiá-4, Claude, GPT-5.6 Terra, Gemini 3.5 Flash, Grok 4.5) — achado do RS** | 18% |
| 5 | O paradoxo da elevação homogênea | Núcleo criatividade/variância — **achado-âncora** | Doshi & Hauser 2024; Padmakumar & He 2024; Moon, Green & Kushlev 2025; Brynjolfsson, Li & Raymond 2025 | 20% |
| 6 | Da frase ao ecossistema | Escala, aprendizagem e realimentação | Kobak et al. 2025; Liang et al. 2025; Bastani et al. 2025; Shumailov et al. 2024 | 12% |
| 7 | A tendência não é destino | Contrapontos, soluções e limites | Wan & Kalman 2025 (preprint); Tucano/Sabiá-2; prompting cultural (limites) | 8% |
| 8 | Escrever desde o Pampa | Implicações pedagógicas e agenda empírica local | Protocolo de auditoria do Pampa (ver banco de evidências, seção 8); gancho com o simpósio | 6% |
| 9 | Conclusão | Retomar voz, desvio e soberania | Síntese | 3% |

### Ordem de redação recomendada

1. **Seção 5** — contém o achado-âncora (Doshi & Hauser) e define o que "mediocridade" significa no artigo.
2. **Seção 4** — elo prático entre modelo e escritor; inclui o achado empírico próprio (auditoria do RS).
3. **Seções 2 e 3** — mecanismo e geografia do centro estatístico.
4. **Seção 6** — escala e ciclo de realimentação.
5. **Seções 7 e 8** — contraprovas, desenho pedagógico, gancho com o simpósio.
6. **Introdução e conclusão por último.**

---

## O que muda em relação ao plano de 8 seções original

- A antiga seção 3 (Frente 1 completa) virou duas seções (3 e 4), separando **geografia/infraestrutura** de **deslocamento em interação** — a auditoria própria dá substância própria a essa segunda parte.
- A antiga seção 4 (Frente 2) virou as seções 5 e 6, separando o **achado-âncora** (parágrafo curto, alto impacto) do **argumento de escala** (Kobak, Liang, Bastani, Shumailov).
- A síntese (antiga seção 5) foi absorvida pela introdução/conclusão e pelo parágrafo-síntese já redigido no banco de evidências (seção 10).
- Contrapontos (antiga seção 6) ganharam evidência real: Wan & Kalman (2025) mostra que personas de IA diversas eliminam a perda de diversidade observada por Doshi & Hauser — a homogeneização é "tendência sociotécnica, não destino matemático".
- Implicações pedagógicas (antiga seção 7) ganharam apoio empírico direto: Bastani et al. (2025, PNAS) mostra causalmente que uma interface sem salvaguardas piora o aprendizado subsequente, enquanto uma interface com salvaguardas pedagógicas não.

## Gráficos (já produzidos, em `artigo/figuras/` e `artigo/mapa-cultural/`)

1. ✅ `figura-1-idiomas-llama2.png` — composição linguística do Llama 2 (Seção 3)
2. ✅ `figura-2-alinhamento-cultural.png` — distância cultural antes/depois de prompting, 5 versões de GPT (Seção 4)
3. ✅ `figura-3-criatividade-diversidade.png` — paradoxo Doshi & Hauser (Seção 5, âncora)
4. ✅ `figura-4-aprendizagem-guardrails.png` — desempenho assistido vs. aprendizagem, Bastani et al. (Seção 6)
5. ✅ `mapa-cultural/figura-mapa-cultural-quatro-condicoes-trajetorias.png` — trajetórias dos 5 LLMs em 4 condições linguístico-culturais (Seção 4, achado próprio)
6. ✅ `mapa-cultural/figura-mapa-cultural-pampa-ia.png` — mapa cultural com RS e versões históricas de GPT (Seção 4)

Todos com fonte, legenda sugerida e texto alternativo já redigidos nos respectivos arquivos de nota metodológica.

## Pendências

- [x] Banco de evidências → [`artigo/banco-de-evidencias.md`](../artigo/banco-de-evidencias.md) (análise dirigida, matriz de força inferencial, 4 proposições testáveis) + apêndice de citações complementares desta sessão
- [x] Verificar as referências do resumo original (McCoy ✓, Kirk — resolvido acima como dois papers ✓, Tao ✓, Doshi & Hauser ✓, Shumailov ✓)
- [x] Achado empírico próprio ancorado no Pampa (auditoria de 5 LLMs, identidade gaúcha)
- [x] Redigir seções na ordem 5 → 4 → 2/3 → 6 → 7/8 → 1 → 9 → [`manuscrito/rascunho.md`](rascunho.md) — rascunho completo (~4.660 palavras), gerado por workflow multiagente (redação → verificação factual por seção → harmonização de terminologia/transições → introdução/conclusão → checagem adversarial final). 5 correções reais aplicadas (2 lacunas de BibTeX, 1 contradição interna, 2 formulações mais fortes do que a evidência sustentava); 7 alarmes falsos do checador final verificados manualmente nas fontes primárias. Ver nota de proveniência ao final do rascunho.
- [x] Versão LaTeX com figuras vetoriais → [`manuscrito/latex/`](latex/) e PDF em [`manuscrito/ao-sul-da-mediana-rascunho.pdf`](ao-sul-da-mediana-rascunho.pdf); linguagem revisada conforme `ESTILO.md` (82 travessões eliminados, zero deriva factual verificada mecanicamente)
- [ ] Definir norma de citação (ABNT, pelo estilo do resumo) e limite de páginas/palavras do simpósio — o LaTeX usa biblatex authoryear; trocar para ABNT exige só ajustar o preâmbulo
- [ ] Segunda busca focal: América Latina, português brasileiro, espanhol rioplatense, línguas indígenas, benchmarks culturais regionais (item 5 dos "próximos passos concretos" do banco de evidências)
- [ ] Revisão humana integral do rascunho antes de qualquer submissão — nenhuma IA generativa é autora deste texto (ver `AUTHORS.md`)
