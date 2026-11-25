"""Build machine-readable analytics and the Quarto report inputs."""

import hashlib
import json

import numpy as np
import pandas as pd

from .data_loader import ROOT, load_data
from .data_validation import require_valid
from .statistical_analysis import GROUPS, effects, sensitivity, summarize, tests
from .visualization import save_figures


def verify(python: pd.DataFrame, r: pd.DataFrame, key: str, values: list[str]) -> pd.DataFrame:
    """Compare matched numerical results and expose missing rows."""
    joint = python.merge(
        r, on=key, suffixes=("_python", "_r"), how="outer", validate="one_to_one", indicator=True
    )
    for value in values:
        left, right = joint[f"{value}_python"], joint[f"{value}_r"]
        joint[f"{value}_agreement"] = np.isclose(
            left, right, rtol=2e-6, atol=0, equal_nan=True
        ) & joint["_merge"].eq("both")
    return joint.drop(columns="_merge")


def build_results() -> None:
    """Validate the dataset and refresh its summaries, tests and figures."""
    frame = load_data()
    quality = require_valid(frame)
    quality["observation_fingerprint"] = hashlib.sha256(
        frame.to_csv(index=False).encode()
    ).hexdigest()
    results = ROOT / "results"
    figures, tables, stats = (results / name for name in ("figures", "tables", "statistical_tests"))
    for folder in (figures, tables, stats):
        folder.mkdir(parents=True, exist_ok=True)
    (tables / "data_quality.json").write_text(json.dumps(quality, indent=2) + "\n")
    groups = {field: summarize(frame, field) for field in GROUPS}
    for field, table in {**groups, "overall": summarize(frame)}.items():
        table.to_csv(tables / f"python_{field}.csv", index=False)
    result, effect = tests(frame), effects(frame)
    result.to_csv(stats / "python_tests.csv", index=False)
    effect.to_csv(stats / "python_effects.csv", index=False)
    sensitivity(frame).to_csv(stats / "sensitivity.csv", index=False)
    for filename, table, key, values in [
        ("tests", result, "test", ["statistic", "p_value"]),
        ("effects", effect[["effect", "estimate"]], "effect", ["estimate"]),
    ]:
        r_path = stats / f"r_{filename}.csv"
        if r_path.exists():
            r = pd.read_csv(r_path)[[key, *values]]
            comparisons = verify(table, r, key, values)
            comparisons.to_csv(stats / f"verification_{filename}.csv", index=False)
            print(f"Cross-language {filename}: {len(comparisons)} rows")
    save_figures(frame, groups, effect, figures)
