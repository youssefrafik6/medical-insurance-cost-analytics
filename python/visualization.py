"""Portfolio graphics and a shared dashboard figure style."""

from pathlib import Path

import matplotlib
import pandas as pd
import plotly.express as px

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

TEAL = "#147D80"
NAVY = "#113849"
ORANGE = "#B65327"
CHARGE = "Recorded charge (USD)"


def style(fig):
    """Apply common interactive typography and margins."""
    fig.update_layout(
        template="plotly_white",
        font_color=NAVY,
        margin=dict(l=12, r=12, t=36, b=15),
        height=330,
        legend_title_text="Smoking status",
    )
    return fig


def charge_scatter(frame: pd.DataFrame, variable: str):
    """Compare recorded charges with a numeric characteristic."""
    fig = px.scatter(
        frame,
        x=variable,
        y="charges",
        color="smoker",
        color_discrete_map={"yes": ORANGE, "no": TEAL},
        opacity=0.56,
        labels={"age": "Age", "bmi": "BMI", "children": "Children", "charges": CHARGE},
    )
    return style(fig.update_yaxes(tickprefix="$", separatethousands=True))


def save_figures(frame: pd.DataFrame, summaries: dict, effects: pd.DataFrame, folder: Path) -> None:
    """Export static figures suitable for reports and GitHub."""
    plt.rcParams.update(
        {
            "font.size": 11,
            "text.color": NAVY,
            "axes.labelcolor": NAVY,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    money = StrMethodFormatter("${x:,.0f}")

    def save(fig, name):
        fig.savefig(folder / f"{name}.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(frame.charges, bins=30, color=TEAL, edgecolor="white")
    ax.xaxis.set_major_formatter(money)
    ax.set(title="Distribution of recorded charges", xlabel=CHARGE, ylabel="Observations")
    save(fig, "charge_distribution")
    for field, label in (("smoker", "smoking status"), ("region", "region"), ("sex", "sex")):
        fig, ax = plt.subplots(figsize=(8, 4))
        grouped = frame.groupby(field).charges
        ax.boxplot(
            [values for _, values in grouped],
            tick_labels=list(grouped.groups),
            orientation="horizontal",
            patch_artist=True,
            boxprops={"facecolor": "#C9E5E3"},
            medianprops={"color": ORANGE},
        )
        ax.xaxis.set_major_formatter(money)
        ax.set(title=f"Recorded charges by {label}", xlabel=CHARGE)
        save(fig, f"box_{field}")
    for name in ("age", "bmi", "children"):
        fig, ax = plt.subplots(figsize=(8, 4))
        for group, subset in frame.groupby("smoker"):
            ax.scatter(
                subset[name],
                subset.charges,
                s=10,
                alpha=0.45,
                color=ORANGE if group == "yes" else TEAL,
                label=group,
            )
        ax.yaxis.set_major_formatter(money)
        ax.set(
            title=f"Recorded charges and {name}",
            xlabel=name.upper() if name == "bmi" else name,
            ylabel=CHARGE,
        )
        ax.legend(title="Smoker", frameon=False)
        save(fig, f"scatter_{name}")
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), layout="constrained")
    for (field, table), ax in zip(summaries.items(), axes, strict=True):
        table.set_index("group")[["mean", "median"]].plot.bar(
            ax=ax, rot=25, color=[TEAL, ORANGE], title=field.capitalize()
        )
        ax.set_xlabel("")
        ax.yaxis.set_major_formatter(money)
    axes[0].set_ylabel(CHARGE)
    save(fig, "mean_vs_median")
    plot = effects.loc[effects.effect.str.startswith("spearman")].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.errorbar(
        plot.estimate,
        plot.index,
        fmt="o",
        color=TEAL,
        xerr=[plot.estimate - plot.lower, plot.upper - plot.estimate],
        capsize=4,
    )
    ax.set_yticks(plot.index, plot.effect.str.removeprefix("spearman_"))
    ax.axvline(0, color="#64748B", linewidth=1)
    ax.set(
        xlim=(-1, 1), xlabel="Spearman rho", title="Rank correlations with 95% bootstrap intervals"
    )
    save(fig, "correlation_intervals")
