-- 1. As primeiras linhas
SELECT * FROM metricas LIMIT 5;

-- 2. Quais campanhas existem
SELECT DISTINCT canal, campanha FROM metricas;

-- 3. Filtro: TikTok na última semana
SELECT data, gasto, conversoes FROM metricas
WHERE canal = 'TikTok Ads' AND data >= '2026-10-19';

-- 4. Gasto por canal, do maior para o menor
SELECT canal, ROUND(SUM(gasto), 2) AS gasto
FROM metricas GROUP BY canal ORDER BY gasto DESC;

-- 5. CPA por canal
SELECT canal, ROUND(SUM(gasto) / NULLIF(SUM(conversoes), 0), 2) AS cpa
FROM metricas GROUP BY canal ORDER BY cpa DESC;

-- 6. CPA por campanha, só em outubro
SELECT campanha, ROUND(SUM(gasto) / NULLIF(SUM(conversoes), 0), 2) AS cpa
FROM metricas
WHERE data >= '2026-10-01'
GROUP BY campanha
ORDER BY cpa DESC;

-- 7. Dias com gasto acima de 100 e zero conversões (acha o problema 2)
SELECT data, campanha, gasto, conversoes
FROM metricas
WHERE gasto > 100 AND conversoes = 0;

-- 8. CPA da Meta - Conversão antes e depois de 07/10 (acha o problema 1)
SELECT CASE WHEN data >= '2026-10-07' THEN 'depois' ELSE 'antes' END AS periodo,
       ROUND(SUM(gasto) / NULLIF(SUM(conversoes), 0), 2) AS cpa
FROM metricas
WHERE campanha = 'Meta - Conversão'
GROUP BY periodo;

-- 9. Os 5 dias com mais conversões (desempate pela data)
SELECT data, SUM(conversoes) AS total_conversoes
FROM metricas
GROUP BY data
ORDER BY total_conversoes DESC, data
LIMIT 5;

-- 10. Gasto médio por canal (AVG = média por linha, ou seja, por campanha em um dia)
SELECT canal, ROUND(AVG(gasto), 2) AS gasto_medio
FROM metricas
GROUP BY canal;