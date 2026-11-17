# Problemas plantados nos dados sintéticos

Arquivo gerado por `gerar_dados.py` (`random.seed(42)`, 90 dias, de 28/07/2026 a 25/10/2026, 5 campanhas, 450 linhas).
Este arquivo é o gabarito das sessões 18, 22 e 26: o agente precisa achar esses dois problemas sozinho.

## Problema 1: queda de conversão

- **Campanha:** Meta - Conversão (Meta Ads)
- **Quando:** de 07/10/2026 até o fim dos dados (25/10/2026)
- **O que acontece:** a taxa de conversão cai pela metade (de 3,0% para 1,5%). O gasto e os cliques continuam normais, as conversões caem e o CPA praticamente dobra.
- **Como aparece nos dados:** gasto estável, cliques estáveis, conversões e CPA mudando a partir de 07/10.
- **Resposta esperada do agente:** o CPA do Meta - Conversão piorou a partir de 07/10 por queda na taxa de conversão, e não por aumento de gasto.

## Problema 2: tag de conversão quebrada

- **Campanha:** Google - Search (Google Ads)
- **Quando:** de 16/10/2026 a 19/10/2026 (4 dias)
- **O que acontece:** gasto e cliques normais, mas zero conversões.
- **Causa simulada:** a tag de conversão parou de registrar.
- **Como aparece nos dados:** 4 linhas seguidas com `conversoes = 0` e gasto normal. O CPA desses dias é indefinido (divisão por zero).
- **Resposta esperada do agente:** nesses dias o CPA é indefinido, e o mais provável é um problema de rastreamento, e não de desempenho.

## Para completar depois da sessão 18

Quando você tiver as consultas SQL, anote aqui os valores reais: CPA do Meta - Conversão antes e depois de 07/10, e as 4 datas com zero conversões no Google - Search.