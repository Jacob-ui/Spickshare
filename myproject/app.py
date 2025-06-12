import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import db # dein db.py Modul mit DB-Funktionen
from db import get_db_con, init_db

app = Flask(__name__)

# Konfiguration
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'spickshare.sqlite')
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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('password')

        #db_con = get_db_con()
        if not username or not pw:
            flash('Please fill out both fields!', category = 'error')
        #elif db.execute("SELECT id FROM users WHERE username = ? and pw = ?", (username, pw)).fetchone(): # überprüfen ob username und passwort übereinstimmen
            #flash('Login successful', category = 'success')
        #else:
            #flash('Username or password is incorrect!', category = 'error')


    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        pw = request.form.get('password1')
        password2 = request.form.get('password2')

        #db_con = get_db_con()

        if not email or not username or not pw or not password2:
            flash('Please fill out all fields!', category = 'error')
            return render_template('register.html')
        if pw != password2: #Beiden Passwörter vergeleichen
            flash('Passwords must match!', category = 'error')
            return render_template('register.html')
        #elif db.execute("SELECT id FROM users WHERE username = ?", (username)).fetchone(): # überprüfen ob username schon existiert
        #    flash('Username already exists!', category = 'error')
        #    return render_template('register.html')
        #elif db.execute("SELECT id FROM users WHERE email = ?", (email)).fetchone(): #überprüfen ob email schonmal verwendet wurde
        #    flash('Email already registered!', category = 'error')   
        #    return render_template('register.html')     
        else:
            #db_con.execute("INSERT INTO users (username, pw, credits, userart, email) VALUES (?, ?, ?, ?, ?)", (username, pw, 0, 'not verified', email))
            #db_con.commit()
            flash('Registration successful!', category = 'success')
            # add User to database
            return render_template('register.html')
    return render_template('register.html')

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