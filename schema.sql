
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    NOT NULL UNIQUE,
    hash     TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title   TEXT    NOT NULL,
    note    TEXT    DEFAULT '',
    due     TEXT,
    done    INTEGER NOT NULL DEFAULT 0,
    created TEXT    NOT NULL DEFAULT (datetime('now'))
);
