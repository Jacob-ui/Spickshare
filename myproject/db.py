import click
import os
import sqlite3
from flask import current_app, g

def get_db_con(pragma_foreign_keys = True):
    if 'db_con' not in g:
        g.db_con = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db_con.row_factory = sqlite3.Row
        if pragma_foreign_keys:
            g.db_con.execute('PRAGMA foreign_keys = ON;')
    return g.db_con

def close_db_con(e=None):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.close()

@click.command('init-db')
def init_db():
    try:
        os.makedirs(current_app.instance_path)
    except OSError:
        pass
    db_con = get_db_con()
    with current_app.open_resource('sql/drop_tables.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    with current_app.open_resource('sql/create_tables.sql') as f:
        db_con.executescript(f.read().decode('utf8'))
    click.echo('Database has been initialized.')

    
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