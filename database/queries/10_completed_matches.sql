-- Synthetic demo data may be present.
SELECT match_date, match_type, result_text FROM matches WHERE LOWER(status) IN ('completed','complete','finished','result') ORDER BY match_date DESC LIMIT 10;
