-- Synthetic demo data may be present.
SELECT t.team_name, COUNT(p.player_id) AS roster_size FROM teams t LEFT JOIN players p ON p.team_id=t.team_id GROUP BY t.team_id ORDER BY roster_size DESC;
