"""Agente com memória: o histórico fica salvo no SQLite e sobrevive ao fechar o programa."""
import sys

from langgraph.checkpoint.sqlite import SqliteSaver

from grafo import construir_grafo, perguntar
from util import custo_usd


conversa = sys.argv[1] if len(sys.argv) > 1 else "conversa-1"

with SqliteSaver.from_conn_string("memoria.db") as memoria:
    grafo = construir_grafo(checkpointer=memoria)
    config = {"configurable": {"thread_id": conversa}}

    # Lê as mensagens que já estavam salvas nessa conversa.
    guardadas = grafo.get_state(config).values.get("messages", [])
    print(f"Conversa '{conversa}': {len(guardadas)} mensagens guardadas.")

    # Calcula o custo que a conversa já tinha antes da próxima pergunta.
    custo_anterior = custo_usd(guardadas)

    while True:
        pergunta = input("\nPergunta (Enter vazio sai): ").strip()
        if not pergunta:
            break

        # A função perguntar devolve o custo acumulado das mensagens do estado.
        resposta, custo_acumulado = perguntar(grafo, pergunta, config)

        # A diferença corresponde ao custo da pergunta atual.
        custo_pergunta = custo_acumulado - custo_anterior

        # Guarda o novo acumulado para comparar com a próxima pergunta.
        custo_anterior = custo_acumulado

        total = len(grafo.get_state(config).values["messages"])

        print(resposta)
        print(
            f"Custo da pergunta: US$ {custo_pergunta:.5f} | "
            f"Custo acumulado: US$ {custo_acumulado:.5f} | "
            f"Mensagens na memória: {total}"
        )