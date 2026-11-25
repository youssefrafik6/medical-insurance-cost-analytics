# Academic project audit

Youssef Rafik submitted *Non-Parametric Analysis of Medical Insurance Charges* for MAT 429, Modern Nonparametric Methods, at Southern Connecticut State University in Spring 2026. The report and R script in this repository are unchanged copies. The academic report is evidence of the original analysis.

The script uses ggplot2 and dplyr for summaries and visual exploration, then base R for Shapiro–Wilk, 1.5 × IQR fences, asymptotic Wilcoxon tests, Kruskal–Wallis, Bonferroni pairwise Wilcoxon, Welch t-tests, ordinary one-way ANOVA and asymptotic Spearman tests. The four research questions cover smoking status, region, sex, and monotonic associations with age, BMI and children.

The supplied CSV has 1,338 rows, seven fields and no blank cells. Age and children are integers, BMI and charges decimals, and sex, smoker and region categorical. Observed age spans 18–64, BMI 15.96–53.13, children 0–5 and charges \$1,121.87–\$63,770.43. One exact repeat is present beyond its first occurrence. Patient identifiers are absent, so the repeat is retained and assessed in sensitivity analysis.

The script uses a working-directory-relative filename and no hardcoded absolute file path. Its top-level workflow has no reusable validation, dependency lock, exported results, or automated tests. The report omits the exact repeat and calls the t-test a two-sample test without identifying the Welch default. Its claim that the rank tests are more reliable based on pooled non-normality overstates what the diagnostics establish. Rank and mean tests target different hypotheses, and pooled Shapiro–Wilk does not test equal variances or within-group residual assumptions. The original plots and results are preserved as academic context.

The expansion preserves all rows and research questions while adding explicit validation, effect sizes, uncertainty, sensitivity analysis, independent Python verification, DuckDB queries, interactive exploration, automated reporting and CI.
