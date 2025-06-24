import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import db # dein db.py Modul mit DB-Funktionen
from db import get_db_con, init_db

app = Flask(__name__)


# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'spickshare.db') 
)

# DB initialisieren
app.cli.add_command(db.init_db)  # CLI-Befehl aus db.py
app.teardown_appcontext(db.close_db_con)

# Startseite
@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    return render_template('index.html', eintraege=eintraege)

#Login:
@app.route('/login/', methods=['GET', 'POST'])
def login():
    error_msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('password')

        if not username or not pw:
            error_msg = 'Please fill out both fields!'
        else:
            db_con = get_db_con()
            user = db_con.execute(
                "SELECT * FROM users WHERE username = ? AND pw = ?",
                (username, pw)
            ).fetchone()
            if user:
                return redirect(url_for('index'))
            else:
                error_msg = 'Username or password incorrect!'

    return render_template('login.html', error=error_msg)


# Registrierung:
@app.route('/register/', methods=['GET', 'POST'])
def register():
    message = None

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        pw = request.form.get('password')

        if not email or not username or not pw:
            message = 'Bitte fülle alle Felder aus.'
        else:
            db_con = get_db_con()
            user_exists = db_con.execute(
                'SELECT id FROM users WHERE username = ? OR email = ?',
                (username, email)
            ).fetchone()
            if user_exists:
                message = 'Benutzername oder E-Mail existiert bereits.'
            else:
                db_con.execute(
                    "INSERT INTO users (username, pw, credits, userart, email) VALUES (?, ?, ?, ?, ?)",
                    (username, pw, 0, 'not verified', email)
                )
                db_con.commit()
                # Nach erfolgreicher Registrierung weiterleiten:
                return render_template('login.html', message="Registrierung erfolgreich! Bitte einloggen.")

    return render_template('register.html', message=message)


# Liste für Sheets (Mit Sheets sind die Einträge für die CheatSheets gemeint)
eintraege = [
    {'id': '0', 'titel': 'Mathe Zusammenfassung', 'beschreibung': 'Inhalte für die Klausur', 'prof': 'Müller', 'score': '6'},
    {'id': '1', 'titel': 'Full-Stack Web Development', 'beschreibung': 'Wie erstelle ich eine Web-App', 'prof': 'Dr. Eck, Alexander', 'score': '10'}
]

# Voting +/-
@app.route("/vote", methods=["POST"])
def vote():
    eintrag_id = request.form.get('id') # fragt id vom sheet an
    vote_input = request.form.get('Voteinput') # liest aus index den +/- Button aus
    for eintrag in eintraege:
        if eintrag['id'] == eintrag_id:
            score = int(eintrag['score'])
            if vote_input == '+':
                score +=1
            elif vote_input == '-':
                score -=1
            eintrag['score'] = str(score) # speichert score
            break
    return render_template('index.html', eintraege=eintraege)



# DB
@app.route('/insert/sample')
def run_insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'

if __name__ == '__main__':
    app.run(debug=True)