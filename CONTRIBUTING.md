# Como contribuir

Contribuições são bem-vindas quando aumentam a verificabilidade, corrigem erros ou ampliam a cobertura cultural sem apagar a proveniência dos dados.

## Antes de abrir uma alteração

1. Abra uma *issue* descrevendo o problema, a fonte e o efeito esperado.
2. Não inclua chaves, tokens, dados pessoais ou microdados do WVS.
3. Para um resultado científico novo, informe desenho, amostra, versão do modelo, data e limitações.
4. Mantenha achados observados separados de inferências e hipóteses.

## Ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make check
```

## Pull requests

- Use mudanças pequenas e rastreáveis.
- Atualize documentação e tabelas afetadas.
- Não regenere respostas de API para “corrigir” recusas ou valores inconvenientes.
- Informe custos e provedores quando houver novas chamadas.
- Execute `make check` antes de enviar.
- Confirme que possui direito de redistribuir qualquer dado externo acrescentado.

Ao contribuir, você concorda em licenciar código original sob MIT e conteúdo original sob CC BY-NC 4.0, salvo acordo explícito diferente.

