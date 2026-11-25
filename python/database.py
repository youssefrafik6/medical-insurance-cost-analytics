"""Transactional DuckDB load and discovery of bundled SQL queries."""

from collections.abc import Iterator

import duckdb
import pandas as pd

from .data_loader import ROOT
from .data_validation import COLUMNS, require_valid


def build(connection: duckdb.DuckDBPyConnection, frame: pd.DataFrame) -> None:
    """Replace the current snapshot within a transaction."""
    require_valid(frame)
    connection.register("incoming_insurance", frame[COLUMNS])
    connection.begin()
    try:
        connection.execute((ROOT / "sql/schema.sql").read_text())
        connection.execute("DELETE FROM insurance")
        connection.execute("INSERT INTO insurance BY NAME SELECT * FROM incoming_insurance")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.unregister("incoming_insurance")


def analytics(connection: duckdb.DuckDBPyConnection) -> Iterator[tuple[str, pd.DataFrame]]:
    """Execute every query and return a stable export name and its result."""
    for path in sorted((ROOT / "sql").glob("*.sql")):
        if path.stem != "schema":
            for index, statement in enumerate(connection.extract_statements(path.read_text()), 1):
                yield f"sql_{path.stem}_{index}", connection.execute(statement).df()
