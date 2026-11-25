"""Descriptive and inferential tools for independent observations."""

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.oneway import anova_oneway

from .data_validation import fences

PREDICTORS = ("age", "bmi", "children")
GROUPS = ("smoker", "region", "sex")


def summarize(frame: pd.DataFrame, field: str | None = None) -> pd.DataFrame:
    """Summarize charges with tail diagnostics by group."""
    records = []
    groups = frame.groupby(field, observed=True) if field else [("Overall", frame)]
    lower, upper = fences(frame.charges)
    for group, subset in groups:
        x = subset.charges
        if x.empty:
            continue
        q1, q3 = x.quantile([0.25, 0.75])
        records.append(
            dict(
                group=group,
                n=len(x),
                mean=x.mean(),
                median=x.median(),
                sd=x.std(),
                variance=x.var(),
                q1=q1,
                q3=q3,
                iqr=q3 - q1,
                minimum=x.min(),
                maximum=x.max(),
                skew=x.skew(),
                tail_n=((x < lower) | (x > upper)).sum(),
                smoker_share=subset.smoker.eq("yes").mean(),
            )
        )
    return pd.DataFrame(records)


def spearman(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Return an undefined result for constants and insufficient paired data."""
    keep = np.isfinite(x) & np.isfinite(y)
    x, y = x[keep], y[keep]
    if len(x) < 3 or min(len(np.unique(x)), len(np.unique(y))) < 2:
        return np.nan, np.nan
    result = stats.spearmanr(x, y)
    return float(result.statistic), float(result.pvalue)


def _groups(frame: pd.DataFrame, field: str) -> dict:
    return {key: group.charges.to_numpy() for key, group in frame.groupby(field)}


def tests(frame: pd.DataFrame) -> pd.DataFrame:
    """Run the academic tests and Welch regional benchmark."""
    rows = []

    def add(name, statistic, p_value):
        rows.append(dict(test=name, statistic=statistic, p_value=p_value))

    x = frame.charges
    if 3 <= len(x) <= 5000 and x.nunique() > 1:
        add("shapiro", *stats.shapiro(x))
    for field in ("smoker", "sex"):
        groups = _groups(frame, field)
        if len(groups) != 2:
            continue
        a, b = groups.values()
        u = stats.mannwhitneyu(a, b, method="asymptotic", use_continuity=True)
        add(f"wilcoxon_{field}", u.statistic, u.pvalue)
        if min(len(a), len(b)) >= 2 and (a.var() > 0 or b.var() > 0):
            t = stats.ttest_ind(a, b, equal_var=False)
            add(f"welch_{field}", t.statistic, t.pvalue)

    regions = _groups(frame, "region")
    if len(regions) >= 2 and x.nunique() > 1:
        groups = list(regions.values())
        add("kruskal_region", *stats.kruskal(*groups))
        if min(map(len, groups)) >= 2 and all(a.var() > 0 for a in groups):
            add("anova_region", *stats.f_oneway(*groups))
            welch = anova_oneway(groups, use_var="unequal")
            add("welch_region", welch.statistic, welch.pvalue)
        pairs = list(combinations(regions, 2))
        for left, right in pairs:
            u = stats.mannwhitneyu(regions[left], regions[right], method="asymptotic")
            add(f"region_{left}_{right}", u.statistic, min(1, len(pairs) * u.pvalue))
    for name in PREDICTORS:
        add(f"spearman_{name}", *spearman(frame[name].to_numpy(), x.to_numpy()))
    return pd.DataFrame(rows, columns=["test", "statistic", "p_value"])


def effects(frame: pd.DataFrame, repeats: int = 2000, seed: int = 429) -> pd.DataFrame:
    """Calculate directed effects and 95% percentile bootstrap intervals."""
    rng = np.random.default_rng(seed)
    rows = []

    def add(label, value, draws):
        finite = np.asarray(draws, dtype=float)
        finite = finite[np.isfinite(finite)]
        low, high = np.quantile(finite, [0.025, 0.975]) if len(finite) else (np.nan, np.nan)
        rows.append(
            dict(effect=label, estimate=value, lower=low, upper=high, valid_replicates=len(finite))
        )

    def two_group(a, b):
        u = stats.mannwhitneyu(a, b, method="asymptotic").statistic
        return np.array(
            [2 * u / (len(a) * len(b)) - 1, np.median(a) - np.median(b), a.mean() - b.mean()]
        )

    for field, first, second in (("smoker", "yes", "no"), ("sex", "male", "female")):
        groups = _groups(frame, field)
        if first in groups and second in groups:
            a, b = groups[first], groups[second]
            estimates = two_group(a, b)
            draws = np.array(
                [two_group(rng.choice(a, len(a)), rng.choice(b, len(b))) for _ in range(repeats)]
            )
            for i, name in enumerate(("rank_biserial", "median_difference", "mean_difference")):
                add(f"{field}_{name}", estimates[i], draws[:, i])
    regions = _groups(frame, "region")
    if len(regions) > 1 and len(frame) > len(regions) and frame.charges.nunique() > 1:
        h = stats.kruskal(*regions.values()).statistic
        add(
            "region_rank_eta_squared",
            max(0, (h - len(regions) + 1) / (len(frame) - len(regions))),
            [],
        )
    for field in PREDICTORS:
        x, y = frame[field].to_numpy(), frame.charges.to_numpy()
        estimate, _ = spearman(x, y)
        draws = []
        if np.isfinite(estimate):
            for _ in range(repeats):
                i = rng.integers(len(x), size=len(x))
                draws.append(spearman(x[i], y[i])[0])
        add(f"spearman_{field}", estimate, draws)
    return pd.DataFrame(rows)


def sensitivity(frame: pd.DataFrame) -> pd.DataFrame:
    """Compare original tests under transparent tail and repeat scenarios."""
    lower, upper = fences(frame.charges)
    scenarios = {
        "All observations": frame,
        "Exact repeats collapsed": frame.drop_duplicates(),
        "Outside pooled IQR fences excluded": frame[frame.charges.between(lower, upper)],
        "Upper 5% capped at pooled cutoff": frame.assign(
            charges=frame.charges.clip(upper=frame.charges.quantile(0.95))
        ),
    }
    parts = []
    for name, subset in scenarios.items():
        result = tests(subset)
        mask = result.test.isin(
            ["wilcoxon_sex", "welch_sex", "kruskal_region", "anova_region", "welch_region"]
        )
        parts.append(result[mask].assign(scenario=name, n=len(subset)))
    return pd.concat(parts, ignore_index=True)
