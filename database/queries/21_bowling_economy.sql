-- Synthetic demo data may be present.
SELECT p.full_name, SUM(b.runs_conceded) AS runs_conceded, SUM(b.overs) AS recorded_overs, ROUND(SUM(b.runs_conceded)/NULLIF(SUM(CAST(b.overs AS INTEGER)*6 + ROUND((b.overs-CAST(b.overs AS INTEGER))*10)),0)*6,2) AS economy FROM bowling_stats b JOIN players p ON p.player_id=b.player_id GROUP BY p.player_id ORDER BY economy ASC;
