SELECT smoker, count(*) AS n, avg(charges) AS mean_charge, median(charges) AS median_charge
FROM insurance GROUP BY smoker ORDER BY smoker;

SELECT smoker, bmi_group, count(*) AS n, avg(charges) AS mean_charge,
       median(charges) AS median_charge
FROM insurance_segments GROUP BY smoker, bmi_group ORDER BY smoker, bmi_group;

SELECT smoker, age_group, count(*) AS n, avg(charges) AS mean_charge
FROM insurance_segments GROUP BY smoker, age_group ORDER BY smoker, age_group;
