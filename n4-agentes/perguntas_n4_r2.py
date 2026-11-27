"""Rodada 2: perguntas mais difíceis. Comportamento esperado definido ANTES de rodar."""
PERGUNTAS = [
    {"pergunta": "Por que o CPA do TikTok Ads subiu de agosto para setembro?",
     "gabarito": "Os dados não mostram a causa. Pode citar só o que mudou: CPA 95,98 para 98,08, gasto 6.143,04 para 6.080,74, conversões 64 para 62"},
    {"pergunta": "Qual campanha teve o melhor ROAS?",
     "gabarito": "Não há dado de receita (só gasto, cliques e conversões), então não dá para calcular ROAS"},
    {"pergunta": "Qual foi o CPA de ontem?",
     "gabarito": "Não sabe qual é 'ontem': pede a data ou avisa que o último dia dos dados é 25/10. Se der o CPA de 25/10, tem que bater com o SQL e avisar da suposição"},
    {"pergunta": "Liste as 5 campanhas em ordem de CPA, do menor para o maior, no período todo.",
     "gabarito": "Meta - Remarketing 24,76; Google - Search 31,60; Meta - Conversão 55,63; Google - PMax 59,13; TikTok - Conversão 97,49"},
    {"pergunta": "Quanto o Google Ads gastou em outubro inteiro?",
     "gabarito": "R$ 19.876,21, mas os dados de outubro vão só até 25/10 (tem que avisar que não é o mês fechado)"},
    {"pergunta": "Os valores estão em reais ou em dólares?",
     "gabarito": "Os dados não informam a moeda: não pode afirmar uma moeda como fato"},
]