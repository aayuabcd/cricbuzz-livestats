"""Validate SQL recipe files against the project database schema."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "database" / "schema.sql"
QUERIES = ROOT / "database" / "queries"

def test_25_sql_recipes_execute():
    files = sorted(QUERIES.glob("*.sql"))
    assert len(files) == 25, f"Expected 25 SQL files, found {len(files)}"
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(SCHEMA.read_text(encoding="utf-8"))
        for file in files:
            sql = file.read_text(encoding="utf-8").strip()
            assert sql.splitlines()[-1].lstrip().upper().startswith("SELECT"), file.name
            db.execute(sql).fetchall()
    finally:
        db.close()
