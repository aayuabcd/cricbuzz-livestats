-- Synthetic demo data may be present.
SELECT series_name, format, start_date, end_date FROM series WHERE start_date >= '2024-01-01' AND start_date < '2025-01-01' ORDER BY start_date;
