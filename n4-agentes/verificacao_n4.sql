.headers on
.mode column

.print "--- E3: Meta - Remarketing em setembro (esperado: gasto 4471.03, cliques 3584)"
SELECT ROUND(SUM(m.gasto),2) AS gasto, SUM(m.cliques) AS cliques FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Meta - Remarketing' AND m.data BETWEEN '2026-09-01' AND '2026-09-30';

.print "--- E5: Meta - Conversao antes e depois de 07/10 (esperado antes: gasto 28964.40, conv 582; depois: gasto 7526.91, conv 74; cliques por dia parecidos)"
SELECT CASE WHEN m.data < '2026-10-07' THEN 'antes' ELSE 'depois' END AS fase, ROUND(SUM(m.gasto),2) AS gasto, SUM(m.conversoes) AS conv, COUNT(*) AS dias, ROUND(SUM(m.cliques)*1.0/COUNT(*),1) AS cliques_por_dia FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Meta - Conversão' GROUP BY fase;

.print "--- E7: TikTok Ads em agosto e setembro (esperado ago: gasto 6143.04, conv 64; set: gasto 6080.74, conv 62)"
SELECT substr(m.data,1,7) AS mes, ROUND(SUM(m.gasto),2) AS gasto, SUM(m.conversoes) AS conv FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.canal='TikTok Ads' AND substr(m.data,1,7) IN ('2026-08','2026-09') GROUP BY mes ORDER BY mes;

.print "--- E8: gasto por campanha no periodo todo (esperado: PMax 27260.60, Search 44752.13, Meta-Conversao 36491.31, Remarketing 13495.71, TikTok 18132.77)"
SELECT c.nome, ROUND(SUM(m.gasto),2) AS gasto FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id GROUP BY c.id ORDER BY c.nome;

.print "--- E10: Google - Search na ultima semana (esperado: conv 95)"
SELECT SUM(m.conversoes) AS conv FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Google - Search' AND m.data BETWEEN '2026-10-19' AND '2026-10-25';

.print "--- E11: Google - PMax em setembro (esperado: gasto 8960.19, conv 154, cliques 6184)"
SELECT ROUND(SUM(m.gasto),2) AS gasto, SUM(m.conversoes) AS conv, SUM(m.cliques) AS cliques FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Google - PMax' AND m.data BETWEEN '2026-09-01' AND '2026-09-30';

.print "--- E13: Google - Search em setembro (esperado: gasto 15033.70, conv 501)"
SELECT ROUND(SUM(m.gasto),2) AS gasto, SUM(m.conversoes) AS conv FROM metricas_diarias m JOIN campanhas c ON c.id=m.campanha_id WHERE c.nome='Google - Search' AND m.data BETWEEN '2026-09-01' AND '2026-09-30';