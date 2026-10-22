-- Synthetic demo data may be present.
SELECT p.full_name, t.team_name, p.role FROM players p LEFT JOIN teams t ON t.team_id=p.team_id WHERE LOWER(REPLACE(p.role,'-','')) LIKE '%allround%' ORDER BY p.full_name;
