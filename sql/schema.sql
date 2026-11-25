CREATE TABLE IF NOT EXISTS insurance (
    age INTEGER NOT NULL CHECK (age BETWEEN 18 AND 120),
    sex VARCHAR NOT NULL CHECK (sex IN ('female', 'male')),
    bmi DOUBLE NOT NULL CHECK (isfinite(bmi) AND bmi BETWEEN 10 AND 80),
    children BIGINT NOT NULL CHECK (children >= 0),
    smoker VARCHAR NOT NULL CHECK (smoker IN ('yes', 'no')),
    region VARCHAR NOT NULL CHECK (region IN ('northeast', 'northwest', 'southeast', 'southwest')),
    charges DOUBLE NOT NULL CHECK (isfinite(charges) AND charges >= 0)
);

CREATE OR REPLACE VIEW insurance_segments AS
SELECT *,
    CASE WHEN age < 30 THEN '18–29' WHEN age < 45 THEN '30–44'
         WHEN age < 60 THEN '45–59' ELSE '60+' END AS age_group,
    CASE WHEN bmi < 18.5 THEN '<18.5' WHEN bmi < 25 THEN '18.5–<25'
         WHEN bmi < 30 THEN '25–<30' ELSE '30+' END AS bmi_group
FROM insurance;
