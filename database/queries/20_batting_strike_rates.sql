-- Synthetic demo data may be present.
SELECT p.full_name, SUM(b.runs) AS runs, SUM(b.balls_faced) AS balls, ROUND(100.0*SUM(b.runs)/NULLIF(SUM(b.balls_faced),0),2) AS strike_rate FROM batting_stats b JOIN players p ON p.player_id=b.player_id GROUP BY p.player_id ORDER BY strike_rate DESC;
