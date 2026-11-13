import csv
import sqlite3

con = sqlite3.connect("campanhas.db")
cur = con.cursor()

cur.executescript("""
DROP TABLE IF EXISTS metricas_diarias;
DROP TABLE IF EXISTS campanhas;

CREATE TABLE campanhas (
    id  INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    canal TEXT NOT NULL
);

CREATE TABLE metricas_diarias (
    campanha_id INTEGER NOT NULL REFERENCES campanhas(id),
    data        TEXT  NOT NULL,
    gasto       REAL,
    impressoes  INTEGER,
    cliques     INTEGER,
    conversoes  INTEGER,
    PRIMARY KEY (campanha_id, data)
);

CREATE INDEX idx_metricas_data ON metricas_diarias(data);
""")

with open("dados_campanhas.csv", encoding="utf-8") as arquivo:
    for linha in csv.DictReader(arquivo):
        cur.execute(
            "INSERT OR IGNORE INTO campanhas (nome, canal) VALUES (?, ?)",
            (linha["campanha"], linha["canal"]),
        )
        campanha_id = cur.execute(
            "SELECT id FROM campanhas WHERE nome = ?", (linha["campanha"],)
        ).fetchone()[0]
        cur.execute(
            "INSERT INTO metricas_diarias VALUES (?, ?, ?, ?, ?, ?)",
            (campanha_id, linha["data"], float (linha["gasto"]),
              int (linha["impressoes"]), int(linha["cliques"]), int(linha["conversoes"])),
            
        )
        
con.commit()
total = cur.execute("SELECT COUNT(*) FROM metricas_diarias").fetchone()[0]
print(f"campanhas.db criado com {total} linhas de métricas")
con.close()