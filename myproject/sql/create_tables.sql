CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL, 
    pw TEXT NOT NULL,
    credits INTEGER,
    userart TEXT,
    email TEXT
);
CREATE TABLE modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE profs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modules_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (modules_id) REFERENCES modules (id) on DELETE CASCADE
);

CREATE TABLE cheatsheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    creditcost INTEGER,
    pdf_datei TEXT,
    modules_id INTEGER,
    profs_id INTEGER,
    users_id INTEGER,
    votes INTEGER,
    FOREIGN KEY (modules_id) REFERENCES modules (id) on DELETE CASCADE,
    FOREIGN KEY (profs_id) REFERENCES profs (id) on DELETE CASCADE,
    FOREIGN KEY (users_id) REFERENCES users (id) on DELETE CASCADE
);
CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INTEGER,
    cheatsheets_id INTEGER,
      upvote BOOLEAN,
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
    users_id INTEGER,
    cheatsheets_id INTEGER,
    PRIMARY KEY (users_id, cheatsheets_id),
    FOREIGN KEY (users_id) REFERENCES users(id) on DELETE CASCADE,
    FOREIGN KEY (cheatsheets_id) REFERENCES cheatsheets (id) on DELETE CASCADE
);