mean_tests <- function(d) {
  ordinary <- broom::tidy(aov(charges ~ region, d))[1, ]
  dplyr::bind_rows(
    test_row("welch_smoker", t.test(charges ~ smoker, d)),
    test_row("welch_sex", t.test(charges ~ sex, d)),
    tibble::tibble(test = "anova_region", statistic = ordinary$statistic,
                   p_value = ordinary$p.value),
    test_row("welch_region", oneway.test(charges ~ region, d))
  )
}
