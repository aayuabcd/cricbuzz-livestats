"""Validated, parameterized SQLite CRUD for teams and players."""
import sqlite3
from utils.db_connection import get_db_connection


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


def _write(query, params):
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.execute(query, params)
            if query.lstrip().upper().startswith(("UPDATE", "DELETE")) and cursor.rowcount == 0:
                raise ValueError("Record not found.")
            return cursor.lastrowid
    finally:
        conn.close()


def create_team(name, country):
    return _write("INSERT INTO teams (team_name,country) VALUES (?,?)", (_text(name,"Team name"), _text(country,"Country")))


def update_team(team_id, name, country):
    return _write("UPDATE teams SET team_name=?,country=? WHERE team_id=?", (_text(name,"Team name"), _text(country,"Country"),team_id))


def delete_team(team_id):
    return _write("DELETE FROM teams WHERE team_id=?", (team_id,))


def create_player(name, team_id, role, country):
    return _write("INSERT INTO players (full_name,team_id,role,country) VALUES (?,?,?,?)", (_text(name,"Player name"),team_id,_text(role,"Role"),_text(country,"Country")))


def update_player(player_id, name, team_id, role, country):
    return _write("UPDATE players SET full_name=?,team_id=?,role=?,country=? WHERE player_id=?", (_text(name,"Player name"),team_id,_text(role,"Role"),_text(country,"Country"),player_id))


def delete_player(player_id):
    return _write("DELETE FROM players WHERE player_id=?", (player_id,))
