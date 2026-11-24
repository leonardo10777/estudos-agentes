"""Servidor MCP de campanhas: expõe as consultas do banco como ferramentas."""
from mcp.server.fastmcp import FastMCP

import ferramentas

mcp = FastMCP("campanhas")


@mcp.tool()
def listar_campanhas() -> list[dict]:
    """Lista todas as campanhas e o canal de cada uma. Use para descobrir os nomes exatos."""
    return ferramentas.listar_campanhas()


@mcp.tool()
def consultar_metricas(
    data_inicio: str,
    data_fim: str,
    canal: str | None = None,
    campanha: str | None = None,
) -> list[dict]:
    """Soma gasto, cliques e conversões e calcula o CPA por campanha num período.

    Datas no formato AAAA-MM-DD. canal: 'Meta Ads', 'Google Ads' ou 'TikTok Ads'.
    campanha: nome exato, como em listar_campanhas.
    """
    return ferramentas.consultar_metricas(data_inicio, data_fim, canal, campanha)


@mcp.tool()
def metricas_por_dia(campanha: str, data_inicio: str, data_fim: str) -> list[dict]:
    """Mostra gasto, cliques e conversões dia a dia de UMA campanha.

    Use para descobrir quando um problema começou. Datas no formato AAAA-MM-DD.
    """
    return ferramentas.metricas_por_dia(campanha, data_inicio, data_fim)


@mcp.tool()
def dias_sem_conversao(data_inicio: str, data_fim: str) -> list[dict]:
    """Lista os dias em que uma campanha gastou mas teve zero conversões, de todas as campanhas, num período.

    Use para achar falhas de rastreamento. Datas no formato AAAA-MM-DD.
    """
    return ferramentas.dias_sem_conversao(data_inicio, data_fim)

if __name__ == "__main__":
    mcp.run(transport="stdio")