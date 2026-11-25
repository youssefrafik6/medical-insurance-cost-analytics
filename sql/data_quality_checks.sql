WITH unique_rows AS (SELECT DISTINCT * FROM insurance),
quartiles AS (
    SELECT quantile_cont(charges, 0.25) AS q1, quantile_cont(charges, 0.75) AS q3
    FROM insurance
)
SELECT count(*) AS observations,
       count(*) - (SELECT count(*) FROM unique_rows) AS duplicate_rows_beyond_first,
       count(*) FILTER (WHERE charges < q1 - 1.5 * (q3-q1)
                         OR charges > q3 + 1.5 * (q3-q1)) AS iqr_outliers
FROM insurance CROSS JOIN quartiles;
