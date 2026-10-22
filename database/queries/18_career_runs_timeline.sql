-- Synthetic demo data may be present.
SELECT p.full_name, m.match_date, SUM(b.runs) AS runs_on_date FROM batting_stats b JOIN players p ON p.player_id=b.player_id JOIN innings i ON i.innings_id=b.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY p.player_id, m.match_date ORDER BY p.full_name, m.match_date;
