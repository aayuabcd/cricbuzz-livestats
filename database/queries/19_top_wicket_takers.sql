-- Synthetic demo data may be present.
SELECT p.full_name, SUM(b.wickets) AS wickets FROM bowling_stats b JOIN players p ON p.player_id=b.player_id GROUP BY p.player_id ORDER BY wickets DESC LIMIT 10;
