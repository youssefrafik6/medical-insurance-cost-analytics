two_group_effects <- function(a, b) {
  ranks <- rank(c(a, b))
  u <- sum(ranks[seq_along(a)]) - length(a) * (length(a) + 1) / 2
  c(2 * u / (length(a) * length(b)) - 1, median(a) - median(b), mean(a) - mean(b))
}

effect_intervals <- function(d, repeats = 2000L, seed = 429L) {
  set.seed(seed)
  row <- function(label, estimate, draws = numeric()) {
    valid <- draws[is.finite(draws)]
    limits <- if (length(valid)) quantile(valid, c(.025, .975)) else c(NA_real_, NA_real_)
    tibble::tibble(effect = label, estimate = estimate, lower = limits[1],
                   upper = limits[2], valid_replicates = length(valid))
  }
  groups <- list(smoker = c("yes", "no"), sex = c("male", "female"))
  tables <- purrr::imap(groups, function(labels, field) {
    a <- d$charges[d[[field]] == labels[1]]
    b <- d$charges[d[[field]] == labels[2]]
    if (!length(a) || !length(b)) return(NULL)
    point <- two_group_effects(a, b)
    draws <- replicate(repeats, two_group_effects(
      a[sample.int(length(a), replace = TRUE)], b[sample.int(length(b), replace = TRUE)]
    ))
    names <- paste(field, c("rank_biserial", "median_difference", "mean_difference"), sep = "_")
    purrr::map_dfr(seq_along(names), function(i) row(names[i], point[i], draws[i, ]))
  })
  regional <- rstatix::kruskal_effsize(d, charges ~ region)
  correlations <- purrr::map_dfr(c("age", "bmi", "children"), function(field) {
    draws <- replicate(repeats, {
      i <- sample.int(nrow(d), replace = TRUE)
      spearman_estimate(d[[field]][i], d$charges[i])
    })
    row(paste0("spearman_", field), spearman_estimate(d[[field]], d$charges), draws)
  })
  dplyr::bind_rows(dplyr::bind_rows(tables), row("region_rank_eta_squared", max(0, regional$effsize)),
                   correlations)
}
