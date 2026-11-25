# Implementation summary

## Delivered

The repository extends Youssef Rafik’s Spring 2026 MAT 429 work. The original PDF, R script and CSV were verified byte for byte during the build. The current repository includes the academic PDF, and the original R script remains with the academic source files. The expanded project uses the same four research questions and retains the supplied 1,338 observations. See the [academic audit](PROJECT_AUDIT.md) for the original methods and limitations.

The additions are reusable R modules, a separate Python implementation, validation reports, seeded bootstrap intervals, directed effect sizes, comparisons of means and ranks, sensitivity checks, a DuckDB analytics layer, 10 SQL result sets, static graphics, a seven-section Streamlit dashboard, and Quarto HTML and PDF reports. The GitHub Actions workflow uses synthetic inputs for tests. Predictive modeling was left outside the scope of this implementation.

## Verification performed

| Check | Local outcome |
| --- | --- |
| Original academic script | Executed from a scratch directory with the supplied CSV |
| Refactored R and independent Python | Both ran on all 1,338 rows |
| Cross-language numerical comparison | All 17 test statistics and p-values and 10 effect estimates agreed within tolerance |
| Input and original materials | All three copies matched the originals byte for byte |
| DuckDB | Snapshot built and all 10 bundled queries executed |
| Python tests | 22 passed, including validation, inference, SQL, filtering and Streamlit page tests |
| R tests | Two testthat cases passed, with nine assertions |
| Formatting and lint | Ruff lint and format checks passed |
| Live dashboard | Overview and smoking pages rendered in Chrome, and the smokers-only selection returned 274 rows |
| Reporting | Quarto generated standalone HTML and a five-page Typst PDF |
| Repository hygiene | Git excludes the raw CSV and DuckDB. A pattern scan of project source and text found no private keys, common service-token patterns or local absolute source paths. |

The primary findings reproduced the paper’s rounded smoking medians, regional p-values, sex p-values, three rank correlations and 139 IQR outliers. The independent Python rank-sum p-value for smoking was 5.27 × 10⁻¹³⁰. The smoking median gap was $27,111 with a 95% bootstrap interval of $22,048 to $28,866. See [the findings](KEY_FINDINGS.md) for the sex and region sensitivity analysis.

The tested environment used arm64 macOS, Python 3.13.2, R 4.5.2 and Quarto 1.6.42. R generated the renv lockfile from the packages used locally. Full clean-room restoration and GitHub-hosted CI were not exercised. The TeX engine on this machine lacked the required class, so Quarto’s bundled Typst engine generated the PDF.

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

## GitHub publication checklist

- [x] Local Git repository initialized on `main`.
- [x] Original academic report included and a code license provided.
- [x] Raw CSV, database, environments, caches and secret configuration excluded by Git.
- [x] Reports, aggregate tables, figures, screenshots and CI configuration prepared.
- [ ] Confirm data redistribution terms before adding the CSV or any row-level export. Review publication rights for the academic report and source-derived figures before pushing.
- [ ] Review the initial commit contents and intended repository visibility. Publish only with the author’s approval.
- [ ] Observe the first hosted CI run after publication or a private push.

The main analytical constraints are unknown sampling and collection dates, observational comparisons, possible confounding and limited demographic detail. See [Limitations](LIMITATIONS.md) and [Data and provenance](../data/README.md).
