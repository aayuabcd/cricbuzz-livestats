-- Synthetic demo data may be present.
SELECT v.country AS venue_country, COUNT(m.match_id) AS matches_played FROM matches m JOIN venues v ON v.venue_id=m.venue_id GROUP BY v.country ORDER BY matches_played DESC;
