# Data and provenance

The byte-preserved MAT 429 source belongs at `raw/insurance.csv`. The academic
copy has SHA-256 `388eff679557d08ac19f463d025de5e0b4adc482537c8456d19934d78621fd47`.
Use your authorized copy or set the `INSURANCE_CSV` environment variable.

The layout and counts are consistent with the educational Medical Cost Personal
Datasets release associated with Brett Lantz's *Machine Learning with R*.
CRAN package documentation identifies this lineage. The GitHub mirror makes a
public-domain assertion, but gives no source-specific chain of rights for this
file. The Kaggle page did not supply independently verifiable upstream rights
during this review. Keep the CSV and derived row-level files out of Git pending
confirmation. The code license does not extend to the data.

- [Kaggle dataset listing](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- [Dataset attribution in CRAN documentation](https://search.r-project.org/CRAN/refmans/PPtreeregViz/html/insurance.html)
- [Educational book dataset mirror](https://github.com/stedy/Machine-Learning-with-R-datasets)

| Column | Type | Interpretation |
| --- | --- | --- |
| age | Integer | Recorded age in years |
| sex | Category | Recorded female/male label |
| bmi | Decimal | Recorded body mass index |
| children | Integer | Number of covered children |
| smoker | Category | Recorded yes/no smoking label |
| region | Category | One of four broad U.S. regions |
| charges | Decimal | Recorded billed charge, labeled USD |
