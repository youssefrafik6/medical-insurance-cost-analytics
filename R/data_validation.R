#' Load and validate the seven source columns.
validate_data <- function(d) {
  categories <- list(sex = c("female", "male"), smoker = c("no", "yes"),
                     region = c("northeast", "northwest", "southeast", "southwest"))
  bounds <- list(age = c(18, 120), bmi = c(10, 80), children = c(0, Inf),
                 charges = c(0, Inf))
  if (anyDuplicated(names(d)) || !setequal(names(d), c(names(categories), names(bounds)))) {
    stop("Expected exactly the seven canonical columns.")
  }
  if (!nrow(d) || anyNA(d)) stop("Dataset must be nonempty and complete.")
  for (field in names(categories)) {
    if (!all(d[[field]] %in% categories[[field]])) stop("Invalid ", field)
  }
  for (field in names(bounds)) {
    x <- d[[field]]
    limits <- bounds[[field]]
    if (!is.numeric(x) || any(!is.finite(x) | x < limits[1] | x > limits[2]) ||
        (field %in% c("age", "children") && any(x != trunc(x)))) stop("Invalid ", field)
  }
  invisible(d)
}
