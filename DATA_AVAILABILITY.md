# Disponibilidade, proveniência e dicionário dos dados

## Princípio geral

O repositório separa quatro camadas:

1. materiais externos de replicação;
2. respostas brutas das APIs;
3. tabelas intermediárias e coordenadas derivadas;
4. figuras e texto analítico.

Nenhuma chave de API e nenhum registro individual do World Values Survey deve ser versionado.

## Auditoria multicondição

Diretório: `artigo/mapa-cultural/`.

| Arquivo | Unidade | Linhas de dados | Conteúdo |
| --- | --- | ---: | --- |
| `auditoria-llms-multicondicao.csv` | chamada | 2.000 | prompt, resposta, pontuação, status, uso e provedor |
| `respostas-openrouter-multicondicao.jsonl` | tentativa | 1.601 | payload normalizado das quatro rotas OpenRouter; inclui uma tentativa com erro antes da resposta substituta |
| `respostas-maritaca-condicoes-adicionais.jsonl` | chamada | 300 | condições adicionais do Sabiá-4 |
| `respostas-llms-multicondicao-wide.csv` | modelo–condição–variante | 200 | matriz dos dez itens para projeção |
| `coordenadas-llms-multicondicao-variantes.csv` | formulação | 200 | coordenadas por descritor |
| `coordenadas-llms-multicondicao-medias.csv` | modelo–condição | 20 | pontos centrais e cobertura |
| `distancias-modelos-paises-interesse-e-vizinhos.csv` | modelo–condição | 20 | distâncias às quatro referências e três vizinhos |
| `deslocamentos-modelos-entre-condicoes.csv` | par de condições | 30 | vetores e distâncias entre condições |
| `efeitos-prompts-culturais-alvos.csv` | modelo–intervenção | 10 | mudança em relação ao alvo declarado |
| `efeitos-prompts-todas-referencias.csv` | modelo–intervenção–referência | 40 | mudança para Brasil, Argentina, Uruguai e RS |
| `contribuicoes-itens-deslocamentos-culturais.csv` | modelo–intervenção–item | 100 | contribuição linear de cada item aos eixos |

Os onze valores não pontuáveis do Gemini são preservados como ausentes, sem imputação.

## Experimento inicial do Sabiá-4

| Arquivo | Conteúdo |
| --- | --- |
| `auditoria-maritaca-sabia4.csv` | cem chamadas iniciais em português |
| `respostas-maritaca-sabia4.jsonl` | registros brutos normalizados |
| `respostas-maritaca-sabia4.csv` | matriz consolidada |
| `coordenadas-maritaca-sabia4-variantes.csv` | pontos por formulação |
| `metadados-experimento-maritaca-sabia4.json` | cobertura, data e configuração |

## Referências humanas

Brasil, Argentina, Uruguai e os demais países provêm das coordenadas agregadas publicadas por Tao et al. O ponto do Rio Grande do Sul foi calculado a partir do WVS Wave 7, Brasil 2018, usando `N_REGION_ISO=76021` e dez itens do mapa cultural.

Somente os seguintes agregados do RS são distribuídos:

- coordenada não ponderada: `(0,265882; 0,397699)`;
- coordenada ponderada de sensibilidade: `(0,288627; 0,424127)`;
- 151 registros identificados no estado;
- 118 casos completos;
- intervalos e covariância do bootstrap simples.

A microbase individual não é distribuída. Consulte [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Integridade

Execute:

```bash
make validate
```

O validador confere arquivos obrigatórios, contagens esperadas, sintaxe dos JSONL, ausência da microbase WVS e padrões comuns de segredos.
Ele também compara os arquivos tabulares e registros com os hashes publicados em `CHECKSUMS.sha256`.
