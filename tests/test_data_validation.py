import pandas as pd
import pytest

from python.data_loader import load_data
from python.data_validation import validate


def test_csv_load(sample, tmp_path):
    path = tmp_path / "input.csv"
    sample.to_csv(path, index=False)
    assert load_data(path).equals(sample)
    assert not validate(load_data(path))["errors"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", 17),
        ("age", 18.5),
        ("bmi", 99.0),
        ("charges", -1.0),
        ("charges", float("inf")),
        ("children", -1),
        ("children", 1.5),
        ("region", "central"),
        ("sex", "other"),
        ("smoker", "maybe"),
        ("charges", "invalid"),
    ],
)
def test_invalid_values(sample, field, value):
    changed = sample[field].tolist()
    changed[0] = value
    assert validate(sample.assign(**{field: changed}))["errors"]


def test_missing_and_empty(sample):
    assert validate(sample.drop(columns="bmi"))["errors"]
    assert validate(sample.iloc[:0])["errors"]
    assert validate(sample.assign(bmi=None))["missing"]["bmi"] == len(sample)


def test_repeat_retained(sample):
    report = validate(pd.concat([sample, sample.iloc[[0]]], ignore_index=True))
    assert not report["errors"]
    assert report["duplicate_rows_beyond_first"] == 1
    assert report["rows"] == 9
