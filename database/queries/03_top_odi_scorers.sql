-- Synthetic demo data may be present.
SELECT p.full_name, SUM(b.runs) AS total_runs FROM batting_stats b JOIN players p ON p.player_id=b.player_id JOIN innings i ON i.innings_id=b.innings_id JOIN matches m ON m.match_id=i.match_id WHERE UPPER(m.match_type)='ODI' GROUP BY p.player_id ORDER BY total_runs DESC LIMIT 10;
