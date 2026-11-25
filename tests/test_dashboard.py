from streamlit.testing.v1 import AppTest

from dashboard.app import filter_data
from python.data_loader import ROOT


def test_combined_filters(sample):
    result = filter_data(sample, {"age": (25, 64), "children": (1, 4)}, {"smoker": ["no"]})
    assert result.age.tolist() == [25, 60, 64]
    assert filter_data(sample, {}, {"sex": []}).empty


def test_app_filter_and_pages(sample, tmp_path, monkeypatch):
    csv = tmp_path / "synthetic.csv"
    sample.to_csv(csv, index=False)
    monkeypatch.setenv("INSURANCE_CSV", str(csv))
    app = AppTest.from_file(ROOT / "dashboard/app.py", default_timeout=30).run()
    assert not app.exception
    assert app.metric[0].value == "8"
    app.multiselect(key="smoker").set_value(["yes"]).run()
    assert app.metric[0].value == "4"
    for page in (
        "Demographics",
        "Smoking analysis",
        "Regional analysis",
        "Correlation analysis",
        "Statistical insights",
        "Data explorer",
    ):
        app.radio[0].set_value(page).run()
        assert not app.exception
    app.text_input[0].set_value("northeast").run()
    assert len(app.dataframe[0].value) == 2
    app.multiselect(key="smoker").set_value([]).run()
    assert app.info[0].value == "No observations match the current filters."
