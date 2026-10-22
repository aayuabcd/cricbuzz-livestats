-- Synthetic demo data may be present.
SELECT t.team_name, COUNT(m.match_id) AS wins FROM teams t LEFT JOIN matches m ON m.winner_team_id=t.team_id GROUP BY t.team_id ORDER BY wins DESC;
