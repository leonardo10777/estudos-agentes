"""Gera dados sintéticos de campanhas, com 2 problemas plantados."""
import csv
import random
from datetime import date, timedelta

random.seed(42)  # mesma semente = mesmos dados toda vez

INICIO = date(2026, 7, 28)
DIAS = 90

# canal, campanha, gasto médio/dia, CPM, CTR, taxa de conversão
CAMPANHAS = [
    ("Meta Ads", "Meta - Conversão", 400, 18.0, 0.012, 0.030),
    ("Meta Ads", "Meta - Remarketing", 150, 25.0, 0.020, 0.050),
    ("Google Ads", "Google - Search", 500, 60.0, 0.050, 0.040),
    ("Google Ads", "Google - PMax", 300, 22.0, 0.015, 0.025),
    ("TikTok Ads", "TikTok - Conversão", 200, 9.0, 0.008, 0.012),
]

linhas = []
for dia in range(DIAS):
    data = INICIO + timedelta(days=dia)
    for canal, campanha, gasto_medio, cpm, ctr, cvr in CAMPANHAS:
        gasto = round(gasto_medio * random.uniform(0.85, 1.15), 2)
        impressoes = int(gasto / cpm * 1000)
        cliques = int(impressoes * ctr * random.uniform(0.9, 1.1))

        # PROBLEMA 1: a partir de 07/10, a conversão do Meta - Conversão cai pela metade
        if campanha == "Meta - Conversão" and data >= date(2026, 10, 7):
            cvr_dia = cvr * 0.5
        else:
            cvr_dia = cvr
        conversoes = round(cliques * cvr_dia * random.uniform(0.85, 1.15))

        # PROBLEMA 2: de 16/10 a 19/10, a tag do Google - Search quebra (gasto normal, zero conversões)
        if campanha == "Google - Search" and date(2026, 10, 16) <= data <= date(2026, 10, 19):
            conversoes = 0

        linhas.append({
            "data": data.isoformat(),
            "canal": canal,
            "campanha": campanha,
            "gasto": gasto,
            "impressoes": impressoes,
            "cliques": cliques,
            "conversoes": conversoes,
        })

with open("dados_campanhas.csv", "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
    escritor.writeheader()
    escritor.writerows(linhas)

print(f"{len(linhas)} linhas salvas em dados_campanhas.csv")