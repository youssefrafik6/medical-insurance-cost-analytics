"""Streamlit interface for descriptive exploration and full-cohort inference."""

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from python.data_loader import ROOT, load_data
from python.data_validation import CATEGORIES, require_valid
from python.statistical_analysis import PREDICTORS, spearman, summarize
from python.visualization import CHARGE, TEAL, charge_scatter, style

SECTIONS = [
    "Overview",
    "Demographics",
    "Smoking analysis",
    "Regional analysis",
    "Correlation analysis",
    "Statistical insights",
    "Data explorer",
]


def filter_data(frame: pd.DataFrame, numeric: dict, categorical: dict) -> pd.DataFrame:
    """Intersect inclusive numeric ranges and selected category sets."""
    mask = pd.Series(True, index=frame.index)
    for field, (lower, upper) in numeric.items():
        mask &= frame[field].between(lower, upper)
    for field, levels in categorical.items():
        mask &= frame[field].isin(levels)
    return frame.loc[mask]


@st.cache_data
def inference(frame: pd.DataFrame, fingerprint: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Reuse published calculations for the matching dataset or compute from the source."""
    import hashlib

    from python.statistical_analysis import effects, tests

    folder = ROOT / "results/statistical_tests"
    if (
        fingerprint
        and hashlib.sha256(frame.to_csv(index=False).encode()).hexdigest() == fingerprint
    ):
        return pd.read_csv(folder / "python_tests.csv"), pd.read_csv(folder / "python_effects.csv")
    return tests(frame), effects(frame)


def range_widget(frame: pd.DataFrame, field: str, title: str) -> tuple:
    """Show fixed values for constant inputs."""
    lower, upper = frame[field].min().item(), frame[field].max().item()
    if lower == upper:
        st.sidebar.caption(f"{title} · {lower}")
        return lower, upper
    return st.sidebar.slider(title, lower, upper, (lower, upper), key=field)


def boxplot(frame: pd.DataFrame, field: str) -> None:
    """Draw the filtered charge distributions."""
    fig = px.box(
        frame,
        x=field,
        y="charges",
        color_discrete_sequence=[TEAL],
        labels={"charges": CHARGE, field: field.capitalize()},
    )
    st.plotly_chart(style(fig.update_yaxes(tickprefix="$")), width="stretch")


def show_groups(frame: pd.DataFrame, field: str) -> None:
    """Show filtered group counts and charge summaries."""
    table = summarize(frame, field)[["group", "n", "mean", "median", "sd", "tail_n"]]
    st.dataframe(
        table,
        hide_index=True,
        column_config={
            key: st.column_config.NumberColumn(format="dollar") for key in ("mean", "median", "sd")
        },
    )


def full_cohort(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Identify inferential scope explicitly beside the output."""
    st.subheader("Full-cohort inference")
    st.caption(f"All {len(frame):,} source observations. Sidebar filters affect descriptive views.")
    quality = ROOT / "results/tables/data_quality.json"
    fingerprint = (
        json.loads(quality.read_text()).get("observation_fingerprint", "")
        if quality.exists()
        else ""
    )
    return inference(frame, fingerprint)


def main() -> None:
    """Run the dashboard."""
    st.set_page_config(page_title="Medical Insurance Cost Analytics", layout="wide")
    st.title("Medical Insurance Cost Analytics")
    st.caption("Explore recorded charges in the MAT 429 educational dataset.")
    try:
        frame = load_data()
        require_valid(frame)
    except (OSError, ValueError) as error:
        st.error(f"Dataset unavailable · {error}")
        st.stop()

    section = st.sidebar.radio("Explore", SECTIONS)
    st.sidebar.header("Filters")
    numeric = {
        field: range_widget(frame, field, title)
        for field, title in (("age", "Age range"), ("bmi", "BMI range"), ("children", "Children"))
    }
    categorical = {
        field: st.sidebar.multiselect(title, options, default=options, key=field)
        for (field, options), title in zip(
            CATEGORIES.items(), ("Sex", "Smoking status", "Region"), strict=True
        )
    }
    filtered = filter_data(frame, numeric, categorical)
    st.header(section)
    st.caption(f"Filtered view · {len(filtered):,} of {len(frame):,} observations")
    if filtered.empty and section != "Statistical insights":
        st.info("No observations match the current filters.")
        return

    if section == "Overview":
        charges = filtered.charges
        metrics = (
            ("Observations", f"{len(filtered):,}"),
            ("Mean charge", f"${charges.mean():,.0f}"),
            ("Median charge", f"${charges.median():,.0f}"),
            ("Highest charge", f"${charges.max():,.0f}"),
            ("Smoking prevalence", f"{filtered.smoker.eq('yes').mean():.1%}"),
        )
        for column, (label, value) in zip(st.columns(5), metrics, strict=True):
            column.metric(label, value)
        st.subheader("Charge distribution")
        fig = px.histogram(
            filtered,
            x="charges",
            nbins=35,
            color_discrete_sequence=[TEAL],
            labels={"charges": CHARGE},
        )
        st.plotly_chart(
            style(fig.update_xaxes(tickprefix="$").update_yaxes(title="Observations")),
            width="stretch",
        )
    elif section == "Demographics":
        for index, field in enumerate(("age", "sex", "region", "bmi", "children")):
            if index % 2 == 0:
                columns = st.columns(2)
            with columns[index % 2]:
                st.subheader(field.upper() if field == "bmi" else field.capitalize())
                st.plotly_chart(
                    style(px.histogram(filtered, x=field, color_discrete_sequence=[TEAL])),
                    width="stretch",
                )
    elif section in {"Smoking analysis", "Regional analysis"}:
        field = "smoker" if section == "Smoking analysis" else "region"
        boxplot(filtered, field)
        show_groups(filtered, field)
        tests, effects = full_cohort(frame)
        st.dataframe(tests[tests.test.str.endswith(f"_{field}")], hide_index=True)
        st.dataframe(effects[effects.effect.str.startswith(f"{field}_")], hide_index=True)
    elif section == "Correlation analysis":
        for field in PREDICTORS:
            rho, _ = spearman(filtered[field].to_numpy(), filtered.charges.to_numpy())
            st.subheader(field.upper() if field == "bmi" else field.capitalize())
            label = f"{rho:.3f}" if pd.notna(rho) else "Unavailable for this selection"
            st.caption(f"Filtered Spearman rho · {label}")
            st.plotly_chart(charge_scatter(filtered, field), width="stretch")
    elif section == "Statistical insights":
        tests, effects = full_cohort(frame)
        st.dataframe(tests, hide_index=True)
        st.dataframe(effects, hide_index=True)
        st.caption(
            "Intervals are 95% percentile bootstrap intervals. Regional rank eta-squared is a point estimate."
        )
        st.subheader("Why Parametric and Nonparametric Tests Disagree")
        st.markdown(
            "Welch and ordinary ANOVA compare means. The rank tests use ordering. "
            "Large upper-tail charges can move group means while changing ranks relatively little. "
            "See the statistical report for group diagnostics and tail sensitivity."
        )
    else:
        query = st.text_input("Search all fields").strip()
        if query:
            matches = (
                filtered.astype(str)
                .apply(lambda values: values.str.contains(query, case=False, regex=False))
                .any(axis=1)
            )
            filtered = filtered[matches]
        st.caption(f"{len(filtered):,} matching rows · Select any column header to sort.")
        st.dataframe(
            filtered,
            hide_index=True,
            column_config={"charges": st.column_config.NumberColumn(format="dollar")},
        )
        st.download_button(
            "Export matching rows",
            filtered.to_csv(index=False),
            "filtered_insurance.csv",
            "text/csv",
        )


if __name__ == "__main__":
    main()
