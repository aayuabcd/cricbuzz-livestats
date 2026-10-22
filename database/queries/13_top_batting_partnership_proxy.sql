-- Synthetic demo data may be present.
SELECT i.innings_id, t.team_name, SUM(b.runs) AS recorded_batter_runs FROM batting_stats b JOIN innings i ON i.innings_id=b.innings_id JOIN teams t ON t.team_id=i.batting_team_id GROUP BY i.innings_id ORDER BY recorded_batter_runs DESC;
