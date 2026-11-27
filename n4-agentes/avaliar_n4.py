"""Roda as perguntas no agente LangGraph + MCP e salva o CSV para você corrigir.

Uso: python avaliar_n4.py              (perguntas_n4.py -> resultados_n4.csv)
     python avaliar_n4.py perguntas_n4_r2   (outro arquivo de perguntas -> resultados_n4_r2.csv)
"""
import asyncio
import csv
import importlib
import sys
import time

from grafo_mcp import construir_grafo, perguntar

nome_modulo = sys.argv[1] if len(sys.argv) > 1 else "perguntas_n4"
PERGUNTAS = importlib.import_module(nome_modulo).PERGUNTAS
SAIDA = "resultados_n4.csv" if nome_modulo == "perguntas_n4" else f"resultados_{nome_modulo.replace('perguntas_', '')}.csv"


async def main():
    try:
        grafo = await construir_grafo()
    except Exception as erro:                          # servidor MCP fora do ar ou caminho errado
        print(f"Não consegui conectar ao servidor MCP: {erro}")
        return
    linhas = []
    custo_total = 0.0

    for numero, item in enumerate(PERGUNTAS, 1):
        inicio = time.perf_counter()
        try:
            resposta, custo = await perguntar(grafo, item["pergunta"])
        except Exception as erro:                      # uma pergunta que quebra não derruba as outras
            resposta, custo = f"FALHOU: {erro}", 0.0
        segundos = round(time.perf_counter() - inicio, 1)
        custo_total += custo

        print(f"\n{numero}. {item['pergunta']}")
        print(f"   esperado: {item['gabarito']}")
        print(f"   resposta: {resposta}")
        print(f"   ({segundos}s, US$ {custo:.5f})")
        linhas.append({"n": numero, "pergunta": item["pergunta"], "gabarito": item["gabarito"],
                       "resposta": resposta, "segundos": segundos, "custo_usd": round(custo, 5),
                       "acerto": ""})                  # 1 = certo, 0.5 = parcial, 0 = errado

    with open(SAIDA, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0].keys()))
        escritor.writeheader()
        escritor.writerows(linhas)
    print(f"\nCusto total: US$ {custo_total:.5f}. Salvei {SAIDA}.")


if __name__ == "__main__":
    asyncio.run(main())