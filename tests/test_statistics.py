import numpy as np
import pytest
from scipy import stats

from python.reporting import verify
from python.statistical_analysis import effects, spearman, summarize
from python.statistical_analysis import tests as run_tests


def test_summary_and_rank_test(sample):
    summary = summarize(sample, "smoker").set_index("group")
    assert summary.loc["no", "median"] == 550
    observed = run_tests(sample).set_index("test").loc["wilcoxon_smoker"]
    a = sample.loc[sample.smoker == "no", "charges"]
    b = sample.loc[sample.smoker == "yes", "charges"]
    expected = stats.mannwhitneyu(a, b, method="asymptotic")
    assert observed.p_value == pytest.approx(expected.pvalue)
    table = effects(sample, repeats=20).set_index("effect")
    assert table.loc["smoker_rank_biserial", "estimate"] == -2 * expected.statistic / 16 + 1


def test_spearman_edges():
    x = np.array([1.0, 2.0, 3.0, np.nan])
    assert spearman(x, -x)[0] == -1
    assert np.isnan(spearman(x, np.ones(4))[0])
    assert np.isnan(spearman(x[:0], x[:0])[0])


def test_single_category_and_constant(sample):
    frame = sample.assign(smoker="no", region="southwest", charges=100.0)
    table = run_tests(frame)
    assert not table.test.isin(["wilcoxon_smoker", "kruskal_region", "shapiro"]).any()
    assert table.loc[table.test.str.startswith("spearman"), "statistic"].isna().all()


def test_comparison_catches_missing_and_small_p_values(sample):
    base = run_tests(sample).iloc[:2].copy()
    altered = base.iloc[[0]].assign(p_value=1e-100)
    report = verify(base, altered, "test", ["statistic", "p_value"])
    assert not report.p_value_agreement.any()
    assert report.statistic_agreement.sum() == 1


@pytest.mark.parametrize("fresh", [False, True], ids=["published", "fresh"])
def test_r_and_python_agree(fresh):
    import os
    from pathlib import Path

    import pandas as pd

    from python.data_loader import ROOT, load_data

    folder = ROOT / "results/statistical_tests"
    if fresh:
        source = Path(os.environ.get("INSURANCE_CSV", ROOT / "data/raw/insurance.csv"))
        if not source.is_file():
            pytest.skip("Fresh parity requires an authorized insurance CSV")
        frame = load_data(source)
        python_tests = run_tests(frame)
        python_effects = effects(frame, repeats=20)
    else:
        python_tests = pd.read_csv(folder / "python_tests.csv")
        python_effects = pd.read_csv(folder / "python_effects.csv")
    computed = verify(
        python_tests,
        pd.read_csv(folder / "r_tests.csv"),
        "test",
        ["statistic", "p_value"],
    )
    assert len(computed) == 17
    assert computed[["statistic_agreement", "p_value_agreement"]].to_numpy().all()
    estimates = verify(
        python_effects[["effect", "estimate"]],
        pd.read_csv(folder / "r_effects.csv")[["effect", "estimate"]],
        "effect",
        ["estimate"],
    )
    assert len(estimates) == 10
    assert estimates["estimate_agreement"].all()
