import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import db # dein db.py Modul mit DB-Funktionen
from db import get_db_con, init_db

app = Flask(__name__, instance_relative_config=True) #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug


# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'spickshare.db') 
)

app.instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance') #https://claude.ai/share/644c973d-59db-4614-8e57-cf71e15b4903 to fix multiple instance folder bug
app.config['DATABASE'] = os.path.join(app.instance_path, 'spickshare.db')

#Schauen ob DB existiert
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# DB initialisieren
app.cli.add_command(db.init_db)  # CLI-Befehl aus db.py
app.teardown_appcontext(db.close_db_con)

print("Instance path:", app.instance_path)
print("Database path:", app.config['DATABASE'])
# Startseite
@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    return render_template('index.html', eintraege=eintraege)

#Login:
@app.route('/login/', methods=['GET', 'POST']) #https://youtu.be/dam0GPOAvVI?t=3449 für die GET und POST Teile des Codes
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
@app.route('/register/', methods=['GET', 'POST']) #
def register():
    message = None

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        pw = request.form.get('password')
        pw2 = request.form.get('password2')

        if not email or not username or not pw or not pw2:
            message = 'Bitte fülle alle Felder aus.'
        elif pw != pw2:
            message = 'Passwörter stimmen nicht überein!' 
        else:
            try: #
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
            except Exception as e: #
                message = f'Database error: {str(e)}' #

    return render_template('register.html', message=message)

@app.route("/logout")
def logout():
    return redirect(url_for('index'))

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