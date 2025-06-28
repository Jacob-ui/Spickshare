import click
import os
import sqlite3
from flask import current_app, g

def get_db_con():
    if 'db_con' not in g:
        db_path = current_app.config['DATABASE'] #
        db_dir = os.path.dirname(db_path) #
        if not os.path.exists(db_dir): #
            os.makedirs(db_dir) #

        g.db_con = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Foreign Keys für jede Verbindung aktivieren
        g.db_con.execute("PRAGMA foreign_keys = ON")
    return g.db_con

def close_db_con(e=None):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.close()

@click.command('init-db')
def init_db():
    db_path = current_app.config['DATABASE']

    db_dir = os.path.dirname(db_path) #
    if not os.path.exists(db_dir): #
        os.makedirs(db_dir) #
    
    # Alte DB entfernen
    if os.path.exists(db_path):
        os.remove(db_path)
        click.echo(f"→ Removed existing database at {db_path}")
    
    # Neue DB erstellen
    db_con = get_db_con()
    
    with db_con:
        with current_app.open_resource('sql/create_tables.sql') as f:
            db_con.executescript(f.read().decode('utf-8'))
        with current_app.open_resource('sql/insert_sample.sql') as f:
            db_con.executescript(f.read().decode('utf-8'))
        
        # Überprüfen ob alles geklappt hat
        tables = db_con.execute("SELECT name FROM sqlite_master").fetchall()
        if not any(t[0] == 'users' for t in tables):
            raise RuntimeError("Table creation failed!")
    
    click.echo("Database initialized successfully")

# #def insert_sample():
#     db_con = get_db_con()

#     # Vorher alles löschen (optional)
#     db_con.execute('DELETE FROM unlocked_cheatsheet')
#     db_con.execute('DELETE FROM users')
#     db_con.execute('DELETE FROM modules')
#     db_con.execute('DELETE FROM profs')
#     db_con.execute('DELETE FROM cheatsheets')
#     db_con.execute('DELETE FROM votes')
#     db_con.execute('DELETE FROM orders')

#     # Beispiel-user
#     db_con.execute("INSERT INTO users (username, pw) VALUES (?, ?)", ("Mensch1","Mensch1"))
#     db_con.execute("INSERT INTO users (username, pw) VALUES (?, ?)", ("Mensch2","Mensch3"))
#     db_con.execute("INSERT INTO users (username, pw) VALUES (?, ?)", ("Mensch3","Mensch3"))

#     # Beispiel-module
#     db_con.execute("INSERT INTO modules (name) VALUES (?)", ("module1"))
#     db_con.execute("INSERT INTO modules (name) VALUES (?)", ("module2"))
#     db_con.execute("INSERT INTO modules (name) VALUES (?)", ("module3"))

#     # Beispiel-prof
#     db_con.execute("INSERT INTO profs (modules_id, name) VALUES (?, ?)", ("prof1", 1))
#     db_con.execute("INSERT INTO profs (modules_id, name) VALUES (?, ?)", ("prof2", 2))
#     db_con.execute("INSERT INTO profs (modules_id, name) VALUES (?, ?)", ("prof3", 1))

#     # Beispiel-cheatsheets
#     db_con.execute("INSERT INTO cheatsheets (title, creditcost, pdf_datei, modules_id, profs_id, users_id, votes) VALUES (?, ?, ?, ?, ?, ?, ? )", ("CS1", "hallo", 1, 1, 1, 2))
#     db_con.execute("INSERT INTO cheatsheets (title, creditcost, pdf_datei, modules_id, profs_id, users_id, votes) VALUES (?, ?, ?, ?, ?, ?, ? )", ("CS2", "hallo", 2, 2, 2, 2))
#     db_con.execute("INSERT INTO cheatsheets (title, creditcost, pdf_datei, modules_id, profs_id, users_id, votes) VALUES (?, ?, ?, ?, ?, ?, ? )", ("CS3", "hallo", 3, 3, 3, 2))

#     #Beispiel-votes
#     db_con.execute("INSERT INTO votes (users_id, cheatsheets_id, upvote) VALUES (?, ?, ?)", (1, 1, 1))
#     db_con.execute("INSERT INTO votes (users_id, cheatsheets_id, upvote) VALUES (?, ?, ?)", (2, 2, 0))
#     db_con.execute("INSERT INTO votes (users_id, cheatsheets_id, upvote) VALUES (?, ?, ?)", (3, 3, 1))

#     #Beispiel-orders
#     db_con.execute("INSERT INTO orders (users_id, creditamount) VALUES (?, ?)", (1, 1))
#     db_con.execute("INSERT INTO orders (users_id, creditamount) VALUES (?, ?)", (2, 2))
#     db_con.execute("INSERT INTO orders (users_id, creditamount) VALUES (?, ?)", (3, 1))
                   
#     #unlocked_cheatsheets  Beispiel
#     db_con.execute("INSERT INTO unlocked_cheatsheets (users_id, cheatsheets_id) VALUES (?, ?)", (1, 1))
#     db_con.execute("INSERT INTO unlocked_cheatsheets (users_id, cheatsheets_id) VALUES (?, ?)", (1, 2))
#     db_con.execute("INSERT INTO unlocked_cheatsheets (users_id, cheatsheets_id) VALUES (?, ?)", (2, 3))

#     db_con.commit()