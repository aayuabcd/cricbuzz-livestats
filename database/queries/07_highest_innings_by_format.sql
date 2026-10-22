-- Synthetic demo data may be present.
SELECT m.match_type, t.team_name, MAX(i.total_runs) AS highest_score FROM innings i JOIN matches m ON m.match_id=i.match_id JOIN teams t ON t.team_id=i.batting_team_id GROUP BY m.match_type, t.team_id ORDER BY highest_score DESC;
