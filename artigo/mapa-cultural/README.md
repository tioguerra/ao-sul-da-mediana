# Auditoria cultural dos modelos

Este diretório reúne três camadas do estudo:

1. reprodução do mapa de Tao et al. (2024) e cálculo do ponto do RS;
2. teste inicial do Sabiá-4;
3. auditoria multicondição de cinco modelos em inglês, português, identidade brasileira e identidade gaúcha.

## Comece por aqui

- [Resultados e discussão](analise-resultados-distancias-llms.md)
- [Nota metodológica multicondição](nota-metodologica-llms-multicondicao.md)
- [Guia das cinco figuras](LEIA-ME-cinco-figuras-llms.md)
- [Disponibilidade de dados no repositório](../../DATA_AVAILABILITY.md)

## Reprodução offline

Na raiz do repositório:

```bash
make cultural-maps
make distances
```

Esses comandos usam os dados já registrados e não acessam APIs. Os scripts `testar-*.py` são coletores separados, exigem chaves próprias e podem gerar custos.

## Material de terceiros

O subdiretório [`fontes/`](fontes/) contém materiais obtidos do OSF de Tao et al. Eles não estão cobertos pelas licenças gerais do projeto. Consulte [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

