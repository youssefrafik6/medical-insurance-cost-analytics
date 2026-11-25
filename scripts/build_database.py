"""Build the local database and export all SQL results."""

import duckdb

from python.data_loader import ROOT, load_data
from python.database import analytics, build


def main() -> None:
    """Create or refresh the DuckDB snapshot."""
    db = ROOT / "data/processed/insurance.duckdb"
    db.parent.mkdir(parents=True, exist_ok=True)
    tables = ROOT / "results/tables"
    tables.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db)) as connection:
        build(connection, load_data())
        for name, result in analytics(connection):
            result.to_csv(tables / f"{name}.csv", index=False)
            print(f"{name}: {len(result)} result rows")


if __name__ == "__main__":
    main()
