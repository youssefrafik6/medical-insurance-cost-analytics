SELECT region, count(*) AS n, avg(charges) AS mean_charge, median(charges) AS median_charge,
       stddev_samp(charges) AS sd_charge, avg((smoker = 'yes')::INTEGER) AS smoking_share
FROM insurance GROUP BY region ORDER BY region;
