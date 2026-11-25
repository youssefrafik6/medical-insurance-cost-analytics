test_row <- function(name, result, statistic = result$statistic) {
  tibble::tibble(test = name, statistic = unname(statistic), p_value = result$p.value)
}

rank_tests <- function(d) {
  rows <- list(test_row("shapiro", shapiro.test(d$charges)))
  for (field in c("smoker", "sex")) {
    rows[[length(rows) + 1]] <- test_row(paste0("wilcoxon_", field),
      wilcox.test(reformulate(field, "charges"), d, exact = FALSE, correct = TRUE))
  }
  rows[[length(rows) + 1]] <- test_row("kruskal_region", kruskal.test(charges ~ region, d))
  groups <- split(d$charges, d$region)
  pairs <- combn(names(groups), 2, simplify = FALSE)
  for (pair in pairs) {
    row <- test_row(paste(c("region", pair), collapse = "_"),
      wilcox.test(groups[[pair[1]]], groups[[pair[2]]], exact = FALSE, correct = TRUE))
    row$p_value <- min(1, length(pairs) * row$p_value)
    rows[[length(rows) + 1]] <- row
  }
  dplyr::bind_rows(rows)
}
