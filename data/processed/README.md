# Local database

Run `python -m scripts.build_database` from the repository root to materialize
`insurance.duckdb`. The database contains source-level records and is ignored
by Git. Stable aggregate SQL outputs are written to `results/tables/`.
