from utils.db_connection import fetch_all, fetch_one, get_table_counts

print("=== Database record counts ===")
for table, count in get_table_counts().items():
    print(f"{table}: {count}")

print("\n=== Top batting scores ===")
rows = fetch_all("""
    SELECT p.full_name, b.runs, b.balls_faced
    FROM batting_stats AS b
    JOIN players AS p ON p.player_id = b.player_id
    ORDER BY b.runs DESC
""")

for row in rows:
    print(f"{row['full_name']}: {row['runs']} runs from {row['balls_faced']} balls")

match = fetch_one(
    "SELECT match_type, status FROM matches WHERE match_id = ?",
    (1,),
)
print("\nMatch lookup:", dict(match) if match else "No match found")
print("\nSUCCESS: Centralized database utility works.")
