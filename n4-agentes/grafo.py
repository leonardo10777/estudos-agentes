"""Agente de campanhas em LangGraph: modelo e ferramentas viram nós de um grafo."""
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, MessagesState, StateGraph

from config import MAX_VOLTAS, MODELO, SISTEMA
from ferramentas import FERRAMENTAS, executar_ferramenta
from util import custo_usd, texto_da

load_dotenv()

modelo = ChatAnthropic(model=MODELO, max_tokens=4096, effort="low").bind_tools(FERRAMENTAS)


def no_modelo(estado: MessagesState):
    mensagens = [SystemMessage(SISTEMA)] + estado["messages"]
    return {"messages": [modelo.invoke(mensagens)]}


def no_ferramentas(estado: MessagesState):
    respostas = []
    for chamada in estado["messages"][-1].tool_calls:
        print(f"  [ferramenta] {chamada['name']}({chamada['args']})")
        try:
            saida = executar_ferramenta(chamada["name"], chamada["args"])
            respostas.append(ToolMessage(content=saida, tool_call_id=chamada["id"]))
        except Exception as erro:
            respostas.append(ToolMessage(content=f"Erro: {erro}", tool_call_id=chamada["id"],
                                         status="error"))
    return {"messages": respostas}


def decidir(estado: MessagesState):
    """Aresta condicional: o modelo pediu ferramenta? Vai para os tools. Senão, termina."""
    return "ferramentas" if estado["messages"][-1].tool_calls else END


def construir_grafo(checkpointer=None):
    construtor = StateGraph(MessagesState)
    construtor.add_node("modelo", no_modelo)
    construtor.add_node("ferramentas", no_ferramentas)
    construtor.add_edge(START, "modelo")
    construtor.add_conditional_edges("modelo", decidir, ["ferramentas", END])
    construtor.add_edge("ferramentas", "modelo")
    return construtor.compile(checkpointer=checkpointer)


def perguntar(grafo, pergunta, config=None):
    config = dict(config or {})
    config["recursion_limit"] = 2 * MAX_VOLTAS + 1  # cada volta = 2 nós (modelo + ferramentas)
    try:
        estado = grafo.invoke({"messages": [HumanMessage(pergunta)]}, config)
    except GraphRecursionError:
        return "Parei: limite de voltas atingido sem resposta final.", 0.0
    return texto_da(estado["messages"][-1]), custo_usd(estado["messages"])


if __name__ == "__main__":
    grafo = construir_grafo()
    print(grafo.get_graph().draw_mermaid())  # o fluxograma em texto (cole em mermaid.live)
    resposta, custo = perguntar(grafo, input("Pergunta: "))
    print(resposta)
    print(f"Custo: US$ {custo:.5f}")