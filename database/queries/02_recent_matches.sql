-- Synthetic demo data may be present.
SELECT m.match_date, a.team_name AS team_1, b.team_name AS team_2, m.match_type, m.status FROM matches m JOIN teams a ON a.team_id=m.team1_id JOIN teams b ON b.team_id=m.team2_id ORDER BY m.match_date DESC LIMIT 10;
