# Final Verification Checklist

## Automated tests

Run from the project root with the virtual environment active:

```powershell
python -m py_compile app.py
python -m pytest -q
```

Expected: Python syntax check completes without an error and all tests pass. Record the actual number of passing tests from the terminal; do not claim a number before running.

## Manual end-to-end verification

- [ ] **Command Center:** Stadium hero, summary metrics, and charts load.
- [ ] **Navigation:** All six pages open and navigation persists through interaction.
- [ ] **Match Center:** Match filter, selected scorecard, innings table and chart work.
- [ ] **Player Matrix:** Batting, bowling and player profile tabs load; player selection works.
- [ ] **SQL Intelligence:** 25 recipes appear; run a query, view table, download CSV.
- [ ] **Team Analytics:** Team table and chart load.
- [ ] **Data Manager:** Create, read, update, and delete a temporary team/player; verify database state and cleanup.
- [ ] **Live Scores:** Valid key retrieves provider data; refresh works.
- [ ] **API failure:** With key removed temporarily, app displays a helpful error rather than crashing; restore key afterward.
- [ ] **Security:** `git ls-files .env .streamlit/secrets.toml` returns nothing.
- [ ] **Git:** Final code and documentation are committed and pushed; backup files and `.env` remain untracked/ignored.

## Sample CRUD test data

Use a unique temporary team such as `Portfolio Test XI`; edit to `Portfolio QA XI`; delete after verifying the change. If a player references the team, remove or reassign that player before deletion, according to the app's foreign-key rules.

## Evidence to capture

Take screenshots of Command Center, SQL query results, Data Manager, and Live Scores **without revealing the API key**. Place images in `docs/screenshots/` if you want them in the repository. Screenshots are optional and not included in this package.

## Known limits

Passing unit tests does not verify external service uptime or every browser interaction. Some SQL queries can legitimately return empty results with the small demo dataset. Do not interpret this alone as a test failure.
