-- Tabellen anlegen
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL, 
    pw TEXT NOT NULL,
    credits INTEGER NOT NULL,
    userart TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE profs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modules_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (modules_id) REFERENCES modules (id) on DELETE CASCADE
);

CREATE TABLE cheatsheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    creditcost INTEGER NOT NULL,
    pdf_datei TEXT NOT NULL,
    modules_id INTEGER NOT NULL,
    profs_id INTEGER NOT NULL,
    users_id INTEGER NOT NULL,
    votes INTEGER NOT NULL,
    FOREIGN KEY (modules_id) REFERENCES modules (id) on DELETE CASCADE,
    FOREIGN KEY (profs_id) REFERENCES profs (id) on DELETE CASCADE,
    FOREIGN KEY (users_id) REFERENCES users (id) on DELETE CASCADE
);
CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INTEGER NOT NULL,
    cheatsheets_id INTEGER NOT NULL,
    upvote BOOLEAN NOT NULL,
    FOREIGN KEY (users_id) REFERENCES users (id) on DELETE CASCADE,
    FOREIGN KEY (cheatsheets_id) REFERENCES cheatsheets (id) on DELETE CASCADE
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INTEGER NOT NULL,
    creditamount INTEGER NOT NULL,
    FOREIGN KEY (users_id) REFERENCES users (id) on DELETE CASCADE
);
CREATE TABLE unlocked_cheatsheet (
    users_id INTEGER NOT NULL,
    cheatsheets_id INTEGER NOT NULL,
    PRIMARY KEY (users_id, cheatsheets_id),
    FOREIGN KEY (users_id) REFERENCES users(id) on DELETE CASCADE,
    FOREIGN KEY (cheatsheets_id) REFERENCES cheatsheets (id) on DELETE CASCADE
);