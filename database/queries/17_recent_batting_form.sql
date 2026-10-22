-- Synthetic demo data may be present.
SELECT p.full_name, m.match_date, b.runs, b.balls_faced FROM batting_stats b JOIN players p ON p.player_id=b.player_id JOIN innings i ON i.innings_id=b.innings_id JOIN matches m ON m.match_id=i.match_id ORDER BY m.match_date DESC, b.runs DESC LIMIT 30;
