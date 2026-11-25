import duckdb
import pytest

from python.database import analytics, build


def test_queries_and_rebuild(sample):
    with duckdb.connect() as connection:
        build(connection, sample)
        build(connection, sample)
        results = dict(analytics(connection))
        assert len(results) == 10
        assert results["sql_data_quality_checks_1"].observations.item() == len(sample)
        assert results["sql_smoking_analysis_1"].median_charge.tolist() == [550.0, 800.0]
        assert results["sql_age_bmi_analysis_3"].charge_rank.min() == 1
        with pytest.raises(ValueError):
            build(connection, sample.assign(charges=-10))
        assert connection.execute("SELECT count(*) FROM insurance").fetchone() == (8,)
