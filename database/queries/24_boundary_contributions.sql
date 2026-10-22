-- Synthetic demo data may be present.
SELECT p.full_name, SUM(b.fours) AS fours, SUM(b.sixes) AS sixes, 4*SUM(b.fours)+6*SUM(b.sixes) AS boundary_runs FROM batting_stats b JOIN players p ON p.player_id=b.player_id GROUP BY p.player_id ORDER BY boundary_runs DESC;
