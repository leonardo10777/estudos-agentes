import sqlite3

con = sqlite3.connect("campanhas.db")
sql = """
    SELECT c.canal, c.nome, ROUND(SUM(m.gasto) / NULLIF(SUM(m.conversoes), 0), 2) AS cpa
    FROM metricas_diarias m
    JOIN campanhas c ON c.id = m.campanha_id
    WHERE m.data BETWEEN ? AND ? AND c.canal = ?
    GROUP BY c.nome
    ORDER BY cpa DESC
"""
for linha in con.execute(sql, ("2026-10-01", "2026-10-25", "Meta Ads")):
    print(linha)