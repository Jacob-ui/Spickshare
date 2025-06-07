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

    
def insert_sample():
    db_con = get_db_con()

    # Vorher alles löschen (optional)
    db_con.execute('DELETE FROM todo_list')
    db_con.execute('DELETE FROM todo')
    db_con.execute('DELETE FROM list')

    # Beispiel-Listen
    db_con.execute("INSERT INTO list (name) VALUES (?)", ("Einkaufen",))
    db_con.execute("INSERT INTO list (name) VALUES (?)", ("Hausarbeit",))
    db_con.execute("INSERT INTO list (name) VALUES (?)", ("Projekte",))

    # Beispiel-Todos
    db_con.execute("INSERT INTO todo (description, complete) VALUES (?, ?)", ("Milch kaufen", 0))
    db_con.execute("INSERT INTO todo (description, complete) VALUES (?, ?)", ("Staubsaugen", 1))
    db_con.execute("INSERT INTO todo (description, complete) VALUES (?, ?)", ("Flask-App bauen", 0))

    # Liste IDs und Todo IDs verbinden
    db_con.execute("INSERT INTO todo_list (list_id, todo_id) VALUES (?, ?)", (1, 1))  # Milch -> Einkaufen
    db_con.execute("INSERT INTO todo_list (list_id, todo_id) VALUES (?, ?)", (2, 2))  # Staubsaugen -> Hausarbeit
    db_con.execute("INSERT INTO todo_list (list_id, todo_id) VALUES (?, ?)", (3, 3))  # Flask -> Projekte

    db_con.commit()

