-- Synthetic demo data may be present.
SELECT role, COUNT(*) AS players FROM players GROUP BY role ORDER BY players DESC;
