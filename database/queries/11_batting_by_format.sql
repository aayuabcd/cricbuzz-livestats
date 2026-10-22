-- Synthetic demo data may be present.
SELECT p.full_name, m.match_type, SUM(b.runs) AS runs, SUM(b.balls_faced) AS balls FROM batting_stats b JOIN players p ON p.player_id=b.player_id JOIN innings i ON i.innings_id=b.innings_id JOIN matches m ON m.match_id=i.match_id GROUP BY p.player_id, m.match_type ORDER BY runs DESC;
