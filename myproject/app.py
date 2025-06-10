import os
from flask import Flask, redirect, url_for, render_template, request, jsonify
import db  # dein db.py Modul mit DB-Funktionen

app = Flask(__name__)

# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'spickshare.sqlite')
)

# DB initialisieren
app.cli.add_command(db.init_db)  # CLI-Befehl aus db.py
app.teardown_appcontext(db.close_db_con)


@app.route('/')
def index():
    return redirect(url_for('login'))

    
@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/insert/sample')
def run_insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'


if __name__ == '__main__':
    app.run(debug=True)