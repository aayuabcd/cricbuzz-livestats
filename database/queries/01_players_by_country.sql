-- Synthetic demo data may be present.
SELECT country, COUNT(*) AS player_count FROM players GROUP BY country ORDER BY player_count DESC, country;
