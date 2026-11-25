SELECT age_group, count(*) AS n, avg(charges) AS mean_charge
FROM insurance_segments GROUP BY age_group ORDER BY age_group;

SELECT bmi_group, count(*) AS n, avg(charges) AS mean_charge,
       median(charges) AS median_charge
FROM insurance_segments GROUP BY bmi_group ORDER BY bmi_group;

WITH segments AS (
    SELECT age_group, sex, smoker, count(*) AS n, avg(charges) AS mean_charge
    FROM insurance_segments GROUP BY age_group, sex, smoker
)
SELECT *, dense_rank() OVER (ORDER BY mean_charge DESC) AS charge_rank
FROM segments ORDER BY charge_rank, age_group, sex, smoker;
