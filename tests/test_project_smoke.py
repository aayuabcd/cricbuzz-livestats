"""Non-destructive project structure and schema smoke tests."""
from __future__ import annotations

import ast
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_app_is_valid_python():
    ast.parse((ROOT / "app.py").read_text(encoding="utf-8-sig"))


def test_25_sql_recipes_exist():
    recipes = sorted((ROOT / "database" / "queries").glob("*.sql"))
    assert len(recipes) == 25, f"Expected 25 recipes, found {len(recipes)}"
    assert all(path.read_text(encoding="utf-8-sig").strip() for path in recipes)


def test_schema_creates_expected_tables():
    schema = (ROOT / "database" / "schema.sql").read_text(encoding="utf-8-sig")
    with sqlite3.connect(":memory:") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(schema)
        actual = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    expected = {"teams", "players", "venues", "series", "matches", "innings", "batting_stats", "bowling_stats"}
    assert expected <= actual, f"Missing tables: {expected - actual}"
