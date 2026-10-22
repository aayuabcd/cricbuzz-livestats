-- Synthetic demo data may be present.
SELECT a.team_name AS team_1, b.team_name AS team_2, COUNT(*) AS matches_played FROM matches m JOIN teams a ON a.team_id=m.team1_id JOIN teams b ON b.team_id=m.team2_id GROUP BY m.team1_id, m.team2_id ORDER BY matches_played DESC;
