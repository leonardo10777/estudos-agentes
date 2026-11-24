"""Cliente de teste: abre o servidor MCP de campanhas, lista e chama as ferramentas."""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVIDOR = Path(__file__).parent / "servidor_mcp.py"


async def main():
    parametros = StdioServerParameters(command=sys.executable, args=[str(SERVIDOR)])
    async with stdio_client(parametros) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            await sessao.initialize()

            lista = await sessao.list_tools()
            print("Ferramentas do servidor:")
            for ferramenta in lista.tools:
                print(f"  - {ferramenta.name}")

            print("\nChamando consultar_metricas:")
            resultado = await sessao.call_tool(
                "consultar_metricas",
                {"data_inicio": "2026-10-01", "data_fim": "2026-10-25", "canal": "Meta Ads"},
            )
            for item in resultado.content:
                print(" ", item.text.replace("\n", ""))

            print("\nChamando dias_sem_conversao:")
            resultado = await sessao.call_tool(
                "dias_sem_conversao",
                {"data_inicio": "2026-10-01", "data_fim": "2026-10-25"},
            )
            for item in resultado.content:
                print(" ", item.text.replace("\n", ""))

            print("\nChamando com campanha que não existe:")
            erro = await sessao.call_tool(
                "metricas_por_dia",
                {"campanha": "Nao existe", "data_inicio": "2026-10-01", "data_fim": "2026-10-25"},
            )
            print("isError:", erro.isError, "|", erro.content[0].text)


asyncio.run(main())