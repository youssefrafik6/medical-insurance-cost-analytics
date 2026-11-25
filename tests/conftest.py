import pandas as pd
import pytest


@pytest.fixture
def sample():
    return pd.DataFrame(
        {
            "age": [18, 25, 30, 52, 60, 64, 44, 38],
            "sex": ["female", "male"] * 4,
            "bmi": [17.0, 24.0, 25.0, 31.0, 28.0, 29.0, 21.0, 26.0],
            "children": [0, 1, 2, 1, 3, 4, 2, 0],
            "smoker": ["no", "no", "yes", "yes"] * 2,
            "region": ["southwest", "southeast", "northwest", "northeast"] * 2,
            "charges": [100.0, 300.0, 400.0, 600.0, 800.0, 900.0, 1000.0, 1200.0],
        }
    )
