## Setup and execution

Run from the repository root with Python 3.13, R 4.5.2, Quarto with Typst and an authorized source CSV. Place the CSV in `data/raw/insurance.csv` or export `INSURANCE_CSV` with its path. If Quarto is bundled with RStudio, export `QUARTO_BIN` with its executable path.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
Rscript -e 'install.packages("renv", repos="https://cloud.r-project.org")'
Rscript -e 'renv::restore(prompt = FALSE)'

Rscript -e 'renv::load(); source("scripts/run_analysis.R")'
python -m scripts.build_database
export R_LIBS="$(Rscript -e 'cat(renv::paths$library())')"
python -m scripts.generate_report --render html
"${QUARTO_BIN:-quarto}" render reports/analysis_report.qmd --to typst

python -m pytest
ruff check python dashboard scripts tests
ruff format --check python dashboard scripts tests
Rscript -e 'renv::load(); source("tests/test_r.R")'
python -m streamlit run dashboard/app.py --server.address 127.0.0.1
```
