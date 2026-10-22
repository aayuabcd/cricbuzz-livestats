from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "cricbuzz.db"


def seed_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        conn.executemany(
            "INSERT OR IGNORE INTO teams VALUES (?, ?, ?)",
            [
                (1, "India", "India"),
                (2, "Australia", "Australia"),
                (3, "England", "England"),
                (4, "South Africa", "South Africa"),
            ],
        )

        conn.executemany(
            """INSERT OR IGNORE INTO players
            (player_id, full_name, team_id, role, batting_style,
             bowling_style, country) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, "Demo Batter One", 1, "Batter", "Right-hand bat", None, "India"),
                (2, "Demo All-Rounder", 1, "All-rounder", "Left-hand bat", "Offbreak", "India"),
                (3, "Demo Bowler One", 2, "Bowler", "Right-hand bat", "Fast", "Australia"),
                (4, "Demo Batter Two", 2, "Batter", "Left-hand bat", None, "Australia"),
                (5, "Demo Wicketkeeper", 3, "Wicketkeeper", "Right-hand bat", None, "England"),
                (6, "Demo Bowler Two", 4, "Bowler", "Right-hand bat", "Left-arm fast", "South Africa"),
            ],
        )

        conn.executemany(
            """INSERT OR IGNORE INTO venues
            (venue_id, venue_name, city, country, capacity)
            VALUES (?, ?, ?, ?, ?)""",
            [
                (1, "Demo Cricket Ground", "Mumbai", "India", 40000),
                (2, "Demo Oval", "Melbourne", "Australia", 50000),
            ],
        )

        conn.execute(
            """INSERT OR IGNORE INTO series
            (series_id, series_name, format, start_date, end_date)
            VALUES (1, 'Demo International Series', 'ODI',
                    '2026-01-10', '2026-01-20')"""
        )

        conn.execute(
            """INSERT OR IGNORE INTO matches
            (match_id, external_match_id, series_id, match_type,
             team1_id, team2_id, venue_id, match_date, status,
             winner_team_id, result_text)
            VALUES (1, 'DEMO-MATCH-001', 1, 'ODI', 1, 2, 1,
                    '2026-01-15', 'completed', 1,
                    'Demo result: India won by 20 runs')"""
        )

        conn.executemany(
            """INSERT OR IGNORE INTO innings
            (innings_id, match_id, innings_number, batting_team_id,
             total_runs, wickets, overs, extras)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, 1, 1, 1, 280, 7, 50.0, 12),
                (2, 1, 2, 2, 260, 10, 48.2, 10),
            ],
        )

        conn.executemany(
            """INSERT OR IGNORE INTO batting_stats
            (batting_stat_id, innings_id, player_id, runs, balls_faced,
             fours, sixes, dismissed, dismissal_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, 1, 1, 105, 110, 9, 2, 1, "caught"),
                (2, 1, 2, 62, 45, 5, 2, 1, "bowled"),
                (3, 2, 3, 25, 30, 2, 0, 1, "caught"),
                (4, 2, 4, 80, 75, 7, 1, 1, "lbw"),
            ],
        )

        conn.executemany(
            """INSERT OR IGNORE INTO bowling_stats
            (bowling_stat_id, innings_id, player_id, overs,
             maidens, runs_conceded, wickets)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, 2, 3, 10.0, 1, 45, 3),
                (2, 2, 6, 9.2, 0, 50, 2),
                (3, 1, 2, 8.0, 0, 42, 2),
                (4, 1, 3, 7.0, 0, 48, 1),
            ],
        )

    with sqlite3.connect(DB_PATH) as conn:
        for table in ("teams", "players", "venues", "series", "matches",
                      "innings", "batting_stats", "bowling_stats"):
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            print(f"{table}: {count} records")

    print("SUCCESS: Demo seed completed. These are synthetic records.")


if __name__ == "__main__":
    seed_database()
