# Data and provenance

The app loads the bundled [insurance.csv](raw/insurance.csv) by default.
Set `INSURANCE_CSV` to use another compatible file. The bundled copy is the
byte-preserved MAT 429 source with SHA-256
`388eff679557d08ac19f463d025de5e0b4adc482537c8456d19934d78621fd47`.

All 1,338 rows match the published educational dataset associated with Brett
Lantz's *Machine Learning with R* in both values and order. The educational
mirror describes its datasets as public domain. The repository's software
license applies to the code.

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
