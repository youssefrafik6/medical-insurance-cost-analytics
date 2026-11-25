save_exploration <- function(d, folder) {
  dollars <- function(x) paste0("$", format(x, big.mark = ",", scientific = FALSE, trim = TRUE))
  base <- theme_minimal(base_size = 13) +
    theme(panel.grid.minor = element_blank(), plot.title.position = "plot")
  save <- function(name, plot) ggsave(file.path(folder, paste0(name, ".png")),
                                      plot + base, width = 8, height = 5, dpi = 160, bg = "white")
  save("r_charge_histogram", ggplot(d, aes(charges)) +
    geom_histogram(bins = 30, fill = "#146D75", color = "white") +
    scale_x_continuous(labels = dollars) + labs(title = "Distribution of recorded charges",
                                                x = "Recorded charge (USD)", y = "Observations"))
  save("r_charge_qq", ggplot(d, aes(sample = charges)) +
    stat_qq(alpha = .5, colour = "#146D75") + stat_qq_line(colour = "#9A471B") +
    scale_y_continuous(labels = dollars) + labs(title = "Normal Q–Q plot of recorded charges",
                                         x = "Theoretical normal quantile", y = "Recorded charge"))
  for (field in c("smoker", "sex", "region", "overall")) {
    d$overall <- "All rows"
    save(paste0("r_box_", field), ggplot(d, aes(.data[[field]], charges)) +
      geom_boxplot(fill = "#C9E5E3", colour = "#18525D") +
      scale_y_continuous(labels = dollars) +
      labs(title = paste("Recorded charges by", field), x = NULL, y = "Recorded charge (USD)"))
  }
  for (field in c("age", "bmi", "children")) {
    save(paste0("r_scatter_", field), ggplot(d, aes(.data[[field]], charges, colour = smoker)) +
      geom_point(alpha = .45, size = 1.4) +
      scale_colour_manual(values = c(no = "#146D75", yes = "#9A471B")) +
      scale_y_continuous(labels = dollars) +
      labs(title = paste("Recorded charges and", field), x = if (field == "bmi") "BMI" else field,
           y = "Recorded charge (USD)", colour = "Smoker"))
  }
}
