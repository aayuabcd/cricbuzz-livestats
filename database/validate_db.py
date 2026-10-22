import sqlite3
from pathlib import Path

db_path = Path("data/cricbuzz.db")

with sqlite3.connect(db_path) as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    checks = {
        "Players with teams": """
            SELECT p.full_name, t.team_name, p.role
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.player_id
        """,
        "Completed matches": """
            SELECT m.match_type, t1.team_name, t2.team_name,
                   m.status, m.result_text
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
        """,
        "Top batting scores": """
            SELECT p.full_name, t.team_name, b.runs, b.balls_faced
            FROM batting_stats b
            JOIN players p ON b.player_id = p.player_id
            JOIN teams t ON p.team_id = t.team_id
            ORDER BY b.runs DESC
        """,
        "Foreign-key violations": "PRAGMA foreign_key_check",
    }

    for title, query in checks.items():
        print(f"\n--- {title} ---")
        for row in conn.execute(query):
            print(row)

print("\nSUCCESS: Database relationship checks completed.")
