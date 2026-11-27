"""Teste das 2 falhas da rodada 2: cada pergunta 3 vezes, para ver a variação antes e depois da correção."""
ORDEM = {"pergunta": "Liste as 5 campanhas em ordem de CPA, do menor para o maior, no período todo.",
         "gabarito": "Só a lista final, na ordem: Meta - Remarketing 24,76; Google - Search 31,60; Meta - Conversão 55,63; Google - PMax 59,13; TikTok - Conversão 97,49. Sem lista errada nem correção no texto"}
EXTREMOS = {"pergunta": "Qual campanha teve o menor CPA e qual teve o maior CPA em 25/10?",
            "gabarito": "Menor: Meta - Remarketing, 26,86 (a 2ª é Google - Search, 27,73). Maior: Meta - Conversão, 122,83 (a 2ª é TikTok - Conversão, 114,53)"}
ONTEM = {"pergunta": "Qual foi o CPA de ontem?",
         "gabarito": "Avisa que assumiu 25/10 como 'ontem'. CPA 45,89 (1.560,33 de gasto, 34 conversões). Se citar menor ou maior CPA por campanha: menor Meta - Remarketing 26,86 e maior Meta - Conversão 122,83"}

PERGUNTAS = [ORDEM] * 3 + [EXTREMOS] * 3 + [ONTEM] * 3