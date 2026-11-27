"""Crew de 2 agentes: o analista consulta os dados e o redator escreve o relatório."""
import json
import os

from crewai import LLM, Agent, Crew, Task
from crewai.tools import tool
from dotenv import load_dotenv

import ferramentas

load_dotenv()

llm = LLM(
    model="anthropic/claude-haiku-5-5",
    max_tokens=2048,
    base_url=os.getenv("ANTHROPIC_BASE_URL_TESTE"),   # vazio = API normal; só para teste local
)


@tool("consultar_metricas")
def consultar_metricas(data_inicio: str, data_fim: str) -> str:
    """Soma gasto, cliques e conversões e calcula o CPA por campanha. Datas AAAA-MM-DD."""
    try:
        return json.dumps(ferramentas.consultar_metricas(data_inicio, data_fim), ensure_ascii=False)
    except ValueError as erro:
        return f"Erro: {erro}"


analista = Agent(
    role="Analista de mídia paga",
    goal="Descobrir quais campanhas tiveram o pior CPA e quanto gastaram",
    backstory="Analista que só afirma o que os dados mostram e nunca inventa números.",
    tools=[consultar_metricas],
    llm=llm,
    verbose=True,
)
redator = Agent(
    role="Redator de relatórios",
    goal="Transformar os achados do analista em um relatório curto para o cliente",
    backstory="Escreve em português, direto, sem exagero e sem números além dos recebidos.",
    llm=llm,
    verbose=True,
)

analisar = Task(
    description="Consulte as métricas de {inicio} a {fim} e aponte as 2 campanhas com maior CPA.",
    expected_output="Lista com as 2 campanhas, CPA e gasto de cada uma.",
    agent=analista,
)
escrever = Task(
    description="Escreva um relatório de até 5 linhas com os achados do analista.",
    expected_output="Relatório de até 5 linhas, em português.",
    agent=redator,
    context=[analisar],
)

crew = Crew(agents=[analista, redator], tasks=[analisar, escrever], verbose=True)

if __name__ == "__main__":
    resultado = crew.kickoff(inputs={"inicio": "2026-10-01", "fim": "2026-10-25"})
    print("\n=== RELATÓRIO ===\n", resultado)