"""Provoca falhas de propósito e mostra como o agente reage."""
import asyncio

from grafo_mcp import construir_grafo, perguntar

CENARIOS = [
    ("Campanha inexistente", "Quanto a campanha Nao Existe gastou em outubro?"),
    ("Período sem dados", "Qual foi o gasto total de todas as campanhas em janeiro de 2026?"),
]


async def main():
    try:
        grafo = await construir_grafo()
    except Exception as erro:
        print(f"Não consegui conectar ao servidor MCP: {erro}")
        return

    for nome, pergunta in CENARIOS:
        print(f"\n=== {nome}\nPergunta: {pergunta}")
        resposta, custo = await perguntar(grafo, pergunta)
        print(resposta)
        print(f"Custo: US$ {custo:.5f}")


if __name__ == "__main__":
    asyncio.run(main())