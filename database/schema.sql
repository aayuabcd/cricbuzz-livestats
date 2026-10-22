PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    team_id INTEGER,
    role TEXT NOT NULL,
    batting_style TEXT,
    bowling_style TEXT,
    country TEXT NOT NULL,
    date_of_birth TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    capacity INTEGER CHECK (capacity IS NULL OR capacity >= 0),
    UNIQUE (venue_name, city)
);

CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY,
    series_name TEXT NOT NULL,
    format TEXT,
    start_date TEXT,
    end_date TEXT
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    external_match_id TEXT UNIQUE,
    series_id INTEGER,
    match_type TEXT NOT NULL,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    venue_id INTEGER,
    match_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    winner_team_id INTEGER,
    result_text TEXT,
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id),
    CHECK (team1_id <> team2_id)
);

CREATE TABLE IF NOT EXISTS innings (
    innings_id INTEGER PRIMARY KEY,
    match_id INTEGER NOT NULL,
    innings_number INTEGER NOT NULL,
    batting_team_id INTEGER NOT NULL,
    total_runs INTEGER NOT NULL DEFAULT 0 CHECK (total_runs >= 0),
    wickets INTEGER NOT NULL DEFAULT 0 CHECK (wickets BETWEEN 0 AND 10),
    overs REAL NOT NULL DEFAULT 0 CHECK (overs >= 0),
    extras INTEGER NOT NULL DEFAULT 0 CHECK (extras >= 0),
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (batting_team_id) REFERENCES teams(team_id),
    UNIQUE (match_id, innings_number)
);

CREATE TABLE IF NOT EXISTS batting_stats (
    batting_stat_id INTEGER PRIMARY KEY,
    innings_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    runs INTEGER NOT NULL DEFAULT 0 CHECK (runs >= 0),
    balls_faced INTEGER NOT NULL DEFAULT 0 CHECK (balls_faced >= 0),
    fours INTEGER NOT NULL DEFAULT 0 CHECK (fours >= 0),
    sixes INTEGER NOT NULL DEFAULT 0 CHECK (sixes >= 0),
    dismissed INTEGER NOT NULL DEFAULT 0 CHECK (dismissed IN (0, 1)),
    dismissal_type TEXT,
    FOREIGN KEY (innings_id) REFERENCES innings(innings_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE (innings_id, player_id)
);

CREATE TABLE IF NOT EXISTS bowling_stats (
    bowling_stat_id INTEGER PRIMARY KEY,
    innings_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    overs REAL NOT NULL DEFAULT 0 CHECK (overs >= 0),
    maidens INTEGER NOT NULL DEFAULT 0 CHECK (maidens >= 0),
    runs_conceded INTEGER NOT NULL DEFAULT 0 CHECK (runs_conceded >= 0),
    wickets INTEGER NOT NULL DEFAULT 0 CHECK (wickets >= 0),
    FOREIGN KEY (innings_id) REFERENCES innings(innings_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE (innings_id, player_id)
);

CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_type ON matches(match_type);
CREATE INDEX IF NOT EXISTS idx_innings_match ON innings(match_id);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_stats(player_id);
