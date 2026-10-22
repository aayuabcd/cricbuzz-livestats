-- Synthetic demo data may be present.
SELECT p.full_name, SUM(b.runs) AS runs, ROUND(100.0*SUM(b.runs)/NULLIF(SUM(b.balls_faced),0),2) AS strike_rate, ROUND(SUM(b.runs)*0.7 + COALESCE(100.0*SUM(b.runs)/NULLIF(SUM(b.balls_faced),0),0)*0.3,2) AS demo_index FROM batting_stats b JOIN players p ON p.player_id=b.player_id GROUP BY p.player_id ORDER BY demo_index DESC;
