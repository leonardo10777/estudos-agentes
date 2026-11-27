.headers on
.mode column

.print "--- Q1: canal com maior CPA, 01/10 a 25/10"
SELECT c.canal, ROUND(SUM(m.gasto),2) AS gasto, SUM(m.conversoes) AS conv, ROUND(SUM(m.gasto)/SUM(m.conversoes),2) AS cpa FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE m.data BETWEEN '2026-10-01' AND '2026-10-25' GROUP BY c.canal ORDER BY cpa DESC;

.print "--- Q2: gasto do Google Ads, 19/10 a 25/10"
SELECT ROUND(SUM(m.gasto),2) AS gasto FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.canal='Google Ads' AND m.data BETWEEN '2026-10-19' AND '2026-10-25';

.print "--- Q3: conversoes da Meta - Remarketing em setembro"
SELECT SUM(m.conversoes) AS conversoes FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Meta - Remarketing' AND m.data BETWEEN '2026-09-01' AND '2026-09-30';

.print "--- Q4: CPA por campanha no periodo todo (menor primeiro)"
SELECT c.nome, ROUND(SUM(m.gasto)/SUM(m.conversoes),2) AS cpa FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id GROUP BY c.id ORDER BY cpa;

.print "--- Q5a: Meta - Conversao, conversoes por dia de 01/10 a 12/10 (procure a queda)"
SELECT m.data, m.gasto, m.conversoes FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Meta - Conversão' AND m.data BETWEEN '2026-10-01' AND '2026-10-12' ORDER BY m.data;

.print "--- Q5b: Meta - Conversao, CPA antes e depois de 07/10"
SELECT CASE WHEN m.data < '2026-10-07' THEN 'antes de 07/10' ELSE 'a partir de 07/10' END AS fase, ROUND(SUM(m.gasto)/SUM(m.conversoes),2) AS cpa, COUNT(*) AS dias FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Meta - Conversão' GROUP BY fase;

.print "--- Q6: dias com gasto e zero conversoes, periodo todo"
SELECT c.nome, m.data, m.gasto FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE m.conversoes=0 AND m.gasto>0 ORDER BY c.nome, m.data;

.print "--- Q7: CPA do TikTok Ads em agosto e setembro"
SELECT substr(m.data,1,7) AS mes, ROUND(SUM(m.gasto)/SUM(m.conversoes),2) AS cpa FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.canal='TikTok Ads' AND substr(m.data,1,7) IN ('2026-08','2026-09') GROUP BY mes ORDER BY mes;

.print "--- Q8: gasto total de todas as campanhas, periodo todo"
SELECT ROUND(SUM(gasto),2) AS gasto_total FROM metricas_diarias;

.print "--- Q9: existe Pinterest? (0 = nao existe)"
SELECT COUNT(*) AS campanhas_pinterest FROM campanhas WHERE canal LIKE '%Pinterest%' OR nome LIKE '%Pinterest%';

.print "--- Q10: gasto por campanha na ultima semana de dados (19/10 a 25/10)"
SELECT c.nome, ROUND(SUM(m.gasto),2) AS gasto FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE m.data BETWEEN '2026-10-19' AND '2026-10-25' GROUP BY c.id ORDER BY gasto DESC;

.print "--- N1 (nova): CPA da Google - PMax em setembro"
SELECT ROUND(SUM(m.gasto)/SUM(m.conversoes),2) AS cpa FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Google - PMax' AND m.data BETWEEN '2026-09-01' AND '2026-09-30';

.print "--- N2 (nova): cliques do TikTok Ads, 01/10 a 25/10"
SELECT SUM(m.cliques) AS cliques FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.canal='TikTok Ads' AND m.data BETWEEN '2026-10-01' AND '2026-10-25';

.print "--- N3 (nova): CPA da Google - Search em setembro e em outubro (ate 25/10)"
SELECT substr(m.data,1,7) AS mes, ROUND(SUM(m.gasto)/SUM(m.conversoes),2) AS cpa FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Google - Search' AND substr(m.data,1,7) IN ('2026-09','2026-10') GROUP BY mes ORDER BY mes;