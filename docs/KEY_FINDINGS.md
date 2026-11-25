# Verified findings

- Median recorded charges were $34,456 for smokers and $7,345 for nonsmokers. The difference was $27,111 (Python 95% bootstrap interval $22,048–$28,866). Rank-biserial correlation was 0.949 (0.935–0.962), and the rank-sum p-value was 5.27 × 10⁻¹³⁰. Of the 139 rows above the pooled IQR fence, 136 recorded smoking.
- Age showed the strongest monotonic association with charges, with Spearman rho 0.534 (0.483–0.584). BMI and number of children showed weaker associations, 0.119 (0.064–0.172) and 0.133 (0.080–0.186).
- Regional rank eta-squared was 0.0013. None of the six exploratory regional rank comparisons had an adjusted p-value below 0.05.

## Why Parametric and Nonparametric Tests Disagree

### Sex

Female and male group sizes were 662 and 676. Means were $12,570 and $13,957, while medians were $9,413 and $9,370. The male-minus-female mean gap was $1,387 (95% bootstrap interval $114–$2,747). The median gap was −$43 (−$970 to $1,232) and rank-biserial correlation was 0.011 (−0.047 to 0.076). The Welch mean test yielded p = 0.03584 and the rank-sum test yielded p = 0.72865.

Both groups had long right tails. Female and male skewness was 1.73 and 1.34, with SDs of $11,129 and $12,971. The male group had 89 rows beyond the pooled IQR fence versus 50 for the female group, and smoking prevalence was 23.5% versus 17.4%, respectively. Larger upper-tail magnitudes can increase the mean even as the probability of a higher randomly drawn charge stays close to 50%. The difference in smoking prevalence suggests a composition issue worth investigating with adequately sampled data.

### Region

Group sizes were 324–364. The southeast had the highest mean ($14,735), the highest SD ($13,971), the most pooled-fence exceedances (57) and the highest smoking prevalence (25.0%). It had the second-highest median ($9,294), below the northeast ($10,058). Mean ordering and median ordering differed across the groups. Regional skewness ranged from 1.25 to 1.68, and observed standard deviations ranged from $11,072 to $13,971. Ordinary ANOVA gave p = 0.03089, Welch ANOVA p = 0.05059, and Kruskal–Wallis p = 0.19233. The Welch result illustrates sensitivity to variance assumptions, while the small regional rank effect indicates weak ordering separation in the original cohort.

### Sensitivity

| Scenario | Sex Welch | Sex rank-sum | Region ANOVA | Region Welch | Region Kruskal–Wallis |
| --- | ---: | ---: | ---: | ---: | ---: |
| All 1,338 rows | .0358 | .7287 | .0309 | .0506 | .1923 |
| Collapse one exact repeat | .0336 | .6945 | .0328 | .0535 | .2016 |
| Exclude beyond pooled fences | .3998 | .0998 | .0177 | .0116 | .0134 |
| Cap charges at pooled p95 | .0342 | .7226 | .0382 | .0552 | .1876 |

Capping changes magnitudes and creates upper-tail ties while preserving records. The broad pattern persisted after capping and after collapsing the repeat. Exclusion changes group composition and the population being described. It attenuated the sex mean result and strengthened the regional rank result, showing that the tail can mask some regional rank differences in the lower-charge subset. These exploratory checks identify where results are sensitive and do not confer a general preference for either test family.
