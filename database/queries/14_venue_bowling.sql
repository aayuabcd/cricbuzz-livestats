-- Synthetic demo data may be present.
SELECT v.venue_name, p.full_name, SUM(b.wickets) AS wickets FROM bowling_stats b JOIN players p ON p.player_id=b.player_id JOIN innings i ON i.innings_id=b.innings_id JOIN matches m ON m.match_id=i.match_id JOIN venues v ON v.venue_id=m.venue_id GROUP BY v.venue_id, p.player_id ORDER BY wickets DESC;
