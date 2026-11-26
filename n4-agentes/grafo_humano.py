"""Humano no loop: o agente pausa e pede aprovação antes de enviar o relatório."""
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command, interrupt

from config import MODELO, SISTEMA
from ferramentas import FERRAMENTAS, executar_ferramenta
from util import texto_da

load_dotenv()

ENVIAR = {
    "name": "enviar_relatorio",
    "description": "Envia o relatório pronto para a equipe. Só chame depois de ter os números.",
    "input_schema": {
        "type": "object",
        "properties": {
            "texto": {
                "type": "string",
                "description": "Texto do relatório",
            }
        },
        "required": ["texto"],
    },
}

# Ações que exigem aprovação humana.
SENSIVEIS = {"enviar_relatorio"}

modelo = ChatAnthropic(
    model=MODELO,
    max_tokens=4096,
    effort="low",
).bind_tools(FERRAMENTAS + [ENVIAR])


def executar(nome, entrada):
    if nome == "enviar_relatorio":
        # Simula o envio gravando o relatório em um arquivo.
        with open("relatorio_enviado.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(entrada["texto"])
        return "Relatório enviado."

    return executar_ferramenta(nome, entrada)


def no_modelo(estado: MessagesState):
    mensagens = [SystemMessage(SISTEMA)] + estado["messages"]
    return {"messages": [modelo.invoke(mensagens)]}


def decidir(estado: MessagesState):
    chamadas = estado["messages"][-1].tool_calls

    if not chamadas:
        return END

    if any(c["name"] in SENSIVEIS for c in chamadas):
        return "aprovacao"

    return "ferramentas"


def no_aprovacao(estado: MessagesState):
    """Pausa aqui e recebe a decisão humana ao retomar."""
    chamadas = estado["messages"][-1].tool_calls

    decisao = interrupt({
        "pergunta": "Aprovar o envio?",
        "acoes": [
            {"ferramenta": c["name"], "entrada": c["args"]}
            for c in chamadas
            if c["name"] in SENSIVEIS
        ],
    })

    if decisao["aprovado"]:
        return Command(goto="ferramentas")

    motivo = decisao["motivo"]

    recusas = [
        ToolMessage(
            content=(
                f"O usuário recusou esta ação. "
                f"Motivo: {motivo}. Não foi executada."
            ),
            tool_call_id=c["id"],
            status="error",
        )
        for c in chamadas
    ]

    return Command(goto="modelo", update={"messages": recusas})


def no_ferramentas(estado: MessagesState):
    respostas = []

    for chamada in estado["messages"][-1].tool_calls:
        print(f"  [ferramenta] {chamada['name']}")

        try:
            saida = executar(chamada["name"], chamada["args"])
            respostas.append(
                ToolMessage(
                    content=saida,
                    tool_call_id=chamada["id"],
                )
            )
        except Exception as erro:
            respostas.append(
                ToolMessage(
                    content=f"Erro: {erro}",
                    tool_call_id=chamada["id"],
                    status="error",
                )
            )

    return {"messages": respostas}


def construir_grafo():
    construtor = StateGraph(MessagesState)

    construtor.add_node("modelo", no_modelo)
    construtor.add_node("aprovacao", no_aprovacao)
    construtor.add_node("ferramentas", no_ferramentas)

    construtor.add_edge(START, "modelo")
    construtor.add_conditional_edges(
        "modelo",
        decidir,
        ["ferramentas", "aprovacao", END],
    )
    construtor.add_edge("ferramentas", "modelo")

    # O checkpointer guarda o estado necessário para pausar e retomar.
    return construtor.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    grafo = construir_grafo()

    config = {
        "configurable": {"thread_id": "relatorio-1"},
        "recursion_limit": 25,
    }

    pedido = "Resuma o CPA por campanha de 01/10 a 25/10 e envie o relatório."

    grafo.invoke({"messages": [HumanMessage(pedido)]}, config)

    # Continua enquanto houver uma etapa pendente.
    while grafo.get_state(config).next:
        pausa = grafo.get_state(config).tasks[0].interrupts[0].value
        print("\nO agente pediu aprovação:", pausa)

        resposta = input("Aprovar? (sim/nao): ").strip().lower()

        if resposta == "sim":
            decisao = {"aprovado": True}
        else:
            motivo = input("Qual o motivo da recusa? ").strip()
            decisao = {"aprovado": False, "motivo": motivo}
            print(f"Motivo informado: {motivo}")

        # Envia a decisão de volta ao interrupt e retoma o grafo.
        grafo.invoke(Command(resume=decisao), config)

    ultima_mensagem = grafo.get_state(config).values["messages"][-1]
    print("\nResposta final:", texto_da(ultima_mensagem))