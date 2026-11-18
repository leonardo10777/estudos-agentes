"""Ferramentas que o agente pode usar para consultar o campanhas.db."""
import json
import sqlite3

BANCO = "campanhas.db"


def listar_campanhas():
    with sqlite3.connect(BANCO) as con:
        linhas = con.execute("SELECT nome, canal FROM campanhas ORDER BY canal, nome").fetchall()
    return [{"campanha": nome, "canal": canal} for nome, canal in linhas]


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


def metricas_por_dia(campanha, data_inicio, data_fim):
    sql = """
        SELECT m.data, m.gasto, m.cliques, m.conversoes
        FROM metricas_diarias m JOIN campanhas c ON c.id = m.campanha_id
        WHERE c.nome = ? AND m.data BETWEEN ? AND ?
        ORDER BY m.data
    """
    with sqlite3.connect(BANCO) as con:
        linhas = con.execute(sql, (campanha, data_inicio, data_fim)).fetchall()
    if not linhas:
        raise ValueError(f"Campanha '{campanha}' sem dados nesse período.")
    return [{"data": l[0], "gasto": l[1], "cliques": l[2], "conversoes": l[3]} for l in linhas]


def dias_sem_conversao(data_inicio, data_fim):
    sql = """
        SELECT c.nome, m.data, m.gasto
        FROM metricas_diarias m JOIN campanhas c ON c.id = m.campanha_id
        WHERE m.conversoes = 0 AND m.gasto > 0 AND m.data BETWEEN ? AND ?
        ORDER BY c.nome, m.data
    """
    with sqlite3.connect(BANCO) as con:
        linhas = con.execute(sql, (data_inicio, data_fim)).fetchall()
    return [{"campanha": l[0], "data": l[1], "gasto": l[2]} for l in linhas]


FERRAMENTAS = [
    {
        "name": "listar_campanhas",
        "description": "Lista todas as campanhas e o canal de cada uma. Use para descobrir os nomes exatos.",
        "input_schema": {"type": "object", "properties": {}},
    },
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
                "campanha": {"type": "string", "description": "Nome exato, como em listar_campanhas"},
            },
            "required": ["data_inicio", "data_fim"],
        },
    },
    {
        "name": "metricas_por_dia",
        "description": "Mostra gasto, cliques e conversões dia a dia de UMA campanha. "
                       "Use para descobrir quando um problema começou.",
        "input_schema": {
            "type": "object",
            "properties": {
                "campanha": {"type": "string"},
                "data_inicio": {"type": "string", "description": "AAAA-MM-DD"},
                "data_fim": {"type": "string", "description": "AAAA-MM-DD"},
            },
            "required": ["campanha", "data_inicio", "data_fim"],
        },
    },
    {
        "name": "dias_sem_conversao",
        "description": "Lista os dias em que uma campanha gastou mas teve zero conversões, "
                       "de todas as campanhas, num período. Use para achar falhas de rastreamento. "
                       "Datas no formato AAAA-MM-DD.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data_inicio": {"type": "string", "description": "AAAA-MM-DD"},
                "data_fim": {"type": "string", "description": "AAAA-MM-DD"},
            },
            "required": ["data_inicio", "data_fim"],
        },
    },
]

FUNCOES = {
    "listar_campanhas": listar_campanhas,
    "consultar_metricas": consultar_metricas,
    "metricas_por_dia": metricas_por_dia,
    "dias_sem_conversao": dias_sem_conversao,
}


def executar_ferramenta(nome, entrada):
    funcao = FUNCOES[nome]
    resultado = funcao(**entrada)
    return json.dumps(resultado, ensure_ascii=False)