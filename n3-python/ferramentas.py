"""Ferramentas que o agente pode usar para consultar o campanhas.db."""
import json
import sqlite3

BANCO = "campanhas.db"


def consultar_metricas(data_inicio, data_fim, canal=None, campanha=None):
    sql = """
        SELECT c.canal, c.nome, ROUND(SUM(m.gasto), 2), SUM(m.cliques), SUM(m.conversoes),
               ROUND(SUM(m.gasto) / NULLIF(SUM(m.conversoes), 0), 2)
        FROM metricas_diarias m JOIN campanhas c ON c.id = m.campanha_id
        WHERE m.data BETWEEN ? AND ?
    """
    parametros = [data_inicio, data_fim]
    if canal:
        sql += " AND c.canal = ?"
        parametros.append(canal)
    if campanha:
        sql += " AND c.nome = ?"
        parametros.append(campanha)
    sql += " GROUP BY c.nome ORDER BY c.canal, c.nome"

    with sqlite3.connect(BANCO) as con:
        linhas = con.execute(sql, parametros).fetchall()
    if not linhas:
        raise ValueError("Nenhum dado para esse filtro. Confira datas, canal e nome da campanha.")
    return [
        {"canal": l[0], "campanha": l[1], "gasto": l[2], "cliques": l[3],
         "conversoes": l[4], "cpa": l[5]}
        for l in linhas
    ]


FERRAMENTAS = [
    {
        "name": "consultar_metricas",
        "description": "Soma gasto, cliques e conversões e calcula o CPA por campanha num período. "
                       "Filtros opcionais por canal ou campanha. Datas no formato AAAA-MM-DD.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data_inicio": {"type": "string", "description": "AAAA-MM-DD"},
                "data_fim": {"type": "string", "description": "AAAA-MM-DD"},
                "canal": {"type": "string", "enum": ["Meta Ads", "Google Ads", "TikTok Ads"]},
                "campanha": {"type": "string", "description": "Nome exato da campanha"},
            },
            "required": ["data_inicio", "data_fim"],
        },
    },
]

FUNCOES = {"consultar_metricas": consultar_metricas}


def executar_ferramenta(nome, entrada):
    funcao = FUNCOES[nome]
    resultado = funcao(**entrada)
    return json.dumps(resultado, ensure_ascii=False)