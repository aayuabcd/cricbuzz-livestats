# System Architecture

## High-level flow

```text
                        User's web browser
                                |
                       Streamlit application
                             app.py
                       /        |        \
                Analytics     Data Manager    Live Scores
                   |              |                |
             db_connection.py   crud.py       cricket_api.py
                   |              |                |
                   +------- SQLite database   CricketData API
                            data/cricbuzz.db   (HTTPS + API key)
                   |
           database/queries/*.sql
              25 SQL recipes
```

## Components

**Presentation:** `app.py` renders the cinematic dashboard, interactive navigation, filters, charts, tables, and live-score section.

**Persistence:** `utils/db_connection.py` accesses local SQLite. `database/schema.sql` defines teams, players, venues, series, matches, innings, batting statistics, and bowling statistics.

**Analytics:** Version-controlled SQL recipes in `database/queries/` aggregate batting, bowling, match, team, and venue data. Pandas prepares query results; Plotly renders visualizations.

**CRUD:** `utils/crud.py` manages local team and player records. The Data Manager is for the demo database, not the external cricket API.

**External integration:** `utils/cricket_api.py` requests cricket data using a key loaded from the local environment. External API responses must be treated as provider data rather than synthetic database data.

## Data model

- `teams` → `players`: a team may have many players.
- `matches` references two teams, optionally a series, venue, and winning team.
- `matches` → `innings`: a match has one or more innings.
- `innings` → `batting_stats` and `bowling_stats`: player performance records are associated with innings.

The database uses foreign keys and constraints to protect basic data integrity.

## Operational considerations

- The live API may be unavailable, rate-limited, or return no current matches; local analytics should still work.
- Local SQLite demo records are not synchronized automatically with the API.
- SQL recipe output is read-only; mutations are handled separately by validated CRUD operations.
- API keys belong in `.env` and must not be committed.
