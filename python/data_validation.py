"""Schema checks and descriptive data quality diagnostics."""

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

CATEGORIES = {
    "sex": ("female", "male"),
    "smoker": ("no", "yes"),
    "region": ("northeast", "northwest", "southeast", "southwest"),
}
BOUNDS = {"age": (18, 120), "bmi": (10, 80), "children": (0, None), "charges": (0, None)}
COLUMNS = ["age", "sex", "bmi", "children", "smoker", "region", "charges"]


def fences(charges: pd.Series) -> tuple[float, float]:
    """Return type-7 1.5 × IQR fences."""
    q1, q3 = charges.quantile([0.25, 0.75])
    return q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)


def validate(frame: pd.DataFrame) -> dict:
    """Report fatal errors and retained duplicate/outlier warnings."""
    errors = []
    report = {"rows": len(frame), "errors": errors, "warnings": []}
    if not frame.columns.is_unique or set(frame) != set(COLUMNS):
        errors.append("Expected exactly the seven canonical columns.")
        return report
    if frame.empty:
        errors.append("Dataset is empty.")
    report["missing"] = {k: int(v) for k, v in frame.isna().sum().items()}
    if any(report["missing"].values()):
        errors.append("Missing observations detected.")
    for field, allowed in CATEGORIES.items():
        if (~frame[field].dropna().isin(allowed)).any():
            errors.append(f"Unexpected label in {field}.")
    for field, (low, high) in BOUNDS.items():
        values = frame[field].dropna()
        if not is_numeric_dtype(values) or values.dtype.kind not in "iuf":
            errors.append(f"{field} must be real numeric.")
            continue
        invalid = ~np.isfinite(values) | (values < low)
        if high is not None:
            invalid |= values > high
        if field in {"age", "children"}:
            invalid |= values % 1 != 0
        if invalid.any():
            errors.append(f"{int(invalid.sum())} invalid values in {field}.")
    if errors:
        return report
    lower, upper = fences(frame.charges)
    report["duplicate_rows_beyond_first"] = int(frame.duplicated().sum())
    report["iqr_outliers"] = int(((frame.charges < lower) | (frame.charges > upper)).sum())
    report["iqr_fences"] = [float(lower), float(upper)]
    for key in ("duplicate_rows_beyond_first", "iqr_outliers"):
        if report[key]:
            report["warnings"].append(f"{key}: {report[key]} retained")
    report["numeric_distributions"] = frame[list(BOUNDS)].describe().to_dict()
    report["categorical_distributions"] = {
        k: frame[k].value_counts().sort_index().to_dict() for k in CATEGORIES
    }
    return report


def require_valid(frame: pd.DataFrame) -> dict:
    """Stop on violations while retaining warned rows."""
    quality = validate(frame)
    if quality["errors"]:
        raise ValueError(" ".join(quality["errors"]))
    return quality
