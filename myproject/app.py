import os
from flask import Flask
import db  # dein db.py Modul mit DB-Funktionen

app = Flask(__name__)

# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'todos.sqlite')
)

# DB initialisieren
app.cli.add_command(db.init_db)  # so wie in deinem db.py heißt der CLI-Befehl init_db_command
app.teardown_appcontext(db.close_db_con)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/lists/')
def lists():
    return 'Todo: implement business logic to show all to-do lists'

@app.route('/lists/<int:id>')
def list(id):
    return f'Todo: implement business logic to show all to-dos of list {id}'

@app.route('/insert/sample')
def run_insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'

if __name__ == '__main__':
    app.run(debug=True)
