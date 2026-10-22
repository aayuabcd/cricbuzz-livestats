# Cricbuzz LiveStats 🏏

**Cinematic cricket intelligence dashboard | Python · Streamlit · SQLite · SQL · Plotly · CricketData API**

Cricbuzz LiveStats is an interactive cricket analytics application combining a cinematic stadium-inspired interface with a relational database, 25 SQL analytics recipes, player and team insights, data management, and current cricket match scores retrieved from a third-party API.

> **Data transparency:** Local SQLite records are synthetic demonstration data. The **Live Cricket Scores** section requests current information from a cricket data provider; availability, freshness, and accuracy depend on that provider. This is an independent educational portfolio project, not an official Cricbuzz product.

## Features

- **Command Center:** Cinematic landing page, KPI metrics, batting and bowling visualizations.
- **Match Center:** Stored match listings, filters, innings breakdowns, and scorecards.
- **Player Matrix:** Batting and bowling leaderboards, player profiles, and individual metrics.
- **SQL Intelligence Lab:** 25 version-controlled SQL recipes, query results, charts, and CSV export.
- **Team Analytics:** Team rosters, match records, and visual comparisons.
- **Data Manager:** Create, view, update, and delete team and player records with validation and deletion safeguards.
- **Live Cricket Scores:** Provider-backed match information, refresh controls, and graceful error handling.

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, custom CSS |
| Analytics | Pandas, Plotly |
| Application | Python 3.11+ |
| Local database | SQLite |
| External data | CricketData / CricAPI HTTP API |
| Configuration | `python-dotenv`, `.env` |
| Tests | pytest |
| Version control | Git and GitHub |

## Quick start (Windows PowerShell)

```powershell
# Clone your own repository or open the existing project folder
cd D:\Cricbuzz_LiveStats

# Create a virtual environment if one does not already exist
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python database/init_db.py
python database/seed_data.py

# Create .env locally if needed; NEVER commit real API keys
Copy-Item .env.example .env
# Edit .env and add: CRICKET_API_KEY=your_private_key

python -m pytest -q
python -m streamlit run app.py
```

Open **http://localhost:8501**. The local analytics pages use SQLite demo data. Live scores require a valid provider key and internet access.

> **Existing installations:** Do not rerun database initialization or seeding over a database you want to preserve. The setup commands above are for a fresh clone.

## Project layout

```text
Cricbuzz_LiveStats/
├── app.py                       # Cinematic Streamlit interface
├── assets/                      # Stadium image and visual assets
├── database/
│   ├── schema.sql               # Relational schema
│   ├── init_db.py               # Database initialization
│   ├── seed_data.py             # Synthetic sample records
│   └── queries/                 # 25 read-only SQL recipes
├── utils/
│   ├── db_connection.py         # SQLite access
│   ├── crud.py                  # Team/player data management
│   └── cricket_api.py           # External cricket API client
├── tests/                       # Automated tests
├── docs/                        # Architecture, testing, demo guide
├── requirements.txt
├── .env.example                 # Public placeholder, no real key
└── .gitignore
```

## SQL Intelligence

The SQL library contains 25 numbered `.sql` files under `database/queries/`. The app loads these recipes and displays results as tables, optional charts, and CSV exports. Some queries may legitimately return zero rows on the small synthetic dataset. Analytical approximations are named as such (for example, partnership *proxy* rather than ball-by-ball partnerships).

## Privacy and security

- Put your real key in a local `.env` file, not in Python source or screenshots.
- Keep `.env`, `.streamlit/secrets.toml`, local `.db` files, and local backups out of Git.
- Use parameterized SQL for user inputs and confirm destructive operations.
- If a credential is accidentally published, rotate it with the provider.

Verify tracked secret paths:

```powershell
git ls-files .env .streamlit/secrets.toml
# Expected: no output
```

## Quality checks

```powershell
python -m py_compile app.py
python -m pytest -q
```

See [docs/TESTING.md](docs/TESTING.md) for browser checks and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the system overview.

## Scope and limitations

- The application is designed for portfolio and educational demonstrations.
- SQLite is a local development datastore, not a production multi-user service.
- The 25 queries operate on the available schema; ball-by-ball analytics cannot be inferred from aggregated innings data.
- Current match information depends on a third-party API and its rate limits.
- Tests validate code paths but do not guarantee that an external API is always reachable.

## Demo

1. Open Command Center and explain the dashboard KPIs.
2. Explore a match in Match Center.
3. Compare batting and bowling metrics in Player Matrix.
4. Run and export one SQL Intelligence query.
5. Add, edit, and delete a temporary record in Data Manager.
6. Expand Live Cricket Scores and refresh a match.

For a 2–3 minute walkthrough, see [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md).
