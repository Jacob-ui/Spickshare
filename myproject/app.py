import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
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

# Startseite
@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index/')
def index():
    return render_template('index.html', eintraege=eintraege)


@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('Passwords must match!', category = 'error')
        else:
            flash('Registration successful!', category = 'success')
            # add User to database

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