from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT_DIR / "database" / "schema.sql"
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "cricbuzz.db"


def initialize_database():
    """Create the SQLite database and its tables."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    schema = SCHEMA_PATH.read_text(encoding="utf-8-sig")

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema)

        table_rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        foreign_key_status = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

    table_names = [row[0] for row in table_rows]

    print(f"Database created: {DB_PATH}")
    print(f"Tables created ({len(table_names)}): {', '.join(table_names)}")

    if foreign_key_status:
        raise RuntimeError(
            f"Foreign-key validation failed: {foreign_key_status}"
        )

    print("SUCCESS: Schema executed and foreign-key check passed.")


if __name__ == "__main__":
    initialize_database()
