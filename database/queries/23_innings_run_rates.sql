-- Synthetic demo data may be present.
SELECT i.innings_id, t.team_name, i.total_runs, i.overs, ROUND(6.0*i.total_runs/NULLIF(CAST(i.overs AS INTEGER)*6 + ROUND((i.overs-CAST(i.overs AS INTEGER))*10),0),2) AS run_rate FROM innings i JOIN teams t ON t.team_id=i.batting_team_id ORDER BY run_rate DESC;
