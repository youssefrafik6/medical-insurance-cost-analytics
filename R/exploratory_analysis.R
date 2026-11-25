charge_fences <- function(x) {
  unname(quantile(x, c(.25, .75)) + c(-1.5, 1.5) * IQR(x))
}

charge_summary <- function(d, field) {
  limits <- charge_fences(d$charges)
  d |>
    dplyr::group_by(group = .data[[field]]) |>
    dplyr::summarise(n = dplyr::n(), mean = mean(charges), median = median(charges),
                     sd = sd(charges), q1 = quantile(charges, .25),
                     q3 = quantile(charges, .75), iqr = IQR(charges),
                     minimum = min(charges), maximum = max(charges),
                     tail_n = sum(charges < limits[1] | charges > limits[2]))
}
