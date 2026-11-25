"""Read the supplied dataset from a project-relative location."""

import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_data(path: Path | str | None = None) -> pd.DataFrame:
    """Load raw observations without deleting or imputing rows."""
    source = Path(path or os.environ.get("INSURANCE_CSV", ROOT / "data/raw/insurance.csv"))
    return pd.read_csv(source)
