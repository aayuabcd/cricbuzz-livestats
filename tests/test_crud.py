import sqlite3
import pytest
from utils import crud

@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    path = tmp_path / "crud_test.db"
    conn = sqlite3.connect(path)
    conn.executescript("""PRAGMA foreign_keys=ON;
    CREATE TABLE teams(team_id INTEGER PRIMARY KEY,team_name TEXT NOT NULL UNIQUE,country TEXT NOT NULL);
    CREATE TABLE players(player_id INTEGER PRIMARY KEY,full_name TEXT NOT NULL,team_id INTEGER REFERENCES teams(team_id),role TEXT NOT NULL,country TEXT NOT NULL);
    CREATE TABLE batting_stats(id INTEGER PRIMARY KEY,player_id INTEGER REFERENCES players(player_id));""")
    conn.close()
    def connection():
        c = sqlite3.connect(path)
        c.execute("PRAGMA foreign_keys=ON")
        return c
    monkeypatch.setattr(crud, "get_db_connection", connection)
    return connection

def test_team_player_crud(isolated_db):
    team = crud.create_team("Demo Team", "India")
    player = crud.create_player("Test Player",team,"Batter","India")
    crud.update_team(team,"Demo XI","India")
    crud.update_player(player,"Updated Player",team,"Bowler","India")
    with isolated_db() as conn:
        assert conn.execute("SELECT team_name FROM teams WHERE team_id=?",(team,)).fetchone()[0] == "Demo XI"
        assert conn.execute("SELECT role FROM players WHERE player_id=?",(player,)).fetchone()[0] == "Bowler"
    with pytest.raises(sqlite3.IntegrityError):
        crud.delete_team(team)
    crud.delete_player(player)
    crud.delete_team(team)

def test_validation_and_fk(isolated_db):
    with pytest.raises(ValueError):
        crud.create_team(" ","India")
    with pytest.raises(sqlite3.IntegrityError):
        crud.create_player("A",999,"Batter","India")
    with pytest.raises(ValueError):
        crud.delete_player(999)
