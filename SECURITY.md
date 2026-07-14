# Segurança e comunicação responsável

## Segredos

Nunca registre chaves de Maritaca, OpenRouter ou qualquer outro provedor em arquivos, *issues*, logs ou commits. Use somente:

- `MARITACA_API_KEY`;
- `OPENROUTER_API_KEY`.

Se uma chave for exposta, revogue-a no provedor antes de apenas removê-la do Git. A remoção de um arquivo no commit mais recente não apaga o segredo do histórico.

## Relato de vulnerabilidades

Não publique uma chave ou vulnerabilidade explorável em uma *issue*. Entre em contato privadamente com o mantenedor pelo perfil GitHub `@tioguerra`, indicando:

- arquivo e versão afetados;
- impacto provável;
- passos mínimos de reprodução, sem dados sensíveis;
- correção sugerida, se houver.

## Escopo

Os scripts de coleta podem gerar custos e enviar prompts a serviços externos. Eles nunca são executados pela integração contínua. Confira `--pilot` e `--limit` antes de iniciar uma coleta.

