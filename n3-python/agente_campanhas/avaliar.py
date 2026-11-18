"""Roda as 10 perguntas de avaliação e salva as respostas para conferência."""
import csv

from agente import perguntar

PERGUNTAS = [
    "Qual canal teve o maior CPA de 01/10 a 25/10?",
    "Quanto o Google Ads gastou de 19/10 a 25/10?",
    "Quantas conversões a campanha Meta - Remarketing teve em setembro?",
    "Qual campanha teve o menor CPA no período todo?",
    "O CPA da campanha Meta - Conversão piorou? Desde quando?",
    "Teve algum dia em que uma campanha gastou mas não converteu nada? Qual campanha e quais dias?",
    "Compare o CPA do TikTok Ads em agosto e em setembro.",
    "Qual foi o gasto total de todas as campanhas no período todo?",
    "Qual foi o CPA do Pinterest em outubro?",
    "Qual campanha mais gastou na última semana de dados?",
]

with open("resultados.csv", "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["numero", "pergunta", "resposta", "esperado", "acertou"])
    for numero, pergunta in enumerate(PERGUNTAS, start=1):
        print(f"\n{numero}. {pergunta}")
        resposta = perguntar(pergunta)
        print(resposta)
        escritor.writerow([numero, pergunta, resposta, "", ""])

print("\nRespostas salvas em resultados.csv. Preencha 'esperado' e 'acertou'.")