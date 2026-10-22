"""Centralized SQLite database access for Cricbuzz LiveStats."""

import sqlite3
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "data" / "cricbuzz.db"


def get_db_connection() -> sqlite3.Connection:
    """Open a configured connection to the project database."""
    if not DB_PATH.is_file():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. "
            "Run: python database/init_db.py"
        )

    connection = sqlite3.connect(str(DB_PATH), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    return connection


def fetch_all(
    query: str,
    params: tuple[Any, ...] = (),
) -> list[sqlite3.Row]:
    """Execute a parameterized read query and return all rows."""
    connection = get_db_connection()
    try:
        return connection.execute(query, params).fetchall()
    finally:
        connection.close()


def fetch_one(
    query: str,
    params: tuple[Any, ...] = (),
) -> sqlite3.Row | None:
    """Execute a parameterized read query and return one row."""
    connection = get_db_connection()
    try:
        return connection.execute(query, params).fetchone()
    finally:
        connection.close()


def get_table_counts() -> dict[str, int]:
    """Return record counts for the project's known tables."""
    tables = (
        "teams",
        "players",
        "venues",
        "series",
        "matches",
        "innings",
        "batting_stats",
        "bowling_stats",
    )

    connection = get_db_connection()
    try:
        counts = {}
        for table in tables:
            # Table names come only from the fixed allowlist above.
            result = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()
            counts[table] = int(result[0])
        return counts
    finally:
        connection.close()
