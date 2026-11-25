library(testthat)
source("R/data_validation.R")
source("R/exploratory_analysis.R")
source("R/correlation_analysis.R")
source("R/effect_sizes.R")

test_that("validation rejects malformed or incomplete observations", {
  d <- data.frame(age = 20L, sex = "female", bmi = 22, children = 0L,
                  smoker = "no", region = "southwest", charges = 1000)
  expect_no_error(validate_data(d))
  expect_error(validate_data(d[FALSE, ]), "nonempty")
  expect_error(validate_data(d[-1]), "canonical")
  expect_error(validate_data(transform(d, bmi = NA_real_)), "complete")
  expect_error(validate_data(transform(d, charges = -1)), "Invalid charges")
})

test_that("quantiles, ranks and constant correlations are handled", {
  expect_equal(charge_fences(1:5), c(-1, 7))
  expect_equal(two_group_effects(c(3, 4), c(1, 2)), c(1, 2, 2))
  expect_equal(spearman_estimate(1:5, 5:1), -1)
  expect_true(is.na(spearman_estimate(1:5, rep(0, 5))))
})
