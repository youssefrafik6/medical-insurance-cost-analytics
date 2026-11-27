# Methodology

Both pipelines require a nonempty dataset with exactly seven canonical fields and no missing or nonfinite values. Age must be a whole number from 18–120, BMI 10–80, children a nonnegative integer, and charges nonnegative. Categorical values must match the labels in [the data dictionary](../data/README.md). The age and BMI bounds are plausibility checks for this educational dataset. Exact repeats and records outside 1.5 × IQR fences are flagged and retained.

The primary unit is the source row. Group tables report counts, means, medians, sample SD, quartiles and IQR. Python adds sample variance, adjusted Fisher–Pearson skewness, the number beyond pooled fences and smoking prevalence. DuckDB loads validated data transactionally and provides age bands, BMI bands and aggregate queries. BMI bands are descriptive and provide no clinical classification of individual records.

The two-sided tests mirror the academic analysis, including Welch t-tests and ordinary ANOVA, and add Welch ANOVA. Rank-biserial effect is 2U/(n₁n₂) − 1, oriented smokers minus nonsmokers and male minus female. Ties count as half a win in U. Raw median and mean differences use the same orientation. Regional rank eta-squared is max(0, (H − k + 1)/(n − k)); the estimate is reported without an interval.

In R and Python, Wilcoxon/Mann–Whitney is explicitly asymptotic with continuity correction and tie-adjusted variance. The reported U is for the alphabetically first group, while directed effects use the comparisons above. Spearman uses average ranks and approximate t p-values. The printed R threshold of 2.2e−16 is a display convention. Exports retain the calculated values.

The verification table compares matched point estimates, test statistics and p-values at relative tolerance 2 × 10⁻⁶ and zero absolute tolerance. This preserves discrimination for very small positive p-values. Two-sided alternatives, group orientation and Bonferroni scope are explicit. Different software defaults can select exact tests, omit a continuity correction or use a different rank convention, especially with ties. The two seeded bootstraps use independent implementation-specific random streams, so intervals are published side by side as separate artifacts.

See [Statistical assumptions](STATISTICAL_ASSUMPTIONS.md), [Findings and sensitivity](KEY_FINDINGS.md) and [Limitations](LIMITATIONS.md).

## Reproduction and verification

Follow the [local reproduction commands](../README.md#reproduce-locally) with an authorized CSV. Independent R and Python runs on all 1,338 observations agreed within tolerance on 17 paired test statistics and p-values and 10 effect estimates. DuckDB executed all 10 bundled queries. Quarto 1.6.42 produced standalone HTML and a five-page Typst PDF on arm64 macOS with Python 3.13.2 and R 4.5.2. The source CSV and local database are excluded from version control.
