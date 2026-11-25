# Load packages
library(ggplot2)
library(dplyr)

# Load the dataset
insurance <- read.csv("insurance.csv")

# Look at the dataset
head(insurance)
str(insurance)
summary(insurance)

# Convert categorical variables to factors
insurance$sex <- as.factor(insurance$sex)
insurance$smoker <- as.factor(insurance$smoker)
insurance$region <- as.factor(insurance$region)

# 1. Basic Dataset Information

# Number of observations and variables
dim(insurance)

# Check for missing values
colSums(is.na(insurance))

# Summary of medical charges
summary(insurance$charges)

# Count observations by smoking status
table(insurance$smoker)

# Count observations by region
table(insurance$region)

# Count observations by sex
table(insurance$sex)

# Summary of charges by smoking status
insurance %>%
  group_by(smoker) %>%
  summarise(
    n = n(),
    median_charges = median(charges),
    mean_charges = mean(charges),
    sd_charges = sd(charges)
  )

# Summary of charges by region
insurance %>%
  group_by(region) %>%
  summarise(
    n = n(),
    median_charges = median(charges),
    mean_charges = mean(charges),
    sd_charges = sd(charges)
  )

# Summary of charges by sex
insurance %>%
  group_by(sex) %>%
  summarise(
    n = n(),
    median_charges = median(charges),
    mean_charges = mean(charges),
    sd_charges = sd(charges)
  )


# 2. Exploratory Data Analysis

# Histogram of charges
ggplot(insurance, aes(x = charges)) +
  geom_histogram(bins = 30, color = "black", fill = "lightblue") +
  labs(
    title = "Histogram of Medical Insurance Charges",
    x = "Charges",
    y = "Frequency"
  )

# Boxplot of charges
ggplot(insurance, aes(x = "", y = charges)) +
  geom_boxplot(fill = "lightblue") +
  labs(
    title = "Boxplot of Medical Insurance Charges",
    x = "",
    y = "Charges"
  )

# Q-Q plot of charges
qqnorm(
  insurance$charges,
  main = "Q-Q Plot of Medical Insurance Charges"
)
qqline(insurance$charges, col = "red")

# Boxplot of charges by smoking status
ggplot(insurance, aes(x = charges, y = smoker, fill = smoker)) +
  geom_boxplot() +
  labs(
    title = "Medical Charges by Smoking Status",
    x = "Charges",
    y = "Smoking Status"
  )

# Boxplot of charges by region
ggplot(insurance, aes(x = charges, y = region, fill = region)) +
  geom_boxplot() +
  labs(
    title = "Medical Charges by Region",
    x = "Charges",
    y = "Region"
  )

# Boxplot of charges by sex
ggplot(insurance, aes(x = charges, y = sex, fill = sex)) +
  geom_boxplot() +
  labs(
    title = "Medical Charges by Sex",
    x = "Charges",
    y = "Sex"
  )

# Scatterplot of BMI and charges
ggplot(insurance, aes(x = bmi, y = charges)) +
  geom_point() +
  labs(
    title = "BMI and Medical Charges",
    x = "BMI",
    y = "Charges"
  )

# Scatterplot of age and charges
ggplot(insurance, aes(x = age, y = charges)) +
  geom_point() +
  labs(
    title = "Age and Medical Charges",
    x = "Age",
    y = "Charges"
  )

# 3. Normality Check

# Shapiro-Wilk normality test for charges
shapiro.test(insurance$charges)


# 4. Outlier Check Using the 1.5 * IQR Rule

Q1 <- quantile(insurance$charges, 0.25)
Q3 <- quantile(insurance$charges, 0.75)
IQR_value <- IQR(insurance$charges)

lower_bound <- Q1 - 1.5 * IQR_value
upper_bound <- Q3 + 1.5 * IQR_value

lower_bound
upper_bound

outliers <- insurance %>%
  filter(charges < lower_bound | charges > upper_bound)

nrow(outliers)

# 5. Research Question 1
# Do medical charges differ between smokers and non-smokers?

# Non-parametric test:
# Wilcoxon rank-sum test

wilcox_smoker <- wilcox.test(
  charges ~ smoker,
  data = insurance,
  exact = FALSE
)

wilcox_smoker

# Parametric benchmark:
# Two-sample t-test

ttest_smoker <- t.test(
  charges ~ smoker,
  data = insurance
)

ttest_smoker

# Group medians and means

insurance %>%
  group_by(smoker) %>%
  summarise(
    n = n(),
    median_charges = median(charges),
    mean_charges = mean(charges)
  )


# 6. Research Question 2
# Do medical charges differ across regions?

# Non-parametric test:
# Kruskal-Wallis test

kruskal_region <- kruskal.test(
  charges ~ region,
  data = insurance
)

kruskal_region

# Parametric benchmark:
# One-way ANOVA

anova_region <- aov(
  charges ~ region,
  data = insurance
)

summary(anova_region)

# Group medians and means

insurance %>%
  group_by(region) %>%
  summarise(
    n = n(),
    median_charges = median(charges),
    mean_charges = mean(charges)
  )

# Pairwise Wilcoxon tests
pairwise.wilcox.test(
  insurance$charges,
  insurance$region,
  p.adjust.method = "bonferroni"
)


# 7. Research Question 3
# Do medical charges differ by sex?

# Non-parametric test:
# Wilcoxon rank-sum test

wilcox_sex <- wilcox.test(
  charges ~ sex,
  data = insurance,
  exact = FALSE
)

wilcox_sex

# Parametric benchmark:
# Two-sample t-test

ttest_sex <- t.test(
  charges ~ sex,
  data = insurance
)

ttest_sex

# Group medians and means

insurance %>%
  group_by(sex) %>%
  summarise(
    n = n(),
    median_charges = median(charges),
    mean_charges = mean(charges)
  )


# 8. Spearman Rank Correlation Tests

# Spearman correlation between BMI and charges

cor.test(
  insurance$bmi,
  insurance$charges,
  method = "spearman",
  exact = FALSE
)


# Spearman correlation between age and charges

cor.test(
  insurance$age,
  insurance$charges,
  method = "spearman",
  exact = FALSE
)


# Spearman correlation between number of children and charges

cor.test(
  insurance$children,
  insurance$charges,
  method = "spearman",
  exact = FALSE
)

# 9. Final Values for Report

# Overall median and maximum charge
median(insurance$charges)
max(insurance$charges)

# Medians by smoking status
tapply(insurance$charges, insurance$smoker, median)

# Medians by region
tapply(insurance$charges, insurance$region, median)

# Medians by sex
tapply(insurance$charges, insurance$sex, median)