# Plano do artigo — "Ao sul da mediana: IA generativa e a hipótese da mediocridade cognitiva"

**Gênero:** position paper acadêmico (Simpósio 31 — IA e gêneros textuais: interfaces pedagógicas ao sul do Equador)
**Tese central:** ao penalizar o improvável, os LLMs exercem uma dupla pressão conformadora — cultural (rumo à norma anglófona/norte-atlântica) e cognitiva (rumo à média estatística) — que, usada de forma massiva e ubíqua, erode a autoria singular e conduz a uma mediocridade cognitiva coletiva.

---

## Estrutura proposta

### 1. Introdução — a pergunta
- Abrir com a pergunta do resumo: o que acontece quando a escrita passa a ser mediada por uma distribuição estatística?
- Situar o lugar de fala: América Latina, Sul Global, Pampa — escrever "ao sul da mediana" em dois sentidos (geográfico e estatístico).
- Enunciar a tese e o caráter de position paper (posição argumentada + evidência empírica emprestada de estudos existentes).

### 2. Por que a média: o mecanismo
- Next-token prediction e função de custo: o que significa, tecnicamente, "premiar a aderência à mediana" (McCoy et al. — Embers of Autoregression: sensibilidade à probabilidade do output).
- RLHF e alinhamento: como o ajuste fino reduz ainda mais a diversidade de saída (evidências de queda de entropia/diversidade pós-RLHF).
- Ponto-chave do argumento: a penalização do improvável não é um bug, é o objetivo de otimização.

### 3. Frente 1 — A voz ausente: viés cultural e colonialismo digital
- **3.1 O corpus não é neutro:** composição linguística dos dados de treinamento (inglês ~90% no GPT-3; português <2%; números do Common Crawl e de modelos abertos como Llama). → *gráfico de barras: línguas nos corpora vs. falantes no mundo*
- **3.2 Alinhamento cultural medido:** estudos com World Values Survey / Hofstede (Tao et al. 2024; Cao et al. 2023; Durmus et al. — GlobalOpinionQA): a que "país" o modelo se parece, e quais países ficam mais distantes. → *gráfico: distância cultural por país*
- **3.3 A escrita deslocada:** evidência experimental de que autocomplete/sugestões ocidentalizam o estilo de escritores não ocidentais (estudo de Cornell com escritores indianos).
- **3.4 Variedades penalizadas:** prejuízo dialetal (Hofmann et al. 2024, Nature — African American English) como prova de conceito do mecanismo que também atinge o português gaúcho/fronteiriço, o espanhol platino etc.
- **3.5 A infraestrutura concentrada:** Stanford AI Index — modelos notáveis e investimento por país; a quase ausência da América Latina. → *gráfico ou tabela*
- **3.6 Enquadramento teórico:** colonialismo digital (Kwet), colonialismo de dados (Couldry & Mejias), epistemologias do Sul aplicadas a dados (Ricaurte; Milan & Treré).
- **3.7 Respostas do Sul:** LatamGPT (CENIA-Chile), Sabiá/Maritaca (Brasil) — mencionar como reação, e discutir limites (treinar localmente resolve o corpus, não a lógica da mediana).

### 4. Frente 2 — A tendência à média: criatividade e homogeneização
- **4.1 O paradoxo individual/coletivo:** Doshi & Hauser 2024 — IA melhora a história do escritor mediano, mas as histórias ficam mais parecidas entre si. Este é o resultado-âncora da tese. → *gráfico: ganho individual vs. perda de diversidade coletiva*
- **4.2 Diversidade de conteúdo:** Padmakumar & He (ICLR 2024); Anderson et al. 2024 — homogeneização na ideação criativa.
- **4.3 Homogeneização detectável em escala:** vocabulário em excesso pós-ChatGPT em abstracts científicos (Kobak et al. — "delve"); fração de textos modificados por LLM (Liang et al.). → *gráfico: curva temporal da frequência de palavras-assinatura*
- **4.4 Compressão de variância no trabalho:** Dell'Acqua et al. (BCG, "jagged frontier"); Brynjolfsson et al. ("Generative AI at Work") — quem mais ganha é quem está abaixo da média: a IA nivela.
- **4.5 Persuasão latente:** Jakesch et al. 2023 — co-escrever com um modelo opinativo muda a opinião de quem escreve.
- **4.6 Dívida cognitiva:** Kosmyna et al. 2025 (EEG, MIT); Lee et al. 2025 (pensamento crítico em knowledge workers) — a terceirização da escrita tem custo mensurável.
- **4.7 O sistema fechando sobre si:** model collapse (Shumailov et al. 2024, Nature) — quando a média realimenta a média, as caudas da distribuição desaparecem. Funciona como metáfora e como mecanismo literal.

### 5. Síntese — onde as frentes se encontram
- As duas frentes são o mesmo fenômeno visto de ângulos diferentes: a mediana do corpus é *culturalmente situada* (Frente 1) e a otimização para ela é *estatisticamente conformadora* (Frente 2).
- Para o Sul Global o efeito é composto: a média para a qual somos puxados nem sequer é a nossa média.
- O argumento histórico (Darwin, Einstein): paradigmas nascem nas caudas da distribuição — o que se perde quando as caudas são penalizadas em escala.

### 6. Contrapontos e limitações (essencial num position paper)
- Estudos que não encontram homogeneização, ou que mostram ganhos reais de acesso/equidade (a IA como niveladora *para cima* de quem escreve em língua estrangeira).
- Limites da evidência: maioria dos estudos é de curto prazo, com modelos específicos, em inglês.
- Acomodações históricas de tecnologias da palavra (escrita, imprensa, calculadora) e por que este caso pode ser diferente (escala, ubiquidade, opacidade, propriedade privada).

### 7. Implicações pedagógicas (gancho com o simpósio)
- O que significa ensinar escrita e leitura "ao sul da mediana": uso crítico vs. proibição; a IA como objeto de estudo, não só ferramenta.
- Defesa da fricção cognitiva como valor pedagógico.
- Soberania de infraestrutura e letramento em IA como pauta de política linguística/educacional.

### 8. Conclusão
- Retomar a pergunta inicial; a escrita sem desvio é uma escrita sem voz.

---

## Gráficos planejados
1. **Barras:** composição linguística dos corpora de treinamento vs. população falante (Frente 1).
2. **Dispersão/mapa:** distância cultural dos LLMs por país — WVS (Frente 1).
3. **Curva temporal:** frequência de palavras-assinatura de LLM em abstracts científicos, antes/depois de 2023 (Frente 2).
4. **Barras pareadas:** Doshi & Hauser — criatividade individual ↑ vs. similaridade coletiva ↑ (Frente 2).
5. **Diagrama conceitual:** model collapse — distribuição estreitando a cada geração (Frente 2 / Síntese).

## Pendências
- [ ] Banco de evidências (pesquisa profunda em andamento → `banco-de-evidencias.md`)
- [ ] Verificar as 5 referências já citadas no resumo (McCoy, Kirk, Tao, Doshi & Hauser, Shumailov)
- [ ] Definir norma de citação (ABNT, pelo estilo do resumo) e limite de páginas do simpósio
- [ ] Redigir seções na ordem 3 → 4 → 2 → 5 → 6 → 7 → 1 → 8
