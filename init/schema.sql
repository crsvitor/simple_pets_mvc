CREATE TABLE IF NOT EXISTS 'pets' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS 'people' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age NUMBER NOT NULL,
    pet_id INTEGER NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);

INSERT INTO pets(name, type)
VALUES
    ('cobra', 'snake'),
    ('cao', 'dog'),
    ('gato', 'cat');