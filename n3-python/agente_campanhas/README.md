# Agente de Inteligência de Campanhas

Agente de IA que responde perguntas sobre campanhas de mídia paga (Meta, Google e TikTok), como "por que o CPA subiu?". Ele consulta um banco SQLite por meio de ferramentas e responde usando só os números que elas devolvem.

Os dados são **sintéticos**: gerados por script (`random.seed(42)`) para desenvolver e avaliar o agente. Não há dados de clientes neste repositório.

## Como funciona

- Modelo: `claude-haiku-5-5`, pela API da Anthropic.
- O agente roda em loop: o modelo pede uma ferramenta, o código executa, devolve o resultado e o modelo decide se responde ou consulta de novo. O limite é de 8 voltas (`MAX_VOLTAS`).
- Erros de ferramenta voltam para o modelo. Falhas temporárias da API têm retries automáticos, e falhas permanentes (como chave errada) viram mensagem clara.
- Cada volta é registrada em `log_agente.jsonl` (tokens, ferramentas e tempo). O custo da pergunta aparece na tela.

## Como rodar

Todos os comandos partem da raiz do repositório.

1. Ative o ambiente virtual do projeto e instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Crie um arquivo `.env` com a sua chave, seguindo o modelo do `.env.example`:
   ```
   ANTHROPIC_API_KEY=...
   ```
   O `.env` não vai para o GitHub. Nunca coloque a chave em outro arquivo.
3. Entre na pasta do projeto:
   ```
   cd n3-python/agente_campanhas
   ```
4. Gere os dados sintéticos (cria `dados_campanhas.csv`):
   ```
   python gerar_dados.py
   ```
5. Carregue os dados no banco (cria `campanhas.db`):
   ```
   python carregar_banco.py
   ```
6. Rode o agente e digite uma pergunta:
   ```
   python agente.py
   ```

## Dados

- Período: 28/07/2026 a 25/10/2026 (90 dias).
- 5 campanhas: Meta - Conversão, Meta - Remarketing, Google - Search, Google - PMax e TikTok - Conversão.
- 450 linhas de métricas diárias.
- Banco: tabela `campanhas` (id, nome, canal) e tabela `metricas_diarias` (campanha_id, data, gasto, impressoes, cliques, conversoes).

## Ferramentas

- `listar_campanhas`: lista as campanhas que existem e o canal de cada uma.
- `consultar_metricas`: devolve gasto, cliques, conversões e CPA de um período, filtrando por canal ou por campanha (`data_inicio`, `data_fim`, `canal`, `campanha`).
- `metricas_por_dia`: devolve as métricas de uma campanha dia a dia, para achar quando algo mudou.

As consultas ao banco são prontas e testadas. O modelo escolhe os parâmetros, mas não escreve SQL.

## Problemas plantados nos dados

Os dados têm dois problemas conhecidos, para testar se o agente encontra a causa certa.

### Problema 1: queda de conversão

- **Campanha:** Meta - Conversão (Meta Ads)
- **Quando:** de 07/10/2026 até o fim dos dados (25/10/2026)
- **O que acontece:** a taxa de conversão cai pela metade (de 3,0% para 1,5%). O gasto e os cliques continuam normais, as conversões caem e o CPA praticamente dobra.

### Problema 2: tag de conversão quebrada

- **Campanha:** Google - Search (Google Ads)
- **Quando:** de 16/10/2026 a 19/10/2026 (4 dias)
- **O que acontece:** gasto e cliques normais, mas zero conversões. O CPA desses dias é indefinido (divisão por zero).
- **Causa simulada:** a tag de conversão parou de registrar.

## Avaliação

A taxa de acerto do agente será medida na sessão 26 e registrada aqui.