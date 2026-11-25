WITH thresholds AS (SELECT unnest([10000, 25000, 50000]) AS threshold)
SELECT threshold, count(*) AS observations,
       avg((charges > threshold)::INTEGER) AS proportion_above
FROM insurance CROSS JOIN thresholds GROUP BY threshold ORDER BY threshold;

WITH cutoff AS (SELECT quantile_cont(charges, 0.95) AS q95 FROM insurance)
SELECT CASE WHEN charges >= q95 THEN 'at or above p95' ELSE 'below p95' END AS segment,
       count(*) AS n, avg(age) AS mean_age, avg(bmi) AS mean_bmi,
       avg((smoker = 'yes')::INTEGER) AS smoking_share, avg(charges) AS mean_charge
FROM insurance CROSS JOIN cutoff GROUP BY segment
UNION ALL
SELECT 'overall', count(*), avg(age), avg(bmi), avg((smoker='yes')::INTEGER), avg(charges)
FROM insurance ORDER BY segment;
