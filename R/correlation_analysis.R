spearman_estimate <- function(x, y) {
  if (length(x) < 3 || length(unique(x)) < 2 || length(unique(y)) < 2) return(NA_real_)
  cor(x, y, method = "spearman")
}

correlation_tests <- function(d) {
  fields <- c("age", "bmi", "children")
  purrr::map_dfr(fields, function(field) {
    x <- d[[field]]
    y <- d$charges
    if (is.na(spearman_estimate(x, y))) {
      return(tibble::tibble(test = paste0("spearman_", field),
                            statistic = NA_real_, p_value = NA_real_))
    }
    result <- cor.test(x, y, method = "spearman", exact = FALSE)
    test_row(paste0("spearman_", field), result, result$estimate)
  })
}
