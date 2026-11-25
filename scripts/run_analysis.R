suppressPackageStartupMessages(library(tidyverse))
here::i_am("scripts/run_analysis.R")
root <- here::here()
for (name in c("data_validation", "exploratory_analysis", "nonparametric_tests",
               "parametric_comparison", "correlation_analysis", "effect_sizes", "visualizations")) {
  source(file.path(root, "R", paste0(name, ".R")))
}
input <- Sys.getenv("INSURANCE_CSV", file.path(root, "data", "raw", "insurance.csv"))
d <- read.csv(input, check.names = FALSE)
validate_data(d)
for (folder in c("figures", "tables", "statistical_tests")) {
  dir.create(file.path(root, "results", folder), showWarnings = FALSE, recursive = TRUE)
}
limits <- charge_fences(d$charges)
write_csv(tibble(rows = nrow(d), duplicates = sum(duplicated(d)),
                 outliers = sum(d$charges < limits[1] | d$charges > limits[2]),
                 lower = limits[1], upper = limits[2]), here::here("results/tables/r_quality.csv"))
for (field in c("smoker", "sex", "region", "overall")) {
  d$overall <- "Overall"
  write_csv(charge_summary(d, field), here::here("results/tables", paste0("r_", field, ".csv")))
}
write_csv(bind_rows(rank_tests(d), mean_tests(d), correlation_tests(d)),
          here::here("results/statistical_tests/r_tests.csv"))
write_csv(effect_intervals(d), here::here("results/statistical_tests/r_effects.csv"))
save_exploration(d, here::here("results/figures"))
