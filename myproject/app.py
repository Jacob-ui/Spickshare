import os
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
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
    return render_template('index.html')

    
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash ('Passwords do not match', category='error')
        else:
            flash ('Registration successful!', category='success')
            # add user to users database
    return render_template('register.html')


@app.route('/insert/sample')
def run_insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'


if __name__ == '__main__':
    app.run(debug=True)