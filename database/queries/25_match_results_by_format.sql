-- Synthetic demo data may be present.
SELECT match_type, status, COUNT(*) AS match_count FROM matches GROUP BY match_type, status ORDER BY match_count DESC;
