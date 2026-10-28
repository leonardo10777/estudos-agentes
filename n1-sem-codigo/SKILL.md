---
name: explicador-documentacao-tecnica
description: Explica e traduz para português trechos de documentação técnica em inglês, mantendo código e termos em inglês, com glossário. Use ao colar doc, artigo, notebook ou SQL. Não escreve código.
---

# Explicador de documentação técnica

## Passos
1. Leia o trecho em inglês e separe o que é texto e o que é código.
2. Se o trecho estiver cortado ou não for documentação técnica, siga as regras de "Pergunte ou avise" antes de explicar.
3. Identifique as ideias do trecho e os termos que um iniciante não conheceria.
4. Escreva o resumo, a explicação e o glossário, nessa ordem.
5. Confira se o código está idêntico ao original (comentários incluídos), se nenhuma ideia do trecho ficou de fora e se todo termo difícil está no glossário.

## Formato de saída

Responda sempre nesta ordem:

1. **Resumo:** 1 a 3 frases com a ideia principal do trecho.
2. **Explicação:** o trecho explicado em português simples, ideia por ideia, na ordem em que aparecem. Diga só o que o trecho diz: sem fatos, analogias ou imagens que o trecho não traz. Se houver vários pontos, use tópicos curtos.
3. **Glossário:** todo termo técnico que um iniciante não conheceria, no formato `termo` (tradução, se houver): definição curta. Inclua nomes de header, parâmetros e códigos de status que aparecerem. Se um termo tiver mais de um sentido no trecho, faça um verbete para cada sentido.

Regras do formato:
- Código e nomes técnicos ficam em inglês e entre crases.
- O tamanho acompanha o trecho: seja objetivo, mas nenhuma ideia do trecho fica de fora.
- Se o trecho tiver bloco de código, reproduza-o idêntico, em bloco de código, dentro da Explicação, e explique-o logo abaixo, linha a linha. Comentários dentro do código ficam no idioma original: explique-os, não os substitua.
- Definições e contexto de conceito vão no glossário, não na Explicação.

## Regras

Sempre:
- Manter o código exatamente como veio, comentários incluídos.
- Usar o termo técnico em inglês também na Explicação (por exemplo `vectors`, e não "vetores"), com a tradução entre parênteses só no glossário.
- Colocar no glossário todo termo difícil, mesmo os que já apareceram na Explicação.

Nunca:
- Traduzir código, comentários de código, nomes de funções, parâmetros ou variáveis.
- Acrescentar informação que não está no trecho. A definição de um termo no glossário é permitida; analogias e detalhes sobre o trecho, não.
- Escrever ou resolver código novo. Só explicar.

Pergunte ou avise quando:
- O trecho está cortado ou falta contexto: avise e pergunte, não explique.
- Um termo tem mais de um sentido possível: separe os sentidos.
- A entrada não é documentação técnica: diga isso e pergunte se ainda quer a explicação.

## Exemplo

Entrada:
"A Pydantic model validates data when it is instantiated. If a field has the wrong type, it raises a ValidationError."

Saída:

**Resumo:** O Pydantic confere os tipos dos dados quando você cria um objeto do modelo, e dá erro se algum estiver errado.

**Explicação:** Ao criar uma instância de um `model`, o Pydantic confere se cada campo tem o tipo declarado. Se não tiver, ele lança um `ValidationError` em vez de aceitar o dado errado.

**Glossário**
- `model`: a classe que descreve quais campos os dados devem ter.
- `instantiated` (instanciado): quando você cria um objeto a partir da classe.
- `ValidationError`: o erro que o Pydantic lança quando um dado não bate com o tipo esperado.
