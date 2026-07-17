# Sondagem ilustrativa: cardápio de intervalo em quatro condições de prompt

Em 16 de julho de 2026, quatro modelos de fronteira receberam o mesmo pedido, um cardápio de intervalo para dois visitantes estrangeiros na universidade em julho, em quatro formulações:

| Arquivo | Língua e registro | Lugar no prompt | Uso no artigo |
| --- | --- | --- | --- |
| `CoffeeBreakTest1.json` | português, coloquial gaúcho ("tchê", "guris", "tri") | implícito, pelo dialeto | condição 1 (3 respostas válidas) |
| `CoffeeBreakTest1B.json` | idem (nova consulta, mesmo dia) | idem | condição 1 (resposta do Gemini, após falha na primeira consulta) |
| `CoffeeBreakTest2.json` | português, formal | ausente | condição 2 |
| `CoffeeBreakTest3.json` | inglês | explícito ("here in RS, Brazil") | não usada no artigo (preservada como dado bruto) |
| `CoffeeBreakTest4.json` | inglês | ausente | condição 3 |

Modelos consultados por condição, em interface multimodelo, com os aliases mais recentes de cada família: Claude Opus Latest, Google Gemini Pro Latest, Grok 4.20, OpenAI GPT Latest. Uma resposta por combinação. Na primeira consulta da condição 1, o Gemini não produziu resposta final (o registro preserva apenas o traço de raciocínio); uma segunda consulta no mesmo dia (`CoffeeBreakTest1B.json`) completou a célula. O artigo usa as condições 1, 2 e 4 (n=4 em cada); a condição em inglês com RS explícito fica preservada como dado bruto.

Os arquivos são exportações brutas das conversas. A sondagem é ilustrativa: uma resposta por célula não sustenta inferência, e os aliases apontam para versões que mudam sem aviso.

## Achados centrais (contagem de modelos que mencionam, sobre as respostas válidas)

- **A estação muda de hemisfério com a língua.** Português (condições 1 e 2): julho tratado como inverno. Inglês sem lugar: julho tratado como verão ("light, summery"; "suitable for summer weather"; melancia, café gelado).
- **chimarrão e cuca**: 4/4 na condição gaúcha; zero nas demais. A bebida sempre com o nome rio-grandense, nunca o "mate" corrente no Uruguai e na Argentina.
- **negrinho**: 1 modelo, apenas sob o dialeto gaúcho (em vez de brigadeiro); **pinhão**: 1 modelo, idem.
- **brigadeiro e pão de queijo**: presentes nas duas condições em português; ausentes em inglês sem lugar.
- **hummus, wraps, frutas de verão**: dominam a condição em inglês; hummus também aparece no português formal (3/4) como opção "internacional".
