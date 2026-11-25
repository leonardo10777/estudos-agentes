"""Agente LangGraph que usa as ferramentas do servidor MCP de campanhas."""
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.errors import GraphRecursionError
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from config import MAX_VOLTAS, MODELO, SISTEMA
from util import custo_usd, texto_da

load_dotenv()

SERVIDOR = Path(__file__).parent / "servidor_mcp.py"


async def construir_grafo(checkpointer=None):
    client = MultiServerMCPClient({
        "campanhas": {
            "transport": "stdio",
            "command": sys.executable,        # o python do .venv, caminho absoluto
            "args": [str(SERVIDOR)],
        }
    })
    ferramentas = await client.get_tools()    # as ferramentas vêm do servidor, não do código
    print("Ferramentas descobertas:", [f.name for f in ferramentas])

    modelo = ChatAnthropic(model=MODELO, max_tokens=4096, effort="low").bind_tools(ferramentas)

    async def no_modelo(estado: MessagesState):
        mensagens = [SystemMessage(SISTEMA)] + estado["messages"]
        return {"messages": [await modelo.ainvoke(mensagens)]}

    construtor = StateGraph(MessagesState)
    construtor.add_node("modelo", no_modelo)
    construtor.add_node("ferramentas", ToolNode(ferramentas))   # nó pronto: executa e devolve ToolMessage
    construtor.add_edge(START, "modelo")
    construtor.add_conditional_edges("modelo", tools_condition, {"tools": "ferramentas", "__end__": "__end__"})
    construtor.add_edge("ferramentas", "modelo")
    return construtor.compile(checkpointer=checkpointer)


async def perguntar(grafo, pergunta, config=None):
    config = dict(config or {})
    config["recursion_limit"] = 2 * MAX_VOLTAS + 1
    try:
        estado = await grafo.ainvoke({"messages": [HumanMessage(pergunta)]}, config)
    except GraphRecursionError:
        return "Parei: limite de voltas atingido sem resposta final.", 0.0
    
    
    ferramentas_chamadas = []

    for mensagem in estado["messages"]:
        for chamada in getattr(mensagem, "tool_calls", []):
            ferramentas_chamadas.append(chamada["name"])

    print("Ferramentas chamadas:", ferramentas_chamadas)
    
    return texto_da(estado["messages"][-1]), custo_usd(estado["messages"])


async def main():
    grafo = await construir_grafo()
    for pergunta in [
        "Quais campanhas existem e de quais canais?",
        "Qual foi o CPA da Meta - Conversão de 01/10 a 25/10?",
        "A campanha Nao Existe gastou quanto em outubro?",
    ]:
        print("\nPergunta:", pergunta)
        resposta, custo = await perguntar(grafo, pergunta)
        print(resposta)
        print(f"Custo: US$ {custo:.5f}")


if __name__ == "__main__":
    asyncio.run(main())