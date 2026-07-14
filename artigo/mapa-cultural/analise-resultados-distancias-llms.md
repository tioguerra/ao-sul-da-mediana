# Resultados e discussão: idioma, identidade solicitada e alinhamento cultural dos LLMs

## Método da comparação

Para cada modelo e condição, calculou-se a distância euclidiana entre o ponto do modelo e o ponto humano de referência no plano de Tao et al. (2024):

\[
d(m,h)=\sqrt{(x_m-x_h)^2+(y_m-y_h)^2},
\]

em que \(x\) representa o eixo sobrevivência–autoexpressão e \(y\), o eixo tradicional–secular-racional. Quanto menor a distância, maior a semelhança entre os dois perfis dentro deste instrumento. A medida tem finalidade descritiva. Ela atribui o mesmo peso aos dois eixos e não incorpora a incerteza das médias humanas nem a dispersão entre formulações dos prompts.

Os pontos humanos usados como referência são: Brasil **(−0,037; −0,376)**, Argentina **(0,628; −0,320)**, Uruguai **(1,184; −0,434)** e Rio Grande do Sul **(0,266; 0,398)**. O ponto do RS foi calculado sobre 118 casos completos do WVS 2018.

## Uma correção importante da leitura visual

A hipótese de que o Sabiá-4 se afastou do Brasil quando recebeu a identidade brasileira não é confirmada pela distância total. Em português sem identidade, sua distância ao Brasil é **1,610**. Com o prompt brasileiro, ela cai para **1,351**, uma redução de **0,259**, ou **16,1%**. O que ocorre é um movimento em direções opostas nos dois eixos. A diferença no eixo sobrevivência–autoexpressão diminui de 1,597 para 1,281, enquanto a diferença no eixo tradicional–secular-racional aumenta de 0,202 para 0,431. O afastamento vertical existe, mas é menor que a aproximação horizontal.

O paralelo mais forte com o resultado de Tao et al. aparece no prompt gaúcho. A distância do Sabiá-4 ao ponto humano do RS sobe de **1,622 para 2,673**, aumento de **64,8%**. O Claude também se afasta, de **1,218 para 1,492**, aumento de **22,5%**. Portanto, a intuição sobre uma possível piora causada pelo condicionamento cultural está correta, mas o caso sustentado pelos números é a identidade gaúcha, não a identidade brasileira do Sabiá.

No artigo de referência, o prompt cultural reduziu a distância média do GPT-4o aos países de 2,42 para 1,57 e melhorou o alinhamento em 71% dos casos. Houve, porém, pioras expressivas justamente em alguns países inicialmente próximos do perfil padrão. Na Finlândia, a distância passou de 0,20 para 2,43; em Luxemburgo, de 0,59 para 2,72; em Andorra, de 0,21 para 2,26; e na Suíça, de 0,45 para 2,48. [Tao et al. (2024)](https://academic.oup.com/pnasnexus/article/3/9/pgae346/7756548) interpretam esse resultado como evidência de que o prompting cultural não é uma solução universal. O resultado do RS é estruturalmente semelhante: nomear a cultura pode ativar uma representação mais caricatural que a resposta sem identidade. Não se trata de uma réplica numérica do caso finlandês, pois as linhas de base e as populações são diferentes.

## Efeito dos prompts culturais sobre os alvos declarados

Na tabela abaixo, valores negativos na mudança indicam aproximação do alvo; valores positivos indicam afastamento. A condição de referência é sempre o mesmo modelo respondendo em português brasileiro, sem identidade nacional ou regional.

| Modelo | Brasil: português | Brasil: identidade brasileira | Mudança | RS: português | RS: identidade gaúcha | Mudança |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sabiá-4 | 1,610 | 1,351 | −0,259 (−16,1%) | 1,622 | 2,673 | +1,051 (+64,8%) |
| Claude Sonnet 5 | 1,710 | 0,752 | −0,958 (−56,0%) | 1,218 | 1,492 | +0,274 (+22,5%) |
| GPT-5.6 Terra | 3,135 | 1,651 | −1,483 (−47,3%) | 2,363 | 0,966 | −1,397 (−59,1%) |
| Gemini 3.5 Flash | 2,327 | 1,618 | −0,710 (−30,5%) | 1,827 | 1,402 | −0,425 (−23,3%) |
| Grok 4.5 | 2,448 | 0,663 | −1,785 (−72,9%) | 1,943 | 0,958 | −0,984 (−50,7%) |

O primeiro resultado é consistente: a identidade brasileira aproximou os cinco modelos do Brasil. A magnitude, contudo, variou muito. O Sabiá apresentou a menor redução absoluta e relativa; o Grok, a maior. Especialização no idioma, portanto, não pode ser tratada como sinônimo de alinhamento aos valores médios da população brasileira. O experimento mede apenas dez respostas e não permite atribuir a diferença aos dados de treinamento. Ainda assim, ele mostra que a competência linguística do Sabiá-4 não tornou desnecessário o condicionamento cultural nem garantiu a maior sensibilidade ao alvo brasileiro.

O segundo resultado é a assimetria do prompt gaúcho. Terra, Gemini e Grok se aproximaram do RS; Sabiá e Claude se afastaram. Mais importante, a identidade gaúcha produziu pouca especificidade regional em quatro modelos. Em comparação com a identidade brasileira, a distância ao RS piorou no Sabiá, de 1,552 para 2,673, e no Claude, de 0,926 para 1,492. No Terra, ela permaneceu praticamente idêntica, 0,966 nas duas condições. No Gemini, a melhora foi de apenas 0,016. Somente o Grok apresentou ganho regional claro, de 1,382 para 0,958.

Há outro indício de baixa especificidade. Para Terra, Gemini e Grok, o prompt gaúcho deixou o modelo ainda mais próximo do Brasil que o próprio prompt brasileiro. As respectivas distâncias ao Brasil foram 1,426 contra 1,651; 1,479 contra 1,618; e 0,578 contra 0,663. Isso sugere que, nesses modelos, “brasileiro” e “gaúcho” acionam vetores parcialmente comuns, em vez de estimativas distintas das duas populações.

## Distâncias completas e países mais próximos

Os vizinhos abaixo foram calculados entre os 107 países do mapa. O nome do país deve ser lido apenas como proximidade geométrica nos dois eixos. Ele não significa que o modelo possua a cultura, a identidade ou a história daquele país.

| Modelo | Condição | Brasil | Argentina | Uruguai | RS | Três países mais próximos |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Sabiá-4 | Inglês | 1,646 | 1,247 | 1,289 | 0,915 | Mongólia (0,368); Tchéquia (0,429); Estônia (0,471) |
| Sabiá-4 | Português | 1,610 | 0,968 | 0,404 | 1,622 | Estados Unidos (0,163); Irlanda do Norte (0,376); Uruguai (0,404) |
| Sabiá-4 | Identidade brasileira | 1,351 | 0,786 | 0,379 | 1,552 | Uruguai (0,379); Irlanda (0,391); Irlanda do Norte (0,406) |
| Sabiá-4 | Identidade gaúcha | 2,312 | 1,879 | 1,494 | 2,673 | Irlanda (1,000); Estados Unidos (1,405); Porto Rico (1,456) |
| Claude Sonnet 5 | Inglês | 1,338 | 0,679 | 0,119 | 1,313 | Irlanda do Norte (0,073); Uruguai (0,119); Estados Unidos (0,206) |
| Claude Sonnet 5 | Português | 1,710 | 1,122 | 0,891 | 1,218 | Eslovênia (0,205); Espanha (0,294); Áustria (0,388) |
| Claude Sonnet 5 | Identidade brasileira | 0,752 | 0,127 | 0,470 | 0,926 | Argentina (0,127); Vietnã (0,219); África do Sul (0,466) |
| Claude Sonnet 5 | Identidade gaúcha | 0,989 | 0,712 | 0,760 | 1,492 | Irlanda (0,345); México (0,547); Vietnã (0,565) |
| GPT-5.6 Terra | Inglês | 3,135 | 2,652 | 2,465 | 2,403 | Japão (0,539); Alemanha (0,907); Tchéquia (1,098) |
| GPT-5.6 Terra | Português | 3,135 | 2,705 | 2,581 | 2,363 | Japão (0,451); Alemanha (1,118); Tchéquia (1,140) |
| GPT-5.6 Terra | Identidade brasileira | 1,651 | 1,205 | 1,195 | 0,966 | Tchéquia (0,388); Eslovênia (0,389); Mongólia (0,490) |
| GPT-5.6 Terra | Identidade gaúcha | 1,426 | 0,852 | 0,723 | 0,966 | Espanha (0,286); Itália (0,302); Eslovênia (0,434) |
| Gemini 3.5 Flash | Inglês | 2,789 | 2,204 | 1,879 | 2,203 | Alemanha (0,307); Finlândia (0,756); Andorra (0,765) |
| Gemini 3.5 Flash | Português | 2,327 | 1,714 | 1,358 | 1,827 | Alemanha (0,324); Áustria (0,434); Finlândia (0,445) |
| Gemini 3.5 Flash | Identidade brasileira | 1,618 | 0,952 | 0,468 | 1,418 | Estados Unidos (0,267); Bélgica (0,283); Espanha (0,301) |
| Gemini 3.5 Flash | Identidade gaúcha | 1,479 | 0,816 | 0,267 | 1,402 | Estados Unidos (0,088); Irlanda do Norte (0,217); Uruguai (0,267) |
| Grok 4.5 | Inglês | 2,456 | 1,883 | 1,597 | 1,865 | Alemanha (0,033); Tchéquia (0,610); Eslovênia (0,617) |
| Grok 4.5 | Português | 2,448 | 1,833 | 1,468 | 1,943 | Alemanha (0,294); Finlândia (0,419); Andorra (0,445) |
| Grok 4.5 | Identidade brasileira | 0,663 | 0,774 | 1,102 | 1,382 | México (0,307); Haiti (0,324); Malta (0,365) |
| Grok 4.5 | Identidade gaúcha | 0,578 | 0,232 | 0,669 | 0,958 | Vietnã (0,030); Argentina (0,232); África do Sul (0,413) |

O quadro mostra que o alvo nomeado raramente é o vizinho efetivo. Com identidade brasileira, nenhum dos cinco modelos tem o Brasil como país mais próximo. Os vizinhos são Uruguai para Sabiá, Argentina para Claude, Tchéquia para Terra, Estados Unidos para Gemini e México para Grok. Com identidade gaúcha, os vizinhos são Irlanda, Irlanda, Espanha, Estados Unidos e Vietnã. A heterogeneidade enfraquece a ideia de uma representação brasileira ou gaúcha estável compartilhada entre sistemas.

Algumas coincidências são quase exatas. O Grok em inglês fica a 0,033 da Alemanha; o mesmo modelo com identidade gaúcha fica a 0,030 do Vietnã; o Claude em inglês fica a 0,073 da Irlanda do Norte; e o Gemini com identidade gaúcha, a 0,088 dos Estados Unidos. Esses números mostram a capacidade discriminatória limitada de uma projeção em dois eixos. Culturas distintas podem ocupar posições semelhantes porque o mapa retém apenas uma pequena parte de suas diferenças.

## Idioma é uma intervenção cultural independente

A distância entre as condições em inglês e português foi de **1,513** no Sabiá, **0,835** no Claude, **0,524** no Gemini, **0,313** no Terra e **0,301** no Grok. Não houve uma direção comum. No Sabiá, o português deslocou o ponto da vizinhança da Mongólia para a dos Estados Unidos e do Uruguai. No Claude, o inglês ficou muito próximo do Uruguai, mas o português passou para a vizinhança da Eslovênia e da Espanha. Terra, Gemini e Grok permaneceram mais próximos de países europeus ou do Japão nas duas línguas, embora com deslocamentos mensuráveis.

Esses resultados impedem que “responder em português” seja usado como aproximação automática de “responder como brasileiro”. Tradução e identidade são tratamentos diferentes. O efeito pode combinar semântica lexical, convenções pragmáticas do idioma, distribuição do treinamento, instruções de sistema do provedor e tendências específicas de resposta ao formato de pesquisa.

O Sabiá foi o modelo mais sensível à troca de idioma e também apresentou a maior distância entre as condições em inglês e com identidade gaúcha, **2,749**. Uma hipótese é que a especialização em português torne as marcas identitárias em português mais salientes. Outra é que esse comportamento decorra de alinhamento, template de sistema ou variação de uma única coleta. O desenho atual não distingue essas explicações.

## O prompt brasileiro produziu uma direção regional ampla

Embora tenha aproximado todos os modelos do Brasil, o prompt brasileiro também aproximou todos os modelos da Argentina, do Uruguai e do RS. Na média dos cinco modelos, a redução foi de 1,039 para o Brasil, 0,900 para a Argentina, 0,618 para o Uruguai e 0,546 para o RS. O efeito não parece ser uma navegação precisa até um ponto brasileiro. Ele se parece mais com um vetor amplo em direção a uma região do mapa associada aos países do Cone Sul.

Em média, a identidade brasileira deslocou os modelos **0,879 unidade para o polo de sobrevivência** e **0,934 unidade para o polo tradicional**. Todos os cinco movimentos ocorreram para a esquerda e para baixo. A convergência de direção contrasta com a dispersão dos pontos finais. O rótulo nacional parece acionar um conjunto recorrente de associações, mas cada modelo parte de uma posição diferente e atribui intensidades diferentes a essas associações.

Essa observação é importante para o argumento do artigo. Um prompt cultural pode reduzir uma métrica de distância sem representar de modo específico a população solicitada. Se a intervenção aproxima simultaneamente o modelo de vários países e o deixa geometricamente mais perto de outro país, “melhora de alinhamento” deve ser interpretada como deslocamento relativo, não como recuperação de uma voz nacional autêntica.

## O prompt gaúcho deslocou todos os modelos para o polo tradicional

O resultado mais regular do prompt gaúcho não ocorreu na distância ao RS, mas no eixo tradicional–secular-racional. Em relação ao português sem identidade, os cinco modelos se moveram para baixo: Sabiá, −1,225; Claude, −1,432; Terra, −1,732; Gemini, −0,948; Grok, −1,156. O deslocamento médio foi de **−1,299**. Quatro modelos também se moveram para o polo de sobrevivência; o Sabiá foi a exceção, com pequeno movimento para a autoexpressão.

O ponto humano do RS está em **0,398** no eixo tradicional–secular-racional. Depois do prompt gaúcho, os modelos ficaram em −1,803 (Sabiá), −1,027 (Claude), 0,288 (Terra), −0,365 (Gemini) e −0,526 (Grok). Somente o Terra terminou próximo do RS nesse eixo. Nos demais casos, a identidade regional tornou a resposta substancialmente mais tradicional que a média observada na subamostra gaúcha.

Uma interpretação plausível é a ativação de um arquétipo regional tradicionalista ou ruralizado, em vez de uma estimativa da distribuição contemporânea de valores no estado. Essa interpretação deve permanecer como hipótese. Os dados não revelam quais documentos, associações internas ou etapas de alinhamento produziram a resposta. Também há um mecanismo mais simples: coerência de papel. Depois de receber a instrução “você é gaúcho”, o modelo pode sentir-se compelido a declarar orgulho nacional, religiosidade ou deferência a tradições, mesmo sem representar uma população real.

## Quais itens produziram os deslocamentos

A transformação dos dez itens para os dois eixos é linear, o que permite decompor cada deslocamento. Na média dos cinco modelos, o prompt brasileiro elevou a importância atribuída a Deus em **2,74 pontos** na escala de 1 a 10; reduziu em **0,34** a resposta de orgulho nacional, na qual números menores significam maior orgulho; deslocou em **−0,48** o índice de prioridades, em direção a ordem e controle de preços; reduziu em **0,62** o índice de qualidades infantis, em direção a fé e obediência e para longe de independência e determinação; e reduziu em **1,16 ponto** a justificabilidade do aborto.

O prompt gaúcho produziu um padrão semelhante. Na média, a importância de Deus subiu **2,72 pontos**; a resposta de orgulho nacional caiu **0,52 ponto**, o que nessa escala significa maior orgulho; a resposta sobre respeito à autoridade deslocou-se **0,42 ponto** em direção a considerá-lo algo bom; e a justificabilidade do aborto caiu **1,26 ponto**. O item de orgulho nacional, sozinho, contribuiu em média com **−0,562** para o deslocamento no eixo tradicional–secular-racional. A autoridade contribuiu com −0,307 e a importância de Deus, com −0,292.

No Sabiá sob identidade gaúcha, os maiores vetores individuais vieram de felicidade, respeito à autoridade e orgulho nacional. A resposta média indicou maior felicidade, maior aprovação da autoridade e maior orgulho, combinação que empurrou fortemente o segundo eixo para baixo. No Claude, o orgulho nacional respondeu pela maior parte do afastamento vertical. No Terra, os principais componentes foram importância de Deus, orgulho e autoridade. No Gemini, autoridade foi o maior componente. No Grok, orgulho e importância de Deus dominaram, acompanhados por menor justificabilidade da homossexualidade e do aborto.

Essa decomposição torna a hipótese do estereótipo mais concreta, mas também revela um possível artefato do instrumento. O prompt fornece uma identidade nacional ou regional antes de perguntar “quão orgulhoso você é de sua nacionalidade?”. Uma resposta de maior orgulho pode refletir obediência narrativa ao papel, não uma inferência cultural baseada em dados. Como esse item possui carga alta no segundo eixo, uma pequena mudança altera muito a coordenada. O teste futuro mais informativo é repetir a análise removendo o item de orgulho e usar personas mais ricas, sem ordenar diretamente que o sistema assuma a identidade avaliada.

## Interpretação geral

Os resultados sustentam quatro proposições para o position paper.

1. **Idioma, nacionalidade e regionalidade não são metadados neutros.** Cada um funciona como uma intervenção sobre as respostas. A simples troca de idioma deslocou todos os modelos, em alguns casos mais que o próprio prompt nacional.
2. **Prompting cultural aproxima com frequência, mas não representa com precisão.** A identidade brasileira reduziu a distância ao Brasil em todos os modelos, porém nenhum ponto terminou mais próximo do Brasil que de qualquer outro país.
3. **A regionalização pode acionar exagero, não granularidade.** A identidade gaúcha produziu um movimento tradicional comum aos cinco modelos, mas só um deles ganhou especificidade clara em relação ao ponto do RS.
4. **Um modelo treinado para um idioma local não é automaticamente um modelo de valores locais.** O Sabiá respondeu fluentemente em português e foi muito sensível ao idioma, mas apresentou a menor aproximação relativa ao Brasil e o maior afastamento do RS sob o prompt correspondente.

Esses achados são compatíveis com uma forma de compressão culturalmente assimétrica. A resposta não converge para uma média universal. Ela é atraída por associações aprendidas e políticas de alinhamento que podem condensar “Brasil” ou “Rio Grande do Sul” em poucos sinais recorrentes. Quando a saída é reutilizada em memorandos, resumos ou subsídios à decisão, pequenas alterações de enquadramento podem se repetir em escala. O experimento não demonstra esse efeito institucional cumulativo, mas identifica um mecanismo plausível: rótulos linguísticos e culturais mudam sistematicamente o perfil de respostas, sem garantia de aproximação da população nomeada.

## Limites e testes necessários

As conclusões devem ser mantidas no escopo do desenho. O instrumento contém dez itens e dois eixos; não mede uma cultura completa nem crenças internas do modelo. As dez formulações do descritor são uma análise de sensibilidade, não réplicas aleatórias. Houve uma observação por combinação e 11 respostas não pontuáveis do Gemini. O ponto do RS usa 118 casos completos de uma pesquisa nacional e não equivale a uma amostra estadual desenhada para esse propósito. Argentina e Uruguai são médias nacionais, não pontos exclusivos do Pampa. A distância euclidiana ignora incertezas e supõe escalas comparáveis nos dois eixos. Os aliases e as políticas dos provedores também podem mudar.

Quatro extensões permitiriam testar as interpretações apresentadas:

- repetir cada combinação em diferentes datas e com réplicas independentes;
- calcular distâncias com intervalos de incerteza para os pontos humanos e para a variação entre prompts;
- refazer a projeção com ablação do orgulho nacional e dos demais itens de maior carga;
- comparar rótulos curtos com personas demograficamente ancoradas, incluindo idade, classe, raça, município, escolaridade e contexto urbano ou rural.

O resultado mais defensável, nesta etapa, não é que os modelos “possuem” uma cultura ou que o prompt revelou sua verdadeira posição. O resultado é mais limitado e mais útil: **a cultura solicitada altera a simulação, mas a direção dessa alteração pode refletir generalização regional, coerência de papel ou estereótipo, e pode afastar o sistema da população que pretende representar**.
